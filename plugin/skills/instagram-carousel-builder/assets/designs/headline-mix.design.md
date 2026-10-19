# headline-mix

```json
{
  "name": "headline-mix",
  "kind": "library",
  "sources": [],
  "mode": "alternating",
  "background": "#0A0B0E",
  "accent": "#0B3FDE",
  "palette": ["#0A0B0E", "#F5F6F8", "#0B3FDE", "#6789EC", "#7A8296", "#565D6E", "#FFFFFF"],
  "fonts": {"display": "Manrope", "body": "Instrument Serif", "label": "JetBrains Mono"},
  "google_fonts": ["Manrope:wght@500;600;700;800", "Instrument+Serif:ital@0;1", "JetBrains+Mono:wght@500;700"],
  "type": {"display_class": "sans-heavy", "case": "mixed"},
  "layout": "centered-stack",
  "emphasis": "size-jump",
  "devices": ["rules", "progress-bar"],
  "visual_style": "editorial-line",
  "visual_kinds": ["big-number", "checklist", "compare", "timeline", "chart"]
}
```

## Look
A magazine-cover headline in two voices: a small condensed italic serif line stacked directly on one
HUGE ExtraBold uppercase sans word, then a short italic serif tail. Flat, unpatterned slides alternate
near-black and off-white, with one full brand-blue slide for the quote or key claim. Everything is
centred, quiet and typographic; visuals are thin-ruled editorial diagrams, never glossy panels.

## Palette
| role | hex | use |
|---|---|---|
| bg (dark) | `#0A0B0E` | odd slides (1, 3, 5) |
| text (dark) | `#F5F6F8` | lead-in, tail, list text on dark |
| muted (dark) | `#7A8296` | footer, source line on dark |
| accent (dark) | `#6789EC` | the huge word, numbers, list index on dark |
| bg (light) | `#F5F6F8` | even slides (2, 4, 6) |
| text (light) | `#0A0B0E` | all text on light |
| muted (light) | `#565D6E` | footer, source on light |
| accent (light) | `#0B3FDE` | the huge word, list index, button on light |
| fill | `#0B3FDE` | quote slide background, button, progress bar |
| on-fill | `#FFFFFF` | all text on the blue slide (muted and accent become white too) |
| line | `rgba(10,11,14,.16)` light / `rgba(245,246,248,.16)` dark | hairline rules, chart tracks (no text) |

Text pairs: `#F5F6F8` on `#0A0B0E` 18.2:1 · `#7A8296` on `#0A0B0E` 5.12:1 · `#6789EC` on `#0A0B0E` 5.97:1 ·
`#0A0B0E` on `#F5F6F8` 18.2:1 · `#565D6E` on `#F5F6F8` 6.09:1 · `#0B3FDE` on `#F5F6F8` 6.99:1 ·
`#FFFFFF` on `#0B3FDE` 7.55:1 (blue slide, button) · `#0B3FDE` on `#FFFFFF` 7.55:1 (inverted button on blue).
Never put `#6789EC` on the light bg or `#0B3FDE` on the dark bg; swap accents with the background.

### Alternate palettes
**Reference (sampled by eye from refs/ref-6.png):** charcoal, cream, signal orange, mustard.
| role | hex | pair and ratio |
|---|---|---|
| bg | `#1C1C1A` | dark slides |
| text | `#F2EEE6` | on bg 14.75:1 |
| muted | `#B5AFA4` | on bg 7.83:1 |
| accent | `#EF4B2C` | huge word on bg 4.64:1 |
| light bg | `#E9E4D8` | cream slides; text `#1C1C1A` 13.45:1, muted `#5C574E` 5.65:1, accent `#A92E17` 5.36:1 |
| fill | `#F5B419` | mustard slide; text `#1C1C1A` 9.29:1 |
The original puts orange on mustard (2.0:1) and orange on cream (2.9:1); both fail, so on cream use
`#A92E17` and on mustard set the huge word in `#1C1C1A`.

