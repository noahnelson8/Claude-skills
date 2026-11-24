"""Regression test for the app-compliance-check scanner.

python -I tests/app-compliance-check/run_tests.py   (from the claude-skills repo root)

bad-app has 12 planted problems; good-app is the same app with them fixed.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCAN = HERE.parents[1] / ".claude" / "skills" / "app-compliance-check" / "scripts" / "scan.py"

EXPECT_BAD = [
    "no privacy/terms page", "Uses AI providers", "Ad pixels or session replay present", "Do Not Sell",
    "public storage", "no storage-object removal", "no self-serve cancel", "no trial-ending reminder",
    "no crisis/self-harm", "talking to an AI", "Testimonials/ratings", "no SMS consent text", "Accessibility",
]


def scan(app):
    out = Path(tempfile.mkdtemp())
    subprocess.run([sys.executable, "-I", str(SCAN), str(HERE / app), "--out", str(out)], check=True, capture_output=True)
    data = json.loads((out / "inventory.json").read_text(encoding="utf-8"))
    leaked = any(s in p.read_text(encoding="utf-8") for p in out.iterdir() for s in ("sk-fake", "sk_test_fake"))
    return data, leaked


def main():
    fails = []
    bad, leaked = scan("bad-app")
    notes = " | ".join(f["note"] for f in bad["flags"])
    for e in EXPECT_BAD:
        if e.lower() not in notes.lower():
            fails.append(f"bad-app: missing flag containing '{e}'")
    if leaked:
        fails.append("bad-app: a secret value leaked into the output")
    if set(bad["env_variable_names"]) != {"OPENAI_API_KEY", "STRIPE_SECRET_KEY", "SUPABASE_URL"}:
        fails.append("bad-app: env variable names not reported correctly")

    good, _ = scan("good-app")
    serious = [f for f in good["flags"] if f["rating"] in ("blocking?", "fix soon?")]
    if serious:
        fails.append("good-app: unexpected flags: " + "; ".join(f["note"] for f in serious))

    print(f"bad-app flags: {len(bad['flags'])}, good-app flags: {len(good['flags'])}")
    print("PASS" if not fails else "FAIL\n- " + "\n- ".join(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
