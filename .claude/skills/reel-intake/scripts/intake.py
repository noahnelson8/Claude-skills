#!/usr/bin/env python3
"""
reel-intake: turn Instagram reels/posts (or local video files) into material Claude can read.

For each input it creates  <out>/<slug>/  containing:
  meta.json        url, creator, date, duration, caption, likes/views if available
  caption.txt      the post caption (where creators often put the prompt / repo / steps)
  transcript.txt   timestamped speech-to-text of the audio (faster-whisper, runs locally)
  frames/          ~1 frame every few seconds (max --max-frames), 640px wide
  sheet.jpg        contact sheet: all frames in one grid image (read this first)
  index.md         one-page summary pointing at everything above
The downloaded video/audio are deleted afterwards unless --keep-video.

Usage:
  python intake.py URL [URL ...]
  python intake.py --file urls.txt            # one URL or local path per line, # comments ok
  python intake.py path/to/saved_reel.mp4      # local files work too

Instagram usually needs you to be logged in. If downloads fail, use one of:
  --cookies-from-browser firefox   (Firefox works best on Windows; Chrome/Edge often block this)
  --cookies cookies.txt            (export with a "Get cookies.txt LOCALLY" browser extension)
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]  # .claude/skills/reel-intake/scripts/intake.py -> repo
DEFAULT_OUT = REPO_ROOT / "intake"


# ---------------------------------------------------------------- helpers
def ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg  # bundled ffmpeg binary, installed via requirements.txt

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit("ffmpeg not found. Run:  pip install -r requirements.txt  (installs imageio-ffmpeg)")


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def probe_duration(ffmpeg: str, video: Path) -> float:
    # ffmpeg -i prints "Duration: 00:00:31.53" to stderr; avoids needing ffprobe
    out = run([ffmpeg, "-hide_banner", "-i", str(video)]).stderr
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", out)
    if not m:
        return 0.0
    h, mnt, s = m.groups()
    return int(h) * 3600 + int(mnt) * 60 + float(s)


def has_audio(ffmpeg: str, video: Path) -> bool:
    return "Audio:" in run([ffmpeg, "-hide_banner", "-i", str(video)]).stderr


def slugify(text: str, max_len: int = 50) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:max_len].strip("-") or "reel"


def is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def move_dir(src: Path, dest: Path, attempts: int = 8) -> None:
    """Rename a folder, tolerating OneDrive/antivirus briefly locking fresh files (WinError 5/32).
    Retries with backoff, then falls back to copy + delete."""
    for i in range(attempts):
        try:
            src.rename(dest)
            return
        except PermissionError:
            time.sleep(0.25 * (i + 1))
    shutil.copytree(src, dest)
    shutil.rmtree(src, ignore_errors=True)


# ---------------------------------------------------------------- download
def download(url: str, workdir: Path, ffmpeg: str, cookies: str | None, cookies_browser: str | None) -> tuple[dict, Path | None]:
    import yt_dlp

    opts = {
        "outtmpl": str(workdir / "video.%(ext)s"),
        "format": "bv*[height<=1080]+ba/b",
        "merge_output_format": "mp4",
        "ffmpeg_location": ffmpeg,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "ignore_no_formats_error": True,  # image posts: still get caption/metadata
        "writethumbnail": True,
    }
    if cookies:
        opts["cookiefile"] = cookies
    if cookies_browser:
        opts["cookiesfrombrowser"] = (cookies_browser,)

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if info and info.get("_type") == "playlist" and info.get("entries"):
            info = next(e for e in info["entries"] if e)  # carousel: take first item

    video = next((p for p in workdir.glob("video.*") if p.suffix.lower() in {".mp4", ".mkv", ".webm", ".mov"}), None)
    return info or {}, video


# ---------------------------------------------------------------- frames
def extract_frames(ffmpeg: str, video: Path, frames_dir: Path, duration: float, max_frames: int, min_gap: float) -> list[Path]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    interval = max(min_gap, duration / max_frames) if duration > 0 else min_gap
    # Offset by half an interval so we skip the black first frame and catch mid-shot text.
    res = run([
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{min(interval / 2, max(duration - 0.1, 0)):.2f}", "-i", str(video),
        "-vf", f"fps=1/{interval:.3f},scale=640:-2",
        "-frames:v", str(max_frames), "-q:v", "4",
        str(frames_dir / "f%02d.jpg"),
    ])
    frames = sorted(frames_dir.glob("f*.jpg"))
    # rename with timestamps so Claude can line frames up with the transcript
    named = []
    for i, f in enumerate(frames):
        t = interval / 2 + i * interval
        new = frames_dir / f"{i + 1:02d}_t{int(t // 60):02d}m{int(t % 60):02d}s.jpg"
        f.rename(new)
        named.append(new)
    if not named and res.stderr:
        print(f"    frame extraction error: {res.stderr.strip()[:200]}")
    return named


def contact_sheet(ffmpeg: str, frames: list[Path], out: Path) -> bool:
    if not frames:
        return False
    n = len(frames)
    cols = 4 if n > 6 else min(n, 3)
    rows = math.ceil(n / cols)
    inputs = []
    for f in frames:
        inputs += ["-i", str(f)]
    # scale every frame to the same size, then xstack into a grid
    w, h = 400, 712
    chains = [f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black[v{i}]" for i in range(n)]
    # pad grid with black tiles if needed
    pad_count = rows * cols - n
    for j in range(pad_count):
        chains.append(f"color=black:s={w}x{h}:d=1[p{j}]")
    labels = [f"[v{i}]" for i in range(n)] + [f"[p{j}]" for j in range(pad_count)]
    layout = "|".join(f"{(k % cols) * w}_{(k // cols) * h}" for k in range(rows * cols))
    graph = ";".join(chains) + ";" + "".join(labels) + f"xstack=inputs={rows * cols}:layout={layout}[out]"
    res = run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", *inputs,
               "-filter_complex", graph, "-map", "[out]", "-frames:v", "1", "-q:v", "4", str(out)])
    if res.returncode != 0:
        print(f"    contact sheet error: {res.stderr.strip()[:200]}")
    return out.exists()


# ---------------------------------------------------------------- transcript
_whisper_model = None


def transcribe(video: Path, model_name: str) -> tuple[str, str]:
    """Returns (transcript_text, language). Raises on failure."""
    global _whisper_model
    from faster_whisper import WhisperModel

    if _whisper_model is None:
        print(f"    loading whisper model '{model_name}' (first run downloads it, ~250MB for small)...")
        _whisper_model = WhisperModel(model_name, device="auto", compute_type="int8")
    segments, info = _whisper_model.transcribe(str(video), vad_filter=True, beam_size=5)
    lines = []
    for seg in segments:
        m, s = divmod(int(seg.start), 60)
        lines.append(f"[{m:02d}:{s:02d}] {seg.text.strip()}")
    return "\n".join(lines), info.language


# ---------------------------------------------------------------- main per-item
def process(item: str, args, ffmpeg: str) -> dict:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    tmp = args.out / f".tmp-{stamp}"
    tmp.mkdir(parents=True, exist_ok=True)
    result = {"input": item, "ok": False}
    stage = "download"  # the login/cookie hint only makes sense for download errors
    try:
        if is_url(item):
            info, video = download(item, tmp, ffmpeg, args.cookies, args.cookies_from_browser)
        else:
            src = Path(item).expanduser()
            if not src.exists():
                raise FileNotFoundError(item)
            video = tmp / f"video{src.suffix}"
            shutil.copy2(src, video)
            info = {"title": src.stem, "webpage_url": str(src)}

        caption = (info.get("description") or "").strip()
        creator = info.get("uploader") or info.get("channel") or info.get("uploader_id") or ""
        base = creator or ""
        first_line = caption.splitlines()[0] if caption else (info.get("title") or "")
        slug = slugify(f"{base} {first_line}") if (base or first_line) else f"reel-{stamp}"
        dest = args.out / slug
        n = 2
        while dest.exists():
            dest = args.out / f"{slug}-{n}"
            n += 1
        stage = "process"
        move_dir(tmp, dest)
        tmp = dest
        video = dest / video.name if video else None

        duration = probe_duration(ffmpeg, video) if video else 0.0
        meta = {
            "url": info.get("webpage_url") or item,
            "creator": creator,
            "creator_id": info.get("uploader_id"),
            "posted": info.get("upload_date"),
            "duration_s": round(duration, 1),
            "likes": info.get("like_count"),
            "views": info.get("view_count"),
            "comments": info.get("comment_count"),
            "intake_date": datetime.now().strftime("%Y-%m-%d"),
            "has_video": bool(video),
        }
        (dest / "caption.txt").write_text(caption or "(no caption)", encoding="utf-8")

        frames, sheet_ok = [], False
        transcript, lang, t_err = "", None, None
        if video:
            print(f"    {duration:.0f}s video, extracting frames...")
            frames = extract_frames(ffmpeg, video, dest / "frames", duration, args.max_frames, args.min_gap)
            sheet_ok = contact_sheet(ffmpeg, frames, dest / "sheet.jpg")
            if args.no_transcribe:
                t_err = "skipped (--no-transcribe)"
            elif not has_audio(ffmpeg, video):
                t_err = "no audio track"
            else:
                print("    transcribing...")
                try:
                    transcript, lang = transcribe(video, args.model)
                except Exception as e:  # keep frames + caption even if speech-to-text fails
                    t_err = f"failed: {e}"
        else:
            t_err = "no video (image post?)"
            thumbs = [p for p in dest.glob("video.*") if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
            if thumbs:
                thumbs[0].rename(dest / f"image{thumbs[0].suffix}")

        (dest / "transcript.txt").write_text(transcript or f"(no transcript: {t_err})", encoding="utf-8")
        meta.update({"language": lang, "frames": len(frames), "transcript_note": t_err})
        (dest / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

        if video and not args.keep_video:
            video.unlink(missing_ok=True)
        for leftover in dest.glob("video.*"):
            if not args.keep_video:
                leftover.unlink(missing_ok=True)

        index = [
            f"# {creator or 'Unknown creator'}: {first_line[:80]}",
            "",
            f"- URL: {meta['url']}",
            f"- Posted: {meta['posted'] or 'unknown'} · Duration: {meta['duration_s']}s · Views: {meta['views']} · Likes: {meta['likes']}",
            f"- Contact sheet: {'sheet.jpg' if sheet_ok else 'none'} · Frames: {len(frames)} in frames/",
            f"- Transcript: {'transcript.txt' + (f' ({lang})' if lang else '') if transcript else t_err}",
            "",
            "## Caption",
            "",
            caption or "(none)",
            "",
            "## Transcript",
            "",
            transcript or f"({t_err})",
            "",
        ]
        (dest / "index.md").write_text("\n".join(index), encoding="utf-8")
        result.update(ok=True, folder=str(dest), frames=len(frames), transcript=bool(transcript), note=t_err)
    except Exception as e:
        msg = str(e)
        low = msg.lower()
        hint = ""
        if isinstance(e, PermissionError):
            hint = " -> a file was locked (OneDrive/antivirus?). Retry, or pass --out to a folder outside OneDrive"
        elif stage != "download" or not is_url(item):
            pass
        elif any(k in low for k in ("proxy", "unable to connect", "getaddrinfo", "network is unreachable")):
            hint = " -> network problem: this machine can't reach the site"
        elif re.search(r"login|cookie|rate.?limit|\b401\b|\b403\b|private|unavailable", low):
            hint = " -> Instagram wants a login. Retry with --cookies-from-browser firefox or --cookies cookies.txt"
        result["error"] = msg.splitlines()[0][:300] + hint
        shutil.rmtree(tmp, ignore_errors=True)
    return result


def main():
    p = argparse.ArgumentParser(description="Download reels and turn them into transcript + frames.")
    p.add_argument("items", nargs="*", help="Instagram/TikTok/YouTube URLs or local video paths")
    p.add_argument("--file", help="text file with one URL/path per line")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output folder (default {DEFAULT_OUT})")
    p.add_argument("--cookies", help="cookies.txt exported from a logged-in browser")
    p.add_argument("--cookies-from-browser", help="firefox | chrome | edge | brave | safari")
    p.add_argument("--model", default="small", help="whisper model: tiny | base | small | medium (default small)")
    p.add_argument("--max-frames", type=int, default=12)
    p.add_argument("--min-gap", type=float, default=2.0, help="minimum seconds between frames")
    p.add_argument("--no-transcribe", action="store_true")
    p.add_argument("--keep-video", action="store_true")
    args = p.parse_args()

    items = list(args.items)
    if args.file:
        for line in Path(args.file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                items.append(line)
    if not items:
        p.error("give at least one URL/path, or --file")

    args.out.mkdir(parents=True, exist_ok=True)
    ffmpeg = ffmpeg_exe()
    results = []
    for i, item in enumerate(items, 1):
        print(f"[{i}/{len(items)}] {item}")
        r = process(item, args, ffmpeg)
        print(f"    -> {'OK ' + r['folder'] if r['ok'] else 'FAILED: ' + r['error']}")
        results.append(r)

    ok = sum(r["ok"] for r in results)
    print(f"\nDone: {ok}/{len(results)} succeeded.")
    (args.out / "last-run.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
