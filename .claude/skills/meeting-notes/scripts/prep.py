#!/usr/bin/env python3
"""
meeting-notes prep: turn any transcript (or an audio/video recording) into one clean, speaker-labelled text
that Claude can read and quote with timestamps.

Usage:
  python -I prep.py <file> [--out <dir>] [--model small] [--chunk-words 6000]

Understands: Fathom ("@12:34 - **Name**" blocks), Wispr / Zoom chat style ("Name: text"), WebVTT (.vtt),
SubRip (.srt), Otter ("Name  12:34" then text), Fathom/Granola markdown, plain text, and audio/video
(.mp3 .m4a .wav .mp4 .mov .webm .ogg .aac .flac), which is transcribed locally with faster-whisper.

Writes to <out> (default: a "<file stem>.prep" folder next to the input):
  transcript.txt   "[mm:ss] Speaker: text" lines (consecutive lines by the same speaker merged)
  stats.json       speakers, talk share by words, duration, word count, detected format, chunk count
  chunk-NN.txt     only for long meetings: pieces of ~chunk-words words, split on speaker turns
Nothing leaves this computer.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AUDIO = {".mp3", ".m4a", ".wav", ".mp4", ".mov", ".webm", ".ogg", ".aac", ".flac", ".mkv"}
TS = r"(?:(\d{1,2}):)?(\d{1,2}):(\d{2})(?:[.,]\d{1,3})?"


def secs(h, m, s) -> int:
    return int(h or 0) * 3600 + int(m) * 60 + int(s)


def fmt(t: int | None) -> str:
    if t is None:
        return ""
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"[{h}:{m:02d}:{s:02d}] " if h else f"[{m:02d}:{s:02d}] "


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


# ---------------------------------------------------------------- parsers: each returns [(t|None, speaker|None, text)]
def parse_fathom(text):
    rx = re.compile(r"^@" + TS + r"\s*-\s*\*\*(.+?)\*\*\s*$")
    out, cur = [], None
    for line in text.splitlines():
        m = rx.match(line.strip())
        if m:
            cur = [secs(*m.groups()[:3]), m.group(4).strip(), []]
            out.append(cur)
        elif cur is not None and line.strip():
            cur[2].append(line.strip())
    return [(t, s, " ".join(ws)) for t, s, ws in out if ws]


def parse_vtt_srt(text):
    rx = re.compile(TS + r"\s*-->\s*" + TS)
    out, t, buf = [], None, []
    def flush():
        if buf:
            line = " ".join(buf)
            m = re.match(r"^<v\s+([^>]+)>(.*?)(</v>)?$", line) or re.match(r"^([A-Z][\w .'\-]{1,40}):\s+(.*)$", line)
            sp, body = (m.group(1).strip(), m.group(2).strip()) if m else (None, line)
            out.append((t, sp, re.sub(r"<[^>]+>", "", body)))
    for raw in text.splitlines():
        line = raw.strip()
        m = rx.search(line)
        if m:
            flush(); buf = []
            t = secs(*m.groups()[:3])
        elif not line or line.isdigit() or line.upper().startswith(("WEBVTT", "NOTE", "STYLE")):
            continue
        else:
            buf.append(line)
    flush()
    return out


def parse_otter(text):
    rx = re.compile(r"^(.{2,40}?)\s{2,}" + TS + r"\s*$")
    out, cur = [], None
    for line in text.splitlines():
        m = rx.match(line.rstrip())
        if m:
            cur = [secs(*m.groups()[1:4]), m.group(1).strip(), []]
            out.append(cur)
        elif cur is not None and line.strip():
            cur[2].append(line.strip())
    return [(t, s, " ".join(ws)) for t, s, ws in out if ws]


def parse_colon(text):
    rx = re.compile(r"^(?:\[?" + TS + r"\]?\s*)?([A-Z][\w.'\-]*(?: [A-Z][\w.'\-]*){0,3}):\s+(.+)$")
    out = []
    for line in text.splitlines():
        m = rx.match(line.strip())
        if m:
            h, mm, ss, sp, body = m.groups()
            out.append((secs(h, mm, ss) if mm else None, sp.strip(), body.strip()))
        elif line.strip() and out and not line.lstrip().startswith(("#", ">", "---", "**")):
            t, sp, body = out[-1]
            out[-1] = (t, sp, body + " " + line.strip())
    return out


def parse_plain(text):
    return [(None, None, p.strip()) for p in re.split(r"\n\s*\n", text) if p.strip() and not p.lstrip().startswith(("#", ">"))]


def detect_and_parse(path: Path, text: str):
    body = strip_frontmatter(text)
    if path.suffix.lower() in {".vtt", ".srt"} or re.search(TS + r"\s*-->\s*" + TS, body[:4000]):
        return "vtt/srt", parse_vtt_srt(body)
    fathom = parse_fathom(body)
    if len(fathom) >= 3:
        return "fathom", fathom
    otter = parse_otter(body)
    if len(otter) >= 3:
        return "otter", otter
    colon = parse_colon(body)
    lines = [l for l in body.splitlines() if l.strip()]
    if len(colon) >= 3 and len(colon) >= 0.3 * max(1, len(lines)):
        return "speaker: text", colon
    return "plain text", parse_plain(body)


def transcribe(path: Path, model: str):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper is not installed. Run: pip install faster-whisper (reel-intake's requirements include it).")
    print(f"Transcribing {path.name} locally with whisper '{model}' (first run downloads the model)...", file=sys.stderr)
    wm = WhisperModel(model, device="auto", compute_type="int8")
    segs, info = wm.transcribe(str(path), vad_filter=True, beam_size=5)
    return "audio (whisper, no speaker labels)", [(int(s.start), None, s.text.strip()) for s in segs]


def merge(turns):
    out = []
    for t, sp, body in turns:
        if sp:  # Fathom/Zoom sometimes add "(company.com)" or "(Guest)" to the same person's name
            sp = re.sub(r"\s*\((?:[\w.\-]+\.\w{2,}|guest|host|external|she/her|he/him|they/them)\)\s*$", "", sp, flags=re.I).strip()
        body = re.sub(r"\s+", " ", body).strip()
        if not body:
            continue
        if out and sp and out[-1][1] == sp:
            out[-1] = (out[-1][0], sp, out[-1][2] + " " + body)
        else:
            out.append((t, sp, body))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--out")
    ap.add_argument("--model", default="small")
    ap.add_argument("--chunk-words", type=int, default=6000)
    a = ap.parse_args()
    src = Path(a.file).expanduser().resolve()
    if not src.is_file():
        sys.exit(f"File not found: {src}")
    out = Path(a.out).resolve() if a.out else src.parent / (src.stem + ".prep")
    out.mkdir(parents=True, exist_ok=True)

    if src.suffix.lower() in AUDIO:
        kind, turns = transcribe(src, a.model)
    else:
        kind, turns = detect_and_parse(src, src.read_text(encoding="utf-8", errors="replace"))
    turns = merge(turns)
    if not turns:
        sys.exit("No transcript text found in the file.")

    lines = [f"{fmt(t)}{(sp + ': ') if sp else ''}{body}" for t, sp, body in turns]
    (out / "transcript.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    words = {}
    for _, sp, body in turns:
        words[sp or "(unlabelled)"] = words.get(sp or "(unlabelled)", 0) + len(body.split())
    total = sum(words.values())
    times = [t for t, _, _ in turns if t is not None]

    chunks, cur, n = [], [], 0
    for line in lines:
        w = len(line.split())
        if cur and n + w > a.chunk_words:
            chunks.append(cur); cur, n = [], 0
        cur.append(line); n += w
    if cur:
        chunks.append(cur)
    for old in out.glob("chunk-*.txt"):
        old.unlink()
    if len(chunks) > 1:
        for i, c in enumerate(chunks, 1):
            (out / f"chunk-{i:02d}.txt").write_text("\n".join(c) + "\n", encoding="utf-8")

    stats = {
        "source": str(src), "format": kind, "turns": len(turns), "words": total,
        "duration": fmt(max(times)).strip(" []") if times else None,
        "speakers": {k: {"words": v, "share": f"{round(100 * v / total)}%"} for k, v in sorted(words.items(), key=lambda x: -x[1])},
        "chunks": len(chunks) if len(chunks) > 1 else 0,
        "note": "Machine transcripts mishear names, numbers and jargon; check anything you quote.",
    }
    (out / "stats.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print(f"\nWrote {out / 'transcript.txt'}" + (f" and {len(chunks)} chunks" if len(chunks) > 1 else ""))


if __name__ == "__main__":
    main()
