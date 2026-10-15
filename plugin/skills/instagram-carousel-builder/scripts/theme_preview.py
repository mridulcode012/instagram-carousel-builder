#!/usr/bin/env python3
"""
theme_preview.py - render the sample script in every theme (and its variants) and save
assets/themes/<name>/preview.png, so themes can be compared side by side and picked by eye.
Previews go next to the theme: a project's own themes/<name>/ (new themes) or, in the repo, the bundled assets/themes.

Usage
  python3 theme_preview.py                 # every theme
  python3 theme_preview.py foundation      # one theme
Uses the same renderer as real carousels.
"""

import glob
import html
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render  # noqa: E402


def main():
    root = render.find_root(os.getcwd())
    if not root:
        sys.exit("No brand kit found (assets/brand/brand.json is missing).")
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__.strip()); return
    # a project's own themes/ (where new themes are drafted) wins; otherwise the skill's bundled themes (maintainers)
    tdir = next((t for t in render.theme_dirs(os.getcwd(), root) if os.path.isdir(t)), os.path.join(render.ASSETS, "themes"))
    render.THEME_START = os.getcwd()
    names = sys.argv[1:] or sorted(d for d in os.listdir(tdir)
                                    if not d.startswith(("_", ".")) and os.path.isfile(os.path.join(tdir, d, "theme.json")))
    sample = os.path.join(tdir, "_sample")
    if not os.path.isfile(os.path.join(sample, "script.json")):
        sample = os.path.join(render.ASSETS, "themes", "_sample")
    binary = render.find_chrome()
    if not binary:
        sys.exit("Chrome/Chromium not found.")
    for name in names:
        meta = render.load_json(os.path.join(tdir, name, "theme.json"))
        if meta is None:
            print(f"skip {name}: no theme.json in {tdir}/{name}"); continue
        rows = [(None, "default")] + [(k, k) for k in (meta.get("variants") or {})]
        work = tempfile.mkdtemp(prefix=f".preview-{name}-", dir=os.getcwd())  # inside the project, so its themes/ is found
        try:
            row_html = []
            for variant, label in rows:
                c = os.path.join(work, label)
                os.makedirs(c)
                shutil.copy(os.path.join(sample, "script.json"), c)
                shutil.copy(os.path.join(sample, "brief.md"), c)
                vision = {"name": f"{name}-preview", "status": "locked", "theme": name}
                if variant:
                    vision["variant"] = variant
                render.write_json(os.path.join(c, "vision.json"), vision)
                r = os.system(f'"{sys.executable}" "{os.path.join(HERE, "render.py")}" "{c}" --no-board > /dev/null')
                if r:
                    sys.exit(f"render failed for {name}/{label}")
                imgs = "".join(f'<img src="{label}/slides/{os.path.basename(p)}">' for p in sorted(glob.glob(os.path.join(c, "slides", "[0-9]*.png"))))
                row_html.append(f'<div class="lbl">{html.escape(name)} &middot; {html.escape(label)}</div><div class="row">{imgs}</div>')
            page = os.path.join(work, "preview.html")
            with open(page, "w", encoding="utf-8") as f:
                f.write(f"""<!doctype html><meta charset="utf-8"><style>
body{{margin:0;padding:40px;width:2000px;box-sizing:border-box;background:#17191E;font:500 22px/1.3 Menlo,monospace;color:#C9CDD6}}
.lbl{{letter-spacing:.12em;text-transform:uppercase;margin:6px 0 14px}} .row{{display:flex;gap:16px;margin-bottom:34px}}
img{{width:262px;height:327px;display:block}}</style>
<div class="lbl" style="font-size:34px;color:#fff">{html.escape(name)}</div><div style="font:400 22px/1.5 Helvetica,Arial,sans-serif;color:#C9CDD6;max-width:1900px;margin-bottom:28px">{html.escape(meta.get('description', ''))}</div>
{''.join(row_html)}<script>Promise.all([...document.images].map(i=>i.decode().catch(()=>{{}}))).then(()=>document.body.dataset.ready=1)</script>""")
            b = render.Browser(binary)
            try:
                sid = b.page(2000, 600)
                b.goto(sid, render.file_url(page))
                h = int(b.js(sid, "document.documentElement.scrollHeight"))
                b.resize(sid, 2000, h)
                b.shot(sid, os.path.join(tdir, name, "preview.png"), 2000, h)
            finally:
                b.close()
            print(f"themes/{name}/preview.png  ({len(rows)} row(s))")
        finally:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
