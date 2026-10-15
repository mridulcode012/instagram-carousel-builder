---
name: instagram-carousel-builder
description: >-
  Make and check Instagram carousels for BuildableLabs, end to end: brief, theme, slide copy with a
  visual on every slide, caption, 1080x1350 slides and a WhatsApp-safe PDF, then a shares-first score
  (lint, 10 hard gates, a fresh judge) with PASS / FIX and slide-level fixes. 4-6 slides, 15 themes
  (10 on-brand, 5 off-brand looks scored on Instagram craft). Use it whenever someone gives a
  carousel topic or hook ("make a 6-slide post about X"), asks for slides, a swipe post or an Instagram
  carousel, wants a carousel redone in another theme, asks "is this ready to post?", wants a carousel
  checked, scored or QA'd, or says a check came back FIX, even if they never say "skill".
---

# Instagram carousel builder

One skill, two jobs. Read the workflow file for the job before doing anything else:

| the person wants to... | read |
|---|---|
| make a carousel from a topic, hook, brief or idea; redo one in another theme; apply fix notes; make the blog-plug version | `workflows/make.md` |
| check, score, QA or approve a carousel; "is this ready to post?" | `workflows/check.md` |
| a carousel from idea to approved post | `workflows/make.md`, then `workflows/check.md` |

`<skill-dir>` below and in those files means this skill's folder. Scripts are in `<skill-dir>/scripts/`
(call them by absolute path), the brand kit and themes in `<skill-dir>/assets/`, and two finished examples in
`<skill-dir>/examples/` (`claude-code-mods`: PAS, poster theme, window/HUD/flow/slots/dialog visuals;
`ai-pilots-stall`: PPP, cards theme, funnel/tags/compare/chart/timeline visuals). Carousels are written to `carousels/<slug>/` in the working folder.

## What every carousel follows (the house rules)

These are hard gates in the check, so the make workflow writes to them from the start:

- **4-6 slides**, 6 by default. The story is PAS or PPP (`references/script.md` §3), recorded in `brief.md`.
- **A visual on every slide**, slide 1 an infographic (10 kinds: `references/visuals.md`).
- **Nothing under 34px**, no overlaps, no dead space, no logo, no slide numbers, no kicker above the headline.
- **Footer `BUILDABLELABS.COM`** with a swipe cue on every slide but the last.
- **No self-promotion and no engagement bait** ("comment MOD", "tag a friend"): one honest ask, usually a send.
- **Every number traced** to evidence in `brief.md`.

## Never judge your own work

The check's judge runs in a **fresh subagent**, never the session that made the slides
(`workflows/check.md` §2). If no subagent is available, label the score `same-session`.

## Requirements

Python 3 and Google Chrome (or Chromium; set `CHROME_PATH` if it's somewhere unusual), plus internet for
Google Fonts. No pip packages. Mac or Linux.
