# instagram-carousel-builder

BuildableLabs' Instagram carousel maker and checker, as one Claude skill packaged as a plugin.
Give it a topic and a hook; it writes the brief, picks a theme, scripts 4-6 slides with a visual on
every slide, writes the caption, renders 1080x1350 slides and a WhatsApp-safe PDF, then scores the
post on a shares-first rubric (lint, 10 hard gates, a fresh judge) and returns PASS or FIX with
slide-level fixes.

```
topic + hook ──▶ make ───────────────────────────────────────▶ check ──────────▶ approve ──▶ post
                 brief (share test, PAS/PPP, search terms)      lint (facts, gates)
                 → theme → copy list you approve                → fresh judge (rubric)
                 → slides + caption + board                     → score.py (weights, pass rule)
                      ▲                                               │
                      └──────────── FIX: slide-level fixes ◀──────────┘   (max 3 rounds)
```

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
/instagram-carousel-builder Claude Code mods. Hook: "You can now mod Claude Code like a video game." 6 slides, pick the best theme
```

1. **Make**: it writes the brief, picks a theme (ask for one: "use brutal"), asks 3-5 quick questions
   ("choose for me" skips them), then shows the copy list for you to approve. Then it renders.
2. **Check**: "check carousels/<slug>". Lint, then a fresh judge: PASS or FIX, a score out of 5,
   the 10 gates and fixes, in `carousels/<slug>/check/round-N.md`.
3. **Fix**: "apply the fixes" (up to 3 rounds).
4. **Approve**: "approved".
5. **Export**: "export the PDF". Upload `carousels/<slug>/slides/*.png` to Instagram and paste `caption.md`;
   share `exports/<slug>.pdf` for review (image PDF, renders the same in WhatsApp).

Also: "show me the themes", "make this post in arcade", "make the blog-plug version",
"don't wait for my approval" (unattended runs).

## The house rules (hard gates)

4-6 slides (6 default) · a visual on every slide, slide 1 an infographic · nothing under 34px · no
overlaps · no dead space · no logo · no slide numbers · no kicker above the headline · footer
`BUILDABLELABS.COM` · no self-promotion · every number sourced · no engagement bait.

## Themes

- **On-brand (10)**: foundation, editorial, swiss-grid, poster, glass, headline-mix, zine, pop, promo, cards.
- **Off-brand (5)**, scored on Instagram craft instead of brand match: arcade, crt (+ amber), brutal,
  poster-original, glass-original.

Previews: `plugin/skills/instagram-carousel-builder/assets/themes/<name>/preview.png`.
More off-brand themes are in progress (`archive/themes-wip/`, not shipped).

## Layout

```
.claude-plugin/marketplace.json      lets claude.ai / Claude Code install the plugin from this repo
plugin/
  .claude-plugin/plugin.json         name + version (bump the version on every release)
  skills/instagram-carousel-builder/
    SKILL.md                         entry point: routes to make or check
    workflows/make.md, check.md      the two jobs, step by step
    references/                      script, visuals, caption, themes, vision, rubric, research
    scripts/                         render.py, export_pdf.py, status.py, theme_preview.py, lint.py, score.py
    rubric.json                      weights, gates, caps, limits (the check's source of truth)
    assets/brand/, assets/themes/    brand kit and themes (a project's own brand/ above a carousel overrides them)
    examples/                        claude-code-mods (PAS, poster), ai-pilots-stall (PPP, cards)
.claude/skills/instagram-carousel-builder → plugin/skills/instagram-carousel-builder
tools/build_zip.sh                   builds dist/instagram-carousel-builder-<version>.zip
carousels/, visions/, archive/       local work, not committed
```

## Releasing a change

1. Edit under `plugin/skills/instagram-carousel-builder/`.
2. Bump `version` in `plugin/.claude-plugin/plugin.json` (and the rubric's `version` if scoring changed).
3. `claude plugin validate --strict ./plugin` and `claude plugin validate --strict .`
4. Push to `main` (GitHub sync picks it up), and/or `tools/build_zip.sh` and upload the zip as a new version.

## Known limits

- The judge is the same model in a fresh context, not a different reviewer. Scores can move about
  one point on a line between judges (the rubric ships `calibrated: false`).
- Contrast is measured only on flat backgrounds; text over gradients or photos is checked by eye.
- Instagram links usually can't be opened (login wall): drop screenshots into `carousels/<slug>/refs/`.
