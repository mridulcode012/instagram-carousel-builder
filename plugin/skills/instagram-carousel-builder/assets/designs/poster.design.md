# poster

```json
{
  "name": "poster",
  "kind": "library",
  "sources": [],
  "mode": "alternating",
  "background": "#0B3FDE",
  "accent": "#0B3FDE",
  "palette": ["#0B3FDE", "#FFFFFF", "#C3D4FA", "#F5F6F8", "#0A0B0E", "#565D6E", "#6789EC"],
  "fonts": {"display": "Manrope", "body": "Manrope", "label": "JetBrains Mono", "script": "Instrument Serif"},
  "google_fonts": ["Manrope:wght@500;600;700;800", "Instrument+Serif:ital@0;1", "JetBrains+Mono:wght@500;700"],
  "type": {"display_class": "sans-heavy", "case": "upper"},
  "layout": "poster",
  "emphasis": "italic-serif-word",
  "devices": ["ghost-word", "swoop-line", "gradient-light", "rules", "progress-bar"],
  "visual_style": "ui-mockup",
  "visual_kinds": ["window", "hud", "flow", "slots", "dialog", "tags", "compare", "chart", "big-number"]
}
```

## Look
An agency poster grid: saturated brand-blue slides with a dark edge vignette alternate with off-white ones.
Each shouts one huge, tight ExtraBold caps headline, flush left, with one word swapped for a serif italic.
A tone-on-tone ghost word echoes behind the visual, a thin calligraphic swoop loops across, and a slim
solid bar holds the footer. Visuals are dark tilted UI panels with soft shadows, like product shots.

## Palette
| role | hex | use |
|---|---|---|
| bg / edge (blue) | #0B3FDE / #0B2987 | odd slides (1, 3, 5); edge is the vignette rim (bg 58% + #0A0B0E) |
| text / muted (blue) | #FFFFFF / #C3D4FA | headline, script word, body / source, secondary labels |
| bg / edge (light) | #F5F6F8 / #DEE1E7 | even slides (2, 4, 6) |
| text / muted / accent (light) | #0A0B0E / #565D6E / #0B3FDE | copy / source / script word, index, button |
| fill | #0A0B0E | UI panels, optional black poster slide, footer bar on light |
| panel text / dim / accent | #F5F6F8 / #B8BECC / #6789EC | text inside the black UI panels |
| ghost / swoop (decor, never text) | #2B58E2 / #7190EC blue · #DBDEE6 / #8CA4EC light | ghost word, swoop line |

Text pairs (WCAG, computed): #FFFFFF on #0B3FDE 7.55:1 · #C3D4FA on #0B3FDE 5.08:1 · #FFFFFF on #0B2987
12.49:1 · #C3D4FA on #0B2987 8.4:1 · #0B3FDE on #FFFFFF 7.55:1 (footer bar and cover tag on blue) ·
#0A0B0E on #F5F6F8 18.2:1 · #565D6E on #F5F6F8 6.09:1 · #0B3FDE on #F5F6F8 6.99:1 (script word, button on
blue slide) · #F5F6F8 on #0A0B0E 18.2:1 (footer bar on light, panels) · #B8BECC on #0A0B0E 10.57:1 ·
#6789EC on #0A0B0E 5.97:1 · #FFFFFF on #0B3FDE 7.55:1 (button on light). Never #6789EC on blue or light.
Ink variant: blue slides become #0A0B0E, text #F5F6F8 18.2:1, muted #7A8296 5.12:1, script #6789EC 5.97:1;
panels #12141A (#F5F6F8 on it 17.02:1, #6789EC 5.58:1).

