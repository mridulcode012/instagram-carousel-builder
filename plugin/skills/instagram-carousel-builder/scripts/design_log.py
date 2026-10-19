#!/usr/bin/env python3
"""
design_log.py - the design library, the last-5 history and the no-repeat check.

A design is a design.md whose first ```json block is its fingerprint (references/design-system.md).
Saved designs live in the working folder's designs/ (log in designs/log.json); the skill ships the
library in assets/designs/.

Usage
  python3 design_log.py library [--root DIR]        list library specs and saved designs
  python3 design_log.py recent [N] [--root DIR]     the last N (default 5) saved designs' fingerprints
  python3 design_log.py check carousels/<slug>      compare this post's design with the last 5 (exit 1 if it repeats)
  python3 design_log.py save carousels/<slug>       validate, copy to designs/ and log the fingerprint
  python3 design_log.py import FILE...              bring earlier posts' <date>-<slug>.design.md files back into the log
"""

import argparse
import colorsys
import datetime as dt
import glob
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

LOOKBACK = 5
MIN_DIFFERENT = 4          # dimensions (of 7) that must differ from each of the last 5 designs
DIMS = ["colour", "accent", "type", "layout", "emphasis", "devices", "visual_style"]
TAKEN_DIMS = ["layout", "type", "colour", "emphasis", "devices", "visual_style"]

VOCAB = {
    "mode": {"dark", "light", "colour", "alternating"},
    "display_class": {"serif", "serif-italic", "sans", "sans-heavy", "sans-condensed", "sans-wide", "slab", "mono", "pixel",
                      "script", "handwritten", "typewriter"},
    "case": {"upper", "sentence", "lower", "mixed"},
    "layout": {"stack-top", "centered-stack", "poster", "split-vertical", "split-horizontal", "grid-modules", "card-on-canvas",
               "full-bleed-visual", "asymmetric-offset", "rail", "collage"},
    "emphasis": {"highlight-block", "underline-marker", "italic-serif-word", "colour-word", "outline-text", "sticker-word",
                 "circled-scribble", "size-jump", "strike-swap", "none"},
    "devices": {"visible-grid", "corner-marks", "swoop-line", "ghost-word", "tape", "stamps", "scribbles", "sunburst", "blobs",
                "circles", "hard-shadow", "pixel-frame", "scanlines", "grain", "dot-pattern", "stripes", "progress-bar",
                "rail-line", "badges", "rules", "gradient-light", "frosted-glass", "speech-bubbles", "hand-arrows",
                "paper-texture", "halftone", "outline-boxes"},
    "visual_style": {"flat-outline", "flat-solid", "ui-mockup", "hand-drawn", "pixel", "isometric", "hard-shadow-blocks",
                     "glass-depth", "editorial-line", "sticker-cutout", "data-minimal"},
}
FIXED_BODY, FIXED_LABEL = "Manrope", "JetBrains Mono"
REQUIRED = ["name", "kind", "mode", "background", "accent", "palette", "fonts", "type", "layout", "emphasis", "devices",
            "visual_style"]


# ---------------------------------------------------------------- fingerprints

