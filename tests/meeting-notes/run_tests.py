"""Regression test for meeting-notes/scripts/prep.py.

python -I tests/meeting-notes/run_tests.py            (text formats)
python -I tests/meeting-notes/run_tests.py --audio    (also transcribes fixtures/speech.wav if present)
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"
PREP = HERE.parents[1] / ".claude" / "skills" / "meeting-notes" / "scripts" / "prep.py"

CASES = {  # file: (expected format, expect speakers, expect timestamps)
    "fathom.md": ("fathom", True, True),
    "wispr.md": ("speaker: text", True, False),
    "zoom.vtt": ("vtt/srt", True, True),
    "teams.vtt": ("vtt/srt", True, True),
    "call.srt": ("vtt/srt", True, True),
    "otter.txt": ("otter", True, True),
    "plain.txt": ("plain text", False, False),
}


def run(name):
    out = Path(tempfile.mkdtemp())
    r = subprocess.run([sys.executable, "-I", str(PREP), str(FIX / name), "--out", str(out)], capture_output=True, text=True)
    if r.returncode:
        return None, r.stderr
    return json.loads((out / "stats.json").read_text(encoding="utf-8")), (out / "transcript.txt").read_text(encoding="utf-8")


def main():
    subprocess.run([sys.executable, "-I", str(HERE / "make_fixtures.py")], check=True, capture_output=True)
    fails = []
    for name, (fmt, speakers, stamps) in CASES.items():
        stats, text = run(name)
        if stats is None:
            fails.append(f"{name}: crashed: {text[-300:]}"); continue
        got = (stats["format"], set(stats["speakers"]) == {"Noah Nelson", "Sam Rivera"}, text.startswith("[00:05]"))
        ok = got[0] == fmt and got[1] == speakers and got[2] == stamps and "three hundred and fifty" in text
        print(f"{'ok  ' if ok else 'FAIL'} {name:11} format={got[0]!r} speakers={got[1]} timestamps={got[2]} words={stats['words']}")
        if not ok:
            fails.append(f"{name}: expected {fmt}/{speakers}/{stamps}, got {got}")
    if "--audio" in sys.argv and (FIX / "speech.wav").exists():
        stats, text = run("speech.wav")
        ok = stats is not None and "north side" in text.lower() and "friday" in text.lower()
        print(f"{'ok  ' if ok else 'FAIL'} speech.wav  format={stats and stats['format']!r} words={stats and stats['words']}")
        if not ok:
            fails.append("speech.wav: transcription missing expected phrases")
    print("PASS" if not fails else "FAIL\n- " + "\n- ".join(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
