#!/usr/bin/env python3
"""
app-compliance-check scanner: a read-only, heuristic inventory of what a codebase collects and where it sends it.

Usage:
  python -I scan.py <project_dir> [--out <dir>] [--max-files 20000]

Writes <out>/inventory.json and <out>/inventory.md (default out: <project_dir>/compliance).
Never prints secret values: for .env-style files it records variable NAMES only.
Every finding is a lead to confirm by opening the file, not a verdict.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", "out", ".venv", "venv", "__pycache__", ".turbo",
             ".vercel", ".cache", "coverage", "vendor", ".svelte-kit", ".nuxt", "compliance", "Pods", ".gradle"}
CODE_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro", ".html", ".htm", ".py", ".rb",
            ".php", ".go", ".java", ".kt", ".swift", ".dart", ".json", ".yml", ".yaml", ".toml", ".sql", ".rules",
            ".md", ".mdx", ".liquid", ".hbs", ".ejs", ".txt", ".tf"}
ENV_NAMES = re.compile(r"^\.env(\..*)?$|\.env$")
MAX_BYTES = 1_500_000

# --- third parties: category -> {name: regex}
SERVICES = {
    "analytics": {
        "Google Analytics / Tag Manager": r"googletagmanager\.com|google-analytics\.com|\bgtag\(|@next/third-parties/google|react-ga",
        "Segment": r"segment\.(com|io)|analytics\.js|@segment/",
        "Mixpanel": r"mixpanel", "PostHog": r"posthog", "Amplitude": r"amplitude",
        "Plausible": r"plausible\.io", "Microsoft Clarity": r"clarity\.ms", "Vercel Analytics": r"@vercel/analytics",
    },
    "ad pixels": {
        "Meta Pixel": r"connect\.facebook\.net|\bfbq\(|facebook-pixel", "TikTok Pixel": r"analytics\.tiktok\.com|\bttq\.",
        "Google Ads": r"googleadservices|AW-\d{6,}", "LinkedIn Insight": r"snap\.licdn\.com|_linkedin_partner_id",
        "X/Twitter pixel": r"static\.ads-twitter\.com|\btwq\(", "Reddit pixel": r"redditstatic\.com/ads|\brdt\(",
    },
    "session replay / error tracking": {
        "Hotjar": r"hotjar", "FullStory": r"fullstory", "LogRocket": r"logrocket", "Sentry": r"@sentry/|sentry_sdk|sentry\.io",
        "Smartlook": r"smartlook", "Mouseflow": r"mouseflow",
    },
    "AI providers": {
        "OpenAI": r"\bopenai\b|api\.openai\.com", "Anthropic": r"@anthropic-ai|\banthropic\b|api\.anthropic\.com",
        "Google Gemini": r"@google/genai|google\.generativeai|generativelanguage\.googleapis|@google/generative-ai",
        "Mistral": r"mistralai", "Cohere": r"\bcohere\b", "Replicate": r"replicate\.com|\breplicate\b",
        "Groq": r"groq-sdk|api\.groq\.com", "ElevenLabs": r"elevenlabs", "OpenRouter": r"openrouter\.ai",
        "Vercel AI SDK": r"from ['\"]ai['\"]|@ai-sdk/",
    },
    "payments": {
        "Stripe": r"\bstripe\b|js\.stripe\.com", "PayPal": r"paypal", "Lemon Squeezy": r"lemonsqueezy",
        "Paddle": r"paddle\.(com|js)|@paddle/", "Square": r"squareup|square\.com/",
    },
    "backend / storage": {
        "Supabase": r"supabase", "Firebase": r"firebase", "AWS S3": r"@aws-sdk/client-s3|aws-sdk|boto3|s3\.amazonaws",
        "Cloudinary": r"cloudinary", "UploadThing": r"uploadthing", "Vercel Blob": r"@vercel/blob",
        "Cloudflare R2": r"r2\.cloudflarestorage", "MongoDB": r"mongodb", "PlanetScale/Neon": r"planetscale|neon\.tech|@neondatabase",
    },
    "email / SMS / CRM": {
        "GoHighLevel / LeadConnector": r"gohighlevel|leadconnector|msgsndr|highlevel", "Twilio": r"twilio",
        "SendGrid": r"sendgrid", "Mailgun": r"mailgun", "Resend": r"\bresend\b", "Postmark": r"postmark",
        "Mailchimp": r"mailchimp", "ConvertKit/Kit": r"convertkit", "Klaviyo": r"klaviyo", "HubSpot": r"hubspot",
        "Brevo": r"brevo|sendinblue", "Intercom": r"intercom", "Crisp": r"crisp\.chat",
    },
    "auth": {"Auth0": r"auth0", "Clerk": r"@clerk/|clerk\.com", "NextAuth/Auth.js": r"next-auth|@auth/", "Firebase Auth": r"firebase/auth"},
}
SERVICE_RX = {cat: {n: re.compile(p, re.I) for n, p in d.items()} for cat, d in SERVICES.items()}

PII_FIELDS = {
    "email": r"type=[\"']email|name=[\"'][^\"']*e-?mail|\bemail\s*[:=]",
    "phone": r"type=[\"']tel|name=[\"'][^\"']*phone|\bphone(_?number)?\s*[:=]",
    "name": r"name=[\"'](first_?name|last_?name|full_?name|name)[\"']",
    "address": r"name=[\"'][^\"']*(address|street|zip|postal)",
    "date of birth": r"(dob|date_?of_?birth|birth_?date|birthday)",
    "government ID": r"\b(ssn|social_security|passport_?number|driver'?s?_?licen[cs]e)\b",
    "payment card": r"(card_?number|cc_?number|cvc|cvv)\b",
    "health": r"\b(diagnosis|medical_?history|medication|health_?condition)\b",
    "file upload": r"type=[\"']file|multipart/form-data|\.upload\(|putObject|PutObjectCommand|createSignedUploadUrl",
    "location": r"navigator\.geolocation|getCurrentPosition",
}
PII_RX = {k: re.compile(v, re.I) for k, v in PII_FIELDS.items()}

CHECKS = {
    "cookies": r"document\.cookie|set-cookie|cookies\(\)|res\.cookie\(|js-cookie|cookieconsent|cookiebot|onetrust|osano|klaro",
    "storage public flags": r"public\s*:\s*true|['\"]?ACL['\"]?\s*:\s*['\"]public-read|public-read|\"Principal\"\s*:\s*\"\*\"|allow read(, write)?\s*:\s*if true|allow read(, write)?;|BlockPublicAcls\s*[:=]\s*false|getPublicUrl\(",
    "delete handlers": r"delete_?(user|account|profile)|deleteUser|deleteAccount|removeUser|destroy_?account|auth\.admin\.deleteUser|\.delete\(\)\s*\.eq\(",
    "storage removal": r"\.remove\(\[|deleteObject|DeleteObjectCommand|delete_object|\.storage\.from\([^)]*\)\.remove|destroy\(|uploader\.destroy|del\(\s*url",
    "subscriptions": r"subscription|recurring|auto-?renew|price_id|priceId|billing_cycle|interval\s*[:=]\s*['\"](month|year)",
    "trials": r"trial_period_days|trial_end|trialEnd|free[ -]trial|trial_will_end|trialDays",
    "cancel flow": r"cancel_?(subscription|plan|membership)|cancelSubscription|subscriptions\.(cancel|update)\([^)]*cancel_at_period_end|billingPortal|billing_portal|customer_portal|>\s*cancel (my )?(subscription|plan)",
    "trial reminder": r"trial_will_end|trial.?reminder|reminder.?(email|before)|days? before (your )?trial",
    "chatbot": r"chat\.completions|messages\.create|responses\.create|generateText|streamText|useChat|role:\s*['\"]system|system_prompt|systemPrompt",
    "crisis language": r"\b988\b|crisis (line|text|hotline)|self-?harm|suicid|samaritans|lifeline",
    "AI disclosure": r"(i am|i'm) an? (ai|artificial|virtual assistant|bot)|ai[- ]generated|powered by (ai|gpt|claude)|you are chatting with an? (ai|bot)",
    "privacy / terms pages": r"privacy[-_ ]?policy|/privacy\b|terms[-_ ]?(of[-_ ]?(service|use))?\b|/terms\b",
    "testimonials / reviews": r"testimonial|aggregateRating|ratingValue|reviewCount|★★★★|stars?\s*[:=]\s*5|\breviews\s*=\s*\[",
    "SMS consent text": r"msg (&|and) data rates|reply stop|text stop|message frequency|consent to receive (text|sms)",
    "email unsubscribe": r"unsubscribe|\{\{\s*unsubscribe|list-unsubscribe|opt[- ]out",
    "do not sell / GPC": r"do not sell|do not share|globalPrivacyControl|Sec-GPC|your privacy choices",
    "age / children": r"\b(under|over) ?1[3-8]\b|age_?verification|coppa|parental consent|min(imum)?_?age",
}
CHECK_RX = {k: re.compile(v, re.I) for k, v in CHECKS.items()}

IMG_NO_ALT = re.compile(r"<img(?![^>]*\balt=)[^>]*>", re.I)
INPUT_TAG = re.compile(r"<input(?![^>]*type=[\"'](hidden|submit|button)[\"'])[^>]*>", re.I)
HAS_LABEL_ATTR = re.compile(r"aria-label|aria-labelledby|\bid=", re.I)
ENV_LINE = re.compile(r"^\s*(?:export\s+)?([A-Z][A-Z0-9_]{2,})\s*=")


def iter_files(root: Path, max_files: int):
    n = 0
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            entries = list(d.iterdir())
        except (PermissionError, OSError):
            continue
        for p in entries:
            if p.is_dir():
                if p.name not in SKIP_DIRS and not p.is_symlink():
                    stack.append(p)
            elif p.is_file():
                yield p
                n += 1
                if n >= max_files:
                    return


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def snippet(text: str, pos: int) -> str:
    s = text.rfind("\n", 0, pos) + 1
    e = text.find("\n", pos)
    line = text[s:e if e != -1 else None].strip()
    # never echo things that look like secrets
    line = re.sub(r"(sk|pk|rk|whsec|xox[bpa]|ghp|AKIA)[-_A-Za-z0-9]{8,}", "<redacted>", line)
    line = re.sub(r"(['\"])[A-Za-z0-9_\-]{32,}\1", "'<redacted>'", line)
    return line[:160]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--out")
    ap.add_argument("--max-files", type=int, default=20000)
    a = ap.parse_args()
    root = Path(a.project).resolve()
    if not root.is_dir():
        sys.exit(f"Not a folder: {root}")
    out = Path(a.out).resolve() if a.out else root / "compliance"

    services = defaultdict(lambda: defaultdict(list))   # cat -> name -> [loc]
    pii = defaultdict(list)
    checks = defaultdict(list)
    env_vars = defaultdict(list)
    a11y = {"img_without_alt": [], "inputs_maybe_unlabelled": []}
    files_scanned = 0

    for p in iter_files(root, a.max_files):
        rel = p.relative_to(root).as_posix()
        if ENV_NAMES.search(p.name):
            try:
                for i, l in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    m = ENV_LINE.match(l)
                    if m:
                        env_vars[m.group(1)].append(f"{rel}:{i}")
            except OSError:
                pass
            continue
        if p.suffix.lower() not in CODE_EXT or p.name in {"package-lock.json", "yarn.lock", "pnpm-lock.yaml"}:
            continue
        try:
            if p.stat().st_size > MAX_BYTES:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        files_scanned += 1
        is_pkg = p.name in {"package.json", "requirements.txt", "pyproject.toml", "Gemfile", "composer.json", "go.mod", "pubspec.yaml"}

        for cat, rx in SERVICE_RX.items():
            for name, r in rx.items():
                m = r.search(text)
                if m:
                    services[cat][name].append(f"{rel}:{line_of(text, m.start())}" + (" (dependency)" if is_pkg else ""))
        if is_pkg:
            continue
        for bucket, rxs in ((pii, PII_RX), (checks, CHECK_RX)):
            for k, r in rxs.items():
                seen = {x["at"] for x in bucket.get(k, [])}
                for m in list(r.finditer(text))[:6]:
                    at = f"{rel}:{line_of(text, m.start())}"
                    if at not in seen and len(seen) < 12:
                        seen.add(at)
                        bucket[k].append({"at": at, "line": snippet(text, m.start())})
        if p.suffix.lower() in {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".ejs", ".hbs", ".liquid"}:
            for m in list(IMG_NO_ALT.finditer(text))[:5]:
                a11y["img_without_alt"].append(f"{rel}:{line_of(text, m.start())}")
            for m in list(INPUT_TAG.finditer(text))[:20]:
                if not HAS_LABEL_ATTR.search(m.group(0)):
                    a11y["inputs_maybe_unlabelled"].append(f"{rel}:{line_of(text, m.start())}")

    # --- derived flags (leads, not verdicts)
    flags = []
    def has(k): return bool(checks.get(k))
    collected = sorted(pii)
    if (collected or services) and not has("privacy / terms pages"):
        flags.append(("blocking?", "Collects data or uses third parties, but no privacy/terms page or link was found."))
    if services.get("AI providers"):
        flags.append(("check", "Uses AI providers: the privacy policy must disclose AI processing and name the providers or category."))
    if services.get("ad pixels") or services.get("session replay / error tracking"):
        flags.append(("check", "Ad pixels or session replay present: disclose them; consider 'Do Not Sell or Share' and consent before firing."))
        if not has("do not sell / GPC"):
            flags.append(("fix soon?", "Ad pixels/session replay found but no 'Do Not Sell or Share' / Global Privacy Control handling."))
    if has("storage public flags"):
        flags.append(("blocking?", "Possible public storage (public bucket / public-read / open rules / getPublicUrl). Confirm user uploads are private."))
    if has("delete handlers") and not has("storage removal"):
        flags.append(("fix soon?", "Delete handlers exist but no storage-object removal calls were found: deleted users' files may remain."))
    if "file upload" in pii and not has("delete handlers"):
        flags.append(("fix soon?", "File uploads exist but no account/data delete path was found."))
    if has("subscriptions") and not has("cancel flow"):
        flags.append(("fix soon?", "Subscriptions found but no self-serve cancel path (cancel button / billing portal)."))
    if has("trials") and not has("trial reminder"):
        flags.append(("blocking?", "Free trial found but no trial-ending reminder (e.g. Stripe trial_will_end webhook or reminder email)."))
    if has("chatbot") and not has("crisis language"):
        flags.append(("blocking?", "AI chat found but no crisis/self-harm handling (988, crisis resources) anywhere in the code."))
    if has("chatbot") and not has("AI disclosure"):
        flags.append(("fix soon?", "AI chat found but no 'you're talking to an AI' disclosure text."))
    if has("testimonials / reviews"):
        flags.append(("check", "Testimonials/ratings in code: confirm each is from a real, consenting customer (FTC review rule)."))
    if "phone" in pii and (services["email / SMS / CRM"].get("Twilio") or services["email / SMS / CRM"].get("GoHighLevel / LeadConnector")) and not has("SMS consent text"):
        flags.append(("blocking?", "Phone numbers + an SMS-capable provider, but no SMS consent text (STOP / msg & data rates) was found."))
    if a11y["img_without_alt"] or a11y["inputs_maybe_unlabelled"]:
        flags.append(("good to have", f"Accessibility: {len(a11y['img_without_alt'])} images without alt, {len(a11y['inputs_maybe_unlabelled'])} inputs possibly unlabelled (sampled)."))

    result = {
        "project": str(root), "scanned": date.today().isoformat(), "files_scanned": files_scanned,
        "personal_data_collected": {k: v for k, v in sorted(pii.items())},
        "third_parties": {c: dict(n) for c, n in services.items()},
        "checks": dict(checks),
        "env_variable_names": {k: v for k, v in sorted(env_vars.items())},
        "accessibility_sample": a11y,
        "flags": [{"rating": r, "note": n} for r, n in flags],
        "note": "Heuristic leads only. Open each location and confirm before reporting.",
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "inventory.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    md = [f"# Compliance inventory: {root.name}", "", f"Scanned {result['scanned']} · {files_scanned} files · heuristic leads, confirm each one.", ""]
    md += ["## Flags", ""] + ([f"- **{r}** {n}" for r, n in flags] or ["- none"]) + [""]
    md += ["## Personal data collected", ""] + ([f"- **{k}**: {', '.join(x['at'] for x in v[:4])}" for k, v in sorted(pii.items())] or ["- none found"]) + [""]
    md += ["## Third parties", ""]
    for c, names in services.items():
        md.append(f"- **{c}**: " + "; ".join(f"{n} ({locs[0]})" for n, locs in names.items()))
    if not services:
        md.append("- none found")
    md += ["", "## Checks", ""]
    for k in CHECKS:
        v = checks.get(k)
        md.append(f"- **{k}**: " + (", ".join(x["at"] for x in v[:4]) if v else "not found"))
    md += ["", "## Environment variable names (values never read into the report)", ""]
    md += [f"- {k}" for k in env_vars] or ["- none"]
    (out / "inventory.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("\n".join(md))
    print(f"\nWrote {out / 'inventory.json'} and {out / 'inventory.md'}")


if __name__ == "__main__":
    main()
