#!/usr/bin/env python3
"""
reference.py - measure an attached template photo so its design can be extracted exactly, then check the copy.

Uses headless Chrome's canvas, so there are no Python packages to install.

  tiles    Split an image that shows several slides (a grid or collage) into one image per slide.
           python3 reference.py tiles board.png --rows 3 --cols 3 --out refs/tiles/
  inspect  Measure one reference slide at 1080px wide: the background colour, the real palette (hex and share
           of the slide) and a copy with a labelled 10% grid, so positions can be read as percentages.
           python3 reference.py inspect refs/tiles/r1.png --out refs/
           If the image has a dark board or a border around the slide, crop to the slide first (pixels of the source):
           python3 reference.py inspect refs/r1.png --crop 40,60,330,420 --out refs/
  compare  Put one of our slides next to the reference (side by side, and a 50% overlay, both with the grid) and
           list the 10% cells whose colours differ most, to catch a drifted background, shape or colour.
           python3 reference.py compare refs/tiles/r1.png carousels/<slug>/slides/01.png --out refs/
           (--crop x0,y0,x1,y1 trims the reference to the slide first, as for inspect.)

Fonts, sizes and weights are read by looking at the image (the Read tool shows it); this script measures the
colours and positions that are hard to eyeball.
"""

import argparse
import base64
import json
import mimetypes
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome  # noqa: E402


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def run(js_body, params, w=1200, h=900):
    """Run an async JS body in a blank Chrome page; it gets `P` (params) and returns a JSON-able value."""
    binary = chrome.find_chrome()
    if not binary:
        sys.exit("No Chrome/Chromium found (set CHROME_PATH).")
    b = chrome.Browser(binary)
    try:
        sid = b.page(w, h)
        b.goto(sid, "about:blank", wait_ready=False)
        expr = "(async () => { const P = %s; %s })()" % (json.dumps(params), js_body)
        return b.js(sid, expr, timeout=120)
    finally:
        b.close()


LOAD = """
const load = src => new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = src; });
const cv = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const hex = (r, g, b) => '#' + [r, g, b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
function grid(ctx, W, H, step) {
  ctx.save(); ctx.lineWidth = 1; ctx.font = '14px monospace';
  for (let k = 1; k < 10; k++) {
    const x = W * k / 10, y = H * k / 10;
    ctx.strokeStyle = 'rgba(255,0,200,.75)'; ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    ctx.fillStyle = '#000'; ctx.fillRect(x + 2, 2, 34, 17); ctx.fillRect(2, y + 2, 34, 17);
    ctx.fillStyle = '#FF00C8'; ctx.fillText(k * 10 + '%', x + 4, 15); ctx.fillText(k * 10 + '%', 4, y + 15);
  }
  ctx.restore();
}
"""


def crop_arg(v):
    if not v:
        return None
    parts = [int(x) for x in v.split(",")]
    if len(parts) != 4 or parts[2] <= parts[0] or parts[3] <= parts[1]:
        sys.exit("--crop needs x0,y0,x1,y1 in source pixels, with x1 > x0 and y1 > y0")
    return parts


def write_png(path, uri):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(uri.split(",", 1)[1]))


def cmd_tiles(a):
    res = run(LOAD + """
      const img = await load(P.src); const tw = Math.floor((img.width - 2 * P.trim) / P.cols), th = Math.floor((img.height - 2 * P.trim) / P.rows);
      const out = [];
      for (let r = 0; r < P.rows; r++) for (let c = 0; c < P.cols; c++) {
        const k = cv(tw, th); k.getContext('2d').drawImage(img, P.trim + c * tw, P.trim + r * th, tw, th, 0, 0, tw, th); out.push(k.toDataURL('image/png'));
      }
      return { w: img.width, h: img.height, tw, th, tiles: out };""",
        {"src": data_uri(a.image), "rows": a.rows, "cols": a.cols, "trim": a.trim})
    for i, uri in enumerate(res["tiles"], 1):
        write_png(os.path.join(a.out, f"tile-{i:02d}.png"), uri)
    print(f"{a.image}: {res['w']}x{res['h']} -> {len(res['tiles'])} tiles of {res['tw']}x{res['th']} in {a.out}")
    print("Look at each tile; delete the ones that are photos or ads, keep the slides you want to copy.")


