---
name: instagram-carousel-builder
description: >-
  Make and check Instagram carousels for BuildableLabs, end to end, with a new design for every post: brief,
  a design mixed from a library of 8 looks (or extracted exactly from a reference photo you attach), slide copy with a
  visual on every slide, caption, hand-built 1080x1350 slides and a WhatsApp-safe PDF, then a shares-first score
  (lint, 10 hard gates, a fresh judge) with PASS / FIX and slide-level fixes. 4-6 slides, no repeated look across the
  last 5 posts. Use it whenever someone gives a carousel topic or hook ("make a 6-slide post about X"), attaches a
  template photo to copy, asks for slides, a swipe post or an Instagram carousel, wants a carousel redone in a different
  look, asks "is this ready to post?", wants a carousel checked, scored or QA'd, or says a check came back FIX, even if they
  never say "skill".
---

# Instagram carousel builder

One skill, two jobs. Read the workflow file for the job before doing anything else:

| the person wants to... | read |
|---|---|
| make a carousel from a topic, hook, brief or idea; copy an attached template photo; redo one in a new design; apply fix notes; make the blog-plug version | `workflows/make.md` |
| check, score, QA or approve a carousel; "is this ready to post?" | `workflows/check.md` |
| a carousel from idea to approved post | `workflows/make.md`, then `workflows/check.md` |

`<skill-dir>` below and in those files means this skill's folder. Scripts are in `<skill-dir>/scripts/` (call them by
absolute path), the design library in `<skill-dir>/assets/designs/`, the slide starting point in
`<skill-dir>/assets/slide-base.html`, and two finished examples in `<skill-dir>/examples/` (`claude-code-mods`: PAS,
a pixel-and-sticker mix; `ai-pilots-stall`: PPP, a paper-and-hairline mix). Carousels are written to `carousels/<slug>/`
in the working folder, and every design made so far to `designs/`.

## How the design works (why two posts don't look alike)

- **Every carousel has its own `design.md`.** With no reference, you mix 2-3 specs from the library, taking each of six
  dimensions (layout, type, colour, emphasis, devices, visual style) from a different one, with colours open and only the headline font free (body is always Manrope, labels JetBrains Mono).
  With a reference photo, you extract its design exactly (`references/reference-mode.md`).
- **A design may not repeat any of the last 5.** `scripts/design_log.py check` compares the new design's fingerprint with
  each of them and fails if it matches on more than 3 of 7 dimensions.
- **You write the slides by hand** (`slides.html`) and draw the visuals fresh for the idea. `render.py` only screenshots
  and measures what you wrote. Full detail: `references/design-system.md`.

## What every carousel follows (the house rules)

These are hard gates in the check, so the make workflow writes to them from the start:

- **4-6 slides**, 6 by default. The story is PAS or PPP (`references/script.md` §3), recorded in `brief.md`.
- **A visual on every slide**, slide 1 an infographic (`references/visuals.md`).
- **Nothing under 34px**, no weight under 400, no overlaps, no dead space, no logo, no slide numbers, no kicker above the
  headline.
- **Footer `BUILDABLELABS.COM`** with a swipe cue on every slide but the last.
- **No self-promotion and no engagement bait** ("comment MOD", "tag a friend"): one honest ask, usually a send.
- **Every number traced** to evidence in `brief.md`.

## No questions

The make workflow doesn't stop to ask. It makes every open decision itself and lists them in the hand-off, so the person
can overrule any of them afterwards. The one exception is an idea that isn't a carousel at all.

## Never judge your own work

The check's judge runs in a **fresh subagent**, never the session that made the slides (`workflows/check.md` §2). If no
subagent is available, label the score `same-session`.

## Running in claude.ai chat

Most use is in a normal chat with code execution, where the sandbox resets between conversations. What changes:

- **Work in `/home/claude/work`** (`mkdir -p` it, run commands from there; `carousels/` and `designs/` go in it). Find this
  skill's folder first (it is where this SKILL.md was read from) and use it as `<skill-dir>`.
- **Chrome is found automatically** (Playwright's Chromium in `/opt/pw-browsers`). If a script says no Chrome was found:
  `pip install playwright && python3 -m playwright install chromium`, then run it again.
- **Fonts load by themselves.** Google Fonts is usually blocked there, so `render.py` falls back to local copies (Manrope and
  JetBrains Mono ship with the skill; any other family is fetched from npm). Nothing to do; a font it couldn't get shows
  up as a problem in the render output.
- **Attached photos** are in `/mnt/user-data/uploads/`: copy them into `carousels/<slug>/refs/` before extracting.
- **Deliver** by copying into `/mnt/user-data/outputs/`: the slide PNGs, `board.png`, `caption.md`, the PDF
  (`export_pdf.py`, run it every time here) and the design as `<date>-<slug>.design.md` (the file `designs/` just saved),
  then present them. Tell the person to keep that design file.
- **Design memory does not survive a new chat.** At the start, if the person attached earlier design files, run
  `python3 <skill-dir>/scripts/design_log.py import <files>` so the last-5 check has its history. With none attached, say once
  in the hand-off that the no-repeat check only covered this chat, and ask them to attach the last few design files next time.
- **No subagents here** unless the tool exists: the check then labels its score `same-session` (`workflows/check.md`).

## Requirements

Python 3 and Google Chrome or Chromium (set `CHROME_PATH` if it's somewhere unusual). No pip packages. Mac, Linux, Claude
Code, and the claude.ai chat sandbox. Fonts come from Google Fonts, or from local copies when that is blocked (npm needed
for any family other than Manrope and JetBrains Mono).
