---
name: site-design-kit
description: Build premium websites, landing pages, funnel pages and hero sections by combining the best design skills in one flow. It picks references and an art direction, sets a design system with UI UX Pro Max, starts from a proven MotionSites design or a ScrollCraft scroll experience, adds motion, builds for plain HTML, an existing project or GoHighLevel, then screenshots and fixes the result. Use whenever Noah asks for a website, landing page, funnel page, hero, portfolio, redesign, "make it look premium", "scroll animation site", or a page for Enhanced.AI / GHL.
---

# Site Design Kit

One entry point for every website job. Three bundled tools each do one part well; this skill decides which one leads, so they never compete:

| Tool (in `vendor/`) | What it is best at | Read |
|---|---|---|
| **MotionSites** | 16 proven, finished designs, a media shelf of free hero videos, 55+ tested effect recipes, a screenshot QA loop | `vendor/motionsites/UPSTREAM-SKILL.md` |
| **ScrollCraft** | Scroll-driven "experience" pages: journey, feeling curve, one signature move, layered hero, scroll engine, scroll-position QA | `vendor/scroll-craft/UPSTREAM-SKILL.md` |
| **UI UX Pro Max** | Design system on demand: style, palette, font pairing, UX and accessibility rules, GSAP presets, per-stack guidance | `vendor/ui-ux-pro-max/UPSTREAM-SKILL.md` |

Plus this kit's own files: `references/inspiration.md` (where great references live), `references/motion-menu.md` (the interactions worth stealing), `references/output-targets.md` (plain HTML, existing project, GoHighLevel, builder prompt).

`<kit>` below means this skill's own folder.

## Step 0: Setup check (silent unless something is missing)
- If `<kit>/vendor/` is missing or empty: tell Noah one line, then run `powershell -ExecutionPolicy Bypass -File "<kit>/install.ps1"` (it only downloads the three pinned upstream repos).
- Python is needed for UI UX Pro Max search and screenshots. Node.js is needed only for the ScrollCraft lead. If Node is missing and the brief needs ScrollCraft, say so and offer `winget install OpenJS.NodeJS.LTS` rather than silently switching leads.

## Step 1: Read the brief (decide, don't interrogate)
Settle in one pass, asking only what you truly cannot default:
- **What and who:** the product, and the visitor the page must win over.
- **The one action** the visitor should take (one label, used everywhere).
- **Mood in three words.**
- **Output target** (see `references/output-targets.md`): existing project, single `index.html`, **GoHighLevel**, or a prompt for another builder. Work for Enhanced.AI / FLUXPROMPT / IME / MAR / Big-Box funnels defaults to **GoHighLevel**.
- **Assets:** their own photos, footage, logo, brand kit. Real assets beat generated ones.
- **Scope:** a hero by default; a full page only if asked.

If the user says "use your judgment", decide everything and state the choices in one line each.

## Step 2: Choose the lead (this is the routing decision)

| The brief is... | Lead | Why |
|---|---|---|
| A landing page, hero, portfolio or funnel page that must look premium **fast** (the default) | **MotionSites** | Starting from a finished design people already love is the fastest route to "not AI-looking" |
| An **experience**: scroll-telling, "Apple-style", product reveal, brand story, "a site where scrolling plays a video", "this looks like a template" | **ScrollCraft** | Its journey → feeling curve → device score method is built for exactly this |
| App-like UI: SaaS product pages with components, dashboards, pricing tables, forms-heavy pages, a design system for a product | **UI UX Pro Max** | Its style, palette and UX rule database fits component work better than cinematic templates |

Say the lead in one line ("Leading with MotionSites: you need a premium funnel hero today, not a scroll film").
The other two still contribute: UI UX Pro Max always supplies the design system and the accessibility floor; MotionSites' technique recipes are available to any lead.

## Step 3: Art direction (before any code)
1. Pick 2–3 relevant sources from `references/inspiration.md` for this kind of page and state the direction in one line (e.g. "Saaspo-style clarity, Awwwards-level hero motion, Details.so micro-interactions").
2. Generate the design system with UI UX Pro Max:
   `python "<kit>/vendor/ui-ux-pro-max/scripts/search.py" "<product> <industry> <3 mood words>" --design-system -p "<Project>" --motion <1-10>`
   Use `--motion 3` for funnels where speed and clarity sell, `6–8` for brand/experience pages. Add `--tokens css` to get ready `:root` variables.