### Alternate palettes
**Electric (poster-original, exact hexes from its theme.json):** electric blue and studio grey, neon stickers.
| role | hex | contrast |
|---|---|---|
| blue: bg #1F55E8, edge #0B2A9C, swoop #0A1E78 | text #FFFFFF / muted #E6ECFF | 5.96:1 / 5.05:1 (white on edge 11.5:1) |
| grey: bg #CFCFD1, ghost #BCBCBF, swoop #9A9AA0 | text and accent #111214 / muted #3E3E44 | 12.05:1 / 6.83:1 |
| fill | #111214 (panels #1C1D21, line #35363C) | #FFFFFF 18.74:1 · dim #9A9AA2 6.71:1 (6.03:1 on #1C1D21) |
| stickers | #F1E80E · #E040E8 · #63F23C | #111214 on each 14.54 / 5.42 / 12.76:1; #F1E80E on #111214 14.54:1 |
Buttons: #FFFFFF with #1F55E8 type on blue, #1F55E8 with #FFFFFF type on grey (both 5.96:1). #1F55E8 as
text on grey is 3.83:1 and fails, so blue appears on grey only as a filled button.

**Azure paper (sampled by eye from refs/ref-3.png):** cool blue and paper white; the sampled #1877D6 (4.52:1
with white) is deepened. Blue slides: bg #1268C4, text #FFFFFF 5.52:1, muted #EEF4FC 4.99:1. Paper slides: bg
#ECECE8, text #111111 15.94:1, muted #4F4F52 6.89:1, accent #0F5FB5 5.33:1. Fill #111111 with #FFFFFF 18.88:1.

**Crimson (new):** for launches and warnings. Red slides: bg #C8102E (edge #7A0A1C), text #FFFFFF 5.88:1
(11.12:1 on the edge), muted #FFECEC 5.17:1. Paper slides: bg #F4EFE8, text #16120F 16.28:1, muted #5C534C
6.56:1, accent #B00E28 6.25:1. Fill #16120F with #FFFFFF 18.62:1; button #B00E28 with #FFFFFF 7.14:1.

## Type
| role | family | size at 1080 | weight | case | tracking | line-height |
|---|---|---|---|---|---|---|
| cover headline | Manrope | 124px | 800 | upper | -.042em, word-spacing .06em | .86 |
| headline | Manrope | 106px (CTA 110px, long 96px) | 800 | upper | -.042em | .88 |
| script word (in headline) | Instrument Serif italic | 1.12em of the headline | 400 | as written, lower | -.01em | 1.02 (inline-block) |
| stat number (in headline) | Manrope | 300px | 800 | upper | -.06em | .8 |
| cover tag / sub | Manrope | 46px | 700 | sentence | 0 | 1.5 |
| body / list item | Manrope | 38px / 40px | 500 / 600 | sentence | -.005em | 1.3 / 1.2 |
| UI panel lines, label, footer, source, index | JetBrains Mono | 34px | 500 / 700 | upper (UI lines as written) | .1em | 1.2 |

Google Fonts: `family=Manrope:wght@500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@500;700`.

**Line-length guide** (Manrope 800 caps at -.042em average about .68em per character, frame 888px wide):
| size | chars per line (with spaces) | lines max | longest single word |
|---|---|---|---|
| 124px cover | 10 | 5 | 10 letters |
| 106px | 12 | 4 | 12 letters |
| 96px | 13 | 4 | 13 letters |
| 84px | 15 | 4 | 15 letters |

So a cover is 6-9 short words, a middle headline 6-10. Break lines by hand with `<br>`. A word over the
limit ("DIFFERENTIATOR", 14) drops the headline one step or gets swapped; never shrink-to-fit.