def cmd_inspect(a):
    res = run(LOAD + """
      const full = await load(P.src); const cr = P.crop || [0, 0, full.width, full.height];
      const img = cv(cr[2] - cr[0], cr[3] - cr[1]); img.getContext('2d').drawImage(full, cr[0], cr[1], img.width, img.height, 0, 0, img.width, img.height);
      const W = 1080, H = Math.round(img.height * W / img.width);
      const c = cv(W, H), ctx = c.getContext('2d'); ctx.drawImage(img, 0, 0, W, H);
      const sm = cv(180, Math.max(1, Math.round(H * 180 / W))), sctx = sm.getContext('2d'); sctx.drawImage(img, 0, 0, sm.width, sm.height);
      const px = sctx.getImageData(0, 0, sm.width, sm.height).data, buckets = new Map();
      for (let i = 0; i < px.length; i += 4) {
        if (px[i + 3] < 200) continue;
        const k = (px[i] >> 4) << 8 | (px[i + 1] >> 4) << 4 | (px[i + 2] >> 4);
        const b = buckets.get(k) || { n: 0, r: 0, g: 0, b: 0 }; b.n++; b.r += px[i]; b.g += px[i + 1]; b.b += px[i + 2]; buckets.set(k, b);
      }
      let cl = [...buckets.values()].map(b => ({ n: b.n, r: b.r / b.n, g: b.g / b.n, b: b.b / b.n })).sort((x, y) => y.n - x.n);
      const merged = [];
      for (const c0 of cl) {
        const m = merged.find(m => Math.hypot(m.r - c0.r, m.g - c0.g, m.b - c0.b) < 36);
        if (m) { const t = m.n + c0.n; m.r = (m.r * m.n + c0.r * c0.n) / t; m.g = (m.g * m.n + c0.g * c0.n) / t; m.b = (m.b * m.n + c0.b * c0.n) / t; m.n = t; }
        else merged.push({ ...c0 });
      }
      merged.sort((x, y) => y.n - x.n);
      const total = px.length / 4;
      // background: the most common colour along the outer edge
      const edge = new Map();
      const add = (x, y) => { const i = (y * sm.width + x) * 4; const k = hex(px[i] >> 4 << 4, px[i + 1] >> 4 << 4, px[i + 2] >> 4 << 4); edge.set(k, (edge.get(k) || 0) + 1); };
      for (let x = 0; x < sm.width; x++) { add(x, 0); add(x, sm.height - 1); }
      for (let y = 0; y < sm.height; y++) { add(0, y); add(sm.width - 1, y); }
      const bg = [...edge.entries()].sort((x, y) => y[1] - x[1])[0][0];
      const g = cv(W, H), gctx = g.getContext('2d'); gctx.drawImage(img, 0, 0, W, H); grid(gctx, W, H);
      const near = (a, b) => { const pa = a.match(/[0-9a-fA-F]{2}/g).map(v => parseInt(v, 16)), pb = b.match(/[0-9a-fA-F]{2}/g).map(v => parseInt(v, 16)); return Math.hypot(pa[0] - pb[0], pa[1] - pb[1], pa[2] - pb[2]) < 40; };
      const top2 = merged.slice(0, 2).map(m => hex(m.r, m.g, m.b));
      const edge_ok = top2.some(t => near(t, bg));
      return { w: img.width, h: img.height, W, H, bg_edge: bg, edge_ok,
        palette: merged.slice(0, 8).map(m => ({ hex: hex(m.r, m.g, m.b), share: +(m.n / total * 100).toFixed(1) })), grid: g.toDataURL('image/png') };""",
        {"src": data_uri(a.image), "crop": crop_arg(a.crop)})
    base = os.path.splitext(os.path.basename(a.image))[0]
    out = os.path.join(a.out, f"{base}-grid.png")
    write_png(out, res["grid"])
    print(f"{a.image}: {res['w']}x{res['h']} (measured at {res['W']}x{res['H']})")
    print(f"background (edge colour, quantised): {res['bg_edge']}")
    if not res["edge_ok"]:
        print("WARNING: the edge colour is not one of the two biggest colours, so there is probably a board or border around the slide.\n"
              "         The palette below includes it. Re-run with --crop x0,y0,x1,y1 (source pixels) to measure the slide alone.")
    if res["w"] < 500:
        print(f"WARNING: the image is only {res['w']}px wide; type sizes and weights will be guesses. Ask for a larger image if you can.")
    print("palette (hex, share of the slide):")
    for p in res["palette"]:
        print(f"  {p['hex']}  {p['share']}%")
    print(f"grid copy -> {out}  (read positions from the labelled 10% lines)")


