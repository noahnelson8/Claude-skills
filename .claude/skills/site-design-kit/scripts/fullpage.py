"""Full-page screenshots after scrolling through (so scroll reveals have fired). Usage: python fullpage.py <html> <outdir>"""
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

page_path = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for name, vw, vh, mobile in (("full-desktop", 1440, 900, False), ("full-mobile", 390, 844, True)):
        ctx = b.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
        pg = ctx.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.goto(page_path.as_uri(), wait_until="networkidle")
        time.sleep(2.5)
        h = pg.evaluate("document.documentElement.scrollHeight")
        for y in range(0, h, vh // 2):
            pg.evaluate(f"window.scrollTo(0,{y})"); time.sleep(0.25)
        time.sleep(1.2)
        pg.evaluate("window.scrollTo(0,0)"); time.sleep(0.6)
        overflow = pg.evaluate("document.documentElement.scrollWidth > window.innerWidth")
        pg.screenshot(path=str(out / f"{name}.png"), full_page=True)
        print(name, "height", h, "overflow", overflow, "console errors", errs)
        ctx.close()
    b.close()