Brand fonts today: Manrope, Instrument Serif, JetBrains Mono. Poster-original: **Archivo** variable
(`Archivo:wdth,wght@62..125,400..900`), 800 at `font-stretch:62%` on blue (cover 150px, headline 126px,
-.004em, lh .9, about 16 chars per line) and 125% on grey at 0.7x (-.03em, lh .96, about 11 chars), also the
label font there; script word **Mrs Saint Delafield** (`Mrs+Saint+Delafield`) at 1.32em blue, 1.5em grey.
Alternate: **Anton** (`Anton`, 400, true condensed poster caps like the refs' WEBSITE), headline 140px,
cover 160px, tracking 0, lh .92, about .46em per character: 13 chars per line at 140px.

## Layout
- 1080 x 1350, margin 96px: frame x 96..984, y 96..1254, flush left. Headline top at y 132, then tag,
  visual, body, footer bar. Slides 1, 3, 5 blue; 2, 4, 6 light; a key claim may use the black fill.
- Footer bar: x 70..1010 (26px past the frame), 76px tall, bottom at y 1254, radius 4px. Optional 6px
  progress bar flush to the bottom edge, width = slide index / total, text colour.
- Visual zone: 60px under the headline block to 40px above the body or bar, 840px wide, centred.
- Body (stake, point): pinned above the bar, max-width 760px, 3px text-colour rule on top, 28px gap.

## Emphasis
`italic-serif-word`: one word per headline (two if one phrase) in Instrument Serif italic 400, lowercase,
1.12em, inside the caps line. White on blue (the font switch is the mark), #0B3FDE on light. `inline-block`,
lh 1.02, `vertical-align:-.06em` so ascenders clear the line above. Body and list emphasis: Manrope 800.

## Devices
- **Edge vignette** (`gradient-light`): radial gradient, bg at 34% to edge at 100% (starter); faint on light.
- **Ghost word** (`ghost-word`): the cover's key noun (never a number), Manrope 800 300px caps stacked three
  times, bleeding off both sides in `--ghost`, fading downward. It sits in `.decor` in a box clipped to the
  `.visual` box, so it is only ever behind the visual. Cover, plus one more slide at most.
- **Swoop line** (`swoop-line`): a 3px and a 1.6px calligraphic stroke with a loop (SVG mask in the starter).
  Light slides mirror it so the profile grid reads as one line; steps slides drop it to 55%.
- **Footer bar** (`rules`): solid bar in text colour, site and cue in bg colour. Body and list rows get a
  3px text-colour top rule. **Cover tag**: the sub-line inverted the same way, radius 4px.

## Visual style
`ui-mockup`: product-shot panels. Near-black #0A0B0E panels, 2px #2C3444 border, radius 4px, shadow
`0 34px 70px rgba(10,11,14,.38)`, tilted -2deg to 2deg. Windows get a #12141A title bar with three 18px
dots and a lowercase mono label; lines in JetBrains Mono 34px #F5F6F8, prompts #6789EC, comments #B8BECC.
A sticker toast (`MOD LOADED`, blue, white border and mono caps, 4deg) overhangs a top corner. Panels stay
black on both slide types. Flows: 3px outlined chips on the slide bg, one black "via" chip, 3px arrows.
Charts: black panel, 48px tracks #12141A, grey bars #7A8296, one #6789EC key bar, mono values. Compare:
"before" rows dim with x glyphs, "after" with a filled header (blue on light, white with blue type on blue);
highlighted slots flip the same way. Icons: 1.8-2.4px stroke line icons, round joins.

## Slide recipes
- **Cover (blue)**: headline 124px, 4-5 lines with one script word, cover tag under it (46px), ghost word
  behind a tilted window or flow (y 760..1120), footer bar with cue. The infographic is the window.
- **Stake / point / compare**: headline 106px, 3-4 lines, visual in the middle (hud, flow, or two black
  compare panels 408px wide with a 24px gap), body with its 3px rule above the bar.
- **Steps (light)**: headline 106px, then 3-4 ruled rows pinned above the footer: index glyph (`A`, `B`,
  `C` or a check) in mono 700 accent, 58px slot, item in Manrope 600 40px. Swoop at 55%.
- **Stat (blue)**: headline opens with the number (`<span class="num">6 WKS</span>`, 300px), a 64px caps
  tail, then a two-bar chart panel and `.source` above the bar.
- **Key claim (black fill)**: `.slide.fill`, headline 96px, script word in #6789EC, small visual.
- **CTA (light)**: headline 110px with a script word, a dialog checklist panel, a #0B3FDE button (Manrope
  600 36px, send icon), footer bar with the site only, no cue.

