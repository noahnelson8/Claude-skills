"""Regression test for study-coach/scripts/study.py. Builds a tiny sample course (pptx, pdf, docx, md), then checks
extraction markers, concept add/update, spaced-repetition scheduling, next ordering, deadlines and report.

python -I tests/study-coach/run_tests.py
"""
import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

STUDY = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "study-coach" / "scripts" / "study.py"
fails = []


def run(*args):
    r = subprocess.run([sys.executable, "-I", str(STUDY), *map(str, args)], capture_output=True, text=True)
    if r.returncode:
        fails.append(f"{args[0]} failed: {r.stderr[-300:]}")
    return r.stdout


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


def make_materials(d: Path):
    from pptx import Presentation
    from pptx.util import Inches
    prs = Presentation()
    for title, body in [("Net Present Value", "NPV = sum of CF_t / (1+r)^t minus initial investment"),
                        ("Decision rule", "Accept the project if NPV > 0")]:
        s = prs.slides.add_slide(prs.slide_layouts[1])
        s.shapes.title.text = title
        s.placeholders[1].text = body
    prs.save(d / "lecture3-npv.pptx")

    import docx
    doc = docx.Document()
    doc.add_paragraph("IRR is the discount rate that makes NPV equal zero.")
    doc.save(d / "notes-irr.docx")

    (d / "syllabus.md").write_text("# FINAN sample\nMidterm covers NPV and IRR.\n", encoding="utf-8")

    html = d / "reading.html"
    html.write_text("<h1>Chapter 4</h1><p>Payback period ignores the time value of money.</p>"
                    "<p style='page-break-before:always'>Page two: WACC weights debt and equity costs.</p>", encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page()
        pg.goto(html.as_uri())
        pg.pdf(path=str(d / "chapter4.pdf"))
        b.close()
    html.unlink()


def main():
    tmp = Path(tempfile.mkdtemp())
    src, course = tmp / "src", tmp / "course"
    src.mkdir()
    make_materials(src)

    run("init", course, "--name", "FINAN sample")
    out = run("extract", course, src)
    mats = {p.name: p.read_text(encoding="utf-8") for p in (course / "materials").glob("*.txt")}
    check(len(mats) == 4, f"4 materials extracted ({len(mats)})")
    check("[slide 2]" in mats.get("lecture3-npv.txt", "") and "NPV > 0" in mats.get("lecture3-npv.txt", ""), "pptx has [slide N] markers and text")
    check("[p.2]" in mats.get("chapter4.txt", "") and "WACC" in mats.get("chapter4.txt", ""), "pdf has [p.N] markers and text")
    check("discount rate" in mats.get("notes-irr.txt", ""), "docx text extracted")

    concepts = tmp / "c.json"
    concepts.write_text(json.dumps([
        {"id": "npv-def", "name": "NPV definition", "level": 1, "source": "lecture3 slide 1", "unit": "Capital budgeting"},
        {"id": "npv-calc", "name": "NPV calculation", "level": 3, "source": "lecture3 slide 1", "unit": "Capital budgeting"},
        {"id": "irr-def", "name": "IRR definition", "level": 1, "source": "notes-irr", "unit": "Capital budgeting"},
        {"id": "payback", "name": "Payback ignores TVM", "level": 2, "source": "ch4 p.1", "unit": "Chapter 4"},
    ]), encoding="utf-8")
    run("add", course, concepts)
    c = json.loads((course / "course.json").read_text(encoding="utf-8"))["concepts"]
    check(len(c) == 4 and all(x["box"] == 0 for x in c.values()), "4 concepts added at box 0")

    run("record", course, "npv-def", "right")
    run("record", course, "npv-def", "right")
    run("record", course, "npv-calc", "wrong")
    run("record", course, "irr-def", "partial")
    c = json.loads((course / "course.json").read_text(encoding="utf-8"))["concepts"]
    t = date.today()
    check(c["npv-def"]["box"] == 2 and c["npv-def"]["due"] == str(t + timedelta(days=2)), "right x2 -> box 2, due in 2 days")
    check(c["npv-calc"]["box"] == 0 and c["npv-calc"]["due"] == str(t), "wrong -> box 0, due now")
    check(c["irr-def"]["box"] == 0 and c["irr-def"]["due"] == str(t + timedelta(days=1)), "partial -> same box, due tomorrow")

    run("deadline", course, "Midterm", str(t + timedelta(days=10)))
    nxt = run("next", course, "--n", "5")
    check("Midterm" in nxt, "next shows upcoming deadline")
    lines = [l for l in nxt.splitlines() if l.startswith("  ")]
    check(lines and lines[0].strip().startswith("npv-calc"), "the concept just missed comes first")
    check(not any(l.strip().startswith("npv-def") for l in lines), "mastering concept not due today is not shown")
    rep = run("report", course)
    check("Weakest so far" in rep and "NPV calculation" in rep, "report lists weakest concepts")

    concepts.write_text(json.dumps([{"id": "npv-def", "name": "NPV definition (updated)", "level": 1}]), encoding="utf-8")
    run("add", course, concepts)
    c = json.loads((course / "course.json").read_text(encoding="utf-8"))["concepts"]
    check(c["npv-def"]["name"].endswith("(updated)") and c["npv-def"]["box"] == 2, "re-adding updates a concept without losing progress")

    print("PASS" if not fails else "FAIL\n- " + "\n- ".join(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
