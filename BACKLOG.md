# Skill Backlog

Status: `idea` → `building` → `built` → `installed` · or `killed` (with reason)
Size: S (a prompt or a few steps) · M (needs scripts, connectors or a schedule) · L (multi-part or external APIs)
Verdict: **BUILD** (custom skill worth making) · **INSTALL** (someone already built it) · **TOOL** (useful software, not a skill) · **SKIP** · **NEED INFO** (send the reel/caption)

_Batch 1 triaged 2026-11-20._

## Build: custom skills worth making

| # | Skill | What it does | From reels | Size | Overlaps | Status |
|---|-------|--------------|-----------|------|----------|--------|
| 1 | `site-design-kit` | Sets an art direction from curated references (Awwwards, curated.design, Saaspo, Unsection, Details.so, Spell UI, Bencho) and a motion menu (scroll transitions, live 3D hero, spatial browsing, touchable surfaces), then builds the site and checks it in a browser. | Website references reel, website effects reel, "Motion sites" GitHub reel, [MotionSites reel (morenicksaraev)](intake/morenicksaraev-motionsites-is-a-free-open-source-s/notes.md) | M→S | Extends `frontend-design` (already installed) instead of replacing it. **`Motionsites-AI/claude-skill` already covers much of this** (16 designs, not the claimed 700+, plus 55+ technique recipes and a screenshot-and-fix loop): install it and build only the references/art-direction layer on top. | idea |
| 2 | `job-scout` | Every morning, Google-searches company career sites directly (Greenhouse, Lever, Ashby, Workday), scores each role against your resume and skips weak fits, then writes the top 10 to a Sheet with tailored bullets. Never submits anything. | career-ops (740 listings), Playwright new-grad reel, "8am search" reel | M | career-ops does the full version in Claude Code (see Install #6) | idea |
| 3 | `reel-intake` | Downloads a reel with yt-dlp on your computer, transcribes it with Whisper, pulls key frames, and adds a backlog row. This would solve "Claude can't watch reels". | yt-dlp + Whisper from the open-source tools list | M | none | built; first run 2026-11-24 worked (2 reels, no cookies needed). The OneDrive rename lock (WinError 5) and the false "Instagram wants a login" hint were both fixed the same day. |
| 4 | `meeting-notes` | Takes a transcript from Fathom, Granola, a phone recording or anything else and turns it into decisions, action items with owners, and a vault note. | Notetaker reel | S | none | idea |

## Install: already built, just add it

| # | Thing | Verdict for you | Status |
|---|-------|-----------------|--------|
| 5 | **skills.sh top 5** (Frontend Design, Grill Me, HyperFrames, Agent Browser, Find Skills) | **Frontend Design:** already installed. **Grill Me:** worth adding, cheap. It's the planning version of `council` (council is several viewpoints; grill-me questions one plan until it holds up). **HyperFrames:** skip, `video-making` covers it. **Agent Browser:** skip in claude.ai, Claude in Chrome covers it; only useful for headless Claude Code. **Find Skills:** worth it in Claude Code CLI only. | idea |
| 6 | **career-ops** (santifer/career-ops, MIT) | The real system behind the 740-listings reel. It's a Claude Code repo, not a claude.ai skill. Use it if you want the full pipeline (tailored CV PDFs, tracker, dashboard); build #2 if you want something lighter that runs on a schedule. | idea |
| 7 | **coreyhaines31/marketingskills** | A real, widely used marketing skill pack. Install selectively: `reverse-engineer-marketing`, `competitors`, `marketing-plan`, `copywriting`. Use it on Nelson Aeration competitors. **Verified from the [Jens Heitmann reel](intake/jens-heitmann-you-can-teach-claude-code-to-reverse/notes.md):** Agent Reach is real (`Panniantong/Agent-Reach`, ~114k stars; read/search X, Reddit, YouTube, GitHub through one CLI). Check what it installs before running it. The "marketing agent framework" is just his merge-and-rank prompt (paraphrased in the notes), not a repo. | idea |
| 8 | **msitarzewski/agency-agents** (~147k stars, MIT) | Persona files for Claude Code. Take the reel's own advice and install one or two divisions, not all 270 files. For you: Reality Checker, plus whatever Marketing/Sales you'd actually use. Mostly overlaps `council`. | idea |

## Tools, not skills: useful software, nothing to build

| # | Tool | Relevance |
|---|------|-----------|
| 9 | **Twenty CRM, cal.com, Documenso, Postiz, Plausible, n8n, Inbox Zero** | Potentially useful for Nelson Aeration: CRM for about 500 clients, online booking, e-signed service agreements, social scheduling, privacy-friendly site analytics, automations, email triage. All self-hosted, so they cost setup and maintenance time instead of a subscription. Only worth it if a paid tool is actually annoying you. |
| 10 | **yt-dlp, Whisper, Ollama** | Building blocks for #3 (reel-intake). Ollama runs local models; not needed otherwise. |
| 11 | **Immich, Jellyfin, Anytype, AppFlowy, tldraw, Penpot, Bitwarden, CrowdSec, Fooocus** | Personal or home-lab tools (photos, media server, notes, whiteboard, design, passwords, security, image generation). Not skills. Bitwarden is the only one worth adopting regardless. |
| 12 | **Fish Audio** | TTS and voice-cloning API. Could add voiceovers to `video-making` later; not a standalone skill. |
| 13 | **Aseprite AI** | Pixel-art tooling. Low relevance; skip unless you start a game or pixel project. |

## Skip

| # | Thing | Why |
|---|-------|-----|
| 14 | **RuFlow (= Ruflo, formerly claude-flow, by ruvnet)** | Real project, but heavy multi-agent orchestration. The reel's "75% cost cut" is marketing, and its own skills.sh page says not to use it for tasks a single agent can finish. Overkill for solo projects. Revisit only if you're running long multi-agent builds in Claude Code. |
| 15 | **"Ripping" to get reel views** | If this means reposting other creators' clips, it's a copyright and account-strike risk. If it means something else, send the reel. |

## Need info: send the reel or caption

| # | Idea | What's missing |
|---|------|----------------|
| 16 | "Learn anything 100x faster with Claude" | The link can't be opened from here. Paste the caption or describe the method. Likely a study/tutor skill for FINAN 4030. |
| 17 | AI Agentic Flywheel concept | What the loop actually was. |
| 18 | Hermes AI agents | Which Hermes (Nous Research's Hermes Agent, or something else)? |
| 19 | Claude Code "Code Mode" | What it did; possibly MCP "code mode" (the agent calls tools by writing code). |
| 20 | Building your own / physical AI notetaker | As a product, this is an app idea for the startup search, not a skill. The skill version is #4. |

## Notes per idea

<!-- One section per idea: what the reel showed, open questions, decisions. -->
