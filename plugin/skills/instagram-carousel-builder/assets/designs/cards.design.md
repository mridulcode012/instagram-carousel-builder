# cards

```json
{
  "name": "cards",
  "kind": "library",
  "sources": [],
  "mode": "alternating",
  "background": "#C3D4FA",
  "accent": "#0B3FDE",
  "palette": ["#C3D4FA", "#0A0B0E", "#F5F6F8", "#FFFFFF", "#1A1D24", "#0B3FDE", "#6789EC", "#565D6E"],
  "fonts": {"display": "Manrope", "body": "Manrope", "label": "JetBrains Mono"},
  "google_fonts": ["Manrope:wght@500;600;700;800", "JetBrains+Mono:wght@500;700"],
  "type": {"display_class": "sans-heavy", "case": "sentence"},
  "layout": "card-on-canvas",
  "emphasis": "highlight-block",
  "devices": ["badges", "speech-bubbles", "blobs", "progress-bar"],
  "visual_style": "ui-mockup",
  "visual_kinds": ["checklist", "dialog", "chart", "big-number", "quote-bubble", "flow", "compare", "slots"]
}
```

## Look
A friendly product-UI system. Slides rotate between a pale tint, off-white and near-black, with the odd
full-blue slide. Headlines are bold sentence-case sans at the top left; everything else lives in big-radius
rounded cards: list rows as stacked cards with a round chip and an arrow chip, a quote as a chat thread, a
stat as a number in a blue panel. Labels sit in pills, the button is a pill with an icon disc, and a dark
curved wave runs along the bottom of the cover and CTA.

## Palette
Each slide picks one tone; cards invert against the slide.
| tone | slide bg | text / muted | card / card text / card muted | accent |
|---|---|---|---|---|
| tint (odd slides, cover, CTA) | #C3D4FA | #0A0B0E / #2C3444 | #FFFFFF / #0A0B0E / #565D6E | #0B3FDE |
| off-white (every 4th: 3, 7) | #F5F6F8 | #0A0B0E / #565D6E | #C3D4FA / #0A0B0E / #2C3444 | #0B3FDE |
| dark (even slides) | #0A0B0E | #F5F6F8 / #B8BECC | #1A1D24 / #F5F6F8 / #B8BECC | #6789EC |
| blue (quote, key claim) | #0B3FDE | #FFFFFF / #C3D4FA | #F5F6F8 / #0A0B0E / #565D6E | #FFFFFF |
Chip #0B3FDE with #FFFFFF text; on the blue slide the chip is #0A0B0E. Panel (stat, button on tint)
#0A0B0E with #F5F6F8 text on tint and dark; #0B3FDE with #FFFFFF text on off-white. The last list row is the
active card: #0B3FDE with white text (#0A0B0E on the blue slide). The wave is #0A0B0E.

Text pairs: #0A0B0E on #C3D4FA 13.23:1 · #2C3444 on #C3D4FA 8.39:1 · #0B3FDE on #C3D4FA 5.08:1 ·
#0A0B0E on #FFFFFF 19.68:1 · #565D6E on #FFFFFF 6.59:1 · #0A0B0E on #F5F6F8 18.2:1 · #565D6E on #F5F6F8
6.09:1 · #F5F6F8 on #0A0B0E 18.2:1 · #B8BECC on #0A0B0E 10.57:1 · #6789EC on #0A0B0E 5.97:1 · #F5F6F8 on
#1A1D24 15.6:1 · #B8BECC on #1A1D24 9.06:1 · #FFFFFF on #0B3FDE 7.55:1 · #C3D4FA on #0B3FDE 5.08:1.

