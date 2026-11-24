"""Write one short fictional call in every transcript format prep.py supports. Fictional people and business."""
from pathlib import Path

HERE = Path(__file__).resolve().parent / "fixtures"
HERE.mkdir(exist_ok=True)

TURNS = [
    (5, "Noah Nelson", "Thanks for jumping on. I want to lock the spring plan for the aeration route today."),
    (12, "Sam Rivera", "Sounds good. I mapped about forty lawns on the north side we could do in the first two weeks of April."),
    (25, "Noah Nelson", "Let's go with the north side first. That's decided."),
    (31, "Sam Rivera", "Great. Who's sending the reminder email to last year's customers?"),
    (36, "Noah Nelson", "I'll send it by Friday. Can you get the second machine serviced before April first?"),
    (44, "Sam Rivera", "Yes, I'll book the service this week. One open question is whether we offer overseeding as an add-on."),
    (55, "Noah Nelson", "Let's park overseeding until we've priced seed. I'll check prices at the supply store."),
    (63, "Sam Rivera", "Okay. And the flyer quote was three hundred and fifty dollars for a thousand flyers."),
    (70, "Noah Nelson", "Perfect. Let's talk again next Tuesday."),
]


def mmss(t):
    return f"{t // 60}:{t % 60:02d}"


def vtt_ts(t, end=False):
    t = t + (5 if end else 0)
    return f"00:{t // 60:02d}:{t % 60:02d}.000"


(HERE / "fathom.md").write_text(
    "---\ndate: 2026-03-10\ntype: raw\n---\n\n# Spring route planning\n\n**VIEW RECORDING - 2 mins**\n\n"
    + "\n".join(f"@{mmss(t)} - **{s}**\n{x}\n" for t, s, x in TURNS), encoding="utf-8")
(HERE / "wispr.md").write_text(
    "# Spring route planning\n\n## Complete transcript\n\n" + "\n".join(f"{s}:  {x}" for _, s, x in TURNS), encoding="utf-8")
(HERE / "zoom.vtt").write_text(
    "WEBVTT\n\n" + "\n".join(f"{i}\n{vtt_ts(t)} --> {vtt_ts(t, True)}\n{s}: {x}\n" for i, (t, s, x) in enumerate(TURNS, 1)), encoding="utf-8")
(HERE / "teams.vtt").write_text(
    "WEBVTT\n\n" + "\n".join(f"{vtt_ts(t)} --> {vtt_ts(t, True)}\n<v {s}>{x}</v>\n" for t, s, x in TURNS), encoding="utf-8")
(HERE / "call.srt").write_text(
    "\n".join(f"{i}\n{vtt_ts(t).replace('.', ',')} --> {vtt_ts(t, True).replace('.', ',')}\n{s}: {x}\n" for i, (t, s, x) in enumerate(TURNS, 1)), encoding="utf-8")
(HERE / "otter.txt").write_text(
    "\n".join(f"{s}  {mmss(t)}\n{x}\n" for t, s, x in TURNS), encoding="utf-8")
(HERE / "plain.txt").write_text(
    "\n\n".join(x for _, _, x in TURNS), encoding="utf-8")
(HERE / "speech.txt").write_text(" ".join(x for _, _, x in TURNS), encoding="utf-8")
print("fixtures written to", HERE)
