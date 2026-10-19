# Reference mode: copy an attached template exactly

Use this when the person attaches one or more template images (Pinterest, Cosmos, Dribbble, Behance, a screenshot
of someone's carousel) with the idea. The carousel should look as if the attached design were its master file:
the same background, colours and shapes in the same positions, the same typography (family, size, weight,
style, case, spacing, alignment, colour) and the same object styling. Only the content changes: our copy, and
objects swapped for ones that show our idea, drawn in the same style.

An attached reference **replaces the library mix** for that carousel. It is exempt from the no-repeat rule (the
person chose that look). It is scored on the Design line: does it read as the same system as the photo, with our
content, and is it good Instagram craft?

## Contents
1. What stays, what changes, what the house rules override
2. Procedure
3. Matching typography
4. Replacing objects and visuals
5. Slide count and layouts
6. Fidelity check
7. Saving

---

## 1. What stays, what changes, what the house rules override

| Stays exactly as the reference | Changes to fit our idea |
|---|---|
| Background: colour, gradient, texture, image treatment | Every word of copy, written to fit the same text slots |
| Every shape (circles, blobs, bars, frames, cards, lines, arrows, pills): colour, size, position, rotation, radius, stroke, shadow, opacity, layer order | Photos, illustrations, icons and 3D items, swapped for drawn ones that show our idea in the **same style, size, position, angle and colour treatment** |
| Typography per text slot: family, size, weight, style, case, tracking, line-height, alignment, colour, highlight treatment | Chart or diagram data (our numbers and labels, the same chart style) |
| Layout: margins, grid, where each element sits, spacing | |
| Decorative system: dividers, pills, buttons, badges, arrows, corner marks | |
| Colour roles: which colour does which job, and how much of each | |

**The house rules still win**, with the smallest change that satisfies each one and keeps the look:

| the reference has | do this instead |
|---|---|
| a logo, brand lockup, handle or url | drop it; the footer shows `BUILDABLELABS.COM` only |
| slide numbers, "01/06", giant numerals | drop them; keep the shape that held the numeral |
| a kicker, eyebrow or label above the headline | fold it into the headline, or move it into the visual or below |
| text under 34px, or weights under 400 | raise to 34px and 400+ (500+ for body); if it no longer fits, cut words |
| text that fails 4.5:1 contrast | nudge the colour just enough to pass and note it |
| photos of people or stock photos | draw a diagram, shape or illustration in the same colours and position |
| more than 6 slides | pick the 6 that carry the story, or merge |
| a layout that puts text over a busy photo | put the text on a flat area of the same colours |

## 2. Procedure

1. **Save the images** to `carousels/<slug>/refs/`. Look at every one (the Read tool shows images). If a link won't
   open (Instagram usually needs a login), ask for a screenshot. Never describe a reference you haven't seen.
   **Resolution:** ask for the largest version of each image you can get. Under about 500px wide, sizes, weights and tracking
   are guesses (`reference.py inspect` warns); say so in `design.md`. If an image has a dark board or border around the slide,
   crop to the slide (`--crop x0,y0,x1,y1`, source pixels) before measuring, or `inspect` and `compare` will measure the board.
2. **Split a collage.** If one image shows several slides: `python3 <skill-dir>/scripts/reference.py tiles refs/board.png
   --rows R --cols C --out refs/tiles/` (use `--trim N` for outer padding). Look at each tile and keep the slides that map
   onto ours (cover, stake or point, steps, stat, quote, CTA). Photo-only tiles are mood, not layouts.
3. **Measure each kept tile**: `reference.py inspect refs/tiles/tile-05.png --out refs/`. It prints the background and
   the real palette (hex and share of the slide) and writes a copy with a labelled 10% grid, so positions read as
   percentages. Sample colours from this, never from memory.
4. **Write the spec sheet** into `design.md` (`references/design-system.md` format, `kind: "reference"`,
   `sources: ["reference:<file>"]`): per slide type, the background, every shape with position and size in %, every
   text slot with font, size, weight, style, case, tracking, colour, alignment and position, and the devices.
5. **Apply the house rules** from section 1 and write each deviation, with its reason, under "House-rule overrides".
6. **Build `slides.html`** from the spec sheet (absolute positions in %, exact hex colours), render, and run the
   fidelity check (section 6) until the slides read as the reference.

## 3. Matching typography

Reference designs are the one place the fixed fonts don't apply: every slot uses the font matched to the photo. Match each text slot to the closest Google Font **by letterform**, not by mood. Check them side by side after the first
render.

| the reference looks like | try |
|---|---|
| tight heavy grotesque caps (Helvetica Black style) | Inter Tight 800-900, Archivo 800, Schibsted Grotesk 800 |
| condensed poster caps | Anton, Bebas Neue, Oswald 700 |
| wide chunky display | Dela Gothic One, Archivo Black, Unbounded 800 |
| friendly rounded geometric | Plus Jakarta Sans 800, DM Sans 700, Nunito 800 |
| editorial serif italic | Instrument Serif italic, Playfair Display italic, Newsreader italic |
| high-contrast didone | Bodoni Moda, Playfair Display |
| script or brush word | Mrs Saint Delafield, Caveat Brush, Permanent Marker (80px+ only) |
| typewriter | Special Elite, Courier Prime, IBM Plex Mono |
| pixel or 8-bit | Press Start 2P, Silkscreen 700, Pixelify Sans 700 |
| monospace labels | JetBrains Mono, DM Mono, Space Mono |

**All-caps references:** type the copy in sentence case and set `text-transform: uppercase` in CSS (SVG `<text>` too).
Lint flags 3 or more shouted words typed in capitals as machine-written; the rendered look is identical.

Estimate the size from the cap height (capitals are about 0.72 of the font size) on the 1080-wide measured copy. If a
slot's text would fall below 34px, raise it and say so. List every font match, and any slot you could not match, in
`design.md`.

## 4. Replacing objects and visuals

The reference's photos and illustrations become drawn objects (inline SVG or CSS) in the same position, crop and
colour treatment. A phone photo becomes a phone-shaped card holding our diagram; a portrait becomes a coloured
circle or shape in the same place; a product shot becomes a flat or outlined drawing of our thing. The infographic on
slide 1 and the visual on every slide still apply (`references/visuals.md`): use the reference's picture slot for it.

## 5. Slide count and layouts

The reference shows a set; our carousel has 4-6 slides. Map each of ours to the closest tile (cover to the hook tile,
points to text tiles, CTA to the closing tile) and reuse a layout rather than inventing one. If a needed slide has no
tile, extend the system from the nearest tile (same shapes, colours and type) and note it.

## 6. Fidelity check

After rendering: `python3 <skill-dir>/scripts/reference.py compare refs/tiles/tile-05.png slides/01.png --out refs/`.
It writes the reference, our slide and a 50% overlay, all with the 10% grid, and lists the cells whose colours differ
most. A mean cell difference over about 40, or a large cell in the wrong colour, means a background or shape has
drifted. Look at the overlay for shapes in the wrong place and type in the wrong size. Fix and re-render; repeat until
the slide reads as the reference with our content.

## 7. Saving

`design_log.py save carousels/<slug>` saves the extracted `design.md` like any other design, so it can be reused or
mixed later. The reference photos stay in `refs/` and are never committed: they are third-party work.
