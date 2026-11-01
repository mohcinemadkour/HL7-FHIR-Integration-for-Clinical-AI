"""Build a PowerPoint file for every deck in the repo.

Each deck-source/ folder (deck.json + slides/*.html) becomes a .pptx next to it:
one full-slide image per slide, with the slide's speaker notes as PowerPoint notes.

Usage:  python tools/build_pptx.py
Needs:  python-pptx, playwright (Chromium)
"""
import json, re, html, base64, pathlib, tempfile
from playwright.sync_api import sync_playwright
from pptx import Presentation
from pptx.util import Emu

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"
PHOTO = ROOT / "assets" / "instructor.png"

def font_face(family, file, weight):
    data = base64.b64encode((FONTS / file).read_bytes()).decode()
    return f"@font-face{{font-family:'{family}';font-weight:{weight};src:url(data:font/woff2;base64,{data}) format('woff2');}}"

CSS = "".join([
    *(font_face("IBM Plex Sans", f"ibm-plex-sans-latin-{w}-normal.woff2", w) for w in (400, 500, 600, 700)),
    *(font_face("JetBrains Mono", f"jetbrains-mono-latin-{w}-normal.woff2", w) for w in (400, 600)),
    "*{margin:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden}",
    "section{position:relative;width:1920px;height:1080px;overflow:hidden}aside{display:none}",
])
PHOTO_URI = "data:image/png;base64," + base64.b64encode(PHOTO.read_bytes()).decode()

def build(src: pathlib.Path, page):
    deck = json.loads((src / "deck.json").read_text())
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)  # 16:9
    blank = prs.slide_layouts[6]
    with tempfile.TemporaryDirectory() as tmp:
        for i, sid in enumerate(deck["order"], 1):
            sec = (src / "slides" / f"{sid}.html").read_text()
            notes_m = re.search(r"<aside>(.*?)</aside>", sec, re.S)
            notes = html.unescape(notes_m.group(1).strip()) if notes_m else ""
            body = re.sub(r'src="/_blob/[^"]+"', f'src="{PHOTO_URI}"', sec)
            page.set_content(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
            page.evaluate("document.fonts.ready")
            png = pathlib.Path(tmp) / f"{i:02d}.png"
            page.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": 1920, "height": 1080})
            slide = prs.slides.add_slide(blank)
            slide.shapes.add_picture(str(png), 0, 0, prs.slide_width, prs.slide_height)
            slide.notes_slide.notes_text_frame.text = notes
    out = src.parent / (re.sub(r"[^A-Za-z0-9-]+", "-", deck["title"]).strip("-") + ".pptx")
    for old in src.parent.glob("*.pptx"):
        old.unlink()
    prs.save(out)
    return out, len(deck["order"])

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        for src in sorted(ROOT.rglob("deck-source")):
            out, n = build(src, page)
            print(f"{out.relative_to(ROOT)}  ({n} slides)")
        browser.close()
