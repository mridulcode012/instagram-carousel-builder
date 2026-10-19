#!/usr/bin/env python3
"""Export a rendered carousel as a PDF, one 1080x1350 slide per page.

Usage:
    python3 export_pdf.py carousels/<slug> [--out path/to/file.pdf] [--vector]

Default (image mode): each page is the rendered slide PNG from slides/. It looks identical in every
viewer (WhatsApp, phone previews, Slack, LinkedIn), because there is nothing left for the viewer to
draw. Use this for anything you share.

--vector: prints slides.html directly, so text stays selectable and sharp at any zoom. Simpler PDF
viewers mis-draw CSS gradients, soft shadows and transparency (flat backgrounds, grey boxes), so
only use it for desktop review in Chrome, Preview or Acrobat.

Run render.py first.
"""
import argparse
import base64
import glob
import html
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome  # noqa: E402  (same folder: Browser, find_chrome, file_url)
import common  # noqa: E402  (W, H)

PAGE_CSS = ("@page{size:%dpx %dpx;margin:0}"
            "html,body{margin:0;padding:0;background:none!important}") % (common.W, common.H)
PRINT_CSS = PAGE_CSS + (".slide{break-after:page;page-break-after:always}"
                        ".slide:last-child{break-after:auto;page-break-after:auto}")


def image_page_html(pngs):
    imgs = "".join(f'<img src="{html.escape(chrome.file_url(p))}">' for p in pngs)
    return ("<!doctype html><html><head><meta charset='utf-8'><style>" + PAGE_CSS +
            "img{display:block;width:%dpx;height:%dpx;break-after:page;page-break-after:always}"
            "img:last-child{break-after:auto;page-break-after:auto}</style></head><body>" % (common.W, common.H) +
            imgs + "<script>Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))"
            ".then(()=>document.body.dataset.ready='1')</script></body></html>")


def main():
    ap = argparse.ArgumentParser(description="Export a rendered carousel to PDF (one slide per page).")
    ap.add_argument("carousel", help="path to carousels/<slug>")
    ap.add_argument("--out", help="output PDF (default: <carousel>/exports/<slug>.pdf)")
    ap.add_argument("--vector", action="store_true",
                    help="print the HTML instead of the PNGs (selectable text; can mis-render in phone/WhatsApp viewers)")
    args = ap.parse_args()

    cdir = os.path.abspath(args.carousel)
    out = os.path.abspath(args.out or os.path.join(cdir, "exports", os.path.basename(cdir) + ".pdf"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = None
    if args.vector:
        src = os.path.join(cdir, "slides.html")
        if not os.path.isfile(src):
            sys.exit("No slides.html in that folder. Run render.py first.")
    else:
        pngs = sorted(glob.glob(os.path.join(cdir, "slides", "[0-9]*.png")))
        if not pngs:
            sys.exit("No slides/*.png in that folder. Run render.py first.")
        fd, tmp = tempfile.mkstemp(suffix=".html", prefix="carousel-pdf-")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(image_page_html(pngs))
        src = tmp

    binary = chrome.find_chrome()
    if not binary:
        sys.exit("No Chrome/Chromium found (set CHROME_PATH).")
    b = chrome.Browser(binary)
    try:
        sid = b.page(common.W, common.H)
        b.goto(sid, chrome.file_url(src))
        if args.vector:
            b.js(sid, "(() => { const s = document.createElement('style'); s.textContent = %r;"
                      " document.head.appendChild(s); document.body.classList.add('all'); return 1; })()" % PRINT_CSS)
        res = b.send("Page.printToPDF", {"printBackground": True, "preferCSSPageSize": True,
                                         "marginTop": 0, "marginBottom": 0, "marginLeft": 0, "marginRight": 0},
                     sid, timeout=120)
        with open(out, "wb") as f:
            f.write(base64.b64decode(res["data"]))
    finally:
        b.close()
        if tmp:
            os.remove(tmp)
    print(f"pdf ({'vector' if args.vector else 'image'}) -> {out}")


if __name__ == "__main__":
    main()
