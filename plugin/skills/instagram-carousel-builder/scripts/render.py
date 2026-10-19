#!/usr/bin/env python3
"""
render.py - screenshot and measure a carousel whose slides Claude wrote by hand.

Reads   <carousel>/slides.html     every slide as <section class="slide"> (contract: assets/slide-base.html)
        <carousel>/design.md       this post's design (optional here; lint and the board use it)
        <carousel>/script.json     the copy (optional here; the board uses the cover headline)

Writes  <carousel>/slides/01.png ...    one PNG per slide, exactly 1080x1350
        <carousel>/render_report.json   what the browser measured: type sizes, clipping, overlaps, empty space,
                                        contrast, structure (headline, visual, footer), fonts that loaded
        <carousel>/board.html + .png    design summary and every slide at phone size, with flags
        <carousel>/status.json          stage -> "rendered"

render.py never edits slides.html. If it reports a problem, fix slides.html and run it again.

Needs Google Chrome or Chromium (set CHROME_PATH for another binary) and internet for Google Fonts.
No Python packages required.

Usage
  python3 render.py carousels/<slug>
  python3 render.py carousels/<slug> --only 2,5     # re-shoot just these slides (the report still covers all)
  python3 render.py carousels/<slug> --no-board
"""

import argparse
import datetime as dt
import glob
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome  # noqa: E402
import common  # noqa: E402

W, H = common.W, common.H
HERE = os.path.dirname(os.path.abspath(__file__))


def slide_flags(s):
    """Short human-readable problems for one slide's measurements."""
    f = []
    if abs(s["size"]["w"] - W) > 0.6 or abs(s["size"]["h"] - H) > 0.6:
        f.append(f"slide is {s['size']['w']:.0f}x{s['size']['h']:.0f}, needs {W}x{H}")
    if s["headline"]["count"] != 1:
        f.append(f"{s['headline']['count']} .headline elements (needs exactly 1)")
    if not s["visual"]["count"]:
        f.append("no .visual")
    elif (s["visual"].get("svg_scale") or 1) < 0.95:
        bx = s["visual"].get("box") or {}
        f.append(f"the visual's SVG is shrunk to {s['visual']['svg_scale']:.2f}x (its box is {bx.get('w')}x{bx.get('h')}): redraw it with "
                 f"viewBox=\"0 0 {bx.get('w')} {bx.get('h')}\" so text stays at its real size")
    if s["visual"]["count"] and s["visual"]["pct"] < 35:
        f.append(f"visual covers {s['visual']['pct']:.0f}% of the slide (aim for 40-60%)")
    if not s["footer"]["site"] or "BUILDABLELABS.COM" not in s["footer"]["site"]:
        f.append("footer BUILDABLELABS.COM missing")
    if s["above_headline"]:
        f.append("text above the headline: " + "; ".join(s["above_headline"][:2]))
    if s["clipped"]:
        f.append("clipped: " + "; ".join(c["text"] for c in s["clipped"][:2]))
    if s["overlaps"]:
        o = s["overlaps"][0]
        f.append(f"text overlaps text: '{o['a']}' / '{o['b']}'")
    if s["text_over_visual"]:
        f.append("text over the visual: " + "; ".join(s["text_over_visual"][:2]))
    if s["highlight_touch"]:
        f.append("highlight block touches a line: " + s["highlight_touch"][0]["block"])
    if s["small_text"]:
        t = s["small_text"][0]
        f.append(f"text at {t['px']}px: '{t['text']}'")
    if s["light_weight"]:
        f.append(f"weight {s['light_weight']['weight']}: '{s['light_weight']['text']}'")
    mc = s["min_contrast"]
    if mc and mc["ratio"] < 4.5:
        f.append(f"contrast {mc['ratio']}:1 on '{mc['text']}'")
    if s["empty"]["pct"] > 30:
        f.append(f"empty block {s['empty']['w']}x{s['empty']['h']} ({s['empty']['pct']}% of the slide)")
    return f


# ---------------------------------------------------------------- board

