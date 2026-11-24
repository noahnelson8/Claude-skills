# Claude Skills

Noah's personal Claude skills. Many of the ideas come from Instagram posts and reels.

## Layout

```
BACKLOG.md          # every idea, triaged: source, what it does, size, status
intake/             # raw reel material (screenshots, captions, notes) per idea
skills/<name>/      # one folder per built skill
  SKILL.md          # the skill itself (frontmatter + instructions)
  scripts/          # optional helper scripts
  examples/         # optional test inputs/outputs
templates/SKILL.md  # starting point for a new skill
.claude/skills/     # skills that operate on this repo itself (auto-load in Claude Code here)
  reel-intake/      # downloads reels -> transcript + frames + caption -> backlog
```

## Reel intake (run on your computer)

One-time setup (Windows, macOS or Linux; needs Python 3.10+ and Claude Code):
```
git clone https://github.com/noahnelson8/claude-skills
cd claude-skills
pip install -r .claude/skills/reel-intake/scripts/requirements.txt
claude
```
Then paste reel links into Claude Code: "intake these reels: <links>". It runs the script, reads every transcript and frame, writes notes, updates `BACKLOG.md` and pushes.

## Workflow

1. **Capture.** Send Claude the reel video, screenshots, the caption, or a short description.
2. **Triage.** Claude adds a row to `BACKLOG.md` and checks for overlap with existing skills.
3. **Build.** Claude drafts `skills/<name>/SKILL.md` and tests it on a real example.
4. **Install.** Claude proposes the skill as a save card in claude.ai so it's on your account. This repo keeps the versions.
