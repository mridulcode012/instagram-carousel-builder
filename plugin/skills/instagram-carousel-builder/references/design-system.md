# Designs: the library, mixing a new one, and the no-repeat check

Every carousel gets its own design, written as `carousels/<slug>/design.md` before any slide is built.
It comes from one of two places:

- **A mix** (no reference photo): 2-3 specs from the design library, combined dimension by dimension
  into something none of them is on its own (section 3).
- **A reference** (the person attached a template photo): the photo's design, extracted exactly
  (`references/reference-mode.md`).

Either way the design must not repeat any of the last 5 posts (section 5), and every design is saved
(section 6), so the library grows with every post.

## Contents
1. The library
2. design.md format
3. Mixing a new design
4. The vocabulary (fingerprint values)
5. The no-repeat check
6. Saving designs
7. What a design can never change (house rules)

---

## 1. The library

`<skill-dir>/assets/designs/*.design.md` ships with the skill. Saved designs from earlier posts sit in
the working folder's `designs/` and count as library entries too. List both:

```bash
python3 <skill-dir>/scripts/design_log.py library
```

| spec | look | lends best |
|---|---|---|
| `swiss-grid` | off-white, visible modular grid, huge tight sans, blue blocks snapped to cells | layout, grid devices |
| `headline-mix` | small serif lead-in over one HUGE caps word | type, emphasis (size jump) |
| `poster` | alternating saturated and light posters, heavy caps, one script word, swoop line | colour rhythm, type |
| `zine` | paper, hand-drawn scribbles, tape, stamps, typewriter labels | devices, visual style |
| `pop` | flat colour, sunburst and circle shapes, big numerals | devices, colour |
| `cards` | friendly rounded UI panels, chat bubbles, soft tints | visual style (UI), layout |
| `arcade` | 8-bit screens, pixel caps, pixel-framed UI, night violet | type, visual style (pixel) |
| `brutal` | one loud flat colour per slide, black outlines, hard shadows, sticker words | devices, visual style |

Read a spec in full before using it. Each one has its palette (and alternates), type, layouts, emphasis,
devices with CSS recipes, visual style, slide recipes and a CSS starter.

## 2. design.md format

Library specs and per-post designs use the same format. The first fenced `json` block is the
**fingerprint**: scripts read it (no-repeat check, board, lint), so keep it valid JSON and use the values
in section 4. Everything after it is the spec Claude builds from.

````markdown
# <name>

```json
{
  "name": "pilots-stall-mix",
  "kind": "mix",
  "sources": ["swiss-grid", "zine"],
  "taken": {"layout": "swiss-grid", "type": "zine", "colour": "own", "emphasis": "zine", "devices": "zine", "visual_style": "swiss-grid"},
  "mode": "light",
  "background": "#F2EDE4",
  "accent": "#E4572E",
  "palette": ["#F2EDE4", "#1B1B1B", "#E4572E", "#6B6B6B"],
  "fonts": {"display": "Archivo Black", "body": "Manrope", "label": "JetBrains Mono"},
  "google_fonts": ["Archivo+Black", "Manrope:wght@500;600;700;800", "JetBrains+Mono:wght@500;700"],
  "type": {"display_class": "sans-heavy", "case": "upper"},
  "layout": "grid-modules",
  "emphasis": "circled-scribble",
  "devices": ["visible-grid", "tape", "stamps"],
  "visual_style": "editorial-line",
  "visual_kinds": ["funnel", "compare", "timeline"]
}
```

## Look
Two or three sentences a designer could picture.

## Palette
| role | hex | use |
|---|---|---|
| bg | ... | ... |
Text pairs with their contrast ratio (every text pair 4.5:1 or better). Library specs may add
`### Alternate palettes`.

## Type
Per role (display, body, label): family, Google Fonts spec, size at 1080px, weight, case, tracking,
line-height. Nothing under 34px, nothing lighter than 400.

## Layout
The grid, margins and where the headline, visual and footer sit, as positions in % or px. 2-3 slide
layouts (e.g. cover, middle, CTA) if they differ.

## Emphasis
How the one key word per slide is marked.

## Devices
Each decorative device with a CSS (or SVG) recipe.

## Visual style
How visuals are drawn: strokes, fills, corners, shadows, icon style, how data is shown.

## Slide recipes
Cover, middle slides (stake, point, steps, stat, compare), CTA.

## CSS starter
A `:root` token block and the key classes, ready to paste into slides.html.

