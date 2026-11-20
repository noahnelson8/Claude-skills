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
```

## Workflow

1. **Capture.** Send Claude the reel video, screenshots, the caption, or a short description.
2. **Triage.** Claude adds a row to `BACKLOG.md` and checks for overlap with existing skills.
3. **Build.** Claude drafts `skills/<name>/SKILL.md` and tests it on a real example.
4. **Install.** Claude proposes the skill as a save card in claude.ai so it's on your account. This repo keeps the versions.
