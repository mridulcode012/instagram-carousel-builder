# Visuals: making slides that stop the scroll

A carousel of type-only slides reads as a wall of words in the feed. **Every slide gets one visual** (house
rule, gate G1), taking roughly 40-60% of the slide, and slide 1's is an infographic: a visual with information in
it. You draw it yourself, as inline SVG or HTML inside the slide's `.visual` element, in the post's design
(its palette, strokes, corners and devices from `design.md`). There are no ready-made visual widgets any more, which
is why two posts no longer look alike: each visual is drawn fresh for the idea and the design.

No stock photos, no photos of people, no robot or brain clichés. Draw it.

## Rules of thumb
- **Cover**: an infographic that shows the promise (the thing in action, a number, a comparison, a process),
  kept clear of the left and right edges for the profile-grid crop.
- **No slide without one.** A quote alone doesn't count.
- **Nothing inside a visual under 34px** (gate G4), SVG text as drawn: a 28-unit label in a viewBox scaled to
  0.8 is 22px. Draw the SVG with `viewBox` units equal to pixels (a 904-wide frame gets `viewBox="0 0 904 H"`),
  set text at 34 or more, and shorten the label instead of shrinking it. `render.py` measures this.
- **One visual per slide, and it must explain something.** If the reader would understand the slide without it, it
  is decoration. Cover the copy: the visual should still hint at the point.
- **Don't repeat a visual device within a carousel**, or across the last few posts. Tease on one slide and
  reveal on the next (the funnel loses another stage, the bar fills), but never show the same mockup twice.
- **Text inside a visual is still copy.** That includes negative examples: a crossed-out "Book a call?" still trips the self-promotion check, so reword it. Lint checks it for numbers that aren't in the brief and for banned
  phrasing. Never invent command output, UI text or figures: show the real command, or describe what it does.
- **Keep reading copy short** when a slide has a visual: headline plus one line. The visual carries the rest.
- **Match the design.** Same stroke weight, corner radius, shadow and fill logic as `design.md` ("Visual style").
  A hand-drawn design gets wobbly strokes; a pixel design gets square steps on a 6px grid; a flat design gets
  flat shapes.
- **Size the viewBox to the box.** The `.visual` box is whatever is left after the headline and copy (render.py prints it, e.g.
  904x470). Draw the SVG with `viewBox` equal to that width and height; an SVG drawn at 904x600 into a 904x470 box is shrunk to
  0.78x and its 34-unit text renders at 26px (render.py and lint flag it). Rough sizes: the box is the 904px frame width by
  (1154 - headline - copy - footer - gaps) high.
- **Fill the box.** Scale the drawing up until it fills the `.visual` area; a small drawing floating in a big
  box leaves dead space (gate G2).

## What to draw: pick the kind by what the slide must explain

| the slide says | draw | notes |
|---|---|---|
| something is lost or narrows | **funnel**: stages narrowing to one outcome | widest first; the last stage in the accent |
| a choice among many | **tags** (a cloud of pills, one or two filled) or **slots** (an inventory grid, one active) | the filled one is the point |
| a turn: the obvious fix fails, BUT | **compare**: two panels, before (crossed) and after (ticked) | 3 short rows each |
| effort, size, where time goes | **chart**: horizontal bars, one highlighted | drawn lengths show shape; a printed figure must be in the brief |
| a plan, what happens when | **timeline**: steps along a rail, one current | glyphs or letters on the nodes, never `01 02 03` |
| how something works | **flow**: input, your thing, outcomes, joined by arrows | chips with icons |
| what it looks like in use | **window**: a terminal or app window | real commands only |
| a status or level | **hud**: meters, hearts, bars | meters are shapes, not statistics |
| something to save or check | **checklist** or **dialog**: rows with ticks and one button | the best send slide |
| one number is the story | **big-number**: the sourced figure, huge, with a one-line label | source line required |
| a quote or reply | **quote-bubble** or a chat thread | real quotes only |
| a metaphor that carries the idea | **illustration**: a few simple shapes | no clichés |

Don't use the same kind twice in one carousel unless the second reveals something the first teased.

## Drawing recipes
- **Frame**: the `.visual` box is flex-centred; put one `<svg viewBox="0 0 W H">` in it with `width:100%;height:100%`, or HTML
  cards for UI-style designs.
- **Labels**: SVG `<text>` with `font-family` set explicitly (the design's body or label font), at 34+ units.
- **Arrows**: a `<path>` with `marker-end`, or a rotated triangle; 3-4px stroke at phone size.
- **Icons**: simple 2-2.6px stroke glyphs (check, x, arrow, shield, terminal, heart, bolt, bookmark) drawn
  inline as `<path>`; round caps for soft designs, square for pixel or brutal ones.
- **Meters**: a track rect plus a fill rect (segmented for pixel designs); hearts as pixel-grid rects.
- **Tilt**: `-2deg` to `2deg` on a mockup reads as a sticker on a poster; skip it for grid and pixel designs.
- **Emphasis**: exactly one thing per visual in the accent colour.

## Example (cover infographic for "AI pilots stall")

A funnel of four stages (`Ideas` > `Demos` > `Pilots` > `In production`), widths 100%, 78%, 56%, 34%, each stage a
rounded box in the design's panel style with a 38px label, a short arrow between them, and the last stage in the
accent. `script.json` says: `"visual": "a funnel that narrows from ideas to in production"`.
