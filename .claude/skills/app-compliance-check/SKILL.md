---
name: app-compliance-check
description: Pre-launch legal-risk audit for an app, website or funnel. Scans the code and/or the live site for what data it really collects and where it sends it (analytics, AI providers, payments, CRM/SMS), then checks the privacy policy matches, storage isn't public, deletes really delete, cancel is as easy as signup, trials remind before charging, testimonials are real, AI chatbots handle self-harm, SMS/email consent and accessibility. Produces a ranked fix list with evidence, fixes the code issues on request and drafts policy wording for review. Use when Noah says "is this safe to launch", "compliance check", "will this get us sued", "check the privacy policy", "audit my app/funnel", before launching any app, SaaS, funnel or chatbot, or for Enhanced.AI / FLUXPROMPT / GHL funnels.
---

# App Compliance Check

The reel version is "10 ways your vibe-coded app gets sued". This skill turns that into a repeatable audit: **find what the app actually does, compare it with what it promises, and rank the gaps**.

**It is not legal advice and never says "you're compliant".** It finds evidence of risk, explains it in plain words, and fixes what code can fix. Anything that needs a judgment call (which laws apply, final policy wording) goes on a short "ask a lawyer" list. Say this once in the report, not on every line.

`<skill>` below means this skill's folder.

## Step 1: Scope (decide, don't interrogate)
Settle from context; ask only what you can't infer:
- **Target:** a code folder, a live URL, or both. Both is best: code shows what's collected, the live site shows what users are told.
- **What it is:** SaaS app, marketing site, GHL funnel, chatbot, mobile app.
- **Who uses it and where:** consumers or businesses; US-only or EU/UK too; could minors use it. Default when unknown: US consumers, adults, California residents included (California's laws are the strictest common case).
- **Money:** free, one-time payment, subscription, free trial.
- **Messaging:** does it send marketing email or SMS (GHL funnels almost always do).

## Step 2: Inventory, from the code
Run the scanner (Python standard library only, read-only, never prints secret values):

```
python -I "<skill>/scripts/scan.py" "<project folder>" --out "<project folder>/compliance"
```

It writes `inventory.json` and `inventory.md`: third-party services by category (analytics, ads pixels, AI providers, payments, backend/storage, email/SMS/CRM, auth, error/session replay), personal-data form fields, cookies, storage-public flags, delete handlers, subscription/trial code, cancel flows, chatbot and crisis-language presence, policy pages, testimonials, SMS/email consent text, and basic accessibility counts.

**The scanner is a heuristic.** Open the files it points to and confirm each finding before reporting it. Drop false positives; note anything it missed.

## Step 3: Inventory, from the live site (if there is a URL)
Use a browser tool or page fetch:
- Footer: are **Privacy Policy** and **Terms** linked from every page, including funnel steps and checkout?
- Read the privacy policy in full. List exactly which data, purposes, third parties and AI use it discloses, plus its "last updated" date.
- Forms: what fields are collected; is there SMS/email consent text next to the phone/email field; is the consent box pre-checked?
- Cookie banner (if EU/UK users or ad pixels): does "Reject" work as easily as "Accept"?
- Network requests on load: which third-party domains are contacted before any consent?
- Testimonials/reviews shown, and whether they say who and whether results are typical.
- Checkout / signup: trial terms, price and renewal shown before the buy button; how many clicks to cancel compared with how many to sign up.

## Step 4: Run the checklist
Work through `references/checklist.md` (one section per risk, each with how to detect it in code and live, what "good" looks like, and the fix). Use `references/laws.md` only to explain *why* something matters. Its figures are maximums and change; it carries a "last checked" date, so re-verify anything you quote if that date is more than six months old.

Rate every finding:
- **Blocking:** real users or money exposed now (public bucket with user files, no privacy policy at all, a chatbot with no crisis handling, auto-renewing trial with no disclosure, fabricated testimonials, SMS without consent).
- **Fix soon:** a mismatch or missing piece that's a clear risk (policy omits AI or a third party, deletes leave files behind, cancel is harder than signup).
- **Good to have:** hygiene (accessibility basics, cookie banner polish, policy date).
- **OK:** checked and fine. List these too, in one line each, so the report shows what was covered.

Every finding needs **evidence**: `file:line`, or the URL plus what's on screen.

## Step 5: Report, in chat (Noah does not open files)
Put the full report in the chat reply, in this order:
1. **One-line verdict:** e.g. "2 blocking, 4 fix-soon, 3 good-to-have. Don't launch until the 2 blocking are fixed."
2. **Blocking** and **Fix soon** as a table: issue · evidence · why it matters (one plain sentence) · fix · who fixes it (me now / Noah in GHL / lawyer).
3. **Good to have** as short bullets.
4. **Checked and OK:** one line.
5. **Ask a lawyer:** at most 3 specific questions (not "is this legal?").
6. The "not legal advice" line, once.

Also save it as `compliance/REPORT.md` next to the inventory, as the durable record.

## Step 6: Fix (only what Noah approves)
Offer to fix the code-fixable items straight away: make buckets private and use signed URLs, delete storage objects when a record is deleted, add a cancel button that works in one step, add trial reminder emails, add a crisis-response layer to the chatbot (`references/checklist.md` §9 has the pattern), add consent text, add alt text and labels.
For **policy text**: draft the missing sections in plain language, marked `DRAFT: have a lawyer review`, built only from facts the inventory proved. Never invent practices the app doesn't have.
For **GHL funnels**: give literal click steps (exact menu path, field, text to paste, what he'll see when it worked).

After fixing, re-run the scanner and show the before/after counts.

## Step 7: Log the run
Append one line to `<skill>/runs.md`: date · target · counts by rating · top issue · scanner false positives or misses. When the same false positive shows up twice, fix the scanner's pattern.

## Never
- Declare an app "compliant", "legal" or "safe from lawsuits".
- Quote a penalty as what *they* would owe. Penalties are maximums and depend on facts and jurisdiction.
- Read or print secret values (keys, tokens, passwords, `.env` contents). The scanner reports variable *names* only.
- Send private code, customer data or policy text to outside services to "check" it.
- Write fake compliance artefacts (fake consent logs, backdated policies).
