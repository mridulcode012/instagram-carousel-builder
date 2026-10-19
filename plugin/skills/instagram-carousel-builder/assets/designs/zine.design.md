# zine

```json
{
  "name": "zine",
  "kind": "library",
  "sources": [],
  "mode": "alternating",
  "background": "#F5F6F8",
  "accent": "#0B3FDE",
  "palette": ["#F5F6F8", "#0A0B0E", "#565D6E", "#0B3FDE", "#FFFFFF", "#C3D4FA"],
  "fonts": {"display": "Instrument Serif", "body": "Manrope", "label": "JetBrains Mono"},
  "google_fonts": ["Instrument+Serif:ital@0;1", "Manrope:wght@500;600;700;800", "JetBrains+Mono:wght@500;700"],
  "type": {"display_class": "serif-italic", "case": "sentence"},
  "layout": "collage",
  "emphasis": "highlight-block",
  "devices": ["tape", "stamps", "scribbles", "hand-arrows", "progress-bar"],
  "visual_style": "hand-drawn",
  "visual_kinds": ["checklist", "compare", "timeline", "big-number", "quote-bubble", "flow", "illustration"]
}
```

## Look
A handmade writing zine. Off-white paper with a strip of translucent tape at the top edge, a slanted mono
label bar for titles, and a few blue hand-drawn marks (wavy underline, loop around a number, burst, arrow).
Headlines are italic serif with one word on a solid blue block. Slides alternate paper, one full-blue quote
slide and a black closing slide. It should look cut, taped and scribbled, with lots of air.

## Palette
| role | hex | use |
|---|---|---|
| bg (paper) | #F5F6F8 | slides 1 to 4 |
| text | #0A0B0E | headline, body, label bars (as a fill with paper text) |
| muted | #565D6E | sub-line, footer, source on paper |
| accent | #0B3FDE | scribbles, stat number, list marks, cue |
| fill | #0B3FDE | emphasis block, quote slide, button |
| on-fill | #FFFFFF | all text on a blue fill |
| tape (decor only) | #C3D4FA at 90% | tape strips, never behind text |
| ink bg | #0A0B0E | closing slide (and the whole deck in the ink variant) |
| ink muted / accent | #B8BECC / #6789EC | footer and sub-line / scribbles on ink |

Text pairs: #0A0B0E on #F5F6F8 18.2:1 · #565D6E on #F5F6F8 6.09:1 · #0B3FDE on #F5F6F8 6.99:1 ·
#FFFFFF on #0B3FDE 7.55:1 (emphasis block, button, quote slide) · #F5F6F8 on #0A0B0E 18.2:1 ·
#B8BECC on #0A0B0E 10.57:1 · #6789EC on #0A0B0E 5.97:1. Never #0B3FDE as text on the black slide.
Ink variant: every slide on #0A0B0E with the ink pairs, scribbles #6789EC, label bars #F5F6F8 with ink text.

### Alternate palettes
**Writing zine (zine-original; the real colours of ref-7.png):** warm cream and grey paper, signal red, black.
| role | hex | contrast |
|---|---|---|
| bg cream / grey | #EDE7D7 / #DAD9D4 | alternate by slide |
| text | #111111 | 15.3:1 on cream, 13.36:1 on grey |
| muted | #55514A | 6.39:1 on cream, 5.58:1 on grey |
| accent (text and scribbles on paper) | #B80E0E | 5.48:1 on cream, 4.78:1 on grey |
| fill (red slide, button) | #E10A0A | #FFFFFF on it 4.94:1 |
| black slide bg | #111111 | text #F5F2EA 16.88:1, muted #B5B0A4 8.73:1, red #FF4B3E 5.69:1 |
Bright #E10A0A is only a fill under white text. As text or a scribble on paper it is 4.0:1 and fails, so
use #B80E0E there. Tape #CEBE96. Add a 4% paper grain with an inline SVG feTurbulence if wanted.

**Riso teal (new):** cream, teal ink and a marker-yellow highlight.
| role | hex | contrast |
|---|---|---|
| bg | #F3EFE4 | cream paper |
| text | #1A1A1A | 15.15:1 on bg |
| muted | #5A564C | 6.37:1 on bg |
| accent and fill | #0E6B6B | 5.48:1 on bg; #FFFFFF on it 6.3:1 |
| highlight | #FFD84A | #1A1A1A on it 12.58:1 (use instead of the blue block, dark text) |
| dark slide | #1A1A1A | text #F3EFE4 15.15:1, muted #B8B3A4 8.31:1, scribbles #3FC1B8 7.9:1 |