### Alternate palettes
**Clinic green (sampled by eye from refs/ref-1.png):** deep green, lime, soft grey.
| role | hex | contrast |
|---|---|---|
| bg grey | #E4E4E2 | text #0F4D3A 7.7:1, muted #3B4A44 7.33:1 |
| bg deep green | #0F4D3A | text #F2F5EE 8.9:1, lime #BDE55B 6.78:1 |
| bg lime | #BDE55B | text #0F4D3A 6.78:1 |
| card / chip | #FFFFFF / #0F4D3A | #0F4D3A on white 9.8:1, white on green 9.8:1 |
**Lime and ink (sampled from refs/ref-10.png):** acid lime and charcoal.
| role | hex | contrast |
|---|---|---|
| bg lime | #C6E81A | text #171712 12.81:1, small accent text #4A4F12 6.19:1 |
| bg ink | #171712 | text #F1F3E4 16.0:1, lime #C6E81A 12.81:1 |
| card | #FFFFFF or #2B2B25 | #171712 on white 17.98:1, lime on #2B2B25 10.14:1 |
**Peach and plum (new):** warm and soft.
| role | hex | contrast |
|---|---|---|
| bg peach | #FFE9DC | text #2B1B3D 13.52:1, muted #5A4666 7.17:1, coral accent #C2331F 4.74:1 |
| bg plum | #2B1B3D | text #FFE9DC 13.52:1, accent #F2B8AE 9.23:1 |
| card / chip | #FFFFFF / #C2331F | #2B1B3D on white 15.83:1, white on coral 5.55:1 |

## Type
| role | family | size at 1080 | weight | case | tracking | line-height |
|---|---|---|---|---|---|---|
| cover headline | Manrope | 112px | 800 | sentence | -.035em | 1.1 |
| headline | Manrope | 88px (steps 76px) | 800 | sentence | -.035em | 1.04 |
| small headline | Manrope | 62px | 700 | sentence | -.025em | 1.12 |
| stat number | Manrope | 240px | 800 | as written | -.05em | .9 |
| sub / body | Manrope | 38px | 500 | sentence | 0 | 1.4 |
| card text | Manrope | 40px | 600 | sentence | 0 | 1.25 |
| chat quote | Manrope | 54px | 700 | sentence | -.02em | 1.2 |
| label, pill, source, footer | JetBrains Mono | 34px | 500 / 700 | upper | .1em | 1 |
| button | Manrope | 36px | 700 | sentence | -.005em | 1 |

Google Fonts: `family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@500;700`.
Alternates by letterform. The ref-1 clinic feel is a clean humanist grotesk: **Plus Jakarta Sans**
(`Plus+Jakarta+Sans:wght@500;600;700;800`) or **DM Sans** (`DM+Sans:wght@500;700`). The ref-10 delivery look
has quirky open forms: **Bricolage Grotesque** (`Bricolage+Grotesque:opsz,wght@12..96,500..800`, 800,
tracking -.03em). Labels: **DM Mono** (`DM+Mono:wght@500`).

## Layout
- 1080 x 1350, margin 88px, flush left. Frame x 88..992. Headline top at y 150, then sub-line, then the
  visual (40-60% of the slide), then the footer at y 1262. 40px between blocks.
- Cards: radius 40-48px, padding 32px, 20px gap. Panels and chat bubbles: radius 48-56px, with the corner
  nearest the speaker squared to 10px.
- Footer pills sit at the bottom: the site in a pill with a 14px dot on the left, the cue in a blue pill on
  the right (no cue on the last slide).
- Cover and CTA: the wave covers the bottom 260px behind the footer only; the visual sits above it, so the
  wave never meets copy. On the other slides there is no wave.
- Progress bar: 8px, flush to the bottom edge, rounded on the right end, width = position / total.

## Emphasis
`highlight-block`: one word per headline on a rounded block:
`display:inline-block; background:var(--em-bg); color:var(--em-text); padding:.04em .16em .1em;
border-radius:.22em; line-height:1; margin:.08em .02em 0`. Blue block with white text on tint, off-white and
dark slides; #0A0B0E block with white text on the blue slide. The headline gets `line-height:1.18` when it
holds a block, so the block never touches the line above. Body emphasis is Manrope 700, no block.

## Devices
- **Pills and chips** (`badges`): round-ended tags with 2px borders or solid fills for labels and chips; a
  round 84px chip holds a letter or glyph; an arrow chip (60px circle, 2px border) ends each list row.
- **Chat bubbles** (`speech-bubbles`): the quote as a bubble (radius 48px, bottom-left corner 10px) in the
  card colour; the attribution as a dark reply bubble, right aligned, bottom-right corner 10px.
- **Wave** (`blobs`): a dark curve along the bottom of the cover and CTA: a #0A0B0E rounded shape
  (`border-radius:50% 50% 0 0 / 100% 100% 0 0`, 260px tall, 140% wide, offset -20%), behind the footer only.
- **Sparkles**: 4-point stars at 34-58px in the accent, one or two per slide, in a corner clear of text. They
  are decoration in `.decor` only.
