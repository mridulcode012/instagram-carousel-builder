# pop

```json
{
  "name": "pop",
  "kind": "library",
  "sources": [],
  "mode": "alternating",
  "background": "#0B3FDE",
  "accent": "#0B3FDE",
  "palette": ["#0B3FDE", "#FFFFFF", "#C3D4FA", "#F5F6F8", "#0A0B0E", "#565D6E", "#3964E5"],
  "fonts": {"display": "Manrope", "body": "Manrope", "label": "JetBrains Mono"},
  "google_fonts": ["Manrope:wght@500;600;700;800", "JetBrains+Mono:wght@500;700"],
  "type": {"display_class": "sans-heavy", "case": "sentence"},
  "layout": "asymmetric-offset",
  "emphasis": "highlight-block",
  "devices": ["circles", "sunburst", "stripes", "outline-boxes", "rules", "progress-bar"],
  "visual_style": "flat-solid",
  "visual_kinds": ["big-number", "checklist", "compare", "chart", "timeline", "tags", "funnel"]
}
```

## Look
Loud retro-pop posters. Flat saturated slides alternate with off-white ones. Each has a chunky, tightly
tracked ExtraBold headline with one word on a black bar, and one huge flat shape doing the work a photo
would: a corner circle, a sunburst fanning out of a corner, concentric wavy rings, thin bracket lines in
the gutters, or a thick black frame. Everything is flat, with no shadows or gradients.

## Palette
| role | hex | use |
|---|---|---|
| bg blue (fill slides) | #0B3FDE | cover, stat, quote, CTA |
| text / muted on blue | #FFFFFF / #C3D4FA | headline, body / sub-line, source |
| bg paper | #F5F6F8 | stake, point, steps, recap |
| text / muted / accent on paper | #0A0B0E / #565D6E / #0B3FDE | copy / sub-line / list marks, big numbers |
| bar | #0A0B0E | emphasis bar (white text), button on blue slides, frames |
| shape tints (decor only) | #3964E5 on blue · #C3D4FA on paper | sunburst rays, circles, rings |
| ink bg / text / muted / accent | #0A0B0E / #F5F6F8 / #B8BECC / #6789EC | ink variant: paper slides turn black |

Text pairs: #FFFFFF on #0B3FDE 7.55:1 · #C3D4FA on #0B3FDE 5.08:1 · #0A0B0E on #F5F6F8 18.2:1 ·
#565D6E on #F5F6F8 6.09:1 · #0B3FDE on #F5F6F8 6.99:1 · #FFFFFF on #0A0B0E 19.68:1 (bar) ·
#F5F6F8 on #0A0B0E 18.2:1 · #B8BECC on #0A0B0E 10.57:1 · #6789EC on #0A0B0E 5.97:1.
Black text on the blue fill is 2.61:1 and fails, so text on blue is always white. The rays (#3964E5 on blue,
1.48:1) are decoration and must never sit behind copy.

### Alternate palettes
**Orange pop (sampled by eye from refs/ref-8.png):** signal orange, cream, black.
| role | hex | contrast |
|---|---|---|
| bg orange (fill slides) | #F4601A | text #0A0A0A 6.16:1 (white fails at 3.21:1) |
| bg cream | #F4F0E4 | text #0A0A0A 17.38:1, muted #5C5448 6.54:1, accent text #B8400A 4.88:1 |
| bar | #0A0A0A | text #F4F0E4 17.38:1 |
| button on cream | #0A0A0A | #F4F0E4 17.38:1 |
Orange as text on cream is 2.82:1: use it only as a fill or shape there, and #B8400A for small accent text.
On orange slides the muted line is plain #0A0A0A.

**Sunshine (new):** marker yellow, hot pink, black.
| role | hex | contrast |
|---|---|---|
| bg yellow (fill slides) | #FFD23F | text #0A0A0A 13.71:1 |
| bg cream-yellow | #FFF6D6 | text #0A0A0A 18.29:1, muted #4A4430 8.98:1, accent #D6125E 4.72:1 |
| pink fill (button, bar, shape) | #D6125E | #FFFFFF on it 5.11:1 |
| black slide | #0A0A0A | text #FFD23F 13.71:1, muted #F4EBC8 16.56:1 |
Pink text on yellow is 3.54:1 and fails: pink is a fill under white text, or a shape.

## Type
| role | family | size at 1080 | weight | case | tracking | line-height |
|---|---|---|---|---|---|---|
| cover headline | Manrope | 124px (first line 62%) | 800 | sentence | -.05em | 1.0 |
| headline | Manrope | 92px (steps 100px) | 800 | sentence | -.045em | 1.04 |
| stat number | Manrope | 270px | 800 | as written | -.065em | .86 |
| sub | Manrope | 43px | 700 | sentence | -.02em | 1.18 |
| body | Manrope | 38px | 500 | sentence | 0 | 1.36 |
| list item | Manrope | 46px | 700 | sentence | -.015em | 1.2 |
| label, source, footer | JetBrains Mono | 34px | 500 / 700 | upper | .08em | 1.2 |
| button | Manrope | 36px | 800 | sentence | -.01em | 1 |

