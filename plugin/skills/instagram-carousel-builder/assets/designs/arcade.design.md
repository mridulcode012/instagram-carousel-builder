# arcade

```json
{
  "name": "arcade",
  "kind": "library",
  "sources": [],
  "mode": "dark",
  "background": "#1A0B3D",
  "accent": "#FFD23F",
  "palette": ["#1A0B3D", "#0C0624", "#261552", "#FFF4DC", "#BDB0FF", "#FFD23F", "#FF4FA3", "#45E6FF", "#9BFF4A"],
  "fonts": {"display": "Press Start 2P", "body": "Chakra Petch", "label": "VT323"},
  "google_fonts": ["Press+Start+2P", "Chakra+Petch:wght@500;600;700", "VT323"],
  "type": {"display_class": "pixel", "case": "upper"},
  "layout": "stack-top",
  "emphasis": "colour-word",
  "devices": ["pixel-frame", "hard-shadow", "halftone", "progress-bar"],
  "visual_style": "pixel",
  "visual_kinds": ["hud", "window", "slots", "dialog", "flow", "chart", "checklist", "timeline", "funnel", "compare"]
}
```

## Look
8-bit arcade screens. Deep night-violet slides with a few single-pixel stars, a dithered floor along the
bottom that holds the footer like a status bar, and a segmented lime power bar for progress. Headlines are
pixel-font caps with one yellow word on a hot-pink drop. Every box uses the same pixel frame (stepped
corners and a stepped hard drop), and visuals become native game UI: windows, heart HUDs, inventory slots,
RPG dialog boxes. The CTA is a full yellow screen.

## Palette
| role | hex | use |
|---|---|---|
| bg (night) | #1A0B3D | slide background |
| deep | #0C0624 | box fills, floor |
| panel | #261552 | title bars, bar tracks |
| text (cream) | #FFF4DC | headline, body |
| muted (lavender) | #BDB0FF | footer, secondary lines |
| accent (yellow) | #FFD23F | key word, active slot, CTA screen |
| pink | #FF4FA3 | hard drops, window title bars, button |
| cyan | #45E6FF | sub-line, icons |
| lime | #9BFF4A | power bar, checks, prompts |
| grape (decor only) | #3D2785 | dither, dashed dividers, headline shadow |

Text pairs: #FFF4DC on #1A0B3D 16.59:1 · #BDB0FF on #1A0B3D 9.33:1 · #FFD23F on #1A0B3D 12.55:1 · #45E6FF on
#1A0B3D 12.09:1 · #FF4FA3 on #1A0B3D 5.95:1 · #9BFF4A on #0C0624 15.74:1 · #FFF4DC on #0C0624 18.02:1 ·
#BDB0FF on #0C0624 10.14:1 · #FFF4DC on #261552 14.66:1 · #FFD23F on #261552 11.09:1 · #1A0B3D on #FFD23F
12.55:1 (CTA screen, active slot) · #1A0B3D on #FF4FA3 5.95:1 (title bars, button) · #1A0B3D on #45E6FF 12.09:1 ·
#1A0B3D on #9BFF4A 14.49:1. Grape on night is 1.58:1: it is decoration only and never carries text.
Yellow CTA screen: bg #FFD23F, text and frames #1A0B3D, drops #FF4FA3, key word #FFD23F on a #1A0B3D block.

### Alternate palettes
**Game Boy (new):** four greens, one hue.
| role | hex | contrast |
|---|---|---|
| bg (lightest) | #9BBC0F | text #0F380F 6.02:1 |
| bg (darkest) | #0F380F | text #9BBC0F 6.02:1 |
| mid | #8BAC0F | #0F380F on it 5.03:1 |
| shadow (decor) | #306230 | on #9BBC0F only 3.29:1: never text |
There is no muted tone: secondary text is the same colour at the same size. Use `#0F380F` frames and drops.
**Daylight arcade (new):** a bright sky level.
| role | hex | contrast |
|---|---|---|
| bg sky | #5C94FC | text #1A0B3D 6.12:1 |
| bg cream | #FFF4DC | text #1A0B3D 16.59:1, brick accent #B31B17 6.23:1 |
| coin yellow | #FBD000 | #1A0B3D on it 12.18:1; as text on night 12.18:1 |
| brick (fill, button) | #B31B17 | #FFFFFF on it 6.81:1 |
Light-red #E52521 on cream is 4.16:1 and fails: use #B31B17 for text and fills under white.