## Decisions            (per-post designs only)
What was taken from which source and why; anything changed to satisfy the no-repeat check or the
house rules. The hand-off repeats this.

## House-rule overrides (library and reference designs)
What in the original must never be copied (logos, slide numbers, kickers, small text...).
````

A **reference** design has no `taken` (it isn't a mix); `sources` is `["reference:<file name>", ...]`. A library spec's fingerprint has `"kind": "library"`, `"sources": []`, and `visual_kinds` lists the kinds
it draws best. 

## 3. Mixing a new design

1. **Read the history**: `python3 <skill-dir>/scripts/design_log.py recent` prints the last 5 designs'
   fingerprints. Note what they used for each dimension.
2. **Pick 2-3 sources** from the library (`design_log.py library`). At least one must not have been a
   source in any of the last 5 posts. Pick by fit first: the topic's tone and the visual the story needs
   (a funnel story wants a spec whose visual style draws funnels well).
3. **Take each dimension from one source**, and write down which in `taken`:

   | dimension | what it covers |
   |---|---|
   | `layout` | grid, margins, where headline, visual and footer sit |
   | `type` | the display font and its class and case, and the type scale (body and label fonts are fixed: section 3a) |
   | `colour` | mode, background, accent, palette (a source's main or alternate palette, or `own`) |
   | `emphasis` | how the key word is marked |
   | `devices` | decoration: grids, tape, shapes, lines, textures |
   | `visual_style` | how diagrams and mockups are drawn |

   Taking everything from one source isn't a mix. Take at least 2 dimensions from a second source (`design_log.py
   check` rejects a mix that doesn't), and change at least one value so the result is new (a fresh palette, a
   different font in the same class, a device used differently). Write all six dimensions into `taken`; `own`
   means you made it up (allowed for `colour`).
4. **Make it cohere.** A mix has to read as one system, not a collage of themes:
   - the fixed fonts below, plus one display font (and at most one second display font); one accent colour (plus at most one
     support colour)
   - the visual style has to suit the type: pixel visuals under a serif italic need a reason
   - test every text pair for 4.5:1 (lint and the renderer measure it anyway)
5. **Colours are open; fonts are fixed except the headline.** Any hex. Body text is always **Manrope** and labels, footer
   and terminal text are always **JetBrains Mono**; only the **display (headline) font** changes per design (section 3a).
   Match the display font to the mood by letterform: condensed heavy caps for loud claims, a serif for considered takes,
   a pixel face for games, a brush or script face for founder notes (80px or larger only). Avoid fonts that ship only
   light weights.
6. **Write `design.md`** in the format above, with the CSS starter filled in for this design.
7. **Run the no-repeat check** (section 5) before building any slide. If it fails, change the dimensions
   it names and run it again.

## 3a. The fixed fonts

Like the LinkedIn skill, every carousel keeps the same body and label fonts, so the feed still reads as one account while the
headline look changes:

| role | font | sizes at 1080 wide |
|---|---|---|
| body, sub-lines, list and card text, diagram labels | **Manrope**, 500-800 | 38-44px reading text, 34px minimum |
| labels, footer, source line, terminal text, tags | **JetBrains Mono**, 500-700 | 34px |
| headline (and one optional second display voice, e.g. an italic serif lead-in or a script word) | **free**: any Google Font, set per design in `fonts.display` (and `fonts.display2`) | 56-200px |

- A library spec may show other body or label faces (arcade's VT323, brutal's Space Mono). In a mix, only that spec's
  display font and its class and case come across (`taken.type`); body and labels stay Manrope and JetBrains Mono.
- `design.md` lists `fonts.body: "Manrope"` and `fonts.label: "JetBrains Mono"` for every mix and reused design;
  `design_log.py` rejects a mix that doesn't, and lint flags any rendered text in a font outside the set
  {Manrope, JetBrains Mono, `fonts.display`, `fonts.display2`}.
- **Reference designs are the exception**: they use the fonts matched to the photo, in every slot
  (`references/reference-mode.md` §3), so lint skips this check for them.

## 4. The vocabulary (fingerprint values)

Use these values so the no-repeat check can compare designs. If nothing fits, use a new short kebab-case
value: it will count as different from everything, so don't invent one to dodge the check.

**mode** (the dominant background): `dark` · `light` · `colour` (a saturated background) · `alternating`
(slides switch between two backgrounds)

**type.display_class**: `serif` · `serif-italic` · `sans` · `sans-heavy` · `sans-condensed` · `sans-wide` ·
`slab` · `mono` · `pixel` · `script` · `handwritten` · `typewriter`
**type.case**: `upper` · `sentence` · `lower` · `mixed`

**layout**
- `stack-top`: headline at the top, visual fills the middle, footer at the bottom
- `centered-stack`: everything centred on the vertical axis
- `poster`: huge type dominates; the visual is smaller or tucked into a corner
- `split-vertical`: a text column beside a visual column
- `split-horizontal`: a full-width visual band above or below a text band
- `grid-modules`: a visible modular grid, with content snapped into cells
- `card-on-canvas`: one floating card or panel holds the content on a textured canvas
- `full-bleed-visual`: the visual covers the slide; the headline sits in a band over it
- `asymmetric-offset`: headline offset to one side, the visual breaking the margin
- `rail`: a continuous line or track runs across slides with content hanging on it
- `collage`: pieces scattered and taped or stacked

**emphasis**: `highlight-block` · `underline-marker` · `italic-serif-word` · `colour-word` · `outline-text` ·
`sticker-word` · `circled-scribble` · `size-jump` · `strike-swap` · `none`

**devices** (a list): `visible-grid` · `corner-marks` · `swoop-line` · `ghost-word` · `tape` · `stamps` ·
`scribbles` · `sunburst` · `blobs` · `circles` · `hard-shadow` · `pixel-frame` · `scanlines` · `grain` ·
`dot-pattern` · `stripes` · `progress-bar` · `rail-line` · `badges` · `rules` · `gradient-light` ·
`frosted-glass` · `speech-bubbles` · `hand-arrows` · `paper-texture` · `halftone` · `outline-boxes`

**visual_style**: `flat-outline` (strokes, no fills) · `flat-solid` (solid shapes, no shadows) · `ui-mockup`
(interface panels) · `hand-drawn` · `pixel` · `isometric` · `hard-shadow-blocks` · `glass-depth` ·
`editorial-line` (thin print-style diagrams) · `sticker-cutout` · `data-minimal` (numbers and bars only)

**visual_kinds** (a list, what this post draws): see `references/visuals.md`.

## 5. The no-repeat check

```bash
python3 <skill-dir>/scripts/design_log.py check carousels/<slug>
```

It compares this post's fingerprint with each of the last 5 saved designs on 7 dimensions:

| dimension | counts as the same when |
|---|---|
| colour | same `mode` and backgrounds within a small colour distance |
| accent | accent hues within 25° (or both near-grey) |
| type | same display font, or same `display_class` and `case` |
| layout | same `layout` |
| emphasis | same `emphasis` |
| devices | half or more of the devices shared |
| visual_style | same `visual_style` |

A design passes when it differs from **each** of the last 5 on at least 4 of the 7 (a shorter history, down to none for
the first post, simply has fewer rows to pass). The script prints a
table and exits 1 if it fails. Lint runs the same check, so a repeated design can't slip through to the
judge. A carousel's own saved entry is skipped, so re-rendering a carousel doesn't fail against itself.

A reference design (the person attached a photo) is exempt: they chose that look. The check still prints
the table, and lint reports a match as info.

## 6. Saving designs

After the render is clean (step 6 of `workflows/make.md`):

```bash
python3 <skill-dir>/scripts/design_log.py save carousels/<slug>
```

This copies `design.md` to `designs/<date>-<slug>.design.md` in the working folder and logs its
fingerprint in `designs/log.json`. Saved designs can be reused ("use the design from the AI pilots post")
or mixed like library specs. Running it again for the same slug replaces that entry instead of adding a
second one.

To share a saved design with everyone, a maintainer copies it into the skill's `assets/designs/` (rename
it, set `"kind": "library"`, clear `sources`), bumps the plugin version and releases. Reference photos are
never committed: they're third-party work.

## 7. What a design can never change (house rules)

Whatever the mix or the reference, every slide keeps these (they're gates in the check):

- 1080x1350, 4-6 slides (6 by default)
- a real visual on every slide, and an infographic on slide 1
- nothing under 34px (labels, chips, diagram text and footer included); no weight under 400
- no overlaps, no clipped text, no dead space
- the headline is the first text on the slide: no kicker, eyebrow or label above it
- footer `BUILDABLELABS.COM` on every slide (bottom-left by default), swipe cue on every slide but the last
- no logo of ours or anyone's, no slide or page numbers, no ghost numerals
- every text pair 4.5:1 or better
- no stock photos or photos of people; draw it instead
