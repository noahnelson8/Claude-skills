---
name: meeting-notes
description: Turn any meeting or call transcript (Fathom, Wispr, Granola, Otter, Zoom/Teams .vtt/.srt, pasted text) or an audio/video recording into a short summary, decisions, action items with owners and due dates, open questions and next steps, then save it in the right vault (work calls into the Enhanced.AI marketing-vault, personal meetings into the Obsidian vault's wiki/meetings). Use when Noah pastes a transcript or drops a recording, or says "summarize this call/meeting", "meeting notes", "what did we decide", "action items from", "notes from my call with Neal/Evan/Mike", or "log this meeting".
---

# Meeting Notes

From a transcript or recording to **what was decided, who does what by when, and what's still open**, with every item traceable to a timestamp. Nothing is invented: an owner or due date that wasn't said stays `unassigned` / `no date`.

`<skill>` below means this skill's folder.

## Step 1: Get the transcript
- **A file** (transcript or recording): run
  `python -I "<skill>/scripts/prep.py" "<file>" --out "<scratch folder>/<stem>.prep"`
  Use a scratch/temp folder for `--out` unless the transcript already lives in a vault. Recordings are transcribed locally with faster-whisper (no speaker labels; ask Noah who was on the call if it matters).
- **Pasted text:** save it to a scratch `.txt` first, then run the same command, so long calls get chunked and timestamps normalised.
- Read `stats.json` (format, speakers, length) and `transcript.txt`. If there are `chunk-NN.txt` files, extract per chunk and then merge, de-duplicating decisions and actions.

## Step 2: Work out the context (decide, don't interrogate)
- **Work or personal?** Work if it involves Enhanced.AI, FLUXPROMPT, IME, MAR, Big-Box, GHL, clients/prospects, or Neal, Evan, Mike, Brad, Chad. Personal for school, Nelson Aeration, family, friends, side projects. If truly unclear, ask once.
- **Kind of meeting:** internal/planning, sales or demo call, client call, 1:1, class/lecture, interview. It decides the optional extras in Step 3.
- **Who's who:** map transcript names to real people. Machine transcripts misspell names (e.g. "Neil" for Neal): pick the right person and note the fix once.

## Step 3: Extract (only what the transcript supports)
Read the whole transcript before writing. Then produce:

1. **Summary:** 3–6 bullets of what the meeting was for and what came out of it.
2. **Decisions:** only things the group actually agreed or someone with authority settled. Each: the decision · who made it · `[mm:ss]`. Ideas that were floated but not agreed go under Open questions instead.
3. **Action items:** each one: the task (starting with a verb) · **owner** (only if someone took it or was given it; otherwise `unassigned`) · **due** (only if said; otherwise `no date`) · `[mm:ss]`. Include Noah's own items first.
4. **Open questions / parked:** unresolved points, disagreements, things to check.
5. **Numbers and commitments to verify:** prices, dates, quantities, promises to a client. Transcripts mishear numbers, so list them with the timestamp so Noah can confirm.
6. **Extras by meeting type** (only when relevant):
   - *Sales or demo call:* the prospect's goals and pain points, objections and how they were answered, buying signals, budget/timeline/decision-maker if mentioned, and the agreed next step.
   - *Client call:* requests, feedback, scope changes, deadlines.
   - *Class/lecture:* key concepts, definitions, anything flagged "on the exam", and assignments with due dates.

Quote sparingly (a few words with a timestamp) and only where the exact wording matters.

## Step 4: Deliver in chat (Noah reads the chat, not files)
Put the full result in the reply using `references/note-template.md` (Summary → Decisions → Action items table → Open questions → Verify → extras). Keep it scannable. Then offer, in one line each, only what fits:
- a follow-up email draft to the other attendees (written from the notes, for Noah to send himself; never send it),
- turning Noah's action items into tasks (personal: `/obsidian-task`; work: the noah repo's task conventions),
- updating person notes with what was learned.

## Step 5: Save it in the right place
**Work meetings** (Enhanced.AI). These belong to the work repo `C:\Users\nwnel\Projects\Enhanced.AI\noah` and its rules apply in full, so read its `CLAUDE.md` and `marketing-vault/_CLAUDE.md` first:
- Save the verbatim transcript to `marketing-vault/raw/` as `YYYY-MM-DD — <title> (<first names>) — <Fathom|Wispr|Zoom|...> transcript.md`, with the immutable raw-source frontmatter and banner used by the existing raw files (`type: raw`, `immutable: true`, `source`, `people`/`attendees`, `tags`). Never edit an existing raw file.
- Write decisions and learnings into `marketing-vault/wiki/` per `_CLAUDE.md` (decision notes link back to the raw transcript); update `index.md` and append to `log.md`.
- Commit and push from that repo **as `noahn-beep`** (its rules: check the active account first).
- If this session can't reach that repo (e.g. it's a personal session), deliver in chat, say the vault wasn't updated, and suggest running it from `claude-work`.

**Personal meetings.** Use the Obsidian vault (`C:\Qweltack's Vault`) through the `obsidian-second-brain` skill's conventions; read the vault's `_CLAUDE.md` and `references/ai-first-rules.md` first:
- Note path `wiki/meetings/YYYY-MM-DD - <kebab-slug>.md` (follow `_CLAUDE.md` if it says otherwise). If `/obsidian-meeting` already created the note, **fill in** its empty Notes, Decisions and Action items sections and never overwrite anything Noah wrote. Otherwise create it with the same frontmatter (`type: meeting`, `date`, `attendees` as `[[Person]]` links, `tags: [meeting]`, `ai-first: true`, `source: <transcript file or tool>`) and sections (`## For future Claude`, `## Context`, `## Attendees`, `## Notes`, `## Decisions`, `## Action items`, `## Source`).
- Propagate as `/obsidian-meeting` does: person notes' `## Recent Interactions`, today's daily note `## Meetings`, and one line in `log.md`.
- Keep the full transcript out of the note unless Noah wants it there: link or store it per `_CLAUDE.md`.

**Neither** (no vault wanted): save `notes.md` next to the transcript, or skip saving if Noah only wanted the chat answer.

## Step 6: Log the run
Append one line to `<skill>/runs.md`: date · meeting · source format · work/personal · counts (decisions / actions / open) · anything the parser got wrong.

## Never
- Invent decisions, owners, due dates or numbers. `unassigned`, `no date` and "unclear in the transcript" are good answers.
- Send emails or messages, create calendar events or change GHL/CRM records from a meeting without Noah's explicit go-ahead.
- Send a transcript to an outside service to process it. Transcription and parsing run locally.
- Put work meeting content in the personal vault or personal content in the work repo.