## Type
**Fixed fonts apply in a mix** (`references/design-system.md` §3a): this spec shows Chakra Petch for body and VT323 for labels, but when mixed
it lends only its display font, class and case; body becomes Manrope and labels JetBrains Mono (re-size labels, since their glyphs are wider).

| role | family | size at 1080 | weight | case | tracking | line-height |
|---|---|---|---|---|---|---|
| cover headline | Press Start 2P | 66px | 400 | upper | 0, word-spacing -.12em | 1.3 |
| headline | Press Start 2P | 58px | 400 | upper | 0, word-spacing -.12em | 1.32 |
| type-only headline | Press Start 2P | 70px | 400 | upper | 0 | 1.3 |
| stat number | Press Start 2P | 170px | 400 | as written | -.02em | 1.05 |
| sub | Chakra Petch | 44px | 600 | sentence | 0 | 1.3 |
| body | Chakra Petch | 40px | 500 | sentence | 0 | 1.36 |
| label, terminal line, HUD label, title bar | VT323 | 50-56px | 400 | upper (terminal as written) | .04em | 1.08 |
| footer | VT323 | 52px | 400 | upper | .06em | 1 |
| button | Press Start 2P | 34px | 400 | upper | 0 | 1 |

Google Fonts: `family=Press+Start+2P&family=Chakra+Petch:wght@500;600;700&family=VT323`.
VT323 has tiny glyphs for its font size, so every VT323 string stays at 46px or more (never at the 34px
floor); Press Start 2P is one weight (400), which is allowed.
**Line length:** Press Start 2P is monospaced at 1em per character, so the 888px frame holds
floor(888 / size) characters: 12 at 70px, 15 at 58px, 13 at 66px. A headline is 6-9 short words on 4-5
lines; break long words or swap them. Never shrink to fit.
Alternates by letterform. A friendlier pixel face that reads at smaller sizes: **Silkscreen**
(`Silkscreen:wght@400;700`, use 700, caps, about 0.75em per character) or **Pixelify Sans**
(`Pixelify+Sans:wght@500;700`, mixed case works). Alternate body: Chakra Petch stays.

## Layout
- 1080 x 1350, margin 96px, flush left. The pixel unit is 6px: every frame step, drop and bar is a multiple.
- Headline top at y 120, then sub-line, then the visual (40-60% of the screen), 64px above the floor.
- Floor: the bottom 126px is a dithered strip (#0C0624) with the footer inside it, `BUILDABLELABS.COM` left
  and the cue right, 52px VT323. The power bar sits at y 1316, 12px tall, in 30px lime segments with 6px
  gaps, width = position / total.
- Stars: single 6px pixels in the margins only (x under 60 or over 1000, or y under 90), plus one or two
  plus-shaped twinkles of 5 pixels. Even slides mirror the star field. They are decoration in `.decor`.

## Emphasis
`colour-word`: one word per headline in #FFD23F with a pink hard drop (`text-shadow:.09em .09em 0 #FF4FA3`);
the rest of the headline is cream with a grape drop. On the yellow CTA screen the key word is yellow on a
#1A0B3D block (padding .08em .18em .02em, no shadow). Body emphasis is Chakra Petch 700 in yellow (night on
the yellow screen).

## Devices
- **Pixel frame** (`pixel-frame`): four box-shadows of 6px in the edge colour make stepped corners:
  `0 -6px 0 0 E, 0 6px 0 0 E, -6px 0 0 0 E, 6px 0 0 0 E` with the box at 6px margin.
- **Hard drop** (`hard-shadow`): `6px 18px 0 0 D, 12px 12px 0 0 D` (pink under hero boxes, grape under small
  ones). No blur anywhere.
- **Dither floor** (`halftone`): a #0C0624 strip topped by two or three rows of 12px conic-gradient checks.
- **Power bar** (`progress-bar`): `repeating-linear-gradient(90deg, #9BFF4A 0 30px, transparent 30px 36px)`.
- **Pixel arrow**: a 30 x 18px stepped clip-path in pink or cream, used for flow arrows and the dialog
  "next" cursor.