BOARD_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1500px;background:#15161A;color:#EDEEF2;font-family:Helvetica,Arial,sans-serif;padding:56px 64px 72px}
.lbl{font-family:Menlo,monospace;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:#8A90A0}
.hd{display:flex;justify-content:space-between;align-items:flex-start;gap:30px;padding-bottom:26px;border-bottom:1px solid #2A2C34;margin-bottom:34px}
.ttl{font-size:46px;font-weight:700;line-height:1.1;margin-top:12px;max-width:1100px}
.tag{font-family:Menlo,monospace;font-size:13px;letter-spacing:.16em;padding:9px 16px;border:1px solid;white-space:nowrap}
.panels{display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:22px;margin-bottom:22px}
.card{background:#1D1F26;border:1px solid #2A2C34;padding:26px 28px}
.look{font-size:18px;line-height:1.5;color:#C9CCD6;margin-top:12px}
.sw{display:flex;gap:12px;align-items:center;margin-top:12px;font-size:15px}
.sw b{width:38px;height:38px;border:1px solid #444;flex:none}
.m{font-family:Menlo,monospace;font-size:12px;color:#8A90A0}
.chip{display:inline-block;font-size:14px;padding:6px 12px;border:1px solid #3A3D48;margin:8px 8px 0 0}
.row{margin-top:12px;font-size:16px;line-height:1.4}
.ok{color:#7FD4A0}.bad{color:#F26B6B}.warn{color:#F2B544}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:16px}
.th img{width:100%;display:block;border:1px solid #2A2C34}
.cap{margin-top:10px;font-size:14px;line-height:1.45}
.cap .f{color:#F2B544}
"""


def build_board(cdir, fp, text, report, script, repeat_summary):
    e = html.escape
    slides = report["slides"]
    title = ((script or {}).get("title") or ((script or {}).get("slides") or [{}])[0].get("headline")
             or os.path.basename(cdir))
    kind = (fp or {}).get("kind", "")
    srcs = ", ".join((fp or {}).get("sources") or [])
    head = f'{e((fp or {}).get("name", "no design.md"))} &middot; {e(kind)}' + ((f" &middot; copies {e(srcs.replace('reference:', ''))}" if kind == "reference" else f" &middot; mixed from {e(srcs)}") if srcs else "")
    pal = "".join(f'<div class="sw"><b style="background:{e(c)}"></b><div class="m">{e(c)}</div></div>'
                  for c in (fp or {}).get("palette", []))
    fonts = (fp or {}).get("fonts") or {}
    fonts_html = "".join(f'<div class="row"><span class="m">{e(k)}</span> &nbsp; {e(str(v))}</div>' for k, v in fonts.items())
    taken = (fp or {}).get("taken") or {}
    taken_html = "".join(f'<span class="chip">{e(k)}: {e(str(v))}</span>' for k, v in taken.items())
    traits = "".join(f'<span class="chip">{e(str(x))}</span>' for x in [
        (fp or {}).get("layout"), (fp or {}).get("emphasis"), (fp or {}).get("visual_style"), *((fp or {}).get("devices") or [])] if x)
    look = common.design_look(text or "")
    font_bad = [f for f in report["fonts"] if f["status"] in ("failed", "missing")]
    font_html = "".join(f'<div class="row bad">font not loaded: {e(f["family"])}</div>' for f in font_bad)
    thumbs = []
    stamp = int(dt.datetime.now().timestamp())
    for s in slides:
        flags = slide_flags(s)
        fl = "".join(f'<div class="f">! {e(x)}</div>' for x in flags) or '<div class="ok">clean</div>'
        thumbs.append(f'<div class="th"><img src="slides/{s["n"]:02d}.png?v={stamp}"><div class="cap"><span class="lbl">'
                      f'{s["n"]:02d} &middot; {e(s["type"])} &middot; min {s["min_px"] or "?"}px &middot; visual {s["visual"]["pct"]:.0f}%'
                      f'</span>{fl}</div></div>')
    rep_html = f'<div class="row">{e(repeat_summary)}</div>' if repeat_summary else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Board</title><style>{BOARD_CSS}</style></head><body>
<div class="hd"><div><div class="lbl">Design board &middot; {head}</div><div class="ttl">{e(title)}</div></div></div>
<div class="panels">
<div class="card"><div class="lbl">The design</div><div class="look">{e(look) or "(no design.md)"}</div>{traits and '<div>' + traits + '</div>'}</div>
<div class="card"><div class="lbl">Palette</div>{pal}</div>
<div class="card"><div class="lbl">Fonts</div>{fonts_html}{font_html}<div class="lbl" style="margin-top:18px">{"Copied from the reference" if kind == "reference" else "Mixed from"}</div>{taken_html or '<div class="row m">(not a mix)</div>'}{rep_html}</div>
</div>
<div class="lbl">Slides at roughly phone size</div>
<div class="grid">{"".join(thumbs)}</div>
<script>(async()=>{{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{{}})));document.body.dataset.ready='1';}})();</script>
</body></html>"""


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Screenshot and measure a carousel's hand-written slides.html.")
    ap.add_argument("carousel", help="path to carousels/<slug>")
    ap.add_argument("--only", help="comma-separated slide numbers to re-shoot")
    ap.add_argument("--no-board", action="store_true")
    args = ap.parse_args()

    cdir = os.path.abspath(args.carousel)
    src = os.path.join(cdir, "slides.html")
    if not os.path.isfile(src):
        sys.exit("No slides.html in that folder. Write it from assets/slide-base.html first.")
    script = common.load_json(os.path.join(cdir, "script.json"))
    fp, dtext, derr = common.load_design(os.path.join(cdir, "design.md"))
    if derr:
        print(f"note: design.md: {derr} (lint will flag it)", file=sys.stderr)

    binary = chrome.find_chrome()
    if not binary:
        print("No Chrome/Chromium found. Install Google Chrome or set CHROME_PATH.", file=sys.stderr)
        sys.exit(2)

    measure = open(os.path.join(HERE, "measure.js"), encoding="utf-8").read()
    os.makedirs(os.path.join(cdir, "slides"), exist_ok=True)
    browser = chrome.Browser(binary)
    problems = []
    try:
        sid = browser.page(W, H)
        browser.goto(sid, chrome.file_url(src), wait_ready=False)
        report = browser.js(sid, measure, timeout=180)
        total = len(report["slides"])
        if not total:
            sys.exit("slides.html has no .slide elements.")
        wanted = list(range(1, total + 1))
        if args.only:
            wanted = [int(x) for x in args.only.split(",") if x.strip()]
        for stale in glob.glob(os.path.join(cdir, "slides", "*.png")):
            n = int(re.sub(r"\D", "", os.path.basename(stale)) or 0)
            if n > total:
                os.remove(stale)
        if script and len(script.get("slides") or []) != total:
            problems.append(f"script.json has {len(script.get('slides') or [])} slides but slides.html has {total}")
        for n in wanted:
            s = report["slides"][n - 1]
            out = os.path.join(cdir, "slides", f"{n:02d}.png")
            browser.shot(sid, out, W, H, x=s["doc"]["x"], y=s["doc"]["y"])
            if chrome.png_size(out) != (W, H):
                problems.append(f"slide {n}: expected {W}x{H}, got {chrome.png_size(out)}")
        report.update({"rendered_at": common.now(), "chrome": binary, "size": [W, H], "problems": problems,
                       "design": (fp or {}).get("name")})
        common.write_json(os.path.join(cdir, "render_report.json"), report)

        if not args.no_board:
            repeat_summary = ""
            try:
                import design_log
                repeat_summary = design_log.summary_line(cdir)
            except Exception:
                pass
            bh = os.path.join(cdir, "board.html")
            with open(bh, "w", encoding="utf-8") as f:
                f.write(build_board(cdir, fp, dtext, report, script, repeat_summary))
            bid = browser.page(1500, 1200)
            browser.goto(bid, chrome.file_url(bh))
            height = int(browser.js(bid, "document.documentElement.scrollHeight"))
            browser.resize(bid, 1500, height)
            browser.shot(bid, os.path.join(cdir, "board.png"), 1500, height)
    finally:
        browser.close()

    sp = os.path.join(cdir, "status.json")
    st = common.load_json(sp, {}) or {}
    st["slug"] = os.path.basename(cdir)
    st["stage"] = "rendered"
    st["updated"] = common.now()
    st.setdefault("history", []).append({"at": st["updated"], "event": "rendered", "slides": wanted if args.only else "all"})
    common.write_json(sp, st)

    print(f"rendered {len(wanted)} slide(s) -> {os.path.relpath(os.path.join(cdir, 'slides'))}/")
    for f in report["fonts"]:
        if f["status"] in ("failed", "missing"):
            print(f"  ! font not loaded, fell back: {f['family']} ({f['status']})")
    clean = True
    for s in report["slides"]:
        flags = slide_flags(s)
        if flags:
            clean = False
            print(f"  slide {s['n']:02d} {s['type']}:")
            for x in flags:
                print("    - " + x)
    for p in problems:
        clean = False
        print("  ! " + p)
    if clean:
        print("  all slides clean (lint and the judge still run)")
    if not args.no_board:
        print(f"board -> {os.path.relpath(os.path.join(cdir, 'board.png'))}")


if __name__ == "__main__":
    main()
