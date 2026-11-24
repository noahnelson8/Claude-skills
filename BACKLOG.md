# Skill Backlog

Status: `idea` → `building` → `built` → `installed` · or `killed` (with reason)
Size: S (a prompt or a few steps) · M (needs scripts, connectors or a schedule) · L (multi-part or external APIs)
Verdict: **BUILD** (custom skill worth making) · **INSTALL** (someone already built it) · **TOOL** (useful software, not a skill) · **SKIP** · **NEED INFO** (send the reel/caption)

_Batch 1 triaged 2026-11-20. Batch 2 (15 reels through reel-intake, notes in `intake/<slug>/notes.md`) triaged 2026-11-24: it confirmed most of batch 1 from the actual reels and added #21–#25. Batch 3 (11 posts, 5 of them carousels) triaged 2026-11-24: it resolved #16 and added #26–#28._

## Build: custom skills worth making

| # | Skill | What it does | From reels | Size | Overlaps | Status |
|---|-------|--------------|-----------|------|----------|--------|
| 1 | `site-design-kit` | Sets an art direction from curated references (Awwwards, curated.design, Saaspo, Unsection, Details.so, Spell UI, Bencho) and a motion menu (scroll transitions, live 3D hero, spatial browsing, touchable surfaces), then builds the site and checks it in a browser. | Website references reel, website effects reel, "Motion sites" GitHub reel, [MotionSites reel (morenicksaraev)](intake/morenicksaraev-motionsites-is-a-free-open-source-s/notes.md) | M→S | Extends `frontend-design` (already installed) instead of replacing it. **`Motionsites-AI/claude-skill` already covers much of this** (16 designs, not the claimed 700+, plus 55+ technique recipes and a screenshot-and-fix loop): install it and build only the references/art-direction layer on top. **Also try [`nextlevelbuilder/ui-ux-pro-max-skill`](intake/nate-herk-comment-die-and-ill-send-it-over/notes.md)** (MIT, ~154k stars, style/color/font guidance) and **`nateherkai/scroll-craft`** (MIT, ~5.4k stars, scroll-driven sites, by the same creator as that reel). That makes three overlapping design skills, so run all three on one brief and keep the best one or two. | idea |
| 2 | `job-scout` | Every morning, Google-searches company career sites directly (Greenhouse, Lever, Ashby, Workday), scores each role against your resume and skips weak fits, then writes the top 10 to a Sheet with tailored bullets. Never submits anything. | career-ops (740 listings), Playwright new-grad reel, "8am search" reel | M | career-ops does the full version in Claude Code (see Install #6) | idea |
| 3 | `reel-intake` | Downloads a reel with yt-dlp on your computer, transcribes it with Whisper, pulls key frames, and adds a backlog row. This would solve "Claude can't watch reels". | yt-dlp + Whisper from the open-source tools list | M | none | built; first run 2026-11-24 worked (2 reels, no cookies needed). The OneDrive rename lock (WinError 5) and the false "Instagram wants a login" hint were both fixed the same day. |
| 4 | `meeting-notes` | Takes a transcript from Fathom, Granola, a phone recording or anything else and turns it into decisions, action items with owners, and a vault note. | Notetaker reel | S | none | idea |
| 21 | `app-compliance-check` | Audits an app before launch: does the privacy policy match what the code actually collects (data, AI use, third parties); are storage buckets private and are "deleted" uploads really deleted; is cancelling as easy as signing up; do trials send reminders; are testimonials real; does any chatbot have a self-harm response. Outputs a fix list marked "not legal advice". | ["10 ways your app gets sued"](intake/aidan-murphy-comment-sued-to-get-sent-over-my-full/notes.md) | M | none | idea |
| 26 | `study-coach` (optional) | Give it your course material (e.g. FINAN 4030 slides). It builds a 5-level learning ladder, runs "quiz me until I break" and Feynman explain-it-back rounds on *your* material, and tracks which concepts you missed across sessions. Resolves #16. | ["Learn anything 100x faster" carousel](intake/stics-ai-ai-tools-like-claude-are-quickly-becoming/notes.md) | S | none; only worth building if you'd use it weekly | idea |

## Install: already built, just add it

| # | Thing | Verdict for you | Status |
|---|-------|-----------------|--------|
| 5 | **skills.sh top 5** (Frontend Design, Grill Me, HyperFrames, Agent Browser, Find Skills) | **Frontend Design:** already installed. **Grill Me:** worth adding, cheap. It's the planning version of `council` (council is several viewpoints; grill-me questions one plan until it holds up). **HyperFrames:** skip, `video-making` covers it. **Agent Browser:** skip in claude.ai, Claude in Chrome covers it; only useful for headless Claude Code. **Find Skills:** worth it in Claude Code CLI only. | idea |
| 6 | **career-ops** (santifer/career-ops, MIT) | The real system behind the 740-listings reel. It's a Claude Code repo, not a claude.ai skill. Use it if you want the full pipeline (tailored CV PDFs, tracker, dashboard); build #2 if you want something lighter that runs on a schedule. | idea |
| 7 | **coreyhaines31/marketingskills** | A real, widely used marketing skill pack. Install selectively: `reverse-engineer-marketing`, `competitors`, `marketing-plan`, `copywriting`. Use it on Nelson Aeration competitors. **Verified from the [Jens Heitmann reel](intake/jens-heitmann-you-can-teach-claude-code-to-reverse/notes.md):** Agent Reach is real (`Panniantong/Agent-Reach`, ~114k stars; read/search X, Reddit, YouTube, GitHub through one CLI). Check what it installs before running it. The "marketing agent framework" is just his merge-and-rank prompt (paraphrased in the notes), not a repo. | idea |
| 8 | **msitarzewski/agency-agents** (~147k stars, MIT) | Persona files for Claude Code. Take the reel's own advice and install one or two divisions, not all 270 files. For you: Reality Checker, plus whatever Marketing/Sales you'd actually use. Mostly overlaps `council`. | idea |
| 22 | **christianjohnston-ai/honeypot** (MIT, new, 0 stars) | [Honeypot reel](intake/christian-comment-honeypot-for-the-free-claude-cod/notes.md). Sets up one decoy (fake key, doc, route or file) for your host using Canarytokens or OpenCanary, and only calls the job done once a test alert has reached you. Good for any app you deploy. It's brand new with no track record, so read SKILL.md before installing. | idea |

## Tools, not skills: useful software, nothing to build

| # | Tool | Relevance |
|---|------|-----------|
| 9 | **Twenty CRM, cal.com, Documenso, Postiz, Plausible, n8n, Inbox Zero, Papermark** (from 3 repo-list carousels in batch 3) | Papermark is new: share a PDF proposal and see who opened it and which pages they read. Potentially useful for Nelson Aeration: CRM for about 500 clients, online booking, e-signed service agreements, social scheduling, privacy-friendly site analytics, automations, email triage. All self-hosted, so they cost setup and maintenance time instead of a subscription. Only worth it if a paid tool is actually annoying you. |
| 10 | **yt-dlp, Whisper, Ollama** | Building blocks for #3 (reel-intake). Ollama runs local models; not needed otherwise. |
| 11 | **Immich, Jellyfin, Anytype, AppFlowy, tldraw, Penpot, Bitwarden, CrowdSec, Fooocus** | Personal or home-lab tools (photos, media server, notes, whiteboard, design, passwords, security, image generation). Not skills. Bitwarden is the only one worth adopting regardless. |
| 12 | **Fish Audio** | TTS and voice-cloning API. Could add voiceovers to `video-making` later; not a standalone skill. |
| 13 | **Aseprite AI** | Pixel-art tooling. Low relevance; skip unless you start a game or pixel project. |
| 23 | **Quad9 DNS, DeFlock, neko** ([OPSEC reel](intake/carter-perez-comment-opsec-and-ill-dm-you-all-the/notes.md)) | Quad9 (9.9.9.9) blocks malicious domains and is a free five-minute change worth making. DeFlock maps license-plate cameras (personal choice). neko is a self-hosted throwaway browser that needs Docker on a server. Note that changing DNS doesn't hide which sites you visit from your ISP. |

## Skip

| # | Thing | Why |
|---|-------|-----|
| 14 | **RuFlow (= Ruflo, formerly claude-flow, by ruvnet)** ([reel seen](intake/nick-sadler-someone-built-the-most-powerful-claude/notes.md); `ruvnet/ruflo` ~82k stars now) | Real project, but heavy multi-agent orchestration. The reel's "75% cost cut" is marketing, and its own skills.sh page says not to use it for tasks a single agent can finish. Overkill for solo projects. Revisit only if you're running long multi-agent builds in Claude Code. |
| 15 | **"Ripping" to get reel views** | [Reel seen](intake/ben-zogby-33-million-views-in-two-weeks/notes.md): an unnamed, gated tool that copies niche outlier videos, rewrites them and auto-posts up to 70 trial reels a week. Skip it: copyright, Instagram automation strikes and a spammy brand. The research half (find outliers, rewrite the *idea* for one specific customer) is worth folding into Enhanced.AI marketing, with a human approving each post. |
| 24 | **"One scene, ten animation styles" prompts** | [Reel](intake/ylenia-fedi-comment-style-for-the-prompts/notes.md). The style list is in the notes and the prompts are gated. `video-making` covers this; at most add the list there. |
| 25 | **10 Claude prompts for stock research** (image carousel) | [Notes](intake/day-trading-10-claude-prompts-for-stock-research/notes.md). "Act as a Goldman analyst" templates; without real data Claude invents the numbers. Only #2 (the DCF outline, run on a real 10-K) is worth keeping, as a FINAN 4030 study aid. |
| 27 | **Trading posts: 12 "hedge-fund" strategy prompts, Unusual Whales options scanner** | [Prompts](intake/stics-ai-claude-cowork-is-making-trading-research/notes.md), [scanner](intake/austin-options-alerts-setups-claude-code-is-actual/notes.md). The prompts ask Claude to "backtest" without data, so it fabricates the results. The scanner reel is an ad for a paid trading Discord with cherry-picked returns. The Unusual Whales MCP itself is real (paid data). |
| 28 | **"Secret codes" for Claude** (REDTEAM, CHAINSAW, /godmode, /devil ...) | [Reel 1](intake/felipe-vogel-ai-guy-3-secret-codes-that-make-claud/notes.md), [reel 2](intake/tech-decodeai-help-you-grow-with-chat-gpt-claude-9/notes.md). Not real features; the words only work as plain instructions. `council` already covers red-teaming. |

## Need info: send the reel or caption

| # | Idea | What's missing |
|---|------|----------------|
| 16 | ~~"Learn anything 100x faster with Claude"~~ | **Resolved 2026-11-24:** it was a 6-prompt study carousel; see Build #26. |
| 17 | ~~AI Agentic Flywheel~~ | **Resolved 2026-11-24:** Noah means **agent-flywheel.com** by Jeffrey Emanuel (`Dicklesworthstone/agentic_coding_flywheel_setup`). It's a free, open-source kit of ~39 tools for running many coding agents at once on a Linux VPS: NTM (agent cockpit in tmux), MCP Agent Mail (agents message each other), beads/bv (task queue and triage), UBS (bug scanner), DCG (a Claude Code hook that blocks destructive commands), session search and memory. The tools are free, but the site's own estimate for running it is about $440–656 a month (VPS plus several Claude Max and ChatGPT Pro accounts), and it's Ubuntu-only, not native Windows. → SKIP the full setup for now (same category as RuFlow #14). Possibly worth borrowing on its own: **DCG** as a safety hook, if it runs on Windows (unchecked). |
| 18 | ~~Hermes AI agents~~ | **Resolved 2026-11-24:** Nous Research's **Hermes Agent** (`NousResearch/hermes-agent`, MIT, ~266k stars). An always-on personal agent you chat with on Telegram, Discord, Slack, WhatsApp or email. It has persistent memory, writes its own skills (same SKILL.md format), and runs scheduled jobs. Bring your own model (OpenRouter, OpenAI, Nous Portal from $20/month), so usage costs extra beyond your Claude plan. You already have most of this (Claude Code, scheduled tasks, memory, the vault); try it only if you want to message an agent from your phone. → TOOL. |
| 19 | ~~Claude Code "Code Mode"~~ | **Resolved 2026-11-24:** "Code Mode" is Cloudflare's name for a way to use MCP: instead of feeding the model dozens of tool definitions, you give it a typed code API and it writes a short script that calls the tools. Anthropic published the same idea ("code execution with MCP"). Cloudflare's own MCP covers 2,500+ API endpoints in about 1,000 tokens. Not a skill to install; it's a design pattern. It's most relevant to the **SPINE MCP platform, which is work (noahn-beep repo)**, if SPINE exposes many tools. → Idea for the work repo, not this one. |
| 20 | Building your own / physical AI notetaker | As a product, this is an app idea for the startup search, not a skill. The skill version is #4. |

## Notes per idea

<!-- One section per idea: what the reel showed, open questions, decisions. -->