## Visual style
`pixel`: native game UI built from flat blocks. Windows have a pink title bar with a VT323 lowercase label
and a deep body; HUDs show 66-72px pixel hearts (full pink, empty grape) and a 60px segmented XP bar in lime;
inventory slots are deep boxes in a 2-column grid, the equipped one yellow with a pink "EQUIPPED" tab; flows
are pixel chips joined by dashed stepped paths; dialogs are RPG menu windows with a yellow title row, lime
check rows and two buttons. Charts use segmented bars (24px segments). All corners are square, all lines
land on the 6px grid, nothing is tilted. Icons: 2-2.6px stroke, square caps, mitred joins.
Text inside visuals: VT323 at 46px or more, or Chakra Petch 600 at 38px or more.

## Slide recipes
- **Cover (night)**: headline 66px with one yellow word, a cyan sub-line behind a pink pixel arrow, a window
  or HUD visual (show the real product state, not a bare command), floor and power bar.
- **Stake / point (night)**: headline 58px, a flow, HUD or window, one body line.
- **Stat (night)**: the sourced number at 170px in yellow with a pink drop, a source line in VT323 50px, a
  segmented two-bar chart.
- **Steps (night)**: headline 58px, a stage-select list: rows separated by dashed grape rules, each row a
  cyan pixel box holding a glyph or letter (`A`, `B`, `C`; never `1 2 3`) and a 44px Chakra Petch line.
- **Quote (night)**: an RPG dialogue box (deep fill, cream frame, pink drop) with a pink blinking-arrow
  cursor, the speaker in a yellow name tag overlapping the top edge.
- **CTA (yellow screen)**: headline 62px, a dialog checklist, a pink pixel button (night text, night frame);
  the footer has the site only.