## Type
| role | family | size at 1080 | weight | case | tracking | line-height |
|---|---|---|---|---|---|---|
| cover headline | Instrument Serif italic | 124px | 400 | sentence | -.012em | 1.0 |
| headline | Instrument Serif italic | 88px (steps 80px) | 400 | sentence | -.012em | 1.04 |
| label-bar title (point slides) | JetBrains Mono | 44px | 700 | upper | .05em | 1.38 |
| stat number | Instrument Serif italic | 230px | 400 | as written | -.02em | .9 |
| sub / body | Manrope | 38-40px | 500 / 600 | sentence | 0 | 1.35 |
| list item | Manrope | 40px | 600 | sentence | 0 | 1.2 |
| label, source, footer, list mark | JetBrains Mono | 34px | 500 / 700 | upper | .08em | 1.2 |
| button | Manrope | 34px | 600 | sentence | 0 | 1 |

Google Fonts: `family=Instrument+Serif:ital@0;1&family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@500;700`.
The label bar (black fill, paper text) is the slide's headline element on point slides; it is not a kicker.
Alternates by letterform. Typewriter label and body: **Special Elite** (`Special+Elite`, 400) for bars and
stamps, **Courier Prime** (`Courier+Prime:wght@400;700`) for body at 38px. Brush headline: **Permanent Marker**
(`Permanent+Marker`, 400), only at 80px or larger and in short lines (about 14 characters at 88px); never for
body, labels or anything near 34px. Typewriter sets wider than Manrope: allow 18 characters per 600px.

## Layout
- 1080 x 1350, margin 96px: frame x 96..984, y 96..1254, flush left.
- Tape sits on the top edge, outside the frame (top 12px, 250 x 56px, left 120px, alternating to right 120px
  on even slides). Nothing readable is within 80px of the top edge on any slide.
- Headline top at y 150 on every slide. Under it: sub-line, then the visual (flex 1, 40-60% of the slide),
  then the footer at y 1254. Keep 48px between blocks.
- Marks live only in the corners and margins: a burst at top right (x 800..984, y 100..300, clear of the
  headline's max-width of 700px beside it) or low right, a wave under the headline's last line, an arrow
  pointing at the button. A mark never crosses text, a visual or the footer (gate G3).
- Progress bar: 6px, flush to the bottom edge, accent colour, width = slide position / total.

## Emphasis
`highlight-block`: the one key word per headline on a solid #0B3FDE block, white italic text:
`display:inline-block; line-height:1; margin:.1em .02em; padding:.02em .12em .08em` (a plain inline span paints over
the descenders of the line above; the inline-block box keeps a gap). The headline needs `line-height:1.18` when it
holds a block. Body emphasis
is Manrope 700 with no block. In the Riso teal palette the block is #FFD84A with #1A1A1A text.

## Devices
- **Tape** (`tape`): a div in `.decor` with a notched clip-path (zigzag left and right edges), tape colour,
  -3deg then +2.5deg on alternate slides, `box-shadow:0 2px 0 rgba(10,11,14,.06)`.
- **Scribbles** (`scribbles`, `hand-arrows`): SVG strokes (5-6px, round caps) used as CSS masks over
  `var(--accent)`: wavy underline, burst of 6 lines, loop ring, zigzag, curly arrow. Draw them freehand-wobbly,
  never geometric. One or two per slide; the scribble colour follows the slide (white on the blue slide).
- **Stamp** (`stamps`): a short mono word in a 4px accent border, rotated -6deg, on a bg-coloured plate.
  It sits inside or beside the visual, after the headline in the DOM and below it on the page, never above.
  Maximum 2 words at 40px caps.
- **Label bar**: `background:var(--text); color:var(--bg); padding:22px 30px 20px; width:fit-content`.
- **List marks**: a small black box with a letter (`A`, `B`, `C`) or a check glyph, rotated -3deg and +2.5deg
  alternately. Never zero-padded `01 02 03`.
- **Dashed rows**: list items separated by `border-top:3px dashed rgba(10,11,14,.38)`.
- **Paper plate for visuals**: a card in bg or #FFFFFF with a 2px #0A0B0E border and a 6px #0A0B0E hard
  offset shadow, rotated 1 or 2 degrees, holding diagrams.

## Visual style
`hand-drawn`: diagrams that look inked on paper. Strokes 3-4px in #0A0B0E, slightly uneven (use SVG paths
with small control-point wobble, `stroke-linecap:round`), blue (accent) for the one thing that matters.
Arrows are curly, circles are loose and overshoot their start. Fills are flat paper tones or the blue block;
no gradients, no glow, no soft shadows. Charts: horizontal bars drawn as thick marker strokes with a
hand-written value in mono 34px. Compare: two paper plates, the "before" crossed out with a scribbled X, the
"after" circled in blue. Checklists: hand-drawn square boxes with a scribbled check. Timelines: a wobbly line
with loop nodes. Quote bubbles: a speech bubble drawn with one wobbly stroke. All diagram text is JetBrains
Mono 34px caps or Manrope 600 38px, never handwriting fonts.

