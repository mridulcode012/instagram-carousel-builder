# swiss-grid

```json
{
  "name": "swiss-grid",
  "kind": "library",
  "sources": [],
  "mode": "light",
  "background": "#F5F6F8",
  "accent": "#0B3FDE",
  "palette": ["#F5F6F8", "#0A0B0E", "#565D6E", "#0B3FDE", "#FFFFFF"],
  "fonts": {"display": "Manrope", "body": "Manrope", "label": "JetBrains Mono"},
  "google_fonts": ["Manrope:wght@500;600;700;800", "JetBrains+Mono:wght@500;700"],
  "type": {"display_class": "sans-heavy", "case": "sentence"},
  "layout": "grid-modules",
  "emphasis": "highlight-block",
  "devices": ["visible-grid", "rules"],
  "visual_style": "editorial-line",
  "visual_kinds": ["chart", "timeline", "checklist", "big-number", "compare", "slots", "flow"]
}
```

## Look
An off-white poster ruled into a strict 4 x 6 grid of thin blue lines, two or three cells filled solid
blue. A huge, tight heavy grotesque headline sits flush left and runs across the grid lines; everything
else (lists, bars, numbers) snaps to the cells.

## Palette
| role | hex | use |
|---|---|---|
| bg | #F5F6F8 | slide background |
| text | #0A0B0E | headline, body, list items |
| muted | #565D6E | source line, secondary labels |
| accent | #0B3FDE | grid rules, list indexes, stat number, swipe cue, chart strokes |
| fill | #0B3FDE | solid cells, emphasis block, bars, button |
| on-fill | #FFFFFF | any text on a solid cell |

Text pairs: text on bg 18.2:1 · muted on bg 6.09:1 · accent on bg 6.99:1 · on-fill on fill 7.55:1.
Black on the blue fill is 2.61:1 and fails, so text on a blue cell is always white.

Dark variant (same system): bg #0A0B0E, text #F5F6F8 (18.2:1), muted #7A8296 (5.12:1), rules and small
accent text #6789EC (5.97:1), cells #0B3FDE with white text (7.55:1).

### Alternate palettes
**Reference paper** (sampled by eye from refs/ref-2.png): the original's speckled beige card and print blue.

| role | hex | contrast |
|---|---|---|
| bg | #DDD8CC | - |
| text | #161616 | 12.73:1 on bg |
| muted | #55524B | 5.48:1 on bg |
| accent | #1A44D8 | 5.16:1 on bg |
| fill | #1A44D8 | on-fill #FFFFFF 7.34:1 |

**Swiss red** (new): warm white, black and signal red.

| role | hex | contrast |
|---|---|---|
| bg | #F2F0EB | - |
| text | #111111 | 16.58:1 on bg |
| muted | #5A5650 | 6.4:1 on bg |
| accent | #C8201A | 5.01:1 on bg (rules, indexes, cue) |
| fill | #C8201A | on-fill #FFFFFF 5.71:1 |

## Type
| role | family | size at 1080 | weight | case | tracking | line-height |
|---|---|---|---|---|---|---|
| cover headline | Manrope | 112-120px | 800 | sentence | -.042em | 1.0 |
| headline | Manrope | 96px (steps 84px) | 800 | sentence | -.042em | .98 |
| stat number | Manrope | 300px | 800 | - | -.065em | .86 |
| sub / body | Manrope | 38-40px | 500 | sentence | -.01em | 1.22 |
| list item | Manrope | 40px | 700 | sentence | -.02em | 1.15 |
| label (index, cue, site, source) | JetBrains Mono | 34px | 500 / 700 | upper | .08em | 1.2 |

Google Fonts: `family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@500;700`.
Brand font today is Manrope, a little rounder than the reference's neo-grotesque (Helvetica Now style,
double-storey G). Closer letterforms: **Inter Tight** 800 (`Inter+Tight:wght@500;700;800`) or
**Schibsted Grotesk** 800 (`Schibsted+Grotesk:wght@500;700;800`), same sizes and tracking.
Alternate label: IBM Plex Mono 500.

## Layout
- Grid box: x 80..936, y 81..1269. 4 columns of 214px, 6 rows of 198px, 2px rules, outer frame closed.
  The strip x 936..1080 is plain margin (no text).
- Cell (c, r) has its top-left at x = 80 + (c-1)*214, y = 81 + (r-1)*198.
- Row 6 is the footer row on every slide: cols 1-2 are one solid blue cell holding `BUILDABLELABS.COM`
  in white, bottom-left, 28px in from the cell corner. The swipe cue sits bottom-right of col 4, row 6,
  in accent blue.
- Text starts 14px right of a grid line, top-aligned 24px under a rule. The headline ignores column
  lines and runs across them; nothing else does.