def validate(fp):
    """(errors, notes) for a fingerprint dict."""
    errs, notes = [], []
    for k in REQUIRED:
        if k not in fp:
            errs.append(f"missing '{k}'")
    if errs:
        return errs, notes
    if fp["kind"] not in ("library", "mix", "reference"):
        errs.append("kind must be library, mix or reference")
    for k in ("background", "accent"):
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(fp[k])):
            errs.append(f"{k} must be a #RRGGBB hex")
    t = fp.get("type") or {}
    for k in ("display_class", "case"):
        if k not in t:
            errs.append(f"type.{k} missing")
    if not isinstance(fp.get("devices"), list):
        errs.append("devices must be a list")
    if not (fp.get("fonts") or {}).get("display"):
        errs.append("fonts.display missing")
    if errs:
        return errs, notes
    for key, val in [("mode", fp["mode"]), ("display_class", t["display_class"]), ("case", t["case"]), ("layout", fp["layout"]),
                     ("emphasis", fp["emphasis"]), ("visual_style", fp["visual_style"])]:
        if val not in VOCAB[key]:
            notes.append(f"{key} '{val}' isn't in the vocabulary (it counts as different from everything)")
    for d in fp["devices"]:
        if d not in VOCAB["devices"]:
            notes.append(f"device '{d}' isn't in the vocabulary")
    if fp["kind"] == "mix" or fp.get("reuse"):
        f_ = fp.get("fonts") or {}
        if f_.get("body") != FIXED_BODY or f_.get("label") != FIXED_LABEL:
            errs.append(f"fonts.body must be '{FIXED_BODY}' and fonts.label '{FIXED_LABEL}' (only the display font is free; "
                        "references/design-system.md section 3a)")
    if fp["kind"] == "mix":
        srcs = fp.get("sources") or []
        taken = fp.get("taken") or {}
        if len(srcs) < 2:
            errs.append("a mix needs at least 2 sources")
        missing = [d for d in TAKEN_DIMS if d not in taken]
        if missing:
            errs.append("taken is missing: " + ", ".join(missing))
        else:
            vals = [v for v in taken.values() if v != "own"]
            if vals:
                top = max(set(vals), key=vals.count)
                other = [v for v in taken.values() if v != top]
                if len(other) < 2:
                    errs.append(f"only {len(other)} dimension(s) come from a second source; take at least 2 (it's a mix, not a copy of '{top}')")
    return errs, notes


def _rgb(h):
    return common.hex_rgb(h)


def _dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(_rgb(a), _rgb(b))) ** 0.5


def _hue(h):
    r, g, b = [c / 255 for c in _rgb(h)]
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, ss, ll


def compare(a, b):
    """Dict of dimension -> True when two fingerprints are the same on it."""
    same = {}
    same["colour"] = a["mode"] == b["mode"] and _dist(a["background"], b["background"]) < 70
    ha, sa, _ = _hue(a["accent"])
    hb, sb, _ = _hue(b["accent"])
    if sa < 0.12 and sb < 0.12:
        same["accent"] = True
    elif sa < 0.12 or sb < 0.12:
        same["accent"] = False
    else:
        dh = abs(ha - hb)
        same["accent"] = min(dh, 360 - dh) <= 25
    fa, fb = a["fonts"], b["fonts"]
    same["type"] = (str(fa.get("display", "")).lower() == str(fb.get("display", "")).lower()
                    or (a["type"]["display_class"] == b["type"]["display_class"] and a["type"]["case"] == b["type"]["case"]))
    same["layout"] = a["layout"] == b["layout"]
    same["emphasis"] = a["emphasis"] == b["emphasis"]
    da, db = set(a["devices"]), set(b["devices"])
    same["devices"] = (not da and not db) or (bool(da and db) and len(da & db) / min(len(da), len(db)) >= 0.5)
    same["visual_style"] = a["visual_style"] == b["visual_style"]
    return same


# ---------------------------------------------------------------- the log

def designs_dir(root):
    return os.path.join(root, "designs")


def load_log(root):
    return common.load_json(os.path.join(designs_dir(root), "log.json"), []) or []


def recent(root, exclude_slug=None, n=LOOKBACK):
    entries = [e for e in load_log(root) if e.get("slug") != exclude_slug]
    return entries[-n:]