## Slide recipes
- **Cover (paper)**: tape, headline 124px with one blue block word (4 lines at most), sub-line, an
  infographic on a paper plate (a hand-drawn compare or big number inside a loop ring), stamp on the plate's
  corner, burst at top right, footer with cue.
- **Stake / point (paper)**: label bar headline (mono 44px, up to 3 lines) or an italic headline, sub-line,
  a hand-drawn flow or compare, a burst low right.
- **Steps (paper)**: headline 80px, three dashed rows (list mark, 40px item), a small hand-drawn glyph at
  the right of each row, an arrow into the next.
- **Stat (paper)**: the sourced number at 230px in a loop ring, one line of headline under it, `.source` in
  a small black label bar, a zigzag in the right margin, a two-bar marker chart as the visual.
- **Quote (full blue)**: `.slide.fill`, quote mark 200px, headline 88px with a white block on the key word
  (blue text), white scribbles, a wave under the last line.
- **CTA (black)**: headline 96px, a blue square button (4px radius, white text) with a curly arrow pointing at
  it, a stamp-like note in the visual box, footer with the site only.

## CSS starter
```css
:root{
  --bg:#F5F6F8; --text:#0A0B0E; --muted:#565D6E; --accent:#0B3FDE; --fill:#0B3FDE; --on-fill:#FFFFFF;
  --tape:rgba(195,212,250,.9); --m:96px;
  --f-display:"Instrument Serif", Georgia, serif;
  --f-body:"Manrope", Helvetica, Arial, sans-serif;
  --f-label:"JetBrains Mono", Menlo, monospace;
  --sv-wave:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 34' fill='none' stroke='black' stroke-width='5' stroke-linecap='round' stroke-linejoin='round'><path d='M5 20C35 6 55 28 95 14S160 8 195 19 258 24 295 9'/><path d='M14 28C70 18 130 30 200 23S265 17 288 22'/></svg>");
  --sv-burst:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 160 160' fill='none' stroke='black' stroke-width='6' stroke-linecap='round'><path d='M80 12L85 66M148 44L98 76M138 128L94 94M62 150L72 100M12 98L64 86M22 30L68 68'/></svg>");
}
*{box-sizing:border-box;margin:0;padding:0}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--bg);color:var(--text);font-family:var(--f-body)}
.slide.fill{--bg:#0B3FDE;--text:#FFFFFF;--muted:#FFFFFF;--accent:#FFFFFF;--tape:rgba(255,255,255,.28)}
.slide.dark{--bg:#0A0B0E;--text:#F5F6F8;--muted:#B8BECC;--accent:#6789EC}
.decor{position:absolute;inset:0;pointer-events:none;z-index:0}
.tape{position:absolute;top:12px;left:120px;width:250px;height:56px;transform:rotate(-3deg);background:var(--tape);
  clip-path:polygon(0 0,3% 14%,0 28%,3% 42%,0 56%,3% 70%,0 84%,3% 100%,100% 100%,97% 86%,100% 72%,97% 58%,100% 44%,97% 30%,100% 16%,97% 0)}
.slide:nth-of-type(even) .tape{left:auto;right:120px;transform:rotate(2.5deg)}
.scribble{position:absolute;background:var(--accent);-webkit-mask:var(--m-img) no-repeat center/100% 100%;mask:var(--m-img) no-repeat center/100% 100%}
.scribble.burst{--m-img:var(--sv-burst);top:100px;right:90px;width:150px;height:150px;transform:rotate(8deg)}
.frame{position:absolute;inset:var(--m);top:150px;display:flex;flex-direction:column;gap:48px;z-index:1}
.headline{font-family:var(--f-display);font-style:italic;font-weight:400;font-size:88px;line-height:1.04;letter-spacing:-.012em;
  max-width:700px;text-wrap:balance}
.slide[data-type=cover] .headline{font-size:124px;line-height:1}
.headline:has(.mark){line-height:1.18}
.mark{display:inline-block;line-height:1;margin:.1em .02em;padding:.02em .12em .08em;color:#FFF;background:var(--fill)}
.slide.fill .mark{background:#FFF;color:var(--fill)}
.bar{display:block;width:fit-content;max-width:100%;background:var(--text);color:var(--bg);padding:22px 30px 20px;
  font-family:var(--f-label);font-style:normal;font-weight:700;font-size:44px;line-height:1.38;letter-spacing:.05em;text-transform:uppercase}
.sub{font-size:40px;font-weight:500;line-height:1.35;color:var(--muted);max-width:820px}
.visual{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}
.plate{background:#FFF;border:2px solid var(--text);box-shadow:6px 6px 0 var(--text);transform:rotate(-1.5deg);padding:28px}
.stamp{display:inline-block;transform:rotate(-6deg);border:4px solid var(--accent);color:var(--accent);background:var(--bg);
  padding:14px 26px 12px;font-family:var(--f-label);font-weight:700;font-size:40px;letter-spacing:.16em;text-transform:uppercase}
.list{list-style:none;display:flex;flex-direction:column;gap:18px}
.list li{display:flex;align-items:center;gap:26px;padding-top:22px;border-top:3px dashed rgba(10,11,14,.38);font-size:40px;font-weight:600;line-height:1.2}
.list .mk{background:var(--text);color:var(--bg);padding:8px 14px 6px;font-family:var(--f-label);font-weight:700;font-size:36px;transform:rotate(-3deg)}
.list li:nth-child(even) .mk{transform:rotate(2.5deg)}
.btn{display:inline-block;background:var(--fill);color:#FFF;border-radius:4px;padding:26px 44px;font-weight:600;font-size:34px}
.source{width:fit-content;background:var(--text);color:var(--bg);padding:9px 16px 8px;font-family:var(--f-label);font-size:34px;letter-spacing:.08em;text-transform:uppercase}
.foot{margin-top:auto;display:flex;justify-content:space-between;font-family:var(--f-label);font-size:34px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.foot .cue{color:var(--accent)}
.progress{position:absolute;left:0;bottom:0;height:6px;background:var(--accent);z-index:2}
```

