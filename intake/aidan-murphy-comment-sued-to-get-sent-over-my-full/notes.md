# 10 ways a vibe-coded app gets sued
**Source:** Aidan Murphy · https://www.instagram.com/reel/Db9Br3XBTPj/ · 2026-08-12

**What it actually shows:** A checklist with a dollar figure for each item:
- no privacy policy
- the policy doesn't say you collect data, use AI, or name the third parties you send data to
- "deleted" uploads still sitting in storage
- public storage buckets
- fake testimonials
- cancelling takes more clicks than signing up
- free trials that auto-charge without a reminder
- an AI chatbot with no self-harm response

**Named things to verify:** These are from memory, not looked up for this note; check them before relying on any of it.
- The figures loosely track real penalty schedules: California's CCPA fines are about $2.5k per violation, or $7.5k if intentional, and data-breach damages run about $100–$750 per consumer. The FTC's fake-reviews rule is about $53k per violation. California's companion-chatbot law is $1k per violation.
- "Per user" is the reel's spin; most of these are *per violation*, and they depend on where your users are.
- The FTC's click-to-cancel rule was struck down in 2025, but state auto-renewal laws still apply.

**Engagement bait?** Yes. The fix-it guide is gated.

**Verdict:** BUILD (new) `app-compliance-check`. It would audit an app's privacy policy against what the code actually collects, check storage bucket permissions and deletion, and check cancel flows, trial reminders, testimonials and chatbot safety replies. It would produce a fix list labelled "not legal advice". Useful for every Enhanced.AI app you ship.