- **Progress bar** as above.

## Visual style
`ui-mockup`: friendly app screens built from rounded cards. Cards are flat (no shadow), or a soft
`0 20px 40px rgba(10,11,14,.12)` on light tones only. Rows: a 84px circle chip with a letter or glyph, 40px
text, an arrow chip; the last row filled blue. Dialogs: a rounded window with a title row, check rows and a
pill button. Charts: rounded bars on rounded tracks, 56px tall, the key bar in blue, values in mono. Big
numbers sit in a rounded blue panel. Flows: pill chips joined by 3px rounded connectors. Compare: two cards,
the "after" card filled blue. Icons: 2.2px stroke, round joins, inside a 76px disc when on a button.
All diagram text is Manrope 600 38px or JetBrains Mono 34px.

## Slide recipes
- **Cover (tint)**: headline 112px with a blue block word, sub-line, a UI card stack as the infographic (three
  rounded rows, one active, or a chat thread), wave and footer pills at the bottom.
- **Stake / point (dark or off-white)**: headline, a round icon chip above or beside it only if it is a
  glyph (never text), body inside a rounded card, a small visual.
- **Stat (off-white)**: the sourced number at 240px in a rounded blue panel with a sparkle, one line of
  sub-text under it, the source in a pill.
- **Steps (dark)**: headline 76px, 3 stacked cards with letter chips (`A`, `B`, `C`) and arrow chips, the last
  card active blue.
- **Quote (blue)**: a round quote chip, the quote as a chat bubble, the attribution as a dark reply bubble.
- **Recap (tint)**: check rows as cards, no arrows.
- **CTA (tint)**: headline 96px, a pill button (36px, an icon disc in a contrasting colour), the wave and the
  site-only footer.