## Mix notes
- Lends best: **devices** (tape, scribbles, stamps, curly arrows) and **visual_style** (hand-drawn diagrams on
  paper plates). Its loose, personal voice also suits a founder-note tone.
- Pairs well with: `swiss-grid` layout under the tape (the grid keeps the scribbles honest), `headline-mix`
  type if the serif stays, `pop` flat colour for the plates, `brutal` hard shadows (already on the plates).
- Clashes: `poster` swoop and ghost word (two competing line devices), `arcade` pixel frames, heavy
  uppercase sans headlines (they fight the italic serif). Never more than two marks per slide.

## House-rule overrides
- No logos or brand lockups. ref-7's "POST TEMPLATE" tag and the photos' credit lines are dropped.
- Nothing readable above the headline: the shipped theme's mono kicker with bullets ("HOW TO WRITE") and slide
  counter are banned, as are the ref's small red "HOW TO WRITE" labels above each title bar. The stamp may
  not sit above the headline either; place it after the headline, over the visual or beside it.
- No slide numbers or ghost numerals. List marks are letters or glyphs, never zero-padded `01 02 03`.
- Nothing under 34px, no weight under 400: the shipped badge was 22px and the ref's typewriter body is
  tiny. Typewriter or marker fonts keep to 34px minimum and 80px for the brush face.
- No photos of people or stock photos: ref-7 is built on portraits, a typewriter and book pages. Replace with
  hand-drawn diagrams.
- Tape and scribbles are decoration only: they live in `.decor`, in the margins, and never cover copy.
- Footer `BUILDABLELABS.COM` bottom-left, swipe cue bottom-right, no cue on the last slide.
