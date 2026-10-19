# brutal

```json
{
  "name": "brutal",
  "kind": "library",
  "sources": [],
  "mode": "colour",
  "background": "#FFE14D",
  "accent": "#111111",
  "palette": ["#111111", "#FFFFFF", "#FFE14D", "#FF6FB5", "#6EE7B7", "#B9A5FF", "#FF7F3F", "#7CC8FF", "#4A4A4A"],
  "fonts": {"display": "Archivo Black", "body": "Space Grotesk", "label": "Space Mono"},
  "google_fonts": ["Archivo+Black", "Space+Grotesk:wght@500;700", "Space+Mono:wght@400;700"],
  "type": {"display_class": "sans-heavy", "case": "sentence"},
  "layout": "stack-top",
  "emphasis": "sticker-word",
  "devices": ["hard-shadow", "outline-boxes", "badges", "progress-bar"],
  "visual_style": "hard-shadow-blocks",
  "visual_kinds": ["checklist", "window", "compare", "flow", "tags", "chart", "hud", "dialog", "big-number"]
}
```

## Look
Neo-brutalist posters in the Gumroad and Figma-community mould. Every slide is one loud flat colour from a
rotating sequence (lemon, pink, mint, lilac, orange, sky), all text is black ink, and everything that is a
box has a 5px black outline and a hard offset shadow with no blur. One headline word sits on a tilted
sticker. Visuals are white outlined cards stacked like paper cut-outs. Nothing is subtle, nothing is rounded
beyond a few pixels.

## Palette
| role | hex | use |
|---|---|---|
| ink | #111111 | all text, outlines, shadows, footer tag |
| paper | #FFFFFF | cards, list rows, sub-line card |
| slide colours in sequence | #FFE14D lemon, #FF6FB5 pink, #6EE7B7 mint, #B9A5FF lilac, #FF7F3F orange, #7CC8FF sky | one per slide, repeating after 6 |
| pop (sticker, button, chip) | the next colour in the cycle | emphasis sticker, button, window title bar |
| dim | #4A4A4A | secondary text inside white cards |
| black slide | #111111 | the quote or key-claim slide, with white text and lemon stickers |

Text pairs: ink #111111 on lemon 14.5:1 · on pink 7.37:1 · on mint 12.39:1 · on lilac 8.89:1 · on orange
7.52:1 · on sky 10.4:1 · on white 18.88:1 · #FFFFFF on #111111 18.88:1 · #FFE14D on #111111 14.5:1 ·
#FF6FB5 on #111111 7.37:1 · #4A4A4A on #FFFFFF 8.86:1. Ink is the only text colour on coloured slides; white
or colour text on a coloured slide is never used.
The pop pairs rotate so the sticker never matches the slide: lemon slide pops pink, pink pops lemon, mint
pops lilac, lilac pops lemon, orange pops sky, sky pops pink.

### Alternate palettes
**Riso pastel (new):** softer, still flat, still outlined in ink.
| role | hex | contrast of #111111 on it |
|---|---|---|
| slide colours | #FFC9E4, #C9F27A, #E8E1FF, #FFD166, #F2EBD9 | 13.24, 14.81, 14.97, 13.1, 15.88:1 |
| pop colours | #FF8FA3, #74B9FF | 8.73, 9.11:1 |
**Paper, acid and cobalt (new):** one acid colour on warm paper, one blue slide.
| role | hex | contrast |
|---|---|---|
| paper slide | #F4EFE6 | ink 16.49:1 |
| acid slide and stickers | #D7FF3F | ink 16.42:1 |
| cobalt slide | #1236FF | #FFFFFF on it 7.01:1 (the only slide with white text) |
| hot red sticker | #FF4D2E | ink 5.71:1 |
**Night mode (new):** dark ink slides with acid and pink. Slide #2B2D42 with text #FFFFFF 13.49:1, stickers
#FFD166 with ink 13.1:1; frames and shadows #FFFFFF.

