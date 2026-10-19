# pilot-paper

```json
{
  "name": "pilot-paper",
  "kind": "mix",
  "sources": ["headline-mix", "swiss-grid"],
  "taken": {"layout": "swiss-grid", "type": "headline-mix", "colour": "own", "emphasis": "headline-mix", "devices": "swiss-grid", "visual_style": "swiss-grid"},
  "mode": "alternating",
  "background": "#F3EFE6",
  "accent": "#B52A16",
  "palette": ["#F3EFE6", "#141414", "#B52A16", "#FF7A57", "#5A564C", "#B8B3A4"],
  "fonts": {"display": "Archivo Black", "display2": "Instrument Serif", "body": "Manrope", "label": "JetBrains Mono"},
  "google_fonts": ["Archivo+Black", "Instrument+Serif:ital@0;1", "Manrope:wght@500;600;700;800", "JetBrains+Mono:wght@500;700"],
  "type": {"display_class": "sans-heavy", "case": "mixed"},
  "layout": "grid-modules",
  "emphasis": "size-jump",
  "devices": ["visible-grid", "rules", "progress-bar"],
  "visual_style": "editorial-line",
  "visual_kinds": ["funnel", "tags", "compare", "chart", "timeline", "checklist"]
}
```

## Look
A printed-paper report. Warm off-white slides alternate with near-black ones, with a single vermilion CTA slide. Each
headline is a small italic serif lead-in stacked on one HUGE heavy word, which is the emphasis. Four hairline columns run
down every slide, and the visuals are thin ruled diagrams that sit on that grid: square corners, 3px strokes, one
element per diagram in vermilion.

## Palette
| role | hex | use |
|---|---|---|
| paper | #F3EFE6 | slides 1, 3, 5 |
| ink | #141414 | text on paper, slides 2 and 4 background |
| accent on paper | #B52A16 | the huge word, key diagram element, CTA slide background |
| accent on ink | #FF7A57 | the huge word and key element on dark slides |
| muted on paper / ink | #5A564C / #B8B3A4 | sub-lines, footer, week labels |
| hairlines (decor) | 14% of the text colour | column rules |

Text pairs: #141414 on #F3EFE6 16.05:1 · #5A564C on #F3EFE6 6.38:1 · #B52A16 on #F3EFE6 5.53:1 · #F3EFE6 on #141414
16.05:1 · #B8B3A4 on #141414 8.79:1 · #FF7A57 on #141414 7.17:1 · #F3EFE6 on #B52A16 5.53:1 (CTA slide).

## Type
Lead-in: Instrument Serif italic 64px. Huge word: Archivo Black caps, tracking -.03em, line-height .9, sized by letter
count (it never wraps): about 0.7em per character, so 4 letters 200px, 6 letters 190px, 7 letters 160px, 8 letters 150px,
11 letters 104px; two-word phrases may break onto two lines at 120px. Tail line: Instrument Serif italic 56px. Body:
Manrope 600 40px. Labels and footer: JetBrains Mono 34px, caps, .08em.

## Layout
Frame 904px wide (margin 88px). Four equal columns marked by hairlines. Headline top-left at y 96, visual fills the middle
from y 560 to 1150, a rule and the footer at the bottom. Everything is left-aligned and snaps to the column lines.

## Emphasis
`size-jump` from headline-mix: the key word is pulled out as its own huge line in the accent colour. One per slide.

## Devices
Four hairline column rules and a footer rule (`visible-grid`, `rules`), and a 8px ink progress bar along the bottom edge.

## Visual style
`editorial-line` from swiss-grid: 3px strokes, square caps and corners, no shadows, no gradients. Only one element in each
diagram uses the accent. Data is drawn as bars and rows on the grid; all diagram text is Manrope 700 38-46px or
JetBrains Mono 34px.

## Slide recipes
Cover: serif lead-in, huge word, sub-line, funnel. Point slides: lead-in, huge word, optional tail, tags / compare / chart /
timeline. CTA: vermilion slide, huge phrase, a ruled checklist box, a square ink button.

## Decisions
- Type and emphasis come from `headline-mix` (a quiet two-voice headline suits a leadership topic); layout, devices and
  visual style come from `swiss-grid` so the diagrams read as clean business graphics, not decoration.
- Colour is new: warm paper, ink and vermilion, to stay away from the blue-and-grey looks of earlier posts.
- The CTA slide is vermilion to make the ask the loudest slide.

## CSS starter
See `slides.html` in this folder: its `<style>` is the finished version of this design.