def cmd_compare(a):
    res = run(LOAD + """
      const refFull = await load(P.ref), ours = await load(P.ours); const cr = P.crop || [0, 0, refFull.width, refFull.height];
      const ref = cv(cr[2] - cr[0], cr[3] - cr[1]); ref.getContext('2d').drawImage(refFull, cr[0], cr[1], ref.width, ref.height, 0, 0, ref.width, ref.height);
      const W = 540, H = Math.round(W * 1350 / 1080);
      const c = cv(W * 3 + 40, H + 20), ctx = c.getContext('2d'); ctx.fillStyle = '#222'; ctx.fillRect(0, 0, c.width, c.height);
      ctx.drawImage(ref, 10, 10, W, H); ctx.drawImage(ours, W + 20, 10, W, H);
      ctx.drawImage(ref, 2 * W + 30, 10, W, H); ctx.globalAlpha = .5; ctx.drawImage(ours, 2 * W + 30, 10, W, H); ctx.globalAlpha = 1;
      for (const x0 of [10, W + 20, 2 * W + 30]) { ctx.save(); ctx.translate(x0, 10); grid(ctx, W, H); ctx.restore(); }
      // 10x10 cell colour difference
      const a1 = cv(100, 100), b1 = cv(100, 100); a1.getContext('2d').drawImage(ref, 0, 0, 100, 100); b1.getContext('2d').drawImage(ours, 0, 0, 100, 100);
      const da = a1.getContext('2d').getImageData(0, 0, 100, 100).data, db = b1.getContext('2d').getImageData(0, 0, 100, 100).data, cells = [];
      for (let cy = 0; cy < 10; cy++) for (let cx = 0; cx < 10; cx++) {
        let s = [0, 0, 0], t = [0, 0, 0];
        for (let y = 0; y < 10; y++) for (let x = 0; x < 10; x++) { const i = ((cy * 10 + y) * 100 + cx * 10 + x) * 4; for (let k = 0; k < 3; k++) { s[k] += da[i + k]; t[k] += db[i + k]; } }
        const d = Math.hypot(...s.map((v, k) => (v - t[k]) / 100));
        cells.push({ x: cx * 10, y: cy * 10, d: +d.toFixed(0), ref: hex(s[0] / 100, s[1] / 100, s[2] / 100), ours: hex(t[0] / 100, t[1] / 100, t[2] / 100) });
      }
      cells.sort((p, q) => q.d - p.d);
      return { img: c.toDataURL('image/png'), cells: cells.slice(0, 8), mean: +(cells.reduce((s, c) => s + c.d, 0) / 100).toFixed(1) };""",
        {"ref": data_uri(a.reference), "ours": data_uri(a.ours), "crop": crop_arg(a.crop)})
    out = os.path.join(a.out, f"compare-{os.path.splitext(os.path.basename(a.ours))[0]}.png")
    write_png(out, res["img"])
    print(f"side by side (reference | ours | 50% overlay) -> {out}")
    print(f"mean colour difference per 10% cell: {res['mean']} (0 identical; over about 40 the colours have drifted)")
    print("cells that differ most (x%, y% of the slide's top-left corner of the cell):")
    for c in res["cells"]:
        print(f"  {c['x']:>3}%,{c['y']:>3}%  diff {c['d']:>3}  reference {c['ref']}  ours {c['ours']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tiles"); t.add_argument("image"); t.add_argument("--rows", type=int, required=True)
    t.add_argument("--cols", type=int, required=True); t.add_argument("--trim", type=int, default=0, help="px to trim from every outer edge")
    t.add_argument("--out", default="refs/tiles")
    i = sub.add_parser("inspect"); i.add_argument("image"); i.add_argument("--out", default="refs")
    i.add_argument("--crop", help="x0,y0,x1,y1 in source pixels: measure only the slide, not a board around it")
    c = sub.add_parser("compare"); c.add_argument("reference"); c.add_argument("ours"); c.add_argument("--out", default="refs")
    c.add_argument("--crop", help="x0,y0,x1,y1 in source pixels: trim the reference to the slide first")
    a = ap.parse_args()
    {"tiles": cmd_tiles, "inspect": cmd_inspect, "compare": cmd_compare}[a.cmd](a)


if __name__ == "__main__":
    main()