## Type
**Fixed fonts apply in a mix** (`references/design-system.md` §3a): this spec shows Space Grotesk for body and Space Mono for labels, but when mixed
it lends only its display font, class and case; body becomes Manrope and labels JetBrains Mono (re-size labels, since their glyphs are wider).

| role | family | size at 1080 | weight | case | tracking | line-height |
|---|---|---|---|---|---|---|
| cover headline | Archivo Black | 108px | 400 | sentence | -.03em | .98 |
| headline | Archivo Black | 80px (steps 70px) | 400 | sentence | -.03em | 1.0 |
| small headline | Archivo Black | 56px | 400 | sentence | -.02em | 1.06 |
| stat number | Archivo Black | 260px | 400 | as written | -.04em | .92 |
| sub / body | Space Grotesk | 40px | 500 / 700 | sentence | 0 | 1.3 |
| list item | Space Grotesk | 40px | 500 | sentence | 0 | 1.25 |
| label, footer, terminal line | Space Mono | 34-38px | 700 | as written / upper | .04em | 1.25 |
| button | Space Grotesk | 51px | 700 | sentence | 0 | 1 |

Google Fonts: `family=Archivo+Black&family=Space+Grotesk:wght@500;700&family=Space+Mono:wght@400;700`.
Archivo Black is one weight (400), which is allowed. About 0.6em per character: the 904px frame holds about
14 characters per line at 108px and 19 at 80px; set long words by hand. Alternates by letterform: a more
condensed shouty display, **Anton** (`Anton`, 400, 0.46em per character); a rounder heavy,
**Bricolage Grotesque** (`Bricolage+Grotesque:opsz,wght@12..96,500..800`, 800); body alternates **DM Sans**
(`DM+Sans:wght@500;700`) and label **IBM Plex Mono** (`IBM+Plex+Mono:wght@500;700`).

## Layout
- 1080 x 1350, margin 88px, flush left. Headline top at y 130, then sub-line, then the visual (40-60% of the
  height), then the footer at y 1262. 36px between blocks.
- Footer: the site left in Space Mono 700 34px, a black swipe tag right (ink fill, slide-colour text, 5px
  shadow in the pop colour, tilted -2deg). No cue on the last slide.
- Progress bar: 16px, ink, flush to the bottom edge, width = position / total.
- Cards sit slightly off-grid: visuals are 56px narrower than the frame and shifted 8px right so the
  shadows breathe. Stickers and cards may be rotated -2 to +2 degrees; the text inside rotates with them.
- An optional starburst sticker (a 12-point star in the pop colour with a black outline and shadow) may sit
  in the bottom-right corner on slides without a visual. Never under text.

## Emphasis
`sticker-word`: one word per headline on a tilted sticker:
`display:inline-block; background:var(--pop); border:5px solid #111; border-radius:.12em;
box-shadow:6px 6px 0 #111; padding:.04em .14em .1em; margin:.06em .02em .1em; transform:rotate(-2deg);
line-height:1`. Ink text on the pop colour. Keep a 10px gap above and below so stickers never touch other
lines (use `margin:.1em 0` and the headline `line-height:1.12`). On the black slide the sticker is lemon with
a pink shadow and lemon border.

## Devices
- **Hard shadow** (`hard-shadow`): `box-shadow:10px 10px 0 #111` on hero cards, `6px 6px 0 #111` on small
  ones, `5px 5px 0 var(--pop)` on the footer tag. Never a blur.
- **Outline** (`outline-boxes`): 5px #111 borders, radii 8-16px, on every card, chip, tag and button.
- **Badges** (`badges`): small chips with a 3-4px border and a 3px shadow, e.g. `HEALTH` or `XP` tags.
- **Chunky bar**: a 132 x 18px ink rule with a pop shadow above a headline, only on slides with no visual
  (it holds no text, so it is not a kicker).
- **Progress bar**: as above.

