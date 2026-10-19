#!/usr/bin/env python3
"""
fonts.py - make the slides' web fonts load where Google Fonts is blocked (the claude.ai chat sandbox).

slides.html names its fonts with one Google Fonts <link>. render.py and export_pdf.py call prepare() before
loading the page and apply() after it. When Google Fonts can't be reached, or a family didn't load, apply()
injects @font-face rules that point at local copies of the same families:

  1. assets/fonts/<slug>/   bundled with the skill (Manrope and JetBrains Mono, the two fixed fonts)
  2. the font cache         ~/.cache/carousel-fonts/<slug>/ (or $CAROUSEL_FONT_CACHE)
  3. npm                    `npm pack @fontsource/<slug>`, the same files Google serves; the result is cached

CAROUSEL_FONTS=web skips all of this, CAROUSEL_FONTS=local forces it (no network probe).
Run `python3 fonts.py <slides.html>` to see which families a page needs and where each one comes from.
"""

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLED = os.path.join(os.path.dirname(HERE), "assets", "fonts")
BLOCK = ["*fonts.googleapis.com*", "*fonts.gstatic.com*"]


def families(html_text):
    """Family names requested from Google Fonts by <link> or @import, in order, without repeats."""
    out = []
    for m in re.finditer(r"fonts\.googleapis\.com/css2?\?([^\"'\s)]+)", html_text or ""):
        for part in re.findall(r"family=([^&:\"'\s]+)", m.group(1)):
            name = urllib.parse.unquote_plus(part).strip()
            if name and name not in out:
                out.append(name)
    return out


def slug(family):
    return re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")


def cache_root():
    root = os.environ.get("CAROUSEL_FONT_CACHE") or os.path.join(os.path.expanduser("~"), ".cache", "carousel-fonts")
    try:
        os.makedirs(root, exist_ok=True)
        if os.access(root, os.W_OK):
            return root
    except OSError:
        pass
    root = os.path.join(tempfile.gettempdir(), "carousel-fonts")
    os.makedirs(root, exist_ok=True)
    return root


def _has_faces(d, s):
    rx = re.compile(rf"^{re.escape(s)}-latin-(\d+|wght)-(normal|italic)\.woff2$")
    return os.path.isdir(d) and any(rx.match(f) for f in os.listdir(d))


def _npm_fetch(pkg, s, dest):
    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        return False
    with tempfile.TemporaryDirectory() as tmp:
        try:
            subprocess.run([npm, "pack", pkg, "--silent"], cwd=tmp, capture_output=True, text=True, timeout=120)
            tgz = [f for f in os.listdir(tmp) if f.endswith(".tgz")]
            if not tgz:
                return False
            with tarfile.open(os.path.join(tmp, tgz[0])) as tf:
                try:
                    tf.extractall(tmp, filter="data")
                except TypeError:  # Python < 3.12
                    tf.extractall(tmp)
            files = os.path.join(tmp, "package", "files")
            os.makedirs(dest, exist_ok=True)
            for f in os.listdir(files):
                if re.match(rf"^{re.escape(s)}-latin-(\d+|wght)-(normal|italic)\.woff2$", f):
                    shutil.copy(os.path.join(files, f), dest)
        except Exception:  # noqa: BLE001 - any failure just means "not available"
            return False
    return _has_faces(dest, s)


def locate(family):
    """(folder, source) holding the family's latin woff2 files, or (None, reason)."""
    s = slug(family)
    if _has_faces(os.path.join(BUNDLED, s), s):
        return os.path.join(BUNDLED, s), "bundled"
    dest = os.path.join(cache_root(), s)
    if _has_faces(dest, s):
        return dest, "cache"
    for pkg in (f"@fontsource/{s}", f"@fontsource-variable/{s}"):
        if _npm_fetch(pkg, s, dest):
            return dest, "npm"
    return None, "not found (no copy on disk and npm could not fetch it)"


def font_css(family, folder):
    """@font-face rules for every latin face in folder."""
    s = slug(family)
    rules = []
    for f in sorted(os.listdir(folder)):
        m = re.match(rf"^{re.escape(s)}-latin-(\d+|wght)-(normal|italic)\.woff2$", f)
        if not m:
            continue
        weight = "100 900" if m.group(1) == "wght" else m.group(1)
        url = "file://" + urllib.parse.quote(os.path.join(folder, f))
        rules.append("@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:block;"
                     "src:url('%s') format('woff2');}" % (family, m.group(2), weight, url))
    return "\n".join(rules)


def _reachable():
    try:
        socket.create_connection(("fonts.googleapis.com", 443), timeout=3).close()
        return True
    except OSError:
        return False


def prepare(browser, sid, html_path):
    """Call before loading the page. Returns True when Google Fonts is out of reach (and blocked, so the page
    fails fast instead of hanging on the <link>)."""
    mode = os.environ.get("CAROUSEL_FONTS", "auto")
    if mode == "web":
        return False
    offline = mode == "local" or not _reachable()
    if offline:
        browser.send("Network.enable", session=sid)
        browser.send("Network.setBlockedURLs", {"urls": BLOCK}, sid)
    return offline


def apply(browser, sid, html_path, offline):
    """Call after loading the page. Injects local @font-face rules for every family that didn't load.
    Returns the families it could not provide."""
    with open(html_path, encoding="utf-8") as f:
        fams = families(f.read())
    if not fams:
        return []
    if offline:
        todo = fams
    else:
        ok = browser.js(sid, "Promise.all(%s.map(f => document.fonts.load('16px \"' + f + '\"')"
                             ".then(r => r.length > 0).catch(() => false)))" % json.dumps(fams))
        todo = [f for f, loaded in zip(fams, ok) if not loaded]
    css, missing = [], []
    for fam in todo:
        folder, why = locate(fam)
        if folder:
            css.append(font_css(fam, folder))
        else:
            missing.append(fam)
    if css:
        browser.js(sid, "(async () => { const s = document.createElement('style'); s.textContent = %s;"
                        " document.head.appendChild(s);"
                        " await Promise.all(%s.map(f => document.fonts.load('16px \"' + f + '\"').catch(() => 0)));"
                        " return 1; })()" % (json.dumps("\n".join(css)), json.dumps(todo)), 120)
    return missing


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: fonts.py slides.html")
    names = families(open(sys.argv[1], encoding="utf-8").read())
    print("fonts requested:", ", ".join(names) or "(none)")
    for n in names:
        d, why = locate(n)
        print(f"  {n}: {why}" + (f"  {d}" if d else ""))