**Forest (new):** deep green and warm gold, for slower, considered takes.
| role | hex | pair and ratio |
|---|---|---|
| bg | `#10291C` | dark slides |
| text | `#F2EDE1` | on bg 13.26:1 |
| muted | `#A9B8A8` | on bg 7.45:1 |
| accent | `#F2B33D` | huge word on bg 8.33:1 |
| light bg | `#F2EDE1` | paper slides; text `#10291C` 13.26:1, muted `#4E5A50` 6.19:1, accent `#1F5135` 7.86:1 |
| fill | `#F2B33D` | gold slide; text `#10291C` 8.33:1 |

## Type
| role | family | size at 1080 | weight | case | tracking | line-height |
|---|---|---|---|---|---|---|
| lead-in (inside headline) | Instrument Serif italic | 64px cover, 64px middle | 400 | sentence | -.01em | 1.02 |
| huge word (inside headline) | Manrope | 190px cover, 150px middle | 800 | upper | -.05em | .84 |
| plain headline (no huge word) | Manrope | 110px cover, 104px middle, 96px CTA | 800 | upper | -.04em, word-spacing .06em | .90 |
| tail / sub | Instrument Serif italic | 52px | 400 | sentence | 0 | 1.10 |
| list item | Instrument Serif italic | 52px | 400 | sentence | 0 | 1.10 |
| stat number | Manrope | 260px | 800 | upper | -.055em | .80 |
| label, source, footer, list index | JetBrains Mono | 34px | 500 (700 for index) | upper | .10-.12em | 1.2 |
| button | Manrope | 36px | 600 | sentence | 0 | 1 |