- Secondary text hangs from a column line: col 3 (x 508, 396px wide) or col 2 (x 294, 612px wide).
- Cover and CTA: row 1 is decoration only (cols 3-4 solid blue, cols 1-2 empty cells), headline in
  rows 2-3, visual in rows 4-5.
- Middle slides: col 4 row 1 is solid blue, headline in rows 1-2 at max-width 620px (cols 1-3) so it
  never touches blue, visual in rows 3-5 (856 x 594).

## Emphasis
One word per headline sits on a solid blue block with white text. The block is a background gradient
sized to the glyph body (1.04em tall at 62%), not the line box, so the tight .98 leading stays and the
block never bites into the line above. Body and list emphasis is weight 800 in text colour, no block.

## Devices
- **Visible grid** (`visible-grid`): two repeating 2px gradients on `.decor` plus right/bottom borders.
- **Solid cells**: `.cell` divs inside `.decor`, whole cells, 2-3 per slide, only white text on them.
- **Ruled rows** (`rules`): list items carry a 2px accent top border and a fixed height of 198px
  (or 99px with 4+ items) so their rules land exactly on grid rows.
- **Square button** (CTA) and optional blue quote slide: `.btn`, `.slide.fill` below.

## Visual style
Editorial line drawing that obeys the grid. Strokes are 2px accent blue, square caps, no rounding over
4px, no shadows, no gradients, no icons beyond simple 2px stroke glyphs. Data is solid blue bars whose
lengths are whole or half cells; axes are the grid rules themselves. Timelines and flows run along a
row rule with square nodes on column lines. Compare uses two 428px columns: left outlined, right solid
blue with white text. UI mockups are flat rectangles with a 2px accent border and a 2px header rule,
filled bg, text 34px+. All diagram text is Manrope 600 38px or JetBrains Mono 34px.

