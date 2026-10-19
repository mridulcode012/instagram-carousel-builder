# instagram-carousel-builder

BuildableLabs' Instagram carousel maker and checker, as one Claude skill packaged as a plugin.
Give it a topic and a hook; it writes the brief, **designs a new look for the post**, scripts 4-6 slides with a visual on
every slide, writes the caption, builds the 1080x1350 slides and a WhatsApp-safe PDF, then scores the post on a
shares-first rubric (lint, 10 hard gates, a fresh judge) and returns PASS or FIX with slide-level fixes.

```
topic + hook ──▶ make ────────────────────────────────────────────▶ check ──────────▶ approve ──▶ post
 (+ photo)       brief (share test, PAS/PPP, search terms)           lint (facts, gates)
                 → design.md: a mix of library looks,                → fresh judge (rubric)
                   or a reference photo copied exactly               → score.py (weights, pass rule)
                 → copy → slides.html (hand-built) → render                │
                      ▲                                                    │
                      └──────────── FIX: slide-level fixes ◀───────────────┘   (max 3 rounds)
```

## Why no two posts look alike

Every carousel gets its own `design.md`. Without a reference, Claude mixes 2-3 of the 8 specs in
`plugin/skills/instagram-carousel-builder/assets/designs/` (swiss-grid, headline-mix, poster, zine, pop, cards, arcade,
brutal), taking layout, type, colour, emphasis, devices and visual style from different ones, with colours open and only the headline font free (body is always Manrope, labels JetBrains Mono).
With a reference photo, it extracts that design exactly. A new design must differ from each of the last 5 on at least 4 of
7 dimensions (`scripts/design_log.py check`), and every design is saved, so the library grows with every post. The slides
are written by hand and the visuals drawn fresh each time; `render.py` just screenshots and measures them.

## Install (pick one)

| way | how | updates |
|---|---|---|
| **claude.ai org / shared plugin** | Upload `dist/instagram-carousel-builder-<version>.zip` in claude.ai → Customize → Plugins (or Organization settings → Plugins & skills), then share it | Upload a new version |
| **GitHub sync** | Org owner: Organization settings → Plugins & skills → Add → Sync from GitHub → this repo | Automatic on every push to `main` |
| **Clone this repo** | `git clone`, open the folder in Claude Code (`.claude/skills/` links to the plugin's skill) | `git pull` |

Plugins added in claude.ai load in Claude Code for anyone signed in with their claude.ai account
(Claude Code 2.1.273+), within about 10 minutes or on a new session.

**Each person needs:** Claude Code, Python 3, Google Chrome (set `CHROME_PATH` if it's somewhere unusual),
internet for Google Fonts. Mac or Linux. No pip packages.

## Use it

Plain words work, or the slash command:

```
/instagram-carousel-builder Claude Code mods. Hook: "You can now mod Claude Code like a video game." 6 slides
```

1. **Make**: it writes the brief, mixes a design, writes the copy, builds and renders the slides. It doesn't ask questions
   or wait for approval; the hand-off lists every decision it made (design sources, angle, story, slide count).
   Attach a template photo and it copies that design exactly instead.
2. **Check**: "check carousels/<slug>". Lint, then a fresh judge: PASS or FIX, a score out of 5, the 10 gates and fixes,
   in `carousels/<slug>/check/round-N.md`.
3. **Fix**: "apply the fixes" (up to 3 rounds).
4. **Approve**: "approved".
5. **Export**: "export the PDF". Upload `carousels/<slug>/slides/*.png` to Instagram and paste `caption.md`; share
   `exports/<slug>.pdf` for review (image PDF, renders the same in WhatsApp).

Also: "use the design from the AI pilots post" (reuse a saved design), "make this post again in a different design",
"make the blog-plug version", "show me the design library".

## The house rules (hard gates)

4-6 slides (6 default) · a visual on every slide, slide 1 an infographic · nothing under 34px · no overlaps · no dead
space · no logo · no slide numbers · no kicker above the headline · footer `BUILDABLELABS.COM` · no self-promotion ·
every number sourced · no engagement bait.

## Layout

```
.claude-plugin/marketplace.json      lets claude.ai / Claude Code install the plugin from this repo
plugin/
  .claude-plugin/plugin.json         name + version (bump the version on every release)
  skills/instagram-carousel-builder/
    SKILL.md                         entry point: routes to make or check
    workflows/make.md, check.md      the two jobs, step by step
    references/                      design-system, reference-mode, script, visuals, caption, rubric, research
    scripts/                         render.py (screenshot + measure), measure.js, design_log.py, reference.py,
                                     lint.py, score.py, export_pdf.py, status.py, chrome.py, common.py
    rubric.json                      weights, gates, caps, limits (the check's source of truth)
    assets/designs/                  the 8 library specs (.design.md)
    assets/slide-base.html           the HTML contract and starting point for every post's slides
    assets/brand/                    handle, footer and the voice rules
    examples/                        claude-code-mods (PAS), ai-pilots-stall (PPP): design.md, script, slides.html, board
.claude/skills/instagram-carousel-builder → plugin/skills/instagram-carousel-builder
tools/build_zip.sh                   builds dist/instagram-carousel-builder-<version>.zip
carousels/, designs/, archive/       local work, not committed
```

## Releasing a change

1. Edit under `plugin/skills/instagram-carousel-builder/`.
2. Bump `version` in `plugin/.claude-plugin/plugin.json` (and the rubric's `version` if scoring changed).
3. `claude plugin validate --strict ./plugin` and `claude plugin validate --strict .`
4. Push to `main` (GitHub sync picks it up), and/or `tools/build_zip.sh` and upload the zip as a new version.

To add a look to the library: copy a saved design from `designs/` into `assets/designs/`, set `"kind": "library"` and clear
`sources`, then release as above. Reference photos are third-party work and are never committed.

## Known limits

- The judge is the same model in a fresh context, not a different reviewer. Scores can move about one point on a line
  between judges (the rubric ships `calibrated: false`).
- Contrast is measured only where the background under the text is a flat colour; text over gradients or images is
  checked by eye. Dead space ignores decoration drawn with gradients.
- Slides are hand-written, so layout bugs depend on `render.py`'s measurements and the judge; it flags clipping,
  overlaps, small text, contrast and highlight blocks that touch a line, but not an ugly composition.
- Instagram links usually can't be opened (login wall): drop screenshots into `carousels/<slug>/refs/`.