Google Fonts: `family=Manrope:wght@500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@500;700`.
Brand fonts today: Manrope, Instrument Serif, JetBrains Mono. Alternates by letterform: for the huge word
**Archivo** (800, tight grotesk caps, closest to the ref's heavy sans) or **Bricolage Grotesque** (800, a
little quirkier); for the lead-in **Playfair Display italic** or **Bodoni Moda italic** (high-contrast
didone italics like the ref's "Five" and "hate"). Keep the serif condensed so the lead-in stays one line.
The huge word never wraps, so size it by letter count (Manrope 800 caps run about 0.7em per letter,
and the frame is 904px wide): up to 5 letters 190px · 6-7 letters 150px · 8-9 letters 120px ·
10 or more: pick a shorter word. Check it in the render; a clipped huge word fails gate G3.

## Layout
- 1080x1350, outer margin 88px, everything centred on the vertical axis (`text-align:center`).
- Frame is a flex column: headline block, sub, visual, footer; gap 34px between headline and sub, 56px
  before the visual.
- Cover: headline block top at y=180, ends near y=600; tail at y=620-700; visual y=760-1160 (width 860px);
  footer bottom edge at y=1262.
- Middle: headline block top at y=150 (plain caps headline 2-4 lines, max-width 880px); visual fills
  y=520-1160.
- Stat: the 260px number is the huge word, centred at y=260-470, italic serif line under it, `.source`
  under that, visual (bar or compare) below.
- CTA: plain caps headline centred at y=300-560, a square blue button under it, a checklist visual below.
- Progress bar: 5px tall, flush to the bottom edge, width = slide index / total, fill colour.

## Emphasis
`size-jump`: the one key word is pulled out of the sentence and set as its own line, 2.3-3x the lead-in
size, ExtraBold uppercase sans in the accent, while the rest of the sentence stays small italic serif.
Secondary, only in the tail or a list line: one italic word underlined in the accent
(`text-decoration-thickness:.075em; text-underline-offset:.16em`). One huge word per slide, at most.

## Devices
- **Hairline rules**: list items and compare rows separated by `border-top:2px solid var(--line)`.
- **Progress bar**: `.decor` child, `position:absolute;left:0;bottom:0;height:5px;background:var(--fill)`,
  width set inline (`style="width:33%"`). On the blue slide use `var(--on-fill)`.
- **Quote mark**: Instrument Serif `“` at 150px, height 64px, line-height .7, accent colour, above the
  quote text and inside `.headline` (it is not readable text, but keep it in the h2 so nothing sits above).
- **Thin arrow cue**: the swipe cue is a long thin arrow, SVG `<path d="M2 13h78M69 3l11 10-11 10"/>`,
  84x26, stroke 2.4, round caps, in the accent, after the word "Swipe".
- **Square button** (CTA): `background:var(--fill);color:#FFF;border-radius:4px;padding:26px 44px`.

## Visual style
`editorial-line`: thin print diagrams, no shadows, no gradients, no glass. Strokes 2-3px in `--text` at
full or 35% opacity; corners square or 4px. One element per visual in the accent (the current step, the
winning bar, the "after" column); everything else is text colour or line colour. Labels in JetBrains Mono
34px uppercase; item text in Instrument Serif italic 44-52px. Big numbers in Manrope 800 accent.
Charts are horizontal bars: 48px tracks in `--line`, bars in `--muted`, the key bar in the accent, value in
mono right-aligned. Checklists are ruled rows with a mono letter index (`A`, `B`, `C`) or a 2px check glyph. Timelines are a 3px vertical rail
with 64px ring nodes. UI mockups, if needed, are flat outlined boxes on the slide bg, not dark panels.
Icons: 2px stroke line icons, round joins.

## Slide recipes
- **Cover (dark)**: headline = lead-in + huge word ("Your AI strategy is only as good as what / DEPLOYS."),
  italic tail, then the infographic (big-number or compare) in editorial lines, footer with cue.
- **Point (light)**: plain caps headline ("MOST AI WORK DIES BETWEEN THE DEMO AND THE HANDOFF."), italic
  tail with one underlined word, then a timeline or compare visual.
- **Steps (light or dark)**: plain caps headline, then a ruled checklist: mono letter index in accent, serif
  italic line, 3-4 rows, max-width 820px.
- **Stat (dark)**: "6 WKS" as the huge word, italic line, mono source, a two-bar chart.
- **Quote / key claim (blue fill)**: quote mark, lead-in + huge word + tail ("When AI collapses execution
  time, / JUDGMENT / is the differentiator."), a small visual in white lines.
- **CTA (light)**: plain caps headline, square blue button, a 3-item checklist; no cue.

## CSS starter
```css
:root{
  --bg:#0A0B0E; --text:#F5F6F8; --muted:#7A8296; --accent:#6789EC;
  --fill:#0B3FDE; --on-fill:#FFFFFF; --line:rgba(245,246,248,.16);
  --f-display:"Manrope", Helvetica, Arial, sans-serif;
  --f-serif:"Instrument Serif", Georgia, serif;
  --f-label:"JetBrains Mono", Menlo, monospace;
  --m:88px;
}
*{box-sizing:border-box;margin:0;padding:0}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;
  background:var(--bg);color:var(--text);font-family:var(--f-serif)}
.slide.light{--bg:#F5F6F8;--text:#0A0B0E;--muted:#565D6E;--accent:#0B3FDE;--line:rgba(10,11,14,.16)}
.slide.blue{--bg:#0B3FDE;--text:#FFFFFF;--muted:#FFFFFF;--accent:#FFFFFF;--line:rgba(255,255,255,.3)}
.decor{position:absolute;inset:0;pointer-events:none;z-index:0}
.frame{position:absolute;inset:var(--m);display:flex;flex-direction:column;align-items:center;
  text-align:center;z-index:1}
/* headline: one h1/h2 holds the lead-in and the huge word */
.headline{font-family:var(--f-display);font-weight:800;text-transform:uppercase;font-size:104px;
  line-height:.9;letter-spacing:-.04em;word-spacing:.06em;max-width:880px;text-wrap:balance}
.slide[data-type=cover] .headline{font-size:110px}
.slide[data-type=cta] .headline{font-size:96px}
.headline .lead{display:block;font-family:var(--f-serif);font-style:italic;font-weight:400;
  text-transform:none;font-size:64px;line-height:1.02;letter-spacing:-.01em;word-spacing:0}
/* emphasis: size-jump */
.headline .big{display:block;color:var(--accent);font-size:150px;line-height:.84;
  letter-spacing:-.05em;margin:.04em 0 .02em;white-space:nowrap}
.slide[data-type=cover] .headline .big{font-size:190px}
.headline .big.long{font-size:120px}
.headline .qmark{display:block;font-family:var(--f-serif);font-size:150px;height:64px;
  line-height:.7;color:var(--accent);letter-spacing:0}
.num{font-family:var(--f-display);font-weight:800;font-size:260px;line-height:.8;
  letter-spacing:-.055em;color:var(--accent);display:block}
.sub{margin-top:28px;font-family:var(--f-serif);font-style:italic;font-size:52px;line-height:1.1;
  max-width:820px;color:var(--text)}
.ul{text-decoration:underline;text-decoration-color:var(--accent);text-decoration-thickness:.075em;
  text-underline-offset:.16em;text-decoration-skip-ink:none}
.source{margin-top:20px;font-family:var(--f-label);font-size:34px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted)}
.visual{flex:1;min-height:0;width:100%;margin-top:56px;display:flex;align-items:center;
  justify-content:center;font-family:var(--f-label)}
.visual svg{width:100%;height:100%}
/* ruled list (checklist / steps) */
.list{list-style:none;width:100%;max-width:820px;display:flex;flex-direction:column;gap:20px;text-align:left}
.list li{display:flex;gap:28px;align-items:baseline;padding-top:22px;border-top:2px solid var(--line);
  font-family:var(--f-serif);font-style:italic;font-size:52px;line-height:1.1}
.list .ix{font-family:var(--f-label);font-style:normal;font-weight:700;font-size:34px;color:var(--accent);min-width:58px}
/* bar chart */
.bar{display:flex;flex-direction:column;gap:14px;width:100%}
.bar .track{height:48px;background:var(--line)}
.bar .track i{display:block;height:100%;background:var(--muted)}
.bar.on .track i{background:var(--accent)}
.btn{display:inline-block;margin-top:40px;background:var(--fill);color:var(--on-fill);border-radius:4px;
  padding:26px 44px;font-family:var(--f-display);font-weight:600;font-size:36px}
.slide.blue .btn{background:var(--on-fill);color:var(--fill)}
.foot{width:100%;margin-top:auto;padding-top:40px;display:flex;justify-content:space-between;align-items:center;
  font-family:var(--f-label);font-size:34px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.foot .cue{display:flex;align-items:center;gap:16px;color:var(--accent)}
.foot .cue svg{width:84px;height:26px;fill:none;stroke:currentColor;stroke-width:2.4;
  stroke-linecap:round;stroke-linejoin:round}
.progress{position:absolute;left:0;bottom:0;height:5px;background:var(--fill)}
.slide.blue .progress{background:var(--on-fill)}
```
Markup: `<h1 class="headline"><span class="lead">Your AI strategy is only as good as what</span><span class="big">Deploys.</span></h1>`.

## Mix notes
- Lends best: **type** (two-voice serif italic plus heavy caps) and **emphasis** (size-jump). Its
  **colour** rhythm (dark, light, one full-accent slide) also travels well.
- Pairs well with: `swiss-grid` layout (the huge word snaps to a wide cell), `cards` or `brutal` visual
  styles if the serif tail stays, `pop` devices kept sparse.
- Clashes: `zine` scribbles and `poster` script words (a third voice fights the two it already has);
  `arcade` pixel type; any emphasis that also marks a word (highlight block, sticker word) on top of the
  size jump. Busy textures behind the huge word kill the contrast in scale that makes it work.

## House-rule overrides
- No logos or brand lockups: drop the ref's "Asterisk Create" name, handwritten asterisk mark and the
  `@asterisk.create` handle in its footers.
- No slide numbers or ghost numerals; the progress bar is the only position hint. List indexes are
  letters or glyphs, never zero-padded `01 02` (those read as slide numbers and fail gate G7).
- Nothing readable above the headline: the ref's small lead-ins ("What is", "it's a", "when it's",
  "The") sit above the big word. Here the lead-in is part of the one h1/h2 with the big word; no kicker,
  eyebrow or top bar.
- Nothing under 34px, nothing under weight 400: the ref's footer text ("save for later", handle) is tiny;
  ours is 34px mono. Drop the centre "save for later" label and bookmark icon entirely.
- No photos: the ref leans on photos of a person (founder shots), stock-style scenes (grass field, sky,
  chair, camera, retro computer). Replace with drawn editorial visuals.
- Fix the ref's failing pairs (orange on mustard 2.0:1, orange on cream 2.9:1) as in the alternate palette.
- Footer `BUILDABLELABS.COM` bottom-left, swipe cue with thin arrow bottom-right, no cue on the last slide.