## Slide recipes
- **Cover**: row 1 blue across cols 3-4; headline 116px rows 2-3 with one emphasis word; infographic
  in rows 4-5 cols 2-4 (642 x 396, e.g. bar chart snapped to cells); col 1 rows 5-6 one tall blue cell
  (the reference's left block) with the site at its bottom; cue bottom-right.
- **Point / stake**: headline rows 1-2 (cols 1-3), visual rows 3-5 full width, sub at col 2 if needed.
- **Steps**: headline 84px rows 1-2; rows 3-5 are three ruled rows, each a mono index (`A`, `B`, `C`
  or a 2px stroke glyph, accent, 72px slot) plus 40px item text and a small 2px stroke glyph at col 4.
- **Stat**: number 300px accent in rows 1-2, one line of 63px headline below it, a bar visual in row
  4-5 comparing the before and after, `.source` in mono 34px muted at the top of row 5 cols 2-4.
- **Compare**: headline rows 1-2; rows 3-5 split into cols 1-2 (outlined, "before") and cols 3-4
  (solid blue, white text, "after").
- **CTA**: as cover; headline 106px rows 2-3; rows 4-5 hold a 3-item checklist and the square button;
  footer has the site only, no cue.

## CSS starter
```css
:root{
  --bg:#F5F6F8; --text:#0A0B0E; --muted:#565D6E; --accent:#0B3FDE; --fill:#0B3FDE; --on-fill:#FFFFFF;
  --f-display:"Manrope", Helvetica, Arial, sans-serif;
  --f-body:"Manrope", Helvetica, Arial, sans-serif;
  --f-label:"JetBrains Mono", Menlo, monospace;
  --col:214px; --row:198px; --gw:2px; --gl:var(--accent);
}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--bg);
  color:var(--text);font-family:var(--f-body)}
.decor{position:absolute;inset:81px 144px 81px 80px;pointer-events:none;z-index:0;
  background-image:
    linear-gradient(90deg,var(--gl) var(--gw),transparent var(--gw)),
    linear-gradient(180deg,var(--gl) var(--gw),transparent var(--gw));
  background-size:var(--col) 100%,100% var(--row);
  background-repeat:repeat-x,repeat-y;
  border-right:var(--gw) solid var(--gl);border-bottom:var(--gw) solid var(--gl)}
/* solid cell: set --c, --r (1-based) and --w, --h (in cells) inline */
.decor .cell{position:absolute;background:var(--fill);
  left:calc((var(--c) - 1) * var(--col));top:calc((var(--r) - 1) * var(--row));
  width:calc(var(--w,1) * var(--col) + var(--gw));height:calc(var(--h,1) * var(--row) + var(--gw))}
.frame{position:absolute;inset:81px 144px 81px 80px;display:flex;flex-direction:column;z-index:1}
.slide[data-type=cover] .frame,.slide[data-type=cta] .frame{padding-top:var(--row)}
.headline{font-family:var(--f-display);font-weight:800;font-size:96px;line-height:.98;
  letter-spacing:-.042em;word-spacing:.05em;margin:24px 0 0 10px;text-wrap:pretty;max-width:620px}
.slide[data-type=cover] .headline{font-size:116px;line-height:1;max-width:none}
.slide[data-type=cta] .headline{font-size:106px;max-width:none}
.slide[data-type=steps] .headline{font-size:84px}
.sub{font-size:38px;font-weight:500;line-height:1.22;letter-spacing:-.01em;color:var(--text);
  margin:32px 0 0 228px;max-width:584px}
.sub.col3{margin-left:442px;max-width:384px}
.visual{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;margin:28px 0}
.visual svg{width:100%;height:100%}
.visual text{font-family:var(--f-body);font-weight:600;font-size:38px;fill:var(--text)}
.visual .on-cell{fill:var(--on-fill)}
.num{font-family:var(--f-display);font-weight:800;font-size:300px;line-height:.86;
  letter-spacing:-.065em;color:var(--accent);margin:24px 0 0 -6px}
.source{font-family:var(--f-label);font-size:34px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.foot{flex:none;height:var(--row);display:flex;justify-content:space-between;align-items:flex-end;
  padding:0 28px 28px;font-family:var(--f-label);font-size:34px;font-weight:500;
  letter-spacing:.06em;text-transform:uppercase}
.foot .site{color:var(--on-fill)}           /* sits on the blue cell at cols 1-2, row 6 */
.foot .cue{color:var(--accent);font-weight:700}
/* emphasis: glyph-height blue block, white text */
.mark{color:var(--on-fill);font-weight:800;padding:0 .1em;margin:0 .02em;
  background:linear-gradient(var(--fill),var(--fill)) 0 62% / 100% 1.04em no-repeat;
  -webkit-box-decoration-break:clone;box-decoration-break:clone}
/* ruled list rows that land on grid rows */
.list{list-style:none;margin-top:auto}
.list li{display:flex;align-items:center;gap:0;height:var(--row);border-top:var(--gw) solid var(--gl);
  font-size:40px;font-weight:700;letter-spacing:-.02em;line-height:1.15;padding-left:14px}
.list:has(li:nth-child(4)) li{height:calc(var(--row) / 2)}
.list .ix{font-family:var(--f-label);font-size:34px;font-weight:700;color:var(--accent);
  min-width:86px;letter-spacing:.08em}
.btn{align-self:flex-start;background:var(--fill);color:var(--on-fill);border-radius:4px;
  font-weight:600;font-size:34px;padding:26px 44px}
/* compare: two 428px halves, left outlined, right solid */
.cmp{display:grid;grid-template-columns:1fr 1fr;width:100%;height:100%}
.cmp>div{padding:24px 28px;font-size:38px;font-weight:600;line-height:1.22}
.cmp>div:first-child{border:var(--gw) solid var(--accent)}
.cmp>div:last-child{background:var(--fill);color:var(--on-fill)}
/* optional quote slide: the whole slide flips to blue */
.slide.fill{background:var(--fill);color:var(--on-fill);--gl:rgba(255,255,255,.45)}
.slide.fill .decor .cell{background:#0A0B0E}
.slide.fill .mark{background-image:linear-gradient(#0A0B0E,#0A0B0E)}
.slide.fill .foot .cue{color:var(--on-fill)}
/* cells: <div class="cell" style="--c:3;--r:1;--w:2"></div> inside .decor; white text only on blue */
```

## Mix notes
- Lends best: **layout** (the 214 x 198 cell grid, snapping) and **devices** (grid, solid cells, ruled
  rows). The heavy tight sans is a good type donor for any flat system.
- Pairs well with: `pop` colour (one flat bright fill in the cells), `cards` UI panels set inside cells,
  `headline-mix` type if the grid stays quiet, `brutal` outlines when cells get black borders.
- Clashes: `zine` tape, scribbles and texture fight the precision; `poster` swoop and script word
  break the grid; `arcade` pixel frames need their own unit. No tilted or overlapping pieces.

## House-rule overrides
- Never copy logos or brand lockups: the reference's "lazohdesign" wordmark in the top blue cell and
  the vertical "LAZOHDESIGN.COM" are dropped. No handle runs down the right margin either.
- The shipped theme put a mono kicker and a slide counter in row 1: both banned. Row 1 holds only
  blue cells or the headline itself, and the headline is the first text on every slide.
- No slide numbers or ghost numerals. List indexes are letters or glyphs, never zero-padded `01 02 03`
  (those read as slide numbers and fail gate G7).
- The shipped theme's 22px source line and small sub-lines are below the floor: everything is 34px+,
  weight 500 or more (the reference's light sub-line is set at 500, never under 400).
- The theme let headline words fall on blue cells in black (2.61:1): blue cells stay clear of the
  headline area, and only white text sits on blue.
- The bookmark corner mark is dropped (bottom-right holds the swipe cue). No photos of people or stock
  photos; draw every visual with grid-snapped shapes.
- Footer: `BUILDABLELABS.COM` bottom-left on the row-6 blue cell, swipe cue bottom-right (not on the last).