Google Fonts: `family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@500;700`.
Mixed sizes in one headline ("You need a / Growth Mindset"): the first line at 62% of the size.
Alternates by letterform. The ref's chunky wide display: **Dela Gothic One** (`Dela+Gothic+One`, 400, run at
84px, tracking -.02em, about 13 characters per line) or **Archivo Black** (`Archivo+Black`, 400, tracking
-.02em). A friendlier heavy grotesque: **Bricolage Grotesque** (`Bricolage+Grotesque:opsz,wght@12..96,500..800`,
800, tracking -.04em). Manrope 800 stays the body in all of them.

## Layout
- 1080 x 1350, margin 96px, flush left. Headline top at y 150, max-width 640px on slides with a top-right
  shape and 888px otherwise. Then sub-line, then the visual (40-60% of the height), then the footer.
- The shape owns one corner or edge and the copy owns the rest; shape and copy never overlap. Corner circle
  radius 300px at most when the headline starts at y 150 (it clears a 640px text column).
- Footer: a 3px rule in the text colour across the frame, the site and cue below it, at y 1254.
- Bracket lines: 3px black L-shapes 30px wide in the gutters (x 46 and x 1004), 300-470px tall, never
  inside the 96px margin.
- Progress bar: 8px, flush to the bottom edge, width = position / total, accent colour.

## Emphasis
`highlight-block`: one word per headline on a solid #0A0B0E bar with white text, drawn as a background
gradient sized to the glyph body (`0 62% / 100% 74%`), `padding:0 .12em`, so tight leading stays and the bar
never touches the lines around it. On blue slides the bar is still #0A0B0E; on the ink variant it is #F5F6F8
with #0A0B0E text. Body and list emphasis is weight 800, no bar.

## Devices
- **Corner circle** (`circles`): `radial-gradient(circle at 100% 0, var(--circle) 0 300px, transparent 301px)`
  on `.decor`, blue on paper slides, paper on blue slides.
- **Sunburst** (`sunburst`, `stripes`): `repeating-conic-gradient(from 0deg at 100% 0%, var(--ray) 0 6deg,
  transparent 6deg 13deg)`, masked to a ring (`radial-gradient(circle at 100% 0%, transparent 0 120px, #000
  121px 380px, transparent 381px)`). Rays are decoration: keep them in a corner, clear of text.
- **Wavy rings** (quote slide): concentric `repeating-radial-gradient` rings in `rgba(255,255,255,.22)`, 3px
  lines every 31px, wobbled with an SVG `feDisplacementMap` filter, masked to the lower 55% so no copy sits on
  them.
- **Frame** (`outline-boxes`, recap slide): a 10px #0A0B0E border inset 40px.
- **Rules** (`rules`): list rows have a 3px text-colour top border; the footer has the same rule.

## Visual style
`flat-solid`: bold flat shapes in two or three palette colours with a 3px black outline where it helps.
No shadows, no gradients, no glow. Corners are square or fully round, never in between. Charts are fat solid
bars (64px tall) with the winner in the accent or the black bar, value in Manrope 800 on the bar. Compare is
two flat blocks, one outlined, one filled. Timelines are a thick rail with solid round nodes. Tags are solid
pills in two colours. Big numbers are the visual: Manrope 800 at 270px. Icons are 3px stroke, square caps.
All diagram text is Manrope 700 38px or JetBrains Mono 34px.

## Slide recipes
- **Cover (blue)**: corner circle (paper) top right, bracket lines in the gutters, headline 124px in white
  with a black-bar word, a flat infographic (big number plus bars) below it, footer with cue.
