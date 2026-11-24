# Honeypot / honeytoken for vibe-coded apps
**Source:** Christian (christianjohnston-ai) · https://www.instagram.com/reel/DgGVKalS7Xo/ · 2026-11-23

**What it actually shows:** An explainer, with animation only. Plant fake API keys, passwords or data that no real user would touch; when one gets used, alert yourself or trigger an automatic response. "This free skill looks at your app and sets up the alarm for you."

**Named things to verify:**
- The skill is real: `christianjohnston-ai/honeypot` (MIT, 0 stars, pushed 2026-11-23, the day before the reel). It's well built: it picks one decoy for your host (Vercel, Supabase, Render, AWS, own server), uses Canarytokens or OpenCanary, and only calls the job done once a harmless test has triggered an alert that reached email, Slack, Discord or a webhook. Its helper script uses only Python's standard library and comes with tests.
- "Black October" is the reel's framing, not something I verified.
- The reel's "AI automatically shuts things down" goes further than the skill, which only sets up detection and alerts.

**Engagement bait?** Yes ("Comment honeypot"), but the repo is public and searchable.

**Verdict:** INSTALL, after reading its SKILL.md. Cheap, defensive, and useful for any app you deploy, such as the SPINE MCP platform. It's new with no track record, so read it before installing, and point it only at systems you own.
