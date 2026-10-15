# swiss-grid: notes

Source: refs/ref-2.png, the "Grid Systems" Swiss-style template (one image, cover only).

## What was taken
- **Grid**: strict 4 x 6 modular grid of thin (2px) rules drawn with `.decor`, outer frame closed, vertical margin strip on the right. Text sits flush-left on grid lines and runs across them.
- **Solid cells**: a few cells filled solid blue (`.decor2`): top-right (cover/cta span two columns), bottom-left (cover spans two rows). Cells only sit in row 1 and row 6, so text never lands on blue except the white counter / swipe cue.
- **Type**: huge heavy grotesque headline, tight, mixed case -> Manrope ExtraBold, letter-spacing -.042em, line-height ~1. Small light sub-line hung from column 3 ("every designer should know") -> `.sub`/`.body` at 428px indent.
- **Details**: tiny label in the top cell (mono kicker + counter), vertical URL down the right margin (handle, reads upward), black bookmark mark bottom-right (corner swipe marker).
- **Emphasis**: the brand's one word on a solid blue block, white text (echoes the blue cells).
- **Slide types**: cover/stake/point = headline top-left + small text low-right; stat = giant blue Manrope number; steps/recap = list rows that snap to grid rows (198px, 99px with 4+ items) so their rules coincide with the grid; quote = full brand blue (fill type) with white rules and near-black cells; cta = cover-style cell + square blue button.

## Colour mapping
- Ref beige paper -> off-white #F5F6F8. Ref blue (rules, cells) -> brand blue #0B3FDE (fill and rules). Ref black -> #0A0B0E. Small blue text on light uses #0B3FDE (7:1); `dark` variant uses #6789EC for rules and small text, near-black bg.

## Could not match
- **Paper grain**: the ref has a speckled beige texture and rounded outer corners; flat off-white here (no textures outside the Alloy patterns).
- **Font**: the ref headline is a wide neo-grotesque (Neue Haas / Helvetica Now style) with a double-storey "G" and condensed spacing; Manrope ExtraBold is the closest brand font and reads a little rounder.
- **Staircase cell**: the ref's blue block steps down into the headline area; ours stays in rows 1 and 6 because headline length varies per carousel and black text on blue fails 4.5:1.
- **Logo lockup** ("lazohdesign"): dropped, posts carry no logo; the counter sits on the blue cell instead.
- **Image slide**: no equivalent in the ref and photos are banned; `.t-image` only gets square corners.
- Headline sizes (96-112px) are above the brand's 56-76px Manrope Bold scale on purpose: this theme is a poster-scale system.