## CSS starter
```css
:root{
  --px:6px; --night:#1A0B3D; --deep:#0C0624; --panel:#261552; --grape:#3D2785; --cream:#FFF4DC; --lav:#BDB0FF;
  --yellow:#FFD23F; --pink:#FF4FA3; --cyan:#45E6FF; --lime:#9BFF4A; --edge:var(--cream); --drop:var(--pink);
  --f-display:"Press Start 2P", "Courier New", monospace;
  --f-body:"Chakra Petch", Helvetica, Arial, sans-serif;
  --f-label:"VT323", "Courier New", monospace;
  --frame:0 calc(-1*var(--px)) 0 0 var(--edge),0 var(--px) 0 0 var(--edge),calc(-1*var(--px)) 0 0 0 var(--edge),var(--px) 0 0 0 var(--edge);
  --hard:var(--px) calc(3*var(--px)) 0 0 var(--drop),calc(2*var(--px)) calc(2*var(--px)) 0 0 var(--drop);
}
*{box-sizing:border-box;margin:0;padding:0}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--night);color:var(--cream);font-family:var(--f-body)}
.slide.yellow{--bg:var(--yellow);background:var(--yellow);color:var(--night);--edge:var(--night)}
.decor{position:absolute;inset:0;pointer-events:none;z-index:0}
.stars{position:absolute;left:0;top:0;width:var(--px);height:var(--px);
  box-shadow:34px 300px 0 var(--cream),50px 560px 0 var(--yellow),26px 840px 0 var(--cyan),1034px 196px 0 var(--cream),
    1048px 430px 0 var(--cyan),1022px 700px 0 var(--cream),1044px 980px 0 var(--yellow),150px 50px 0 var(--cream),846px 40px 0 var(--cream)}
.floor{position:absolute;left:0;right:0;bottom:0;height:126px;background:var(--deep)}
.floor::before{content:"";position:absolute;left:0;right:0;top:-24px;height:24px;
  background:conic-gradient(var(--deep) 25%,transparent 0 50%,var(--deep) 0 75%,transparent 0) 0 0/12px 12px repeat-x}
.frame{position:absolute;inset:120px 96px 52px;display:flex;flex-direction:column;gap:48px;z-index:1}
.headline{font-family:var(--f-display);font-weight:400;font-size:58px;line-height:1.32;letter-spacing:0;word-spacing:-.12em;
  text-transform:uppercase;text-shadow:.09em .09em 0 var(--grape);max-width:888px}
.slide[data-type=cover] .headline{font-size:66px;line-height:1.3}
.headline em{font-style:normal;color:var(--yellow);text-shadow:.09em .09em 0 var(--pink)}
.slide.yellow .headline{text-shadow:.09em .09em 0 var(--pink)}
.slide.yellow .headline em{background:var(--night);padding:.08em .18em .02em;text-shadow:none}
.sub{font-weight:600;font-size:44px;line-height:1.3;color:var(--cyan)}
.visual{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:28px;padding:6px}
.box{margin:var(--px);background:var(--deep);color:var(--cream);box-shadow:var(--frame),var(--hard)}
.titlebar{background:var(--pink);color:var(--night);padding:16px 26px 14px;font-family:var(--f-label);font-size:50px;line-height:1;letter-spacing:.04em}
.ln{font-family:var(--f-label);font-size:54px;line-height:1.08;padding:6px 34px}
.ln .pr{color:var(--lime)}
.heart{width:72px;height:auto;fill:var(--pink)} .heart.off{fill:var(--grape)}
.xp{height:60px;margin:var(--px);padding:6px;background:var(--deep);display:flex;gap:6px;box-shadow:var(--frame)}
.xp i{flex:1;background:var(--panel)} .xp i.on{background:var(--lime)}
.slot{min-height:250px;padding:34px 30px;background:var(--deep);box-shadow:var(--frame),var(--hard);
  font-weight:700;font-size:40px;line-height:1.1;display:flex;align-items:flex-end}
.slot.on{background:var(--yellow);color:var(--night)}
.btn{display:inline-block;background:var(--pink);color:var(--night);font-family:var(--f-display);font-size:34px;line-height:1;
  padding:28px 36px 26px;margin-left:var(--px);box-shadow:var(--frame),var(--hard)}
.foot{position:absolute;left:96px;right:96px;bottom:60px;z-index:2;display:flex;justify-content:space-between;align-items:center;
  font-family:var(--f-label);font-size:52px;line-height:1;letter-spacing:.06em;text-transform:uppercase;color:var(--lav)}
.foot .cue{color:var(--yellow)}
.progress{position:absolute;left:0;bottom:22px;height:12px;z-index:3;background:repeating-linear-gradient(90deg,var(--lime) 0 30px,transparent 30px 36px)}
```

## Mix notes
- Lends best: **type** (pixel caps) and **visual_style** (pixel game UI), either of which turns a calm design
  playful. The status-bar floor and segmented power bar are small, portable **devices**.
- Pairs well with: `pop` flat colour blocks for a bright arcade, `swiss-grid` layout (the 6px unit and the grid
  agree), `cards` UI structure under pixel type, `poster` colour rhythm.
- Clashes: `zine` hand-drawn marks (curvy against pixel), `headline-mix` size-jump with Press Start 2P (too wide),
  soft shadows, rounded corners and gradients of any kind. Wrong for serious leadership topics; right for
  dev tools, games, plugins and playful how-tos.

## House-rule overrides
- No logos or brand lockups, and no game characters or console marks.
- No slide numbers or ghost numerals: no "LEVEL 3", "STAGE 2/6", "1UP" or "SCORE" counters that follow the
  slide position, and no inventory slot numerals (the judge flagged the shipped 1 to 4 corner keys as clutter
  and a G7 risk). List marks are letters or glyphs, never `01 02 03`.
- Nothing readable above the headline: the shipped theme hid its kicker and counter; do the same. Stars are
  single pixels in the margins, never glyphs.
- Nothing under 34px by font-size, and nothing below weight 400. VT323 and Press Start 2P are 46px and 58px or
  more in this design, so their small-looking glyphs still read on a phone.
- No photos or sprites of people or characters: draw UI boxes, hearts and shapes.
- Keep hard drops and stars clear of copy (G3), and keep the grape tone off any text (1.58:1).
- Footer `BUILDABLELABS.COM` bottom-left in the floor, swipe cue bottom-right, no cue on the last slide.