## CSS starter
```css
:root{
  --bg:#0B3FDE; --edge:#0B2987; --text:#FFFFFF; --muted:#C3D4FA; --accent:#FFFFFF;
  --fill:#0A0B0E; --ghost:#2B58E2; --swoop:#7190EC; --btn:#F5F6F8; --on-btn:#0B3FDE;
  --ui-bg:#0A0B0E; --ui-panel:#12141A; --ui-line:#2C3444; --ui-text:#F5F6F8; --ui-dim:#B8BECC; --ui-accent:#6789EC;
  --f-display:"Manrope", Helvetica, Arial, sans-serif;
  --f-script:"Instrument Serif", Georgia, serif;
  --f-label:"JetBrains Mono", Menlo, monospace; --m:96px;
}
*{box-sizing:border-box;margin:0;padding:0}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;color:var(--text);font-family:var(--f-display);
  background:radial-gradient(ellipse 125% 92% at 50% 26%,var(--bg) 34%,var(--edge) 100%)}
.slide.light{--bg:#F5F6F8;--edge:#DEE1E7;--text:#0A0B0E;--muted:#565D6E;--accent:#0B3FDE;
  --ghost:#DBDEE6;--swoop:#8CA4EC;--btn:#0B3FDE;--on-btn:#FFFFFF}
.slide.fill{--bg:#0A0B0E;--edge:#0A0B0E;--text:#F5F6F8;--muted:#7A8296;--accent:#6789EC;
  --ghost:#1A1C22;--swoop:#2C3444;--ui-bg:#12141A}
.decor{position:absolute;inset:0;pointer-events:none;z-index:0}
.swoop{position:absolute;inset:0;background:var(--swoop);
  mask:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1080 1350'><g fill='none' stroke='black' stroke-linecap='round'><path stroke-width='3' d='M-60 1130 C 200 1010 360 760 600 760 C 820 760 820 1010 650 1000 C 470 990 520 700 780 600 C 930 540 1030 520 1160 470'/><path stroke-width='1.6' d='M-60 1190 C 240 1080 420 860 640 840 C 860 820 980 900 1160 800'/></g></svg>") center/100% 100% no-repeat}
.slide.light .swoop{transform:scaleX(-1)} .slide[data-type=steps] .swoop{opacity:.55}
/* ghost word: set top/height inline to match the .visual box, so it never sits behind copy */
.ghost{position:absolute;left:0;right:0;overflow:hidden;display:flex;justify-content:center}
.ghost span{white-space:pre;text-align:center;font-weight:800;font-size:300px;line-height:.8;letter-spacing:-.055em;
  text-transform:uppercase;color:var(--ghost);
  mask-image:linear-gradient(180deg,#000 30%,transparent 92%)}
.frame{position:absolute;inset:var(--m);display:flex;flex-direction:column;z-index:1}
.headline{margin-top:36px;font-weight:800;font-size:106px;line-height:.88;letter-spacing:-.042em;word-spacing:.06em;
  text-transform:uppercase;color:var(--text)}
.slide[data-type=cover] .headline{font-size:124px;line-height:.86}
.slide[data-type=cta] .headline{font-size:110px} .headline.long{font-size:96px}
/* emphasis: one script word */
.script{display:inline-block;font-family:var(--f-script);font-style:italic;font-weight:400;text-transform:none;
  font-size:1.12em;line-height:1.02;vertical-align:-.06em;letter-spacing:-.01em;word-spacing:0;
  color:var(--accent);padding-right:.06em}
.num{display:block;font-size:300px;line-height:.8;letter-spacing:-.06em;margin-left:-.04em}
.headline .tail{display:block;font-size:64px;line-height:.96;letter-spacing:-.035em;margin-top:24px}
.sub{align-self:flex-start;margin-top:34px;background:var(--text);color:var(--bg);font-weight:700;
  font-size:46px;line-height:1.5;padding:.16em .7em;border-radius:4px}
.body{margin-top:auto;padding-top:28px;border-top:3px solid var(--text);max-width:760px;
  font-size:38px;font-weight:500;line-height:1.3;letter-spacing:-.005em}
.body b{font-weight:800}
.visual{flex:1;min-height:0;width:840px;margin:60px auto 40px;display:flex;align-items:center;justify-content:center;
  font-family:var(--f-label);transform:rotate(var(--tilt,0deg))}
.win{width:100%;background:var(--ui-bg);color:var(--ui-text);border:2px solid var(--ui-line);border-radius:4px;
  box-shadow:0 34px 70px rgba(10,11,14,.38);position:relative}
.win-bar{display:flex;gap:12px;align-items:center;padding:14px 24px;background:var(--ui-panel);border-bottom:2px solid var(--ui-line);font-size:34px;color:var(--ui-dim)}
.win-bar i{width:18px;height:18px;border-radius:50%;background:var(--ui-line)}
.ln{padding:6px 28px;font-size:34px;line-height:1.3} .ln .pr{color:var(--ui-accent);font-weight:700}
.toast{position:absolute;right:-14px;top:-30px;background:#0B3FDE;color:#FFFFFF;border:2px solid #FFFFFF;
  border-radius:4px;padding:12px 22px;font-size:34px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;transform:rotate(4deg)}
.list{list-style:none;margin-top:auto}
.list li{display:flex;gap:24px;align-items:baseline;padding:22px 0;border-top:3px solid var(--text);
  font-size:40px;font-weight:600;line-height:1.2}
.list .ix{font-family:var(--f-label);font-size:34px;font-weight:700;color:var(--accent);min-width:58px}
.btn{align-self:flex-start;margin-top:auto;background:var(--btn);color:var(--on-btn);border-radius:4px;
  padding:26px 44px;font-weight:600;font-size:36px}
.source{margin-top:auto;font-family:var(--f-label);font-size:34px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.foot{flex:none;margin:32px -26px 0;height:76px;padding:0 26px;border-radius:4px;background:var(--text);color:var(--bg);
  display:flex;justify-content:space-between;align-items:center;
  font-family:var(--f-label);font-size:34px;font-weight:500;letter-spacing:.1em;text-transform:uppercase}
.foot .cue{font-weight:700} .progress{position:absolute;left:0;bottom:0;height:6px;background:var(--text);z-index:2}
```
Markup: `<h1 class="headline">You can now<br><span class="script">mod</span> Claude<br>Code like a<br>video game.</h1>`.

