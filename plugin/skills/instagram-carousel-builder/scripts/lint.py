#!/usr/bin/env python3
"""
lint.py - the checks a carousel can fail without anyone's opinion.

Runs before the rubric judge so the judge cannot talk its way past a hard fact.
Each finding names the rubric line it affects and, through rubric.json "caps",
the highest score that line can get while the finding stands.

Checks
  files        one PNG per slide, each exactly 1080x1350, slide count in range
  words        visible words per slide, cover headline length, dense bodies
  contrast     every colour pair the template uses, WCAG ratio
  render       clipped text, shrink-to-fit, smallest type, fonts that fell back
               (needs render_report.json from render.py; Canva exports skip this)
  brand        fonts and colours inside brand.json, locked vision, handle on
  numbers      every number on a slide must appear in brief.md, stats need a source
  cta          last slide is the ask, says what to do, asks for one thing
  copy         em dashes, stock AI phrasing, brand.json voice "never" list

Usage
  python3 lint.py carousels/<slug>            # writes check/lint.json, prints a summary
  python3 lint.py carousels/<slug> --json     # print the JSON instead
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUBRIC = os.path.join(HERE, "..", "rubric.json")

COPY_FIELDS = ("headline", "sub", "body", "number", "quote", "button")
ACTIONS = {
    "save": ["save", "bookmark", "keep this"],
    "follow": ["follow"],
    "comment": ["comment", "reply", "tell us", "drop a"],
    "share": ["share", "send this", "send it", "send to"],
    "read": ["read", "link in bio", "full breakdown", "full post", "blog", "subscribe", "newsletter"],
    "dm": ["dm ", "dm us", "message us"],
}
SLOP = ["delve", "leverage", "unlock", "unleash", "game-changer", "game changer", "seamless", "robust",
        "elevate", "supercharge", "revolutionize", "revolutionise", "harness", "ever-evolving",
        "fast-paced world", "in today's", "pivotal", "synergy", "empower", "cutting-edge", "next-level",
        "landscape", "journey", "tapestry", "navigate the", "it's not just", "here's the thing"]
SLOP += ["crucial", "testament to", "in the realm of", "it's worth noting", "dive into", "deep dive", "transformative",
         "foster", "meticulous", "embark", "paramount", "furthermore", "moreover", "in conclusion", "stop scrolling",
         "run, don't walk", "the algorithm loves", "you won't believe", "let that sink in", "buckle up", "unlock the power"]
# Machine-written sentence shapes: flagged, not rewritten, because fixing them needs judgement.
AI_PATTERNS = [
    ("'It's not X, it's Y'", re.compile(r"\b(?:it's|it is|this is|that's|that is)\s+not\s+(?:just\s+|only\s+)?[^.;!?]{1,50}?"
                                        r"[,;:]\s*(?:it's|it is|this is|that's|that is)\b", re.IGNORECASE)),
    ("'not only X but also Y'", re.compile(r"\bnot only\b[^.!?]{1,80}\bbut also\b", re.IGNORECASE)),
    ("a one-word question line ('The result?')", re.compile(r"(?:^|[.!?\n]\s*)(?:the\s+|and the\s+|so the\s+)?[A-Za-z']+\?(?=\s|$)", re.IGNORECASE)),
    ("3+ shouted words in a row", re.compile(r"\b[A-Z]{2,}[!?.,]?(?:\s+[A-Z]{2,}[!?.,]?){2,}")),
]
NUMBER_WORDS_RE = re.compile(r"\b(two|three|four|five|six|seven|eight|nine|ten)\s+(?=[a-z])", re.IGNORECASE)
# Invisible characters: zero-width, bidi marks, soft hyphen, BOM, Unicode tags. A keyboard never types them; they ride in on pasted AI text.
INVISIBLE_RE = re.compile("[\u00AD\u061C\u180E\u200B-\u200F\u202A-\u202E\u2060-\u2064\u2066-\u2069\uFEFF\U000E0000-\U000E007F]")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[\w-]+\.(?:com|io|ai|co|dev|app|net|org|in)\b(?:/\S*)?", re.IGNORECASE)
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF\u2600-\u27BF\u2B00-\u2BFF]")
JUNK_TAGS = {"#viral", "#fyp", "#foryou", "#foryoupage", "#explore", "#explorepage", "#trending", "#instagood",
             "#reels", "#likeforlike", "#like4like", "#follow", "#followforfollow", "#follow4follow", "#instadaily", "#viralpost"}
# Engagement bait: prompts that exist to inflate counts. Instagram/Meta demote them (references/engagement-research.md).
BAIT_RE = re.compile(r"\btag\s+(?:a|an|one|two|three|\d+|your|someone|a friend|the friend)\b|\blike\s+(?:this\s+)?if\b|"
                     r"\bshare\s+(?:this\s+)?if\b|\bdouble[- ]tap\b|\bfollow\s+for\s+(?:part|more)\b|"
                     r"\bcomment\s+(?:yes|below if|if you)\b|\btype\s+\S+\s+(?:below|in the comments)\b|\bdrop\s+an?\s+emoji\b",
                     re.IGNORECASE)
BAIT_KEYWORD_RE = re.compile(r"\b(?:[Cc]omment|DM|[Rr]eply)\s+[\"'“‘]?[A-Z]{2,}[\"'”’]?(?:\s|$|[.,!])")  # "comment MOD for the link"
# Self-promotion (gate G8): the post sells us instead of helping the reader.
PROMO_RE = re.compile(r"\bwe help\b|\bbook a (?:call|demo|meeting)\b|\bfree (?:consultation|audit|strategy call)\b|"
                      r"\bdiscovery call\b|\bhire us\b|\bwork with us\b|\bcontact us\b|\bget in touch\b|"
                      r"\bour (?:services|agency|team can)\b|\bbuildable ?labs (?:can|will|helps)\b", re.IGNORECASE)
UNVERIFIED_RE = re.compile(r"test fixture|not real|unverified|needs? verif|verify before|placeholder|\btbd\b|\btk\b|"
                           r"made[- ]up|dummy|fake", re.IGNORECASE)
NUM_RE = re.compile(r"(?<![\w.])(?:[$€£₹]\s?)?\d[\d,]*(?:\.\d+)?\s?(?:%|percent|x\b|k\b|m\b|bn\b|million|billion)?",
                    re.IGNORECASE)


# ---------------------------------------------------------------- utils

def load(path, default=None):
    if not os.path.isfile(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# Brand kit and themes: a brand/brand.json above the carousel (a project's own kit) wins; otherwise this
# skill's bundled assets/ (assets/brand, assets/themes). Carousels themselves live in the working folder.
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


def find_root(start):
    d = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(d, "brand", "brand.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return ASSETS if os.path.isfile(os.path.join(ASSETS, "brand", "brand.json")) else None


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def hex_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def contrast(a, b):
    def lum(h):
        def ch(c):
            c /= 255
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b_ = hex_rgb(h)
        return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b_)
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def plain(t):
    t = str(t or "").replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\*(.+?)\*", r"\1", t)


def words(t):
    return [w for w in plain(t).split() if re.search(r"[A-Za-z0-9]", w)]


def slide_copy(s):
    """Reading copy on a slide (not labels, counters, handle or source line)."""
    parts = [s.get(k) for k in COPY_FIELDS if s.get(k)]
    parts += [it for it in s.get("items") or []]
    return [plain(p) for p in parts]


def visual_text(s):
    """Text drawn inside a slide's visual (UI mockup or diagram). Not counted as reading words, but
    still checked for numbers and voice, because a made-up figure in a mockup is still a claim."""
    out = []
    def walk(x, key=None):
        if isinstance(x, str):
            if key not in ("kind", "icon", "from_icon", "via_icon", "toast_icon", "s"):
                out.append(plain(x))
        elif isinstance(x, list):
            for y in x:
                walk(y, key)
        elif isinstance(x, dict):
            for k, y in x.items():
                if k not in ("hearts", "bar", "tilt", "active"):  # meter values are drawn, not printed
                    walk(y, k)
    walk(s.get("visual") or {})
    return out


def norm_number(tok):
    t = tok.lower().replace(",", "").replace(" ", "")
    t = t.replace("percent", "%").replace("million", "m").replace("billion", "bn")
    return t


def numbers_in(text, keep_small=False):
    out = []
    for m in NUM_RE.finditer(text):
        tok = m.group(0).strip()
        n = norm_number(tok)
        bare = re.fullmatch(r"\d+", n)
        if bare and int(n) <= 10 and not keep_small:
            continue  # counts like "3 steps" are structure, not claims
        out.append((tok, n))
    return out


def evidence_lines(brief, n):
    """Lines of brief.md that contain the normalised number n."""
    return [ln for ln in brief.splitlines() if n in {x for _, x in numbers_in(ln, keep_small=True)}]


# ---------------------------------------------------------------- lint

def search_terms(brief):
    """Phrases listed under '## Search terms' in brief.md (bullets or comma-separated)."""
    m = re.search(r"^##\s*Search terms\s*$(.*?)(?=^##\s|\Z)", brief or "", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    out = []
    for ln in m.group(1).splitlines():
        ln = re.sub(r"^\s*[-*\d.)]+\s*", "", ln).strip().strip('"\'')
        if ln and not ln.startswith(("<!--", ">")):
            out += [t.strip().strip('"\'') for t in ln.split(",") if t.strip()]
    return out


def run(cdir):
    cdir = os.path.abspath(cdir)
    rubric = load(RUBRIC)
    L = rubric["limits"]
    root = find_root(cdir)
    brand = load(os.path.join(root, "brand", "brand.json"), {}) if root else {}
    script = load(os.path.join(cdir, "script.json"))
    vision = load(os.path.join(cdir, "vision.json"), {}) or {}
    report = load(os.path.join(cdir, "render_report.json"))
    brief_path = os.path.join(cdir, "brief.md")
    brief = open(brief_path, encoding="utf-8").read() if os.path.isfile(brief_path) else ""

    findings = []

    gate_of = {lid: g["id"] for g in rubric.get("gates") or [] for lid in g.get("lint") or []}

    def add(fid, sev, msg, slide=None):
        cap = rubric["caps"].get(fid)
        gate = gate_of.get(fid) if sev in ("fatal", "error") else None
        findings.append({"id": fid, "severity": sev, "slide": slide, "message": msg, "gate": gate,
                         "line": cap["line"] if cap else None, "cap": cap["max"] if cap else None})

    if not root:
        add("no_brand", "fatal", "No brand/brand.json above this folder; can't check brand limits.")
    if script is None:
        add("no_script", "fatal", "script.json is missing; nothing to check against.")
        return finish(cdir, rubric, findings, {})

    slides = script.get("slides") or []
    variant = script.get("variant", "standard")
    total = len(slides)
    stats = {"slides": total, "variant": variant, "words": []}

    # files -------------------------------------------------------------
    sdir = os.path.join(cdir, "slides")
    pngs = sorted(f for f in os.listdir(sdir) if re.match(r"^\d+\.(png|jpe?g)$", f, re.I)) if os.path.isdir(sdir) else []
    if len(pngs) != total:
        add("missing_files", "fatal", f"script.json has {total} slides but slides/ has {len(pngs)} image(s). Re-render first.")
    want = tuple(L["slide_size"])
    for f in pngs:
        size = png_size(os.path.join(sdir, f))
        if size != want:
            add("wrong_size", "error", f"{f} is {size}, needs {want[0]}x{want[1]}.", int(re.sub(r'\D', '', f)))
    if total > L["slides_hard_max"]:
        add("too_many_slides", "fatal", f"{total} slides; Instagram allows {L['slides_hard_max']}.")
    if variant == "blog-plug":
        if total != L["blog_plug_slides"]:
            add("blog_plug_count", "warn", f"Blog-plug carousels are {L['blog_plug_slides']} slides (3 explain, 1 sends to the blog); this has {total}.")
    else:
        if total < L["slides_min"]:
            add("too_few_slides", "warn", f"{total} slides; under {L['slides_min']} the swipe rarely builds.")
        elif total > L["slides_max"]:
            add("over_six_slides", "error", f"{total} slides; the house maximum is {L['slides_max']}. Cut or merge slides.")

    # words -------------------------------------------------------------
    for i, s in enumerate(slides, 1):
        n_words = sum(len(words(p)) for p in slide_copy(s))
        stats["words"].append(n_words)
        if n_words > L["words_per_slide_hard"]:
            add("words_way_over", "error", f"{n_words} words; limit {L['words_per_slide']}. This is two slides.", i)
        elif n_words > L["words_per_slide"]:
            add("words_over", "warn", f"{n_words} words; limit {L['words_per_slide']}.", i)
        hl = len(words(s.get("headline")))
        if s.get("type") == "cover":
            if hl > L["cover_words_hard"]:
                add("cover_way_long", "error", f"Cover headline is {hl} words; aim for {L['cover_words']} or fewer.", i)
            elif hl > L["cover_words"]:
                add("cover_long", "warn", f"Cover headline is {hl} words; aim for {L['cover_words']} or fewer.", i)
            if not s.get("alt"):
                add("no_alt", "warn", "Cover has no alt text.", i)
        elif hl > L["headline_words"]:
            add("long_headline", "warn", f"Headline is {hl} words; headlines read best under {L['headline_words']}.", i)
        body = plain(s.get("body"))
        if len([x for x in re.split(r"[.!?]+\s", body) if x.strip()]) > 2:
            add("dense_body", "warn", "Body has 3+ sentences; may be two ideas on one slide.", i)
        if s.get("type") == "image" and s.get("image") and not re.match(r"^[a-z]+:", s["image"]):
            if not os.path.isfile(os.path.join(cdir, s["image"])):
                add("missing_image", "fatal", f"Image not found: {s['image']}", i)

    # contrast ----------------------------------------------------------
    # Prefer what was actually rendered (vision + renderer defaults) over the raw file.
    resolved = (report or {}).get("vision_resolved") or {}
    vlook = {k: resolved.get(k) or vision.get(k) or {} for k in ("colors", "type", "layout")}
    vlook["theme"] = resolved.get("theme") or (vision.get("theme") if vision.get("theme") not in ("dark", "light") else None)
    c = vlook["colors"]
    has_fill = vlook["layout"].get("cta_fill") or any(s.get("fill") for s in slides)
    pairs = [("text", "bg"), ("muted", "bg"), ("accent", "bg")]
    if has_fill:
        pairs.append(("on_fill", "fill"))
    for fg, bg in pairs:
        if c.get(fg) and c.get(bg):
            r = contrast(c[fg], c[bg])
            if r < L["contrast_min"]:
                add("low_contrast", "error", f"{fg} {c[fg]} on {bg} {c[bg]} is {r:.1f}:1; needs {L['contrast_min']}:1.")

    # render ------------------------------------------------------------
    if report:
        for fam, ok in (report.get("fonts_loaded") or {}).items():
            if not ok:
                add("font_fallback", "error", f"'{fam}' did not load; slides rendered in a fallback font.")
        for s in report.get("slides") or []:
            n = s.get("n")
            if s.get("overflow"):
                add("overflow", "error", "Text is clipped even after shrinking to fit.", n)
            elif (s.get("fit") or 1) < L["fit_warn_below"]:
                add("shrunk", "warn", f"Shrunk to {int(s['fit'] * 100)}% to fit; the slide is dense.", n)
            mc = s.get("min_contrast")
            if mc and mc["ratio"] < 3:
                add("low_contrast_text", "error", f"'{mc['text']}' is {mc['ratio']}:1 against its background; "
                    "nothing should be under 3:1 (4.5:1 for secondary text).", n)
            elif mc and mc["ratio"] < L["contrast_min"] and mc["px"] < 48:
                add("low_contrast_text", "warn", f"'{mc['text']}' ({mc['px']}px) is {mc['ratio']}:1; secondary text needs "
                    f"{L['contrast_min']}:1 to read on a phone in daylight.", n)
            lw = s.get("light_weight")
            if lw:
                add("light_weight", "error", f"'{lw['text']}' is set in {lw['family']} at weight {lw['weight']}; light weights "
                    "vanish at phone size. Use 400+ (500+ for body text).", n)
            low = min([x for x in (s.get("min_content_px"), s.get("min_meta_px")) if x] or [99])
            if low < L["min_text_px"] - 0.5:
                add("text_under_min", "error", f"Text down to {low:.0f}px; nothing may be under {L['min_text_px']}px "
                    "(labels and footer included). Cut words rather than shrinking.", n)
        rendered = os.path.getmtime(os.path.join(cdir, "render_report.json"))
        for src in ("script.json", "vision.json"):
            sp = os.path.join(cdir, src)
            if os.path.isfile(sp) and os.path.getmtime(sp) > rendered + 1:
                add("stale_render", "fatal", f"{src} changed after the last render. Re-render before checking.")
        for f in pngs:
            if os.path.getmtime(os.path.join(sdir, f)) < rendered - 600:
                add("stale_render", "fatal", f"slides/{f} is older than the last render. Re-render before checking.")
                break
    else:
        add("no_render_report", "info", "No render_report.json (slides made outside render.py, e.g. Canva). "
            "Clipping, type size and font loading were NOT machine-checked; the judge must look for them.")

    # brand -------------------------------------------------------------
    # A "free" theme (theme.json "brand": "free") is off-brand by design: it is checked against its own
    # palette and fonts, and the judge scores the Brand line as Design (Instagram craft).
    free = resolved.get("brand_mode") == "free"
    bfonts = {e.get("family") for e in (brand.get("fonts") or {}).values() if isinstance(e, dict)}
    bfonts |= {e.get("family") for e in (brand.get("fonts") or {}).get("extra", []) or []}
    bpal = {v.lower() for v in (brand.get("palette") or {}).values()}
    where = "brand.json"
    if free:
        bfonts |= set(resolved.get("theme_fonts") or [])
        bpal |= {str(v).lower() for v in (resolved.get("theme_palette") or {}).values()}
        where = f"brand.json or the '{vlook.get('theme') or resolved.get('theme')}' theme"
        add("free_theme", "info", f"Theme '{resolved.get('theme')}' is off-brand by design. Score the Brand line as "
            "Design: how good the look is for Instagram, not brand match.")
    for role in ("display", "body", "mono"):
        fam = vlook["type"].get(role)
        if fam and bfonts and fam not in bfonts:
            add("font_off_brand", "error", f"{role} font '{fam}' is not in {where}.")
    for k, v in c.items():
        if bpal and v.lower() not in bpal:
            add("colour_off_brand", "warn", f"{k} {v} is not in the {'theme or brand' if free else 'brand'} palette.")
    theme = vision.get("theme") or resolved.get("theme")
    def theme_found(name):
        d = os.path.abspath(cdir)
        while True:
            if os.path.isfile(os.path.join(d, "themes", name, "theme.json")):
                return True
            if os.path.dirname(d) == d:
                break
            d = os.path.dirname(d)
        return any(os.path.isfile(os.path.join(r, "themes", name, "theme.json")) for r in (root, ASSETS))
    if root and theme and not theme_found(theme) and theme != "editorial":
        add("unknown_theme", "error", f"Theme '{theme}' isn't in themes/.")
    if vision.get("status") != "locked":
        add("vision_not_locked", "warn", "vision.json is not locked; the designer hasn't signed off the look.")
    if brand.get("handle") and vlook["layout"].get("handle") is False:
        add("no_handle", "warn", "Handle is switched off; screenshots travel without it.")
    m = vlook["layout"].get("margin")
    if m is not None and m < L["margin_min"]:
        add("tight_margin", "warn", f"Margin {m}px; under {L['margin_min']}px text risks the grid crop.")

    # numbers -----------------------------------------------------------
    brief_nums = {n for _, n in numbers_in(brief, keep_small=True)}
    for i, s in enumerate(slides, 1):
        found = numbers_in(" ".join(slide_copy(s) + visual_text(s)))
        if s.get("type") == "stat" or s.get("number"):
            found += numbers_in(str(s.get("number") or ""), keep_small=True)  # a headline number is always a claim
        for tok, n in dict((n, (tok, n)) for tok, n in found).values():
            if n not in brief_nums:
                add("unsourced_number", "error", f"'{tok}' is not in brief.md's evidence. Source it or cut it.", i)
                continue
            lines = evidence_lines(brief, n)
            if lines and all(UNVERIFIED_RE.search(ln) for ln in lines):
                add("unverified_evidence", "error", f"'{tok}' comes from evidence the brief marks as unverified "
                    "or test data. It can't go on a slide.", i)
        if s.get("type") == "stat" and not s.get("source"):
            add("stat_without_source", "error", "Stat slide has no source line.", i)
    if not brief:
        add("no_brief", "warn", "No brief.md, so numbers couldn't be traced to evidence.")

    # cta ---------------------------------------------------------------
    last = slides[-1] if slides else {}
    if last.get("type") != "cta":
        add("no_cta", "error", "The last slide is not a CTA slide.", total)
    else:
        text = " ".join(slide_copy(last)).lower() + " " + str(last.get("action") or "")
        hits = {k for k, keys in ACTIONS.items()
                if any(re.search(r"\b" + re.escape(key.strip()) + r"\b", text) for key in keys)}
        if not hits:
            add("cta_no_action", "error", "The CTA doesn't say what to do (save, follow, comment, read...).", total)
        elif len(hits) > 1:
            add("cta_many_asks", "warn", f"The CTA asks for {len(hits)} things ({', '.join(sorted(hits))}). Pick one.", total)
        if variant == "blog-plug" and "read" not in hits:
            add("blog_plug_no_link", "warn", "Blog-plug CTA should send people to the blog (link in bio).", total)

    # copy --------------------------------------------------------------
    never = [w.lower() for w in ((brand.get("voice") or {}).get("never") or [])]
    for i, s in enumerate(slides, 1):
        hits = [w for w in never if w in " ".join(slide_copy(s) + visual_text(s)).lower()]
        if hits:
            add("brand_voice", "warn", "Brand voice 'never' list: " + ", ".join(hits), i)
    for i, s in enumerate(slides, 1):
        text = " ".join(slide_copy(s) + visual_text(s))
        if "—" in text or " – " in text:
            add("em_dash", "warn", "Em/en dash in copy; reads as machine-written. Use a comma or a full stop.", i)
        low = text.lower()
        hits = [w for w in SLOP if w in low]
        if hits:
            add("stock_phrasing", "warn", "Stock phrasing: " + ", ".join(hits), i)
        tells = [name for name, rx in AI_PATTERNS if any(rx.search(t) for t in slide_copy(s) + visual_text(s))]
        if tells:
            add("ai_pattern", "warn", "Reads machine-written: " + "; ".join(tells) + ". Rewrite the line in your own words.", i)
        m = NUMBER_WORDS_RE.search(" ".join(slide_copy(s) + visual_text(s)))
        if m:
            add("number_words", "warn", f"'{m.group(0).strip()} ...': use numerals on slides ('3 steps', not 'three steps'); "
                "they read faster in the feed.", i)
        if INVISIBLE_RE.search(text + " " + (s.get("alt") or "")):
            add("invisible_chars", "error", "Invisible characters (zero-width, bidi or tag characters) in the copy. Delete them.", i)
    # caption ---------------------------------------------------------------------------
    cap_path = os.path.join(cdir, "caption.md")
    caption = open(cap_path, encoding="utf-8").read().strip() if os.path.isfile(cap_path) else None
    if caption is None:
        add("no_caption", "error", "No caption.md. The caption is part of the post: first line as a second hook, one ask, 3-5 hashtags.")
    else:
        stats["caption_chars"] = len(caption)
        if len(caption) > L["caption_max_chars"]:
            add("caption_too_long", "error", f"Caption is {len(caption)} characters; Instagram's limit is {L['caption_max_chars']}.")
        first = next((ln.strip() for ln in caption.splitlines() if ln.strip()), "")
        if len(first) > L["caption_hook_chars"]:
            add("caption_hook_long", "warn", f"Caption line 1 is {len(first)} characters; the feed cuts at about "
                f"{L['caption_hook_chars']} ('...more'), so the hook gets truncated.")
        if slides and plain(first).lower().strip(" .") == plain(slides[0].get("headline")).lower().strip(" ."):
            add("caption_repeats_cover", "info", "Caption line 1 repeats the cover word for word. A second hook gives non-swipers another reason.")
        tags = re.findall(r"(?<!\w)#\w+", caption)
        if len(tags) > L["hashtags_max"]:
            add("hashtags_many", "warn", f"{len(tags)} hashtags; use 3-{L['hashtags_max']} precise ones.")
        elif not tags:
            add("no_hashtags", "info", "No hashtags. Add 3-5 precise ones so Instagram can classify the post.")
        body = re.sub(r"(?<!\w)#\w+", "", caption)
        words_n = len(words(body))
        stats["caption_words"] = words_n
        if words_n > L["caption_words_max"]:
            add("caption_long", "info", f"Caption body is {words_n} words. Long captions work only when every line earns it.")
        low = body.lower()
        asks = {k for k, keys in ACTIONS.items() if any(re.search(r"\b" + re.escape(key.strip()) + r"\b", low) for key in keys)}
        if len(asks) > 1:
            add("caption_many_asks", "warn", f"Caption asks for {len(asks)} things ({', '.join(sorted(asks))}). Keep one ask.")
        for tok, n in dict((n, (tok, n)) for tok, n in numbers_in(body)).values():
            if n not in brief_nums:
                add("unsourced_number", "error", f"Caption: '{tok}' is not in brief.md's evidence. Source it or cut it.")
        hits = [w for w in never if w in low]
        if hits:
            add("brand_voice", "warn", "Caption uses the brand voice 'never' list: " + ", ".join(hits))
        hits = [w for w in SLOP if w in low]
        if hits:
            add("stock_phrasing", "warn", "Caption stock phrasing: " + ", ".join(hits))
        if "—" in body or " – " in body:
            add("em_dash", "warn", "Em/en dash in the caption; use a comma or a full stop.")
        stats["caption_preview"] = first[:L["caption_hook_chars"]]
        if INVISIBLE_RE.search(caption):
            add("invisible_chars", "error", "Invisible characters (zero-width, bidi or tag characters) in the caption. Delete them.")
        if re.match(r"\s*(?:#|[\U0001F300-\U0001FAFF\u2600-\u27BF]|(?:hey|hi|hello)\b)", first, re.IGNORECASE):
            add("caption_weak_opener", "warn", "Caption line 1 opens with a hashtag, an emoji or a greeting. Open with the hook.")
        m = LINK_RE.search(body)
        if m:
            add("caption_link", "error", f"Link in the caption ('{m.group(0)}'). Caption links aren't clickable; say 'link in bio' instead.")
        emo = len(EMOJI_RE.findall(caption))
        if emo and emo / max(len(caption), 1) * 100 > 4:
            add("caption_emoji", "warn", f"{emo} emoji in {len(caption)} characters; use them as punctuation, not decoration (4 per 100 max).")
        junk = sorted({t.lower() for t in tags} & JUNK_TAGS)
        if junk:
            add("hashtag_junk", "warn", "Hashtags that describe nothing: " + ", ".join(junk) + ". Use topic labels people search.")
        tells = [name for name, rx in AI_PATTERNS if rx.search(body)]
        if tells:
            add("ai_pattern", "warn", "Caption reads machine-written: " + "; ".join(tells) + ".")
        if brief and not re.search(r"^##\s*Story\s*$[\s\S]*?\b(PAS|PPP)\b", brief, re.MULTILINE | re.IGNORECASE):
            add("no_story_framework", "info", "brief.md has no '## Story' naming PAS or PPP. Pick one (references/script.md "
                "§3): PAS when readers underestimate the problem, PPP when they doubt the fix.")
        terms = search_terms(brief)
        if terms is None:
            add("no_search_terms", "info", "brief.md has no '## Search terms'. List 2-3 phrases people would type into "
                "Instagram search, so the caption and alt text can carry them.")
        else:
            missing = [t for t in terms if t.lower() not in low]
            if missing:
                add("search_term_missing", "warn", "Search terms not in the caption as plain words: " + ", ".join(missing)
                    + ". Instagram search reads the caption; hashtags don't count.")
            alts = " ".join((s.get("alt") or "") for s in slides).lower()
            if terms and not any(t.lower() in alts for t in terms):
                add("search_term_alt", "info", "None of the search terms appear in the alt text.")

    # engagement bait (slides and caption) ------------------------------------------------
    for i, s in enumerate(slides, 1):
        txt = " ".join(slide_copy(s) + visual_text(s))
        if BAIT_RE.search(txt) or BAIT_KEYWORD_RE.search(txt):
            add("engagement_bait", "error", "Engagement bait on the slide (tag/comment-a-word/like-if). Ask for one honest action instead.", i)
    if caption and (BAIT_RE.search(caption) or BAIT_KEYWORD_RE.search(caption)):
        m = BAIT_RE.search(caption) or BAIT_KEYWORD_RE.search(caption)
        add("engagement_bait", "error", f"Engagement bait in the caption ('{m.group(0).strip()}'). Instagram demotes it; ask for one honest action.")

    # house rules ------------------------------------------------------------------------
    if vlook["layout"].get("counter"):
        add("slide_numbers", "error", "The slide counter is on (layout.counter). No slide or page numbers on slides.")
    for i, s in enumerate(slides, 1):
        txt = " ".join(slide_copy(s) + visual_text(s))
        m = PROMO_RE.search(txt)
        if m:
            add("self_promo", "error", f"Self-promotion on the slide ('{m.group(0)}'). Help the reader; don't sell us.", i)
    if caption and PROMO_RE.search(caption):
        add("self_promo", "error", f"Self-promotion in the caption ('{PROMO_RE.search(caption).group(0)}').")

    # engagement: a run of text-only slides reads as a wall of words in the feed ------------------
    def has_visual(s):
        return bool(s.get("visual") or s.get("image") or s.get("number") or s.get("type") in ("stat", "quote"))
    # gate G1: a real visual on every slide (the judge also checks it isn't just decoration)
    for i, s in enumerate(slides, 1):
        if not (s.get("visual") or s.get("image") or s.get("number")):
            add("slide_no_visual", "error", "No visual on this slide. Every slide needs one (window, hud, flow, slots, "
                "dialog, funnel, tags, compare, chart, timeline, an image or a big sourced number); slide 1 needs an infographic.", i)
    return finish(cdir, rubric, findings, stats)


def finish(cdir, rubric, findings, stats):
    caps = {}
    for f in findings:
        if f["line"] and f["cap"] is not None:
            caps[f["line"]] = min(caps.get(f["line"], 5), f["cap"])
    order = {"fatal": 0, "error": 1, "warn": 2, "info": 3}
    findings.sort(key=lambda f: (order[f["severity"]], f["slide"] or 0))
    gates = {}
    for f in findings:
        if f.get("gate"):
            gates.setdefault(f["gate"], []).append((f"slide {f['slide']}: " if f["slide"] else "") + f["message"])
    out = {
        "rubric_version": rubric["version"],
        "gates_failed": gates,
        "counts": {k: sum(1 for f in findings if f["severity"] == k) for k in order},
        "caps": caps,
        "stats": stats,
        "findings": findings,
    }
    os.makedirs(os.path.join(cdir, "check"), exist_ok=True)
    with open(os.path.join(cdir, "check", "lint.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return out


def summary(out):
    c = out["counts"]
    lines = [f"lint: {c['fatal']} fatal, {c['error']} error, {c['warn']} warn, {c['info']} info"]
    for f in out["findings"]:
        where = f"slide {f['slide']:02d}" if f["slide"] else "carousel"
        cap = f"  [caps {f['line']} at {f['cap']}]" if f["cap"] is not None else ""
        gate = f"  [GATE {f['gate']}]" if f.get("gate") else ""
        lines.append(f"  {f['severity'].upper():5} {where:9} {f['message']}{cap}{gate}")
    if out.get("gates_failed"):
        lines.append("gates failed: " + ", ".join(sorted(out["gates_failed"], key=lambda g: int(g[1:]))) + "  (any failed gate blocks a pass)")
    prev = (out.get("stats") or {}).get("caption_preview")
    if prev:
        lines.append(f"feed shows before '...more': | {prev} |")
    if out["caps"]:
        lines.append("caps: " + ", ".join(f"{k} <= {v}" for k, v in out["caps"].items()))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Hard checks for a rendered carousel.")
    ap.add_argument("carousel")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run(args.carousel)
    print(json.dumps(out, indent=2, ensure_ascii=False) if args.json else summary(out))
    sys.exit(2 if out["counts"]["fatal"] else 0)


if __name__ == "__main__":
    main()
