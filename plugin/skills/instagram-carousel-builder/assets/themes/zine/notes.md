# zine: notes

Source: refs/ref-7.png, a writing-zine Instagram template set (12 tiles).

## What was taken from the reference
- Grid and mood: off-white paper, text-light slides with lots of air, one dark slide and one full-colour slide in the run.
- Label bar: black bar with light mono caps for titles -> `.t-point .h` (inverts on the ink variant) and the `.source` line.
- Highlighted word ("ACCOUNTABLE" in a white box) -> the one-word emphasis, as a solid brand-blue block with white text (brand rule).
- Kicker "• HOW TO WRITE •" in small red mono -> mono kicker in blue with bullets either side.
- Red scribbles (circle around "Outline your story", crown/asterisk bursts, zigzag) -> brand-blue SVG scribbles used as CSS masks on `.decor`/`.decor2`: wavy underline (replaces `.rule`), hand-drawn ring (around the stat number and around the cover stamp), burst, zigzag, arrow.
- Collage devices without photos: tape strip at the top edge (alternates left/right), a rotated mono stamp from `ghost` (cover) and `badge` (cta).
- Red full-bleed WRITE slide -> the quote slide as full brand blue (`fill_types: ["quote"]`), with a white burst and underline.
- Black slide with white mono text -> the closing cta slide is near-black with a blue square button.
- Mixed type: mono for labels, stamp and point titles; Instrument Serif italic for headlines; Manrope for body and list items.
- Scribble colour follows `--accent` (brand blue on paper, #6789EC on ink, white on the blue slide), so contrast holds on every variant.

## What could not be matched
- Photography (portraits, typewriter, book pages): banned by the brand. The collage energy is carried by tape, stamp and scribbles only.
- The reference's brush-painted hand lettering (WRITE) and rough paint texture: no equivalent font or asset. Not drawn.
- Typewriter body copy: body stays Manrope (brand rule); mono is reserved for labels and point titles.
- Red: no brand equivalent; blue is the single accent.
- Warm cream and mid-grey paper: only off-white #F5F6F8 is in the palette.
- The reference's busy hand-drawn density is deliberately toned down (one or two marks per slide).
- Split image/text and circle-cropped portrait layouts need a new slide type; not attempted.

## Variants
- default: paper (light). `ink`: near-black substrate, #6789EC scribbles, off-white label bars.
- The cta slide is always black, so on `ink` it matches the other slides.