def check(cdir):
    """(ok, rows, fp, errs, notes): rows are (entry, same-dict, differing-count)."""
    cdir = os.path.abspath(cdir)
    fp, _, err = common.load_design(os.path.join(cdir, "design.md"))
    if err:
        return False, [], None, [f"design.md: {err}"], []
    errs, notes = validate(fp)
    if errs:
        return False, [], fp, errs, notes
    root = common.work_root(cdir)
    rows = []
    for e in recent(root, exclude_slug=os.path.basename(cdir)):
        s = compare(fp, e["fingerprint"])
        rows.append((e, s, sum(1 for d in DIMS if not s[d])))
    ok = all(diff >= MIN_DIFFERENT for _, _, diff in rows) or fp["kind"] == "reference" or bool(fp.get("reuse"))
    return ok, rows, fp, errs, notes


def summary_line(cdir):
    ok, rows, fp, errs, _ = check(cdir)
    if errs or not fp:
        return "no-repeat check: " + ("; ".join(errs) if errs else "no design.md")
    if not rows:
        return "no-repeat check: first design in the log"
    if fp["kind"] == "reference" or fp.get("reuse"):
        return "no-repeat check: reference or reused design, exempt (the person chose that look)"
    worst = min(d for _, _, d in rows)
    tag = "reference, exempt" if (fp["kind"] == "reference" or fp.get("reuse")) else ("pass" if ok else "FAIL")
    return f"no-repeat check: {tag} (closest of the last {len(rows)} differs on {worst} of 7 dimensions, needs {MIN_DIFFERENT})"


# ---------------------------------------------------------------- commands

def cmd_library(root):
    paths = sorted(glob.glob(os.path.join(common.LIBRARY, "*.design.md")))
    saved = sorted(glob.glob(os.path.join(designs_dir(root), "*.design.md")))
    print(f"{'name':22} {'kind':9} {'mode':12} {'display':24} {'layout':18} {'emphasis':17} {'visual style':18} devices")
    for p in paths + saved:
        fp, _, err = common.load_design(p)
        if err:
            print(f"{os.path.basename(p):22} (unreadable: {err})")
            continue
        t = fp["type"]
        where = "" if p in paths else "  [saved]"
        print(f"{fp['name']:22} {fp['kind']:9} {fp['mode']:12} {t['display_class'] + '/' + t['case']:24} {fp['layout']:18} "
              f"{fp['emphasis']:17} {fp['visual_style']:18} {', '.join(fp['devices'])}{where}")
    if not saved:
        print(f"(no saved designs yet in {designs_dir(root)})")


def cmd_recent(root, n):
    entries = load_log(root)[-n:]
    if not entries:
        print("no saved designs yet")
        return
    for e in entries:
        fp = e["fingerprint"]
        t = fp["type"]
        print(f"{e['date']} {e['slug']}: {fp['name']} ({fp['kind']}) mode={fp['mode']} bg={fp['background']} accent={fp['accent']} "
              f"display={fp['fonts'].get('display')} {t['display_class']}/{t['case']} layout={fp['layout']} "
              f"emphasis={fp['emphasis']} devices={','.join(fp['devices'])} visual={fp['visual_style']}")


def cmd_check(cdir):
    ok, rows, fp, errs, notes = check(cdir)
    for n in notes:
        print("note: " + n)
    if errs:
        print("design.md is not valid:")
        for e in errs:
            print("  - " + e)
        return 1
    print(f"design: {fp['name']} ({fp['kind']})")
    if not rows:
        print("no earlier designs in the log: nothing to repeat")
        return 0
    print(f"{'vs':36} " + " ".join(f"{d[:8]:8}" for d in DIMS) + "  differs")
    for e, s, diff in rows:
        cells = " ".join(f"{('same' if s[d] else '-'):8}" for d in DIMS)
        mark = "" if diff >= MIN_DIFFERENT else "   <-- too close"
        print(f"{(e['date'] + ' ' + e['slug'])[:36]:36} {cells}  {diff}/7{mark}")
    if fp["kind"] == "reference" or fp.get("reuse"):
        print("reference or reused design: exempt from the no-repeat rule (the person chose that look)")
        return 0
    if ok:
        print(f"pass: differs on {MIN_DIFFERENT}+ of 7 dimensions from each of the last {len(rows)}")
        return 0
    print(f"FAIL: each of the last {LOOKBACK} must differ on at least {MIN_DIFFERENT} of 7. Change the dimensions marked 'same' "
          "on the closest rows (a new layout, emphasis or palette is the cheapest) and run it again.")
    return 1


