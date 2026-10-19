# mod-night

```json
{
  "name": "mod-night",
  "kind": "mix",
  "sources": ["arcade", "brutal"],
  "taken": {"layout": "arcade", "type": "arcade", "colour": "own", "emphasis": "brutal", "devices": "brutal", "visual_style": "arcade"},
  "mode": "dark",
  "background": "#12131C",
  "accent": "#C6F432",
  "palette": ["#12131C", "#1E2030", "#F4F1E8", "#C6F432", "#FF5EA8", "#A8AEC9"],
  "fonts": {"display": "Press Start 2P", "body": "Manrope", "label": "JetBrains Mono"},
  "google_fonts": ["Press+Start+2P", "Manrope:wght@500;600;700;800", "JetBrains+Mono:wght@500;700"],
  "type": {"display_class": "pixel", "case": "upper"},
  "layout": "stack-top",
  "emphasis": "sticker-word",
  "devices": ["hard-shadow", "outline-boxes", "badges", "progress-bar"],
  "visual_style": "pixel",
  "visual_kinds": ["window", "hud", "flow", "slots", "dialog"]
}
```

## Look
A game screen with brutalist furniture. Near-black slides with pixel-font caps headlines, where one word sits on a
tilted acid-green sticker. Every box is outlined in cream with a hard pink offset shadow instead of the arcade
theme's stepped frames. Visuals are pixel game UI: hearts, a segmented XP bar, inventory slots, flow chips. The
final CTA slide flips to full acid green.

## Palette
| role | hex | use |
|---|---|---|
| bg | #12131C | slides 1-5 |
| panel | #1E2030 | boxes |
| text | #F4F1E8 | headline, body, box outlines |
| muted | #A8AEC9 | secondary lines, footer |
| accent / sticker | #C6F432 | sticker word, equipped slot, power bar, title bars |
| pink (shadows, hearts) | #FF5EA8 | hard shadows, hearts, tags |
| CTA slide bg | #C6F432 | slide 6, text and outlines #12131C |

Text pairs (computed at render time): #F4F1E8 on #12131C, #A8AEC9 on #12131C, #C6F432 on #12131C, #12131C on #C6F432
(sticker, title bars, CTA slide), #F4F1E8 on #1E2030.

## Type
Display: Press Start 2P 58px (cover 62px), caps, line-height 1.4, no tracking; one monospaced em per character, so 904px holds
about 15 characters per line at 58px and 14 at 62px. Body (fixed): Manrope 700 42px for the sub-line and body. Labels (fixed):
JetBrains Mono 700 at 36-40px for title bars, HUD labels, chips, terminal lines and the footer (34px minimum). Only the headline
font comes from `arcade`; body and labels are the skill's fixed Manrope and JetBrains Mono.

## Layout
1080 x 1350, frame inset 100px 88px 96px. Headline at the top, sub-line, a visual that fills the middle, the footer at
the bottom. A segmented acid power bar runs along the bottom edge (width = position / total).

## Emphasis
`sticker-word` from brutal: one word per headline on an acid sticker (ink text, 4px cream outline, 6px pink hard
shadow, rotated -2deg, `margin:.12em 0` and a taller headline line-height so it never touches the lines around it).

## Devices
Hard offset shadows (8px 8px 0 pink) on boxes, 4px cream outlines, a small badge tag on windows ("MOD LOADED"), and the
progress bar. No stars or dither floor: they were dropped to keep the screens clean.

## Visual style
`pixel` from arcade: hearts built from 1px grid rects, a segmented XP bar (20 segments), square corners, mono labels in
JetBrains Mono, dashed stepped connectors. Windows have an acid title bar with a lowercase label.

## Slide recipes
Cover: headline, "There's a catch." in acid, a Claude Code window with a HUD strip above the install command and a MOD
LOADED sticker. Stake: the HUD alone. Point: flow, slots, validate terminal. CTA: acid slide with a checklist box and a
pink button.

## Decisions
- Layout, type and visual style come from `arcade` because the topic is a game-like developer feature; emphasis and
  devices come from `brutal` so it doesn't look like the stock arcade screens (cream outlines and pink hard shadows
  replace stepped frames and the dithered floor).
- Colour is new: near-black violet-grey with an acid green accent and pink, instead of arcade's night violet and yellow.
- Slot numerals and level counters are left out (G7). The cover shows a real modded prompt, not a bare command.

## CSS starter
See `slides.html` in this folder: its `<style>` is the finished version of this design.
