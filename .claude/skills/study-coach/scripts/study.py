#!/usr/bin/env python3
"""
study-coach tracker: course materials in, concept progress out. Plain files, no accounts, nothing leaves the PC.

  python -I study.py init    <course_dir> --name "FINAN 4030"
  python -I study.py extract <course_dir> <file-or-folder> [...]   # pdf, pptx, docx, txt, md -> materials/*.txt with [p.N]/[slide N] markers
  python -I study.py add     <course_dir> <concepts.json>          # [{"id","name","level":1-5,"source":"lecture3.pdf p.4","unit":"..."}]
  python -I study.py record  <course_dir> <concept_id> <right|partial|wrong> [--note "..."] [--kind quiz|feynman|problem]
  python -I study.py next    <course_dir> [--n 5] [--unit "..."]   # what to study now (spaced repetition)
  python -I study.py report  <course_dir>                          # mastery by level and unit, weakest concepts, history
  python -I study.py deadline <course_dir> "<what>" <YYYY-MM-DD>   # exams/assignments, shown in report/next

Spaced repetition (Leitner boxes 0-5): right -> next box; partial -> same box, due tomorrow; wrong -> box 0, due now.
Box intervals in days: 0, 1, 2, 4, 8, 16. Box 5 = mastered (still reviewed every 16 days).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

INTERVALS = [0, 1, 2, 4, 8, 16]
TEXT_EXT = {".txt", ".md", ".markdown", ".csv"}


def load(course: Path) -> dict:
    f = course / "course.json"
    if not f.exists():
        sys.exit(f"No course here. Run: study.py init \"{course}\" --name \"<course name>\"")
    return json.loads(f.read_text(encoding="utf-8"))


def save(course: Path, data: dict):
    (course / "course.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def today() -> date:
    return date.today()


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "file"


# ---------------------------------------------------------------- extract
def extract_file(p: Path) -> str:
    ext = p.suffix.lower()
    if ext == ".pdf":
        from pypdf import PdfReader
        r = PdfReader(str(p))
        return "\n\n".join(f"[p.{i}]\n{(pg.extract_text() or '').strip()}" for i, pg in enumerate(r.pages, 1))
    if ext == ".pptx":
        from pptx import Presentation
        out = []
        for i, s in enumerate(Presentation(str(p)).slides, 1):
            bits = []
            for sh in s.shapes:
                if sh.has_text_frame:
                    bits += [para.text for para in sh.text_frame.paragraphs if para.text.strip()]
                if getattr(sh, "has_table", False) and sh.has_table:
                    bits += [" | ".join(c.text for c in row.cells) for row in sh.table.rows]
            if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
                bits.append("Speaker notes: " + s.notes_slide.notes_text_frame.text.strip())
            out.append(f"[slide {i}]\n" + "\n".join(bits))
        return "\n\n".join(out)
    if ext == ".docx":
        import docx
        d = docx.Document(str(p))
        return "\n".join(par.text for par in d.paragraphs if par.text.strip())
    if ext in TEXT_EXT:
        return p.read_text(encoding="utf-8", errors="replace")
    raise ValueError(f"unsupported file type: {p.name} (pdf, pptx, docx, txt, md)")


def cmd_extract(a):
    course = Path(a.course)
    data = load(course)
    mats = course / "materials"
    mats.mkdir(exist_ok=True)
    files = []
    for src in a.sources:
        sp = Path(src)
        files += sorted(x for x in sp.rglob("*") if x.is_file()) if sp.is_dir() else [sp]
    done = []
    for f in files:
        try:
            text = extract_file(f)
        except ValueError:
            continue
        except Exception as e:  # a broken file shouldn't stop the rest
            print(f"  skipped {f.name}: {e}")
            continue
        words = len(text.split())
        out = mats / f"{slug(f.stem)}.txt"
        out.write_text(f"# source: {f.name}\n\n{text}\n", encoding="utf-8")
        data.setdefault("materials", {})[f.name] = {"file": out.name, "words": words, "added": str(today())}
        done.append((f.name, words))
        warn = "  (almost no text: scanned slides? read the original visually)" if words < 40 else ""
        print(f"  {f.name} -> materials/{out.name} ({words} words){warn}")
    save(course, data)
    print(f"Extracted {len(done)} file(s).")


# ---------------------------------------------------------------- concepts & progress
def cmd_init(a):
    course = Path(a.course)
    course.mkdir(parents=True, exist_ok=True)
    f = course / "course.json"
    if f.exists():
        print(f"Already set up: {f}")
        return
    save(course, {"name": a.name, "created": str(today()), "materials": {}, "concepts": {}, "deadlines": [], "sessions": []})
    (course / "materials").mkdir(exist_ok=True)
    print(f"Course '{a.name}' set up in {course}")


def cmd_add(a):
    course = Path(a.course)
    data = load(course)
    items = json.loads(Path(a.json).read_text(encoding="utf-8"))
    added = updated = 0
    for it in items:
        cid = it.get("id") or slug(it["name"])
        cur = data["concepts"].get(cid)
        base = {"name": it["name"], "level": int(it.get("level", 1)), "source": it.get("source", ""), "unit": it.get("unit", "")}
        if cur:
            cur.update({k: v for k, v in base.items() if v})
            updated += 1
        else:
            data["concepts"][cid] = {**base, "box": 0, "due": str(today()), "seen": 0, "right": 0, "partial": 0, "wrong": 0, "history": []}
            added += 1
    save(course, data)
    print(f"{added} concept(s) added, {updated} updated. Total: {len(data['concepts'])}.")


def cmd_record(a):
    course = Path(a.course)
    data = load(course)
    c = data["concepts"].get(a.concept)
    if not c:
        sys.exit(f"Unknown concept id '{a.concept}'. Known: {', '.join(list(data['concepts'])[:20])}")
    if a.result == "right":
        c["box"] = min(5, c["box"] + 1)
        c["due"] = str(today() + timedelta(days=INTERVALS[c["box"]]))
    elif a.result == "partial":
        c["due"] = str(today() + timedelta(days=1))
    else:
        c["box"] = 0
        c["due"] = str(today())
    c["seen"] += 1
    c[a.result] += 1
    c["history"].append({"at": datetime.now().strftime("%Y-%m-%d %H:%M"), "result": a.result, "kind": a.kind, "note": a.note or ""})
    c["history"] = c["history"][-30:]
    data.setdefault("sessions", []).append({"date": str(today()), "concept": a.concept, "result": a.result, "kind": a.kind})
    save(course, data)
    print(f"{c['name']}: {a.result} -> box {c['box']}, next review {c['due']}")


def due_list(data, unit=None):
    t = str(today())
    cs = [(cid, c) for cid, c in data["concepts"].items() if (not unit or c.get("unit") == unit)]
    due = [x for x in cs if x[1]["due"] <= t]
    # weakest first: wrong recently, low box, low level (foundations before advanced)
    due.sort(key=lambda x: (x[1]["box"], -(x[1]["history"][-1]["result"] == "wrong") if x[1]["history"] else 0, x[1]["level"], x[1]["due"]))
    unseen = [x for x in cs if x[1]["seen"] == 0]
    return due, unseen


def upcoming(data, days=21):
    t = today()
    out = []
    for d in data.get("deadlines", []):
        dd = date.fromisoformat(d["date"])
        if t <= dd <= t + timedelta(days=days):
            out.append(f"{d['what']} on {d['date']} ({(dd - t).days} days)")
    return out


def cmd_next(a):
    data = load(Path(a.course))
    due, unseen = due_list(data, a.unit)
    for u in upcoming(data):
        print(f"Coming up: {u}")
    print(f"Due now: {len(due)} · never studied: {len(unseen)} · total: {len(data['concepts'])}")
    for cid, c in due[: a.n]:
        last = c["history"][-1]["result"] if c["history"] else "new"
        print(f"  {cid} | {c['name']} | level {c['level']} | box {c['box']} | last: {last} | source: {c['source']}")


def cmd_report(a):
    data = load(Path(a.course))
    cs = data["concepts"]
    if not cs:
        print("No concepts yet.")
        return
    print(f"# {data['name']}: {len(cs)} concepts")
    for u in upcoming(data, 60):
        print(f"Coming up: {u}")
    mastered = sum(1 for c in cs.values() if c["box"] >= 4)
    print(f"Mastered (box 4-5): {mastered}/{len(cs)} · in progress: {sum(1 for c in cs.values() if 1 <= c['box'] < 4)} · weak/new: {sum(1 for c in cs.values() if c['box'] == 0)}")
    by = {}
    for c in cs.values():
        by.setdefault(f"level {c['level']}", []).append(c["box"])
    for k in sorted(by):
        print(f"  {k}: {len(by[k])} concepts, avg box {sum(by[k]) / len(by[k]):.1f}")
    units = {}
    for c in cs.values():
        if c.get("unit"):
            units.setdefault(c["unit"], []).append(c["box"])
    for k, v in units.items():
        print(f"  unit '{k}': {sum(1 for b in v if b >= 4)}/{len(v)} mastered")
    weak = sorted((c for c in cs.values() if c["seen"]), key=lambda c: (c["wrong"] - c["right"], -c["box"]), reverse=True)[:5]
    if weak:
        print("Weakest so far:")
        for c in weak:
            print(f"  {c['name']}: {c['right']} right / {c['partial']} partial / {c['wrong']} wrong, box {c['box']}")
    days = sorted({s['date'] for s in data.get('sessions', [])})
    print(f"Study days logged: {len(days)}" + (f" (last {days[-1]})" if days else ""))


def cmd_deadline(a):
    course = Path(a.course)
    data = load(course)
    date.fromisoformat(a.date)
    data.setdefault("deadlines", []).append({"what": a.what, "date": a.date})
    save(course, data)
    print(f"Added: {a.what} on {a.date}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("course"); p.add_argument("--name", required=True); p.set_defaults(f=cmd_init)
    p = sub.add_parser("extract"); p.add_argument("course"); p.add_argument("sources", nargs="+"); p.set_defaults(f=cmd_extract)
    p = sub.add_parser("add"); p.add_argument("course"); p.add_argument("json"); p.set_defaults(f=cmd_add)
    p = sub.add_parser("record"); p.add_argument("course"); p.add_argument("concept"); p.add_argument("result", choices=["right", "partial", "wrong"])
    p.add_argument("--note"); p.add_argument("--kind", default="quiz", choices=["quiz", "feynman", "problem"]); p.set_defaults(f=cmd_record)
    p = sub.add_parser("next"); p.add_argument("course"); p.add_argument("--n", type=int, default=5); p.add_argument("--unit"); p.set_defaults(f=cmd_next)
    p = sub.add_parser("report"); p.add_argument("course"); p.set_defaults(f=cmd_report)
    p = sub.add_parser("deadline"); p.add_argument("course"); p.add_argument("what"); p.add_argument("date"); p.set_defaults(f=cmd_deadline)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
