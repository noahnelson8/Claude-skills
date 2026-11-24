# Output targets

## 1. Existing project
If the folder has `package.json`, a framework or a components folder, build **inside it** in its stack and conventions. Get stack rules from UI UX Pro Max: `search.py "<concern>" --stack <react|nextjs|astro|html-tailwind|...>`.

## 2. Standalone page (default outside a project)
One self-contained `index.html`: inline CSS and JS, CDN libraries pinned to an exact version, opens by double-clicking. Media from the user's own files, MotionSites' media shelf (exact URLs from `MEDIA.md`), or none.

## 3. GoHighLevel funnel / website page (default for Enhanced.AI work)
GHL page builders inject their own CSS and JS into the page, so the code must live in a **scoped block** that can't break or be broken by the builder.

**Code rules**
- Wrap everything in one root element with a unique class, e.g. `<div class="sdk-ime-hero">`. Prefix **every** CSS selector with it. No rules on `html`, `body`, `*`, or bare tags.
- One block of HTML + `<style>` + `<script>`, ready to paste into a single **Custom JS/HTML (code) element**. Fonts via `<link>` at the top of that block.
- JavaScript runs after load, queries only inside the root element, and fails safe (if it errors, the static page still reads correctly).
- **Lead capture stays native.** Use GHL's own Form or Survey element (placed directly below the custom block), or a GHL form embed, so leads land in the CRM and workflows fire. Never build a custom `<form>` that posts elsewhere.
- Media: upload images and videos to GHL **Media Library** and use those URLs, or use MotionSites' shelf URLs. Keep the hero video under ~5 MB and add a poster image.
- Keep tracking intact: don't remove or override GHL's head/body tracking code.

**Delivery: literal click steps (Noah follows these exactly)**
Write them for the specific page, in this shape:
1. GHL → **Sites** → **Funnels** (or **Websites**) → open *<funnel name>* → the *<step name>* step → **Edit**.
2. Add a full-width **Section** → in it a one-column **Row** → in that, click **+ Add Element** → choose **Custom JS/HTML** (it may be named **Code**).
3. Click the element → **Open Code Editor** → paste the block below → **Save**.
4. Below it, add the native **Form** element and pick *<form name>*.
5. Top bar: **Preview**, then switch to the **phone** view. You should see *<what the hero looks like>*. If you see raw code or a blank box, tell me what's on screen.
6. **Save** → **Publish**.

GHL's menu names change between versions. If a label doesn't match, the user should say what he sees and you adapt the step; then record the correct path in the work vault (`marketing-vault`, via the noah repo rules) so the next build is right the first time.

**First real GHL build:** treat it as a test of these rules. Note what worked in `<kit>/runs.md` and fix this file if anything here was wrong.

## 4. Prompt for another builder (Lovable, Bolt, v0, Cursor ...)
Use MotionSites' `references/spec-template.md` and `references/builders.md`, plus the design system tokens from UI UX Pro Max.