## Visual style
`hard-shadow-blocks`: white cards with thick outlines, stacked as if cut from paper. Windows have a pop-colour
title bar with three coloured 26px dots (orange, lemon, mint) and mono labels; terminal text is Space Mono
at 38px. HUD hearts are pink with a black outline made of `drop-shadow` copies; the XP bar is a white track
with ink segments. Lists are stacked white cards with a 66px square chip (pop colour, 4px border, letter
inside). Compare is two cards, the "after" card in a pop colour. Flows are outlined chips joined by 4px
ink arrows. Charts are ink bars in white tracks with a 4px border, the winner in a pop colour. The big
number is outlined text (`-webkit-text-stroke:7px #111`, `paint-order:stroke fill`) with a 12px shadow.
Icons: 2.4-2.6px stroke, round joins. All diagram text is Space Mono 700 34px or Space Grotesk 700 38px.

## Slide recipes
- **Cover (lemon)**: headline 108px with a sticker word, a white sub-line card tilted -1deg, a window or
  checklist visual with a toast sticker on its corner, footer with the black swipe tag.
- **Stake / point (pink, mint, lilac)**: headline 80px with a sticker word, one white-card visual (flow,
  compare, tags), body line.
- **Stat (any colour)**: the sourced number at 260px, outlined, one line under it, the source in mono,
  a two-bar chart in a white card.
- **Steps (orange)**: headline 70px, three stacked white cards with letter chips (`A`, `B`, `C`), the
  active one in the pop colour.
- **Quote (black)**: lemon quote mark 300px, white 72px headline with a lemon sticker word, pink shadows.
- **CTA (sky)**: headline 86px with a sticker word, a white dialog checklist, a pop-colour button with a
  5px outline and 10px shadow; the footer has the site only.