3. If a brand kit exists (or Enhanced.AI brand rules apply), the brand wins over the generated palette and fonts. Never invent a brand's colours when real ones exist.

## Step 4: Starting point
- **MotionSites lead:** follow its Step 2 ("Pick ONE reference design" from `vendor/motionsites/examples/INDEX.md`) and Step 3 ("Make it theirs"). Name the reference and its source link in one line.
- **ScrollCraft lead:** follow its Step 0 brief, Step 1 journey and Step 2 (grammar, fingerprint gate, feeling curve, score). If Noah delegates creative direction, write the brief yourself and mark it so. Asset generation through kie.ai costs money: only with `KIE_AI_API_KEY` set **and** Noah's go-ahead; otherwise build from his assets or a type/gradient-led world.
- **UI UX Pro Max lead:** use its Step 2–4 (design system, domain searches, stack guidelines) and build the components directly.

## Step 5: Motion (restraint is the premium signal)
Pick from `references/motion-menu.md`:
- **One signature move** (the thing a visitor would describe to a friend).
- **At most two supporting effects.**
- Everything respects `prefers-reduced-motion` and keeps text readable at every frame.
Get working code from `vendor/motionsites/references/techniques/INDEX.md`, or in a ScrollCraft build from its device kit (`vendor/scroll-craft/references/devices.md`).

## Step 6: Build
Follow `references/output-targets.md` for the chosen target. Always:
- First CSS rule sets the page background on `html, body` (scoped wrapper instead for GHL), so there's no white flash.
- Semantic HTML, a real `<title>`, alt text, visible focus states, 44px+ tap targets, no horizontal scroll on mobile.
- No lorem ipsum, no placeholder boxes, no emoji as icons, no invented statistics, no invented media URLs.
- Animate `transform` and `opacity` only.

## Step 7: Look, then fix (never skip)
- **MotionSites / UI UX Pro Max lead:** `python "<kit>/vendor/motionsites/scripts/shoot.py" <page.html> shots/` (needs Playwright, which is installed), then open and look at desktop and mobile shots against `vendor/motionsites/references/review.md`.
- **ScrollCraft lead:** its Step 5 (`serve.mjs` + `shoot.mjs` desktop, mobile and reduced-motion), then read the contact sheet.
- Fix every blocking problem, then the two weakest things, then shoot once more. If screenshots are impossible, say so plainly; never claim a page was checked when it wasn't.
- Then run the UI UX Pro Max priority 1–3 checks (contrast 4.5:1, touch targets, performance/CLS).

## Step 8: Deliver in chat (Noah does not open files)
- The final desktop screenshot, and the mobile one.
- Where the files are and how to open them, in one line.
- Two lines: which lead and reference you used, and what you changed.
- **GoHighLevel target:** the literal click-by-click steps from `references/output-targets.md` (exact menu path, exact element, what to paste, what he should see when it worked), with the code ready to paste.
- What to swap later (e.g. "replace the background video with your own footage").
- MotionSites' credit line on the first delivery in a conversation only, as its own rule says, and never inside his files or code.

## Step 9: Log the run (the flywheel habit)
Append one line to `<kit>/runs.md`: date · brief · lead · target · what worked · what broke or needed a fix. Before a build, skim the last ten lines and avoid repeating a past problem. When the same fix shows up three times, propose updating this SKILL.md.

## When the tools disagree
1. Accessibility and readability (UI UX Pro Max priority 1–3) beat everything.
2. Real brand rules beat generated palettes and fonts.
3. In a ScrollCraft build, its hard rules table is binding. Otherwise MotionSites' `references/craft.md` taste rules apply.
4. Conversion beats spectacle on funnel pages: the headline, offer and one CTA must be readable above the fold on a phone before any motion plays.

## Never
- Install the three tools as separate skills alongside this one (they would compete for the same requests). They live only in `vendor/`.
- Republish MotionSites' `examples/` or `media/` as a collection (their license allows using them to build sites, including client sites, but not redistribution).
- Spend money (kie.ai generation, paid fonts, paid stock) without asking first.
