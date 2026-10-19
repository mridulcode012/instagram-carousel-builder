"""
common.py - small helpers shared by the carousel scripts: paths, JSON, and reading design.md files.

A design.md (library spec, per-post design or saved design) starts with a fenced ```json block, the
fingerprint, followed by the spec in prose. See references/design-system.md.
"""

import datetime as dt
import json
import os
import re

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL, "assets")
LIBRARY = os.path.join(ASSETS, "designs")
W, H = 1080, 1350


def load_json(path, default=None):
    if not os.path.isfile(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def now():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def find_brand_root(start):
    """Folder holding brand/brand.json: a project's own kit above the carousel wins, else the skill's assets/."""
    d = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(d, "brand", "brand.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return ASSETS if os.path.isfile(os.path.join(ASSETS, "brand", "brand.json")) else None


def load_brand(start):
    root = find_brand_root(start)
    return load_json(os.path.join(root, "brand", "brand.json"), {}) if root else {}


def work_root(cdir):
    """The working folder a carousel belongs to: the parent of carousels/, else the carousel's parent."""
    cdir = os.path.abspath(cdir)
    parent = os.path.dirname(cdir)
    if os.path.basename(parent) == "carousels":
        return os.path.dirname(parent)
    return parent


FENCE_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def parse_design(text):
    """(fingerprint dict or None, error message or None) from a design.md's text."""
    m = FENCE_RE.search(text or "")
    if not m:
        return None, "no ```json fingerprint block"
    try:
        fp = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        return None, f"fingerprint is not valid JSON ({e})"
    if not isinstance(fp, dict):
        return None, "fingerprint is not a JSON object"
    return fp, None


def load_design(path):
    """(fingerprint, text, error) for a design.md path. Missing file -> (None, '', 'missing')."""
    if not os.path.isfile(path):
        return None, "", "missing"
    text = open(path, encoding="utf-8").read()
    fp, err = parse_design(text)
    return fp, text, err


def design_title(text):
    m = re.search(r"^#\s+(.+)$", text or "", re.MULTILINE)
    return m.group(1).strip() if m else ""


def design_look(text):
    """First paragraph under '## Look'."""
    m = re.search(r"^##\s+Look\s*$\n+(.+?)(?:\n\s*\n|\n##|\Z)", text or "", re.MULTILINE | re.DOTALL)
    return " ".join(m.group(1).split()) if m else ""


def hex_rgb(h):
    h = str(h).strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