def cmd_save(cdir):
    cdir = os.path.abspath(cdir)
    path = os.path.join(cdir, "design.md")
    fp, text, err = common.load_design(path)
    if err:
        print(f"design.md: {err}")
        return 1
    errs, notes = validate(fp)
    if errs:
        print("design.md is not valid: " + "; ".join(errs))
        return 1
    root = common.work_root(cdir)
    slug = os.path.basename(cdir)
    date = common.now()[:10]
    dest = os.path.join(designs_dir(root), f"{date}-{slug}.design.md")
    os.makedirs(designs_dir(root), exist_ok=True)
    log = [e for e in load_log(root) if e.get("slug") != slug]
    for old in glob.glob(os.path.join(designs_dir(root), f"*-{slug}.design.md")):
        if old != dest:
            os.remove(old)
    shutil.copyfile(path, dest)
    log.append({"slug": slug, "date": date, "file": os.path.relpath(dest, root), "fingerprint": fp})
    common.write_json(os.path.join(designs_dir(root), "log.json"), log)
    print(f"saved {os.path.relpath(dest, root)} and logged '{fp['name']}' ({len(log)} designs in the log)")
    return 0


def cmd_import(root, paths):
    """Add earlier posts' design files (named <date>-<slug>.design.md, as save writes them) to the log. For a
    fresh sandbox with no history: the person attaches the last few design files and this brings them back."""
    log = load_log(root)
    known = {e["slug"] for e in log}
    os.makedirs(designs_dir(root), exist_ok=True)
    added = 0
    for p in paths:
        fp, _, err = common.load_design(p)
        if err:
            print(f"skipped {p}: {err}")
            continue
        base = os.path.basename(p)
        m = re.match(r"^(\d{4}-\d{2}-\d{2})-(.+?)\.design\.md$", base)
        date, slug = (m.group(1), m.group(2)) if m else (dt.date.fromtimestamp(os.path.getmtime(p)).isoformat(),
                                                         re.sub(r"\.design\.md$|\.md$", "", base))
        if slug in known:
            print(f"skipped {base}: '{slug}' is already in the log")
            continue
        dest = os.path.join(designs_dir(root), f"{date}-{slug}.design.md")
        if os.path.abspath(p) != os.path.abspath(dest):
            shutil.copyfile(p, dest)
        log.append({"slug": slug, "date": date, "file": os.path.relpath(dest, root), "fingerprint": fp})
        known.add(slug)
        added += 1
    log.sort(key=lambda e: e["date"])
    common.write_json(os.path.join(designs_dir(root), "log.json"), log)
    print(f"imported {added} design(s); {len(log)} in the log")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["library", "recent", "check", "save", "import"])
    ap.add_argument("arg", nargs="*", help="carousel folder (check, save), N (recent) or design files (import)")
    ap.add_argument("--root", default=os.getcwd(), help="working folder that holds designs/ (default: current folder)")
    a = ap.parse_args()
    if a.command == "library":
        cmd_library(a.root)
    elif a.command == "recent":
        cmd_recent(a.root, int(a.arg[0]) if a.arg else LOOKBACK)
    elif a.command == "check":
        if not a.arg:
            ap.error("check needs a carousel folder")
        sys.exit(cmd_check(a.arg[0]))
    elif a.command == "import":
        if not a.arg:
            ap.error("import needs one or more design files")
        sys.exit(cmd_import(a.root, a.arg))
    else:
        if not a.arg:
            ap.error("save needs a carousel folder")
        sys.exit(cmd_save(a.arg[0]))


if __name__ == "__main__":
    main()