- **Stake (paper)**: blue corner circle, headline 92px, sub-line, a compare or tags visual.
- **Point (paper)**: pale-blue circle (#C3D4FA), headline, one flat visual (funnel, flow), body line.
- **Stat (blue)**: sunburst top right, the sourced number at 270px in white as the first word of the
  headline, one line under it, `.source`, a two-bar chart.
- **Steps (paper)**: sunburst in blue top right (headline max-width 640), three ruled rows with a letter mark
  (`A`, `B`, `C`, accent, 800) and 46px items.
- **Quote (blue)**: wavy rings in the lower half, a black quote mark 300px, centred 92px headline with a
  black-bar word, a small visual.
- **Recap (paper)**: thick black frame, pale-blue quarter circle, ruled list.
- **CTA (blue)**: paper circle rising from the bottom-right corner with rays around it (decor), headline
  at the top, a black square button, the site only in the footer.

## CSS starter
```css
:root{
  --bg:#0B3FDE; --text:#FFFFFF; --muted:#C3D4FA; --accent:#FFFFFF; --bar:#0A0B0E; --bar-text:#FFFFFF;
  --circle:#F5F6F8; --ray:#3964E5; --btn:#0A0B0E; --btn-text:#FFFFFF; --m:96px;
  --f-display:"Manrope", Helvetica, Arial, sans-serif;
  --f-label:"JetBrains Mono", Menlo, monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--bg);color:var(--text);font-family:var(--f-display)}
.slide.paper{--bg:#F5F6F8;--text:#0A0B0E;--muted:#565D6E;--accent:#0B3FDE;--circle:#0B3FDE;--ray:#0B3FDE;--btn:#0B3FDE}
.decor{position:absolute;inset:0;pointer-events:none;z-index:0}
.decor.circle{background:radial-gradient(circle at 100% 0,var(--circle) 0 300px,transparent 301px)}
.decor.burst{background:repeating-conic-gradient(from 0deg at 100% 0%,var(--ray) 0 6deg,transparent 6deg 13deg);
  -webkit-mask-image:radial-gradient(circle at 100% 0%,transparent 0 120px,#000 121px 380px,transparent 381px);
  mask-image:radial-gradient(circle at 100% 0%,transparent 0 120px,#000 121px 380px,transparent 381px)}
.bracket{position:absolute;top:620px;left:46px;width:30px;height:420px;border:3px solid #0A0B0E;border-right:none}
.frame{position:absolute;inset:var(--m);top:150px;display:flex;flex-direction:column;gap:44px;z-index:1}
.headline{font-weight:800;font-size:92px;line-height:1.04;letter-spacing:-.045em;max-width:640px;text-wrap:balance}
.slide[data-type=cover] .headline{font-size:124px;line-height:1;letter-spacing:-.05em}
.headline .first{font-size:.62em;letter-spacing:-.03em}
.mark{color:var(--bar-text);padding:0 .12em;margin:0 .02em;
  background:linear-gradient(var(--bar),var(--bar)) 0 62%/100% 74% no-repeat;
  -webkit-box-decoration-break:clone;box-decoration-break:clone}
.num{display:block;font-size:270px;font-weight:800;line-height:.86;letter-spacing:-.065em}
.sub{font-size:43px;font-weight:700;line-height:1.18;letter-spacing:-.02em;color:var(--muted);max-width:780px}
.visual{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}
.visual svg{width:100%;height:100%}
.visual text{font-family:var(--f-display);font-weight:700;font-size:38px}
.list{list-style:none;display:flex;flex-direction:column;gap:20px;width:100%}
.list li{display:flex;gap:26px;align-items:center;padding-top:20px;border-top:3px solid var(--text);
  font-size:46px;font-weight:700;letter-spacing:-.015em;line-height:1.2}
.list .mk{font-weight:800;color:var(--accent);min-width:64px;font-size:48px}
.btn{display:inline-block;background:var(--btn);color:var(--btn-text);border-radius:4px;padding:28px 46px;font-size:36px;font-weight:800}
.source{font-family:var(--f-label);font-size:34px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.foot{margin-top:auto;border-top:3px solid currentColor;padding-top:18px;display:flex;justify-content:space-between;
  font-family:var(--f-label);font-size:34px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--text)}
.foot .cue{font-weight:700}
.progress{position:absolute;left:0;bottom:0;height:8px;background:var(--accent);z-index:2}
```

## Mix notes
- Lends best: **devices** (corner circle, sunburst, rings: one big flat shape per slide) and **colour**
  (blue and paper alternating, hard black bar). The flat-solid visual style is easy to carry into other designs.
- Pairs well with: `swiss-grid` layout with the shapes snapped to cells, `headline-mix` type with the sunburst
  behind the huge word's corner, `cards` rounded panels as the visuals, `poster` type under pop shapes.
- Clashes: `zine` tape and scribbles (two kinds of mess), `arcade` pixel frames, `poster` swoop line and
  ghost word. Soft shadows, glass and gradients break the flat look. One big shape per slide, not two.

## House-rule overrides
- No logos or brand lockups: ref-8's "Youth Pro" mark, its web address and the social handles are dropped.
- The shipped theme's big corner numeral ("02", "03" at 132px) acting as the page counter is banned (slide
  numbers and ghost numerals, gate G7), and so is its mono kicker chip. Nothing readable sits above the
  headline: the shipped cover put a ghost word ("Deploy") in the circle above the headline, which also goes.
- List marks are letters or glyphs, never zero-padded `01 02 03` (the shipped steps slide used them).
- Nothing under 34px, no weight under 400: ref-8's small body lines, urls and buttons are tiny; the shipped
  source line and kicker were 22px.
- No photos of people or stock photos: ref-8 uses a crowd, a telephone and a notebook. Draw flat shapes or
  diagrams instead.
- Rays and rings are decoration: keep copy off them, and keep brand-blue shapes away from black text.
- Footer `BUILDABLELABS.COM` bottom-left under its rule, swipe cue bottom-right, no cue on the last slide.