## Mix notes
- Lends best: **colour** (saturated and light slides alternating, vignette rim) and **type** (tight heavy
  caps plus one serif italic word). Ghost word and swoop are a good **devices** donor for flat systems.
- Pairs well with: `cards` or `arcade` visual styles under poster caps, `pop` shapes (one per slide),
  `brutal` hard shadows in place of the soft drop shadow.
- Clashes: `swiss-grid` (swoop and script break the grid), `headline-mix` (size jump on top of the script
  word), `zine` scribbles and tape over the ghost word. Never two emphasis marks in one headline.

## House-rule overrides
- No logos or brand lockups: the refs put the "Netroots" lockup at the top of every tile and Facebook,
  Instagram and LinkedIn icons in every footer bar. Both are dropped; the bar holds only our site and cue.
- Nothing readable above the headline: the refs' lead-ins ("WE OFFER", "BOOST YOUR", "CHOOSING THE", the
  script "designin ain't") and the shipped theme's mono kicker and counter are banned. Fold them in.
- No slide numbers or ghost numerals (the shipped stat slide ghosted "6 WKS"). List indexes are letters or
  glyphs, never zero-padded `01 02 03` (the shipped steps slide used them).
- Ghost words may sit behind a visual, never behind copy: the shipped ghost ran behind the cover tag, the
  source line and the footer bar, and the refs run "GROWTH" and "FUTURE" behind text. Clip it to the visual box.
- Nothing under 34px, no weight under 400: the shipped footer and badge were 22px, the refs' body copy and
  url tiny. All text is 34px+ here; the badge is dropped.
- No photos of people or stock photos: the refs are built on them (statues, an astronaut, hands, a chess
  set, laptops). Draw a UI panel or diagram instead.
- Footer `BUILDABLELABS.COM` bottom-left in the bar, swipe cue bottom-right, no cue on the last slide.
