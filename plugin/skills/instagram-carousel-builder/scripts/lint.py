#!/usr/bin/env python3
"""
lint.py - the checks a carousel can fail without anyone's opinion.

Runs before the rubric judge so the judge cannot talk its way past a hard fact.
Each finding names the rubric line it affects and, through rubric.json "caps",
the highest score that line can get while the finding stands.

Checks
  files        one PNG per slide, each exactly 1080x1350, slide count in range
  words        visible words per slide (script.json), cover headline length, dense bodies
  render       what render.py measured in slides.html: clipped text, overlaps, text under 34px, light weights,
               contrast, highlight blocks touching lines, text above the headline, footer, fonts that fell back
  design       design.md exists and is valid, and differs from the last 5 designs (design_log.py)
  numbers      every number on a slide must appear in brief.md, stats need a source
  cta          last slide is the ask, says what to do, asks for one thing
  copy         em dashes, stock AI phrasing, machine-written shapes, brand.json voice "never" list
  caption      length, first line, hashtags, search terms, bait, links

Usage
  python3 lint.py carousels/<slug>            # writes check/lint.json, prints a summary
  python3 lint.py carousels/<slug> --json     # print the JSON instead
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import design_log  # noqa: E402

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


def _stem(w):
    return re.sub(r"(ing|ed|es|s)$", "", w) if len(w) > 4 else w


def term_in(term, text):
    """A search term is in the text as the exact phrase, or with every one of its words present (stemmed, any order)."""
    t, low = term.lower().strip(), text.lower()
    if t in low:
        return True
    have = {_stem(w) for w in re.findall(r"[a-z0-9']+", low)}
    return all(_stem(w) in have for w in re.findall(r"[a-z0-9']+", t))


def run(cdir):
    cdir = os.path.abspath(cdir)
    rubric = load(RUBRIC)
    L = rubric["limits"]
    root = find_root(cdir)
    brand = load(os.path.join(root, "brand", "brand.json"), {}) if root else {}
    script = load(os.path.join(cdir, "script.json"))
    report = load(os.path.join(cdir, "render_report.json"))
    brief_path = os.path.join(cdir, "brief.md")
    brief = open(brief_path, encoding="utf-8").read() if os.path.isfile(brief_path) else ""

    findings = []
    W_, H_ = L["slide_size"]
    _rs = (report or {}).get("slides") or []

    def vtext(i, s):
        """Every readable string the browser drew on slide i (visual labels included), minus the footer and decoration.
        A made-up figure inside a mockup is still a claim, so numbers and voice are checked on all of it."""
        if i - 1 < len(_rs):
            return [plain(t["t"]) for t in _rs[i - 1].get("texts") or [] if not t.get("foot") and not t.get("decor")]
        return []

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

    # render ------------------------------------------------------------
    # render.py measured the real layout of slides.html; every check below is on what the browser drew.
    rep_slides = (report or {}).get("slides") or []
    if report:
        for fnt in report.get("fonts") or []:
            if fnt.get("status") in ("failed", "missing"):
                add("font_fallback", "error", f"'{fnt['family']}' did not load; slides rendered in a fallback font.")
        for pr in report.get("problems") or []:
            add("render_problem", "warn", pr)
        for s_ in rep_slides:
            n = s_["n"]
            sz = s_.get("size") or {}
            if abs(sz.get("w", W_) - W_) > 0.6 or abs(sz.get("h", H_) - H_) > 0.6:
                add("wrong_size", "error", f".slide is {sz.get('w')}x{sz.get('h')}, needs {W_}x{H_}.", n)
            if (s_.get("headline") or {}).get("count") != 1:
                add("headline_count", "error", f"{(s_.get('headline') or {}).get('count')} .headline elements; every slide has exactly one.", n)
            if s_.get("above_headline"):
                add("text_above_headline", "error", "Text above the headline ('" + "', '".join(s_["above_headline"][:2]) +
                    "'). The headline is the first text on a slide: no kicker, eyebrow or label above it.", n)
            site = (s_.get("footer") or {}).get("site") or ""
            if "BUILDABLELABS.COM" not in site.upper():
                add("no_footer", "error", "Footer BUILDABLELABS.COM is missing.", n)
            elif (s_["footer"].get("site_box") or {}).get("y", 0) < 1350 * 0.7:
                add("footer_position", "warn", "The footer sits in the top 70% of the slide; keep it at the bottom.", n)
            if n < total and not (s_.get("footer") or {}).get("cue"):
                add("no_swipe_cue", "warn", "No swipe cue (.foot .cue) on a slide that isn't the last.", n)
            if s_.get("clipped"):
                c0 = s_["clipped"][0]
                add("overflow", "error", f"Text is clipped or off the slide ('{c0['text']}': {c0['why']}).", n)
            if s_.get("overlaps"):
                o = s_["overlaps"][0]
                add("text_overlap", "error", f"Text overlaps text ('{o['a']}' and '{o['b']}', {o['w']}x{o['h']}px).", n)
            if s_.get("text_over_visual"):
                add("text_overlap", "error", "Text sits on top of the visual ('" + "', '".join(s_["text_over_visual"][:2]) + "').", n)
            if s_.get("highlight_touch"):
                h0 = s_["highlight_touch"][0]
                add("highlight_touch", "error", f"The highlight block '{h0['block']}' touches the line around it (gap {h0['gap']}px); "
                    "give it 8px+ with a larger headline line-height.", n)
            mc = s_.get("min_contrast")
            if mc and mc["ratio"] < 3:
                add("low_contrast_text", "error", f"'{mc['text']}' is {mc['ratio']}:1 against its background; "
                    "nothing should be under 3:1 (4.5:1 for text under 48px).", n)
            elif mc and mc["ratio"] < L["contrast_min"] and mc["px"] < 48:
                add("low_contrast_text", "warn", f"'{mc['text']}' ({mc['px']}px) is {mc['ratio']}:1; "
                    f"secondary text needs {L['contrast_min']}:1 to read on a phone in daylight.", n)
            lw = s_.get("light_weight")
            if lw:
                add("light_weight", "error", f"'{lw['text']}' is set in {lw['family']} at weight {lw['weight']}; light weights "
                    "vanish at phone size. Use 400+ (500+ for body text).", n)
            if s_.get("small_text"):
                t0 = s_["small_text"][0]
                add("text_under_min", "error", f"Text down to {t0['px']:.0f}px ('{t0['text']}'); nothing may be under "
                    f"{L['min_text_px']}px (labels, diagram text and footer included, SVG text as drawn). Cut words rather than shrinking.", n)
            if (s_.get("empty") or {}).get("pct", 0) > 30:
                e0 = s_["empty"]
                add("dead_space", "warn", f"An empty block of {e0['w']}x{e0['h']}px ({e0['pct']}% of the slide) at x{e0['x']},y{e0['y']}. "
                    "Decoration may fill it; if it reads as a gap, enlarge the visual (gate G2).", n)
            sc = (s_.get("visual") or {}).get("svg_scale")
            if sc is not None and sc < 0.95:
                add("svg_scaled", "warn", f"The visual's SVG is drawn bigger than its box and shrunk to {sc:.2f}x, so its text is smaller than it looks "
                    f"in the source. Redraw it with the viewBox equal to the box ({(s_['visual'].get('box') or {}).get('w')}x{(s_['visual'].get('box') or {}).get('h')}).", n)
            for dg in s_.get("big_digits") or []:
                add("ghost_numeral", "warn", f"A lone {dg['px']:.0f}px numeral '{dg['text']}' outside the headline reads as a giant slide number (gate G7).", n)
            for tx in s_.get("texts") or []:
                if re.fullmatch(r"\s*0\d\s*", tx["t"]) or re.fullmatch(r"\s*\d{1,2}\s*(/|of)\s*\d{1,2}\s*", tx["t"]):
                    add("slide_numbers", "error", f"'{tx['t']}' reads as a slide or page number. Use letters or glyphs for list marks.", n)
                    break
        rendered = os.path.getmtime(os.path.join(cdir, "render_report.json"))
        sh = os.path.join(cdir, "slides.html")
        if os.path.isfile(sh) and os.path.getmtime(sh) > rendered + 1:
            add("stale_render", "fatal", "slides.html changed after the last render. Re-render before checking.")
        for f in pngs:
            if os.path.getmtime(os.path.join(sdir, f)) < rendered - 600:
                add("stale_render", "fatal", f"slides/{f} is older than the last render. Re-render before checking.")
                break
    else:
        add("no_render_report", "info", "No render_report.json (slides made outside render.py, e.g. Canva). "
            "Clipping, type size and font loading were NOT machine-checked; the judge must look for them.")

    # design ------------------------------------------------------------
    dfp, _, derr = common.load_design(os.path.join(cdir, "design.md"))
    if derr:
        add("no_design", "error", f"design.md: {derr}. Every carousel starts from its own design.md (references/design-system.md).")
    else:
        derrs, dnotes = design_log.validate(dfp)
        for e_ in derrs:
            add("design_invalid", "error", "design.md fingerprint: " + e_ + ".")
        for n_ in dnotes:
            add("design_vocab", "info", "design.md: " + n_ + ".")
        if not derrs:
            ok_, rows_, _, _, _ = design_log.check(cdir)
            if rows_ and not ok_:
                worst = min(rows_, key=lambda r: r[2])
                same = [d for d in design_log.DIMS if worst[1][d]]
                add("design_repeat", "error", f"The design is too close to '{worst[0]['slug']}' (differs on {worst[2]} of 7, needs "
                    f"{design_log.MIN_DIFFERENT}); same on: {', '.join(same)}. Change those and run design_log.py check.")
            elif rows_ and (dfp["kind"] == "reference" or dfp.get("reuse")) and min(r[2] for r in rows_) < design_log.MIN_DIFFERENT:
                add("design_repeat_ref", "info", "This reference or reused design resembles a recent post; allowed, because the person chose it.")
            if report and dfp["kind"] != "reference":
                allowed = {"manrope", "jetbrains mono", str(dfp["fonts"].get("display", "")).lower(), str(dfp["fonts"].get("display2", "")).lower()}
                stray = sorted(f_["family"] for f_ in report.get("fonts") or [] if f_["family"].lower() not in allowed)
                if stray:
                    add("font_off_system", "error", "Fonts outside the fixed set were used: " + ", ".join(stray) + ". Body is Manrope, labels "
                        "JetBrains Mono; only the display font (fonts.display, optionally fonts.display2) may differ.")
            if report:
                used = {f_["family"].lower() for f_ in report.get("fonts") or []}
                want = str((dfp.get("fonts") or {}).get("display", "")).lower()
                if want and used and want not in used:
                    add("design_font_unused", "warn", f"design.md names display font '{dfp['fonts']['display']}' but the render never used it.")

    # numbers -----------------------------------------------------------
    brief_nums = {n for _, n in numbers_in(brief, keep_small=True)}
    for i, s in enumerate(slides, 1):
        found = numbers_in(" ".join(slide_copy(s) + vtext(i, s)))
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
        hits = [w for w in never if w in " ".join(slide_copy(s) + vtext(i, s)).lower()]
        if hits:
            add("brand_voice", "warn", "Brand voice 'never' list: " + ", ".join(hits), i)
    for i, s in enumerate(slides, 1):
        text = " ".join(slide_copy(s) + vtext(i, s))
        if "—" in text or " – " in text:
            add("em_dash", "warn", "Em/en dash in copy; reads as machine-written. Use a comma or a full stop.", i)
        low = text.lower()
        hits = [w for w in SLOP if w in low]
        if hits:
            add("stock_phrasing", "warn", "Stock phrasing: " + ", ".join(hits), i)
        tells = [name for name, rx in AI_PATTERNS if any(rx.search(t) for t in slide_copy(s) + vtext(i, s))]
        if tells:
            add("ai_pattern", "warn", "Reads machine-written: " + "; ".join(tells) + ". Rewrite the line in your own words.", i)
        m = NUMBER_WORDS_RE.search(" ".join(slide_copy(s) + vtext(i, s)))
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
        # the one ask lives in the last paragraph (references/caption.md); earlier paragraphs may use the same words as plain prose
        paras = [p_ for p_ in re.split(r"\n\s*\n", body) if p_.strip()]
        ask_text = paras[-1].lower() if paras else low
        asks = {k for k, keys in ACTIONS.items() if any(re.search(r"\b" + re.escape(key.strip()) + r"\b", ask_text) for key in keys)}
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
            missing = [t for t in terms if not term_in(t, low)]
            if missing:
                add("search_term_missing", "warn", "Search terms not in the caption as plain words: " + ", ".join(missing)
                    + ". Instagram search reads the caption; hashtags don't count.")
            alts = " ".join((s.get("alt") or "") for s in slides).lower()
            if terms and not any(term_in(t, alts) for t in terms):
                add("search_term_alt", "info", "None of the search terms appear in the alt text.")

    # engagement bait (slides and caption) ------------------------------------------------
    for i, s in enumerate(slides, 1):
        txt = " ".join(slide_copy(s) + vtext(i, s))
        if BAIT_RE.search(txt) or BAIT_KEYWORD_RE.search(txt):
            add("engagement_bait", "error", "Engagement bait on the slide (tag/comment-a-word/like-if). Ask for one honest action instead.", i)
    if caption and (BAIT_RE.search(caption) or BAIT_KEYWORD_RE.search(caption)):
        m = BAIT_RE.search(caption) or BAIT_KEYWORD_RE.search(caption)
        add("engagement_bait", "error", f"Engagement bait in the caption ('{m.group(0).strip()}'). Instagram demotes it; ask for one honest action.")

    # house rules ------------------------------------------------------------------------
    for i, s in enumerate(slides, 1):
        txt = " ".join(slide_copy(s) + vtext(i, s))
        m = PROMO_RE.search(txt)
        if m:
            add("self_promo", "error", f"Self-promotion on the slide ('{m.group(0)}'). Help the reader; don't sell us.", i)
    if caption and PROMO_RE.search(caption):
        add("self_promo", "error", f"Self-promotion in the caption ('{PROMO_RE.search(caption).group(0)}').")

    # gate G1: a real visual on every slide (the judge also checks it isn't just decoration)
    for i, s in enumerate(slides, 1):
        if report and i - 1 < len(_rs):
            has = _rs[i - 1]["visual"]["count"] > 0
            cover = _rs[i - 1]["visual"]["pct"]
            if has and cover < 35:
                add("visual_small", "warn", f"The visual box covers {cover:.0f}% of the slide; aim for 40-60% (enlarge the drawing or trim the copy).", i)
        else:
            has = bool(s.get("visual") or s.get("image") or s.get("number"))
        if not has:
            add("slide_no_visual", "error", "No .visual on this slide. Every slide needs one that explains the point "
                "(diagram, mockup, chart, checklist, image or a big sourced number); slide 1 needs an infographic.", i)
    # script.json and slides.html must tell the same story
    for i, s in enumerate(slides, 1):
        if i - 1 < len(_rs) and s.get("headline"):
            dom = re.sub(r"\W+", " ", plain(_rs[i - 1]["headline"].get("text", ""))).lower().strip()
            scr = re.sub(r"\W+", " ", plain(s["headline"])).lower().strip()
            if dom and scr and dom != scr:
                add("script_html_mismatch", "warn", f"script.json headline ('{plain(s['headline'])[:50]}') differs from the slide's .headline; "
                    "keep script.json in step with slides.html.", i)
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
