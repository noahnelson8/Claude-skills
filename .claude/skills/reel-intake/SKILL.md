---
name: reel-intake
description: Download Instagram reels/posts (or TikTok, YouTube Shorts, local videos) and turn them into a transcript, key frames and caption that Claude can actually read, then log each idea in BACKLOG.md. Use when Noah pastes reel links, says "intake these reels", "process my reels", "look at this reel", or drops video files into intake/.
---

# Reel Intake

Claude can't watch a reel from a link. This skill converts each reel into things Claude can read: a **timestamped transcript** of the speech, **frames** sampled every few seconds (on-screen text, code, UI, repo names), a **contact sheet** grid of those frames, and the **caption**. Claude then writes up what the reel actually shows and adds it to the backlog.

Runs on Noah's computer, in Claude Code opened at the root of the `claude-skills` repo. The cloud workspace can't reach Instagram.

## Steps

1. **Collect inputs.** URLs (`instagram.com/reel/...`, `/p/...`, TikTok, YouTube) and/or local video paths. For more than 3, write them to `intake/queue.txt`, one per line.

2. **First run only:** install dependencies:
   ```
   pip install -r .claude/skills/reel-intake/scripts/requirements.txt
   ```
   The first transcription downloads the Whisper `small` model (~250 MB, one time).

3. **Run the script** from the repo root:
   ```
   python .claude/skills/reel-intake/scripts/intake.py --file intake/queue.txt
   ```
   or `python .claude/skills/reel-intake/scripts/intake.py URL1 URL2 ...`
   - If a download fails with a login, rate-limit or "private" error, retry those URLs with `--cookies-from-browser firefox`. Chrome and Edge on Windows usually block cookie reading. If no Firefox, ask Noah to export a `cookies.txt` with the "Get cookies.txt LOCALLY" extension while logged into Instagram, then use `--cookies cookies.txt`. Never commit cookies.txt.
   - Long or talk-heavy reels with a bad transcript: re-run that one with `--model medium`.
   - Check `intake/last-run.json` for per-item results.

4. **Read each new folder** `intake/<slug>/`:
   - `sheet.jpg` first (one image, the whole reel at a glance).
   - `transcript.txt` and `caption.txt`.
   - Open individual `frames/NN_tMMmSSs.jpg` only where on-screen text matters (repo names, commands, prompts, settings). Frame filenames carry timestamps, so they line up with the transcript.

5. **Write `intake/<slug>/notes.md`** for each reel:
   ```
   # <Idea name>
   **Source:** <creator> · <url> · <posted date>
   **What it actually shows:** 2–4 sentences, concrete: tools, repos, commands, prompts.
   **Named things to verify:** repos, products, numbers the reel claims.
   **Engagement bait?** e.g. "Comment X for the link", meaning the real steps aren't in the reel.
   **Verdict:** BUILD | INSTALL | TOOL | SKIP | NEED INFO, with one line why.
   ```
   Verify named repos and products with a quick web search before giving a verdict. Reels exaggerate star counts and savings.

6. **Update `BACKLOG.md`.** Add or update a row in the matching section (Build / Install / Tools / Skip / Need info). If the reel matches an existing row (same repo or idea), update that row and add the new source instead of duplicating it. Check overlap with Noah's installed skills (frontend-design, council, video-making, skill-creator, obsidian vault skills, etc.).

7. **Commit and push:**
   ```
   git add intake BACKLOG.md && git commit -m "Intake: <n> reels" && git push
   ```
   Videos are gitignored; frames, sheets, transcripts and notes are committed, so Claude in claude.ai can read them from the repo later.

8. **Report back** in a short list: one line per reel (idea → verdict), then which ones look worth building.

## Gotchas
- Image posts and carousels have no video. The script still saves the caption and the first image; read `image.*`.
- Reels with only music have nothing to transcribe. The transcript says so; rely on frames and caption.
- Instagram rate-limits bulk downloads. For 20+ reels, use cookies and expect a few retries.
- Don't download or repost creators' videos anywhere else. They're kept only long enough to extract notes, then deleted (`--keep-video` overrides).