## CSS starter
```css
:root{
  --bg:#C3D4FA; --text:#0A0B0E; --muted:#2C3444; --accent:#0B3FDE; --card:#FFFFFF; --card-text:#0A0B0E;
  --card-muted:#565D6E; --chip:#0B3FDE; --chip-text:#FFFFFF; --em-bg:#0B3FDE; --em-text:#FFFFFF;
  --btn:#0A0B0E; --btn-text:#FFFFFF; --btn-disc:#0B3FDE; --line:rgba(10,11,14,.14); --m:88px;
  --f-display:"Manrope", Helvetica, Arial, sans-serif;
  --f-label:"JetBrains Mono", Menlo, monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--bg);color:var(--text);font-family:var(--f-display)}
.slide.off{--bg:#F5F6F8;--muted:#565D6E;--card:#C3D4FA;--card-muted:#2C3444}
.slide.dark{--bg:#0A0B0E;--text:#F5F6F8;--muted:#B8BECC;--accent:#6789EC;--card:#1A1D24;--card-text:#F5F6F8;
  --card-muted:#B8BECC;--btn:#0B3FDE;--btn-disc:#0A0B0E;--line:#22242B}
.slide.blue{--bg:#0B3FDE;--text:#FFFFFF;--muted:#C3D4FA;--accent:#FFFFFF;--card:#F5F6F8;--chip:#0A0B0E;
  --em-bg:#0A0B0E;--btn:#FFFFFF;--btn-text:#0A0B0E;--btn-disc:#0B3FDE;--line:rgba(255,255,255,.3)}
.decor{position:absolute;inset:0;pointer-events:none;z-index:0}
.wave{position:absolute;left:-20%;right:-20%;bottom:0;height:260px;background:#0A0B0E;border-radius:50% 50% 0 0/100% 100% 0 0}
.spark{position:absolute;width:58px;height:58px;top:100px;right:96px;background:var(--accent);
  clip-path:polygon(50% 0,60% 40%,100% 50%,60% 60%,50% 100%,40% 60%,0 50%,40% 40%)}
.frame{position:absolute;inset:var(--m);top:150px;display:flex;flex-direction:column;gap:40px;z-index:1}
.headline{font-weight:800;font-size:88px;line-height:1.04;letter-spacing:-.035em;max-width:820px;text-wrap:balance}
.slide[data-type=cover] .headline{font-size:112px;line-height:1.1}
.headline:has(.mark){line-height:1.18}
.mark{display:inline-block;line-height:1;padding:.04em .16em .1em;margin:.08em .02em 0;border-radius:.22em;background:var(--em-bg);color:var(--em-text)}
.sub{font-size:38px;font-weight:500;line-height:1.4;color:var(--muted);max-width:820px}
.visual{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:20px}
.card{background:var(--card);color:var(--card-text);border-radius:40px;padding:32px;font-size:40px;font-weight:600;line-height:1.25}
.row{display:flex;align-items:center;gap:28px}
.row .chip{flex:none;width:84px;height:84px;border-radius:50%;display:grid;place-items:center;background:var(--chip);color:var(--chip-text);
  font-family:var(--f-label);font-weight:700;font-size:38px}
.row .txt{flex:1}
.row::after{content:"→";flex:none;width:60px;height:60px;border-radius:50%;display:grid;place-items:center;font-size:34px;
  border:2px solid color-mix(in srgb,var(--card-text) 18%,transparent)}
.row.active{background:#0B3FDE;color:#FFF}
.row.active .chip{background:#FFF;color:#0B3FDE}
.panel{background:#0A0B0E;color:#F5F6F8;border-radius:56px;padding:64px}
.num{font-size:240px;font-weight:800;line-height:.9;letter-spacing:-.05em}
.bubble{background:var(--card);color:var(--card-text);border-radius:48px 48px 48px 10px;padding:52px 56px;font-size:54px;font-weight:700;letter-spacing:-.02em;line-height:1.2}
.bubble.reply{align-self:flex-end;background:#0A0B0E;color:#F5F6F8;border-radius:40px 40px 10px 40px;padding:22px 30px;font-family:var(--f-label);font-size:34px;letter-spacing:.08em;text-transform:uppercase}
.pill{display:inline-flex;align-items:center;gap:24px;border-radius:999px;background:var(--btn);color:var(--btn-text);padding:16px 44px 16px 16px;font-size:36px;font-weight:700}
.pill .disc{width:76px;height:76px;border-radius:50%;background:var(--btn-disc);color:#FFF;display:grid;place-items:center}
.foot{margin-top:auto;position:relative;z-index:2;display:flex;justify-content:space-between;align-items:center;
  font-family:var(--f-label);font-size:34px;letter-spacing:.1em;text-transform:uppercase}
.foot>span{display:inline-flex;align-items:center;gap:12px;padding:12px 22px;border-radius:999px;line-height:1;white-space:nowrap}
.foot .site{border:2px solid var(--line);color:var(--muted)}
.foot .site::before{content:"";width:14px;height:14px;border-radius:50%;background:var(--accent)}
.foot .cue{background:var(--chip);color:var(--chip-text);font-weight:700}
.progress{position:absolute;left:0;bottom:0;height:8px;border-radius:0 8px 8px 0;background:var(--accent);z-index:3}
```

## Mix notes
- Lends best: **visual_style** (rounded UI cards, chat bubbles, panels) and **layout** (content held in cards
  on a calm canvas). The pill chrome is a good **devices** donor for quiet designs.
- Pairs well with: `swiss-grid` (cards snapped to cells), `poster` or `headline-mix` type over card visuals,
  `pop` flat colour on the panels, `zine` hand marks on a card (use sparingly).
- Clashes: `brutal` hard shadows and thick outlines on the same rounded cards, `arcade` pixel frames, `zine`
  tape across a card edge. Round corners and sharp corners should not share a slide.

## House-rule overrides
- No logos or brand lockups: ref-1's "Nurnberg" clinic mark and ref-10's "Sendam" mark and url in every tile
  are dropped. No handle or url except our footer.
- The shipped theme's mono kicker pill at the top and counter pill (top right) are banned: nothing readable
  above the headline, and no counters. The shipped round number chips (`01`, `02`, `03`) are replaced with
  letters or glyphs, never zero-padded (they read as slide numbers, gate G7).
- A decorative round icon chip above the headline must be a glyph with no text, in `.decor`.
- Nothing under 34px, no weight under 400: ref-1's tiny pills and ref-10's small subtext are not copied.
- No photos of people or stock photos: ref-1 uses doctor portraits and phone photos; ref-10 uses illustrated
  people, boxes and houses with flat shading. Draw simple UI cards or shapes instead.
- Rounded corners up to 56px are part of this design; do not mix them with 4px corners on one slide.
- Footer `BUILDABLELABS.COM` bottom-left in its pill, swipe cue bottom-right, no cue on the last slide.