## CSS starter
```css
:root{
  --ink:#111111; --paper:#FFFFFF; --bg:#FFE14D; --pop:#FF6FB5; --pop2:#6EE7B7; --bw:5px;
  --sh:10px 10px 0 #111111; --sh-sm:6px 6px 0 #111111; --m:88px;
  --f-display:"Archivo Black", "Arial Black", Impact, sans-serif;
  --f-body:"Space Grotesk", Helvetica, Arial, sans-serif;
  --f-label:"Space Mono", "Courier New", monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--f-body)}
.slide.c2{--bg:#FF6FB5;--pop:#FFE14D;--pop2:#7CC8FF} .slide.c3{--bg:#6EE7B7;--pop:#B9A5FF;--pop2:#FFE14D}
.slide.c4{--bg:#B9A5FF;--pop:#FFE14D;--pop2:#FF6FB5} .slide.c5{--bg:#FF7F3F;--pop:#7CC8FF;--pop2:#FFE14D}
.slide.c6{--bg:#7CC8FF;--pop:#FF6FB5;--pop2:#FFE14D}
.slide.black{--bg:#111111;--pop:#FFE14D;--pop2:#FF6FB5;color:#FFF}
.decor{position:absolute;inset:0;pointer-events:none;z-index:0}
.frame{position:absolute;inset:var(--m);top:130px;display:flex;flex-direction:column;gap:36px;z-index:1}
.headline{font-family:var(--f-display);font-weight:400;font-size:80px;line-height:1.12;letter-spacing:-.03em;max-width:904px;text-wrap:balance}
.slide[data-type=cover] .headline{font-size:108px;line-height:1.05}
.mark{display:inline-block;line-height:1;margin:.1em .02em;padding:.04em .14em .1em;color:#111;background:var(--pop);
  border:var(--bw) solid #111;border-radius:.12em;box-shadow:var(--sh-sm);transform:rotate(-2deg)}
.slide.black .mark{border-color:#FFE14D;box-shadow:6px 6px 0 #FF6FB5}
.sub{align-self:flex-start;max-width:820px;background:var(--paper);color:#111;font-weight:700;font-size:42px;line-height:1.22;
  padding:16px 26px;border:var(--bw) solid #111;border-radius:12px;box-shadow:var(--sh-sm);transform:rotate(-1deg)}
.visual{flex:1;min-height:0;width:calc(100% - 56px);margin-left:8px;display:flex;flex-direction:column;justify-content:center;gap:22px}
.card{background:var(--paper);color:#111;border:var(--bw) solid #111;border-radius:12px;box-shadow:var(--sh-sm);padding:20px 26px;
  font-size:40px;font-weight:500;line-height:1.25}
.card.hero{border-radius:16px;box-shadow:var(--sh);padding:0;overflow:hidden}
.titlebar{display:flex;align-items:center;gap:12px;background:var(--pop);border-bottom:var(--bw) solid #111;padding:16px 24px;
  font-family:var(--f-label);font-weight:700;font-size:36px;letter-spacing:.04em}
.titlebar i{width:26px;height:26px;border:4px solid #111;background:#FFF}
.titlebar i:nth-child(1){background:#FF7F3F} .titlebar i:nth-child(2){background:#FFE14D} .titlebar i:nth-child(3){background:#6EE7B7}
.ln{font-family:var(--f-label);font-size:38px;line-height:1.25;padding:6px 34px}
.row{display:flex;align-items:center;gap:24px}
.chip{flex:none;width:66px;height:66px;display:grid;place-items:center;background:var(--pop);border:4px solid #111;border-radius:8px;
  font-family:var(--f-label);font-weight:700;font-size:39px}
.tag{display:inline-block;font-family:var(--f-label);font-weight:700;font-size:36px;background:var(--pop2);border:3px solid #111;
  border-radius:8px;padding:6px 14px 5px;box-shadow:3px 3px 0 #111}
.num{font-family:var(--f-display);font-size:260px;line-height:.92;letter-spacing:-.04em;color:var(--pop);
  -webkit-text-stroke:7px #111;paint-order:stroke fill;text-shadow:12px 12px 0 #111}
.btn{display:inline-flex;align-items:center;gap:18px;background:var(--pop);color:#111;border:var(--bw) solid #111;border-radius:14px;
  box-shadow:var(--sh);font-weight:700;font-size:51px;padding:24px 38px 24px 32px}
.source{font-family:var(--f-label);font-weight:700;font-size:34px;letter-spacing:.04em;text-transform:uppercase}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-family:var(--f-label);font-weight:700;font-size:34px;letter-spacing:.06em}
.foot .cue{background:#111;color:var(--bg);padding:12px 18px 11px;box-shadow:5px 5px 0 var(--pop);transform:rotate(-2deg)}
.progress{position:absolute;left:0;bottom:0;height:16px;background:#111;z-index:2}
```

## Mix notes
- Lends best: **devices** (hard shadows, thick outlines, stickers) and **visual_style** (outlined paper cards).
  The slide-by-slide colour rotation is a strong **colour** donor for any flat design.
- Pairs well with: `pop` shapes behind the cards, `swiss-grid` layout (outlined cells), `arcade` type
  (pixel headline over hard-shadow cards), `headline-mix` size-jump with a sticker word.
- Clashes: `cards` (rounded soft cards vs hard blocks), `poster` swoop and script word, `zine` tape, any
  gradient or blur. Do not combine two emphasis marks, or round corners past 16px.

## House-rule overrides
- No logos or brand lockups, and no mascots or illustrated characters.
- No slide numbers or ghost numerals: list chips hold letters or glyphs, never `01 02 03` and never a
  number that matches the slide position. The shipped steps used `WEEK 1` labels inside rows, which are
  fine as content only if they are not zero-padded counters.
- Nothing readable above the headline: the shipped theme hid its kicker and counter; keep it that way. The
  chunky bar above a headline is a plain ink rule with no text.
- Nothing under 34px, no weight under 400: Space Mono labels are 34px or more, Space Grotesk is 500 or 700.
- Stickers and toasts sit on card corners, with their text fully inside their own chip (G3). A sticker never
  touches the line above or below it.
- No photos of people or stock photos: draw cards, shapes and icons.
- Footer `BUILDABLELABS.COM` bottom-left, black swipe tag bottom-right, no tag on the last slide.
