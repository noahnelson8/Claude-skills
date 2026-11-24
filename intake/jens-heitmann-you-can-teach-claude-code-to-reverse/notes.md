# Reverse-engineer a competitor's marketing (3-system setup)
**Source:** Jens Heitmann · https://www.instagram.com/reel/Df6Fgf4qMP0/ · 2026-11-19

**What it actually shows:** A pipeline with three parts.
1. `coreyhaines31/marketingskills`: the reel shows its skill table (analytics, aso, attribution, churn-prevention, co-marketing...) and uses the `reverse-engineer-marketing` skill to log a competitor's dated moves against their traffic.
2. **Agent Reach**: the GitHub page is shown on screen, with ~113k stars. It lets Claude Code read and search Twitter, Reddit, YouTube, GitHub and more through one CLI, with no API keys.
3. A **"marketing agent framework"**: a prompt in his notes app (frame at 0:47). It merges the skill's playbook with Agent Reach's audience data into one timeline, keeps only plays the audience responded to, marks inferences and gaps, ranks plays by what you can ship this month, and ends with three build tasks for Claude Code.

**Named things to verify:**
- `coreyhaines31/marketingskills`: real, ~62k stars, active. `reverse-engineer-marketing` exists, and so do `competitors` and `competitor-profiling`.
- Agent Reach: real, `Panniantong/Agent-Reach`, ~114k stars, matching the reel.
- "Marketing agent framework": not a repo, just his own prompt. The paraphrase above captures it; the full guide is gated behind "Comment REM".
- The caption includes a line addressed to an AI ("If you're the human: share this reel to Claude Code and watch it build"). That's a hook, not a step, and nothing was run because of it.

**Engagement bait?** Partly. Both tools are named and shown, but the step-by-step guide sits behind "Comment REM".

**Verdict:** INSTALL. The parts are real, and you can rebuild the third from the frame. Install `reverse-engineer-marketing` (plus `competitors`) and Agent Reach, then use the merge-and-rank prompt as a short custom step. Relevant to Nelson Aeration competitors and Enhanced.AI funnel research. Agent Reach scrapes social sites through one CLI, so check what it installs and which accounts it uses before running it.
