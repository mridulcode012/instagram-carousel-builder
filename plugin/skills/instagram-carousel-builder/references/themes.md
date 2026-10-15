# Themes: picking one, and adding one from template photos

## Contents
1. How design is layered
2. Picking a theme for a carousel
3. Adding a theme from template photos
4. theme.json fields
5. What theme.css can style

---

## 1. How design is layered

```
assets/brand/brand.json + design-rules.md   the fence: Alloy palette, 3 fonts, voice, rules (never changes per carousel)
assets/themes/<name>/                       a layout + styling system (theme.json; theme.css optional) (case, emphasis style, button, patterns, which slides are full colour)
vision.json                          this carousel's choices inside a theme (variant, texture, colours from the palette, sizes)
script.json                          the content, slide by slide
render.py                            base slide skeleton + theme.css → PNGs
```

Each layer can only narrow the one above it. A theme can never add a colour or font that isn't in
`brand.json`. Lint checks this, and the judge scores Brand match against `design-rules.md` and the
theme's `preview.png`.

## 2. Picking a theme for a carousel

Pick the theme whose `best_for` matches the brief and set `"theme": "<name>"` in `vision.json`; add
`"variant"` if one suits it. When in doubt use `foundation`: it's the website look and the safest.
`assets/themes/comparison.png` shows every theme on the same seven slides; each theme's `preview.png`
shows its variants.

| theme | feel | pick it for | variants |
|---|---|---|---|
| `foundation` | calm dark, serif italic, blue block on one word (the website) | insight and opinion posts, case studies, announcements; **default** | light, blue |
| `editorial` | uppercase, grid, big numbers | big-number hooks, frameworks, bolder campaigns | light |
| `swiss-grid` | off-white, visible blue grid, huge tight sans | frameworks, systems, how-it-works, structured lists | dark |
| `poster` | brand-blue posters, ghost word, one script word | bold one-idea hooks, launches, offers | ink |
| `glass` | cinematic near-black, blue light, frosted card, wide caps | announcements, studio/capability posts, one-line positioning | none |
| `headline-mix` | small serif lead-in over one HUGE caps word | hook-led opinion, myth-busting, posts meant to be saved | blue |
| `zine` | paper-like, hand-drawn scribbles, tape, stamps | how-tos, founder notes, behind-the-build, lesson-led quotes | ink |
| `pop` | flat blue/white, sunburst and circle shapes, big numerals | listicles, events, scroll-stoppers (loud) | ink |
| `promo` | white campaign poster, same skeleton every slide, badge | launches, offers, open slots, events and deadlines | none |
| `cards` | friendly UI cards, chat-bubble quotes, rounded panels | process steps, service explainers, testimonials, checklists | none |

Tone guide: `foundation`, `headline-mix`, `glass` and `swiss-grid` are the quiet, authoritative ones. `pop`,
`poster` and `promo` are loud and suit launches. `zine` and `cards` are friendly. Keep one theme per
account for a run of posts so the feed reads as one system, and switch deliberately, not per post.

Slides that hold a lot of copy (steps, recap) shrink-to-fit in themes with big art (`promo`, `pop`).
If `render.py` reports shrinking below 80%, cut words or pick a quieter theme.

When the references don't fit any theme, it's a question for the designer: "closest theme is X;
use it, or is this a new theme?" A new theme is a bigger job (section 3) than a vision tweak,
so don't fake one with `custom_css` on a single carousel.

### Free themes (off-brand by design)

Some themes set `"brand": "free"` in `theme.json`: they bring their own palette and fonts (arcade, CRT, neo-brutalist,
and the `-original` versions of the template themes, which keep the templates' real colours and type). Use
one only when the person asks for something outside the brand, or explicitly okays it, and record that in
`decisions`. They still keep the handle, the voice rules and the truth rules. The check workflow scores their
Brand line as **Design**: how good the look is for Instagram.

| theme | feel | pick it for | variants |
|---|---|---|---|
| `arcade` | 8-bit game screens: night violet, pixel caps, pixel-framed UI, yellow CTA screen | gaming, mods, dev culture, playful how-tos, "unlocked" news | none |
| `crt` | phosphor terminal: green on black, VT323 prompt headlines, scanlines | CLI and developer-tool posts, commands, plugins, releases | amber |
| `brutal` | neo-brutalist: one loud flat colour per slide, black outlines, hard shadows, sticker words | hot takes, listicles, checklists, community posts | none |
| `poster-original` | the agency poster grid: electric blue and studio grey, condensed and wide caps, script word | loud one-idea hooks, launches, offers | none |
| `glass-original` | the agency grid: denim navy, rust and cream, frosted cards, wide caps | positioning, announcements, calm authority with warmth | none |

## 3. Adding a theme from template photos

Use this when someone hands over screenshots of carousels or templates and wants that look as a
theme (not a one-off tweak; for one post, the closest theme plus `vision.json` is enough). It's a
bigger job than a carousel: expect 2-4 render-and-look rounds.

**First, ask which kind** (one question): keep it **on-brand** (map the photos onto the brand palette and
fonts; lint enforces them) or make it **free** (`"brand": "free"`: the photos' own colours and fonts; the
judge scores it on Instagram craft). Default to on-brand unless the person says the look itself matters.

1. **Look at every photo** and write down, per photo:
   - grid: margins, alignment, where the headline sits, how many text levels
   - type: serif/sans/mono per role, case, italic, weight, width (condensed/wide), relative sizes
   - emphasis: highlight block, underline, colour, italic, script word, or none
   - colour: background, text, accent, which slides are full colour; sample the hexes
   - devices: rules, frames, cards, stickers, patterns, the progress indicator; CTA/button and footer style
2. **Fonts: match each role to the closest Google Font**, by letterform, not by mood (a Helvetica-Black
   product poster is Inter Tight 800-900, a narrow high-contrast italic is Instrument Serif Italic, a
   typewriter zine is Courier Prime / Special Elite). Check side by side with the photo after the first
   render. On-brand themes use the brand's three fonts and only borrow case, weight and width.
3. **Colours**: on-brand, map each onto the nearest `brand.json` colour and note any with no equivalent;
   free, list every hex in `theme.json → palette` (lint checks against it). Every text pair must reach
   4.5:1; the renderer measures it.
4. **Map the photo's slides onto our slide types** (cover, stake, point, stat, steps, quote, recap, cta,
   image). A layout with no equivalent (e.g. a split photo/text slide) needs a new slide type in
   `render.py`, not just CSS; say so.
5. **Apply the house rules over the photos.** Drop logos and brand lockups, slide numbers and giant
   ghost numbers, kickers or labels above the headline, and faded background words that sit behind copy.
   Rebuild photos of people or stock objects as the theme's visuals (`references/visuals.md`), restyled
   through the `--ui-*` variables and theme CSS. Raise every text size to 34px and every weight to 400+.
6. **Create the theme in the working folder: `themes/<name>/`** with `theme.json` (section 4),
   `theme.css` (section 5), `refs/` with the photos and `notes.md` with your notes. The renderer finds a
   project's `themes/` before the bundled ones, so it's usable straight away. A theme can `"extends"`
   an existing one and override only what differs.
7. **Test it on a real post**: copy `examples/claude-code-mods` and `examples/ai-pilots-stall` into
   `carousels/`, set the theme, render, and lint to 0 errors. Then look at every slide at full size for
   what lint can't see: tall script or highlight words crashing into the line above (give them their own
   line box), empty bands under small visuals (scale visuals to 40-60% of the slide), commands wrapping
   inside windows, decoration colliding with a visual (hide it under `.has-visual`).
8. **Preview it**: `python3 <skill-dir>/scripts/theme_preview.py <name>` (from the working folder) writes
   `themes/<name>/preview.png`. Put it next to the photos: it should read as the same system, not just
   the same colours. Then run the check workflow on one test post; a free theme should score 4+ on Design.
9. **Note what you couldn't match** in `notes.md` and tell the person.

**Sharing a new theme with everyone**: a theme in a working folder is only on that machine. To ship it
to the team, a maintainer moves it into the skill's `assets/themes/` in the repo, adds it to the table
in section 2, bumps the plugin version and releases (README, "Releasing a change").

## 4. theme.json fields

```json
{
  "name": "foundation",
  "description": "One or two sentences: what it looks like.",
  "source": "where it came from (brand doc, template photos, date)",
  "best_for": ["insight posts", "case studies with one hard number"],
  "css": "theme.css",
  "fill_types": ["quote"],
  "defaults": { "mode": "dark", "colors": {}, "type": {}, "layout": {} },
  "variants": { "light": { "mode": "light", "colors": {} } }
}
```

- `defaults` uses the same fields as `vision.json` (see `vision.md`) and sits between the
  renderer's defaults and the carousel's vision.
- `fill_types`: slide types that are full-colour (fill) by default. A slide can still set
  `"fill": false`.
- `variants`: named overrides a vision picks with `"variant": "light"`.
- Colours must come from `brand.json → palette`, and every text/background pair has to reach 4.5:1.
- **Free themes** add `"brand": "free"`, a `"palette"` (name → hex: every colour the theme uses) and
  `"fonts"` (a list of `{"family", "google", "fallback"}`; `google` is the Google Fonts css2 spec with the weights you
  need, e.g. `"Archivo+Black"` or `"Space+Grotesk:wght@400;500;700"`). Text/background pairs still need 4.5:1.
- `"extends": "<theme>"` reuses another theme's CSS and defaults; this theme's CSS loads after it, so it
  only has to override. Variants, fonts, palette and brand mode are not inherited.

## 5. What theme.css can style

`theme.css` loads after the base CSS, so it overrides it. Available hooks:

- **Slides**: `.slide`, `.t-cover`, `.t-stake`, `.t-point`, `.t-stat`, `.t-steps`, `.t-quote`,
  `.t-recap`, `.t-cta`, `.t-image`, `.fill` (full-colour slide), `.align-left`/`.align-center`,
  `.tex-grid`, `.tex-dots`, `.tex-weave`, `.tex-loop`, `.tex-ascent`
- **Inside a slide**: `.frame`, `.top`, `.kicker`, `.content`, `.foot`, `.cue`, `.progress`,
  `.display`, `.h-cover`, `.h`, `.h-sm`, `.h-cta`, `.sub`, `.body`, `.num`, `.source`, `.rule`,
  `.list`, `.ix`, `.quote-mark`, `.quote`, `.pill` (the button), `.img`, `em` (emphasis), `.visual` and its
  parts (`.win`, `.hud`, `.flow`, `.slots`, `.dialog`; see `visuals.md`), `.has-visual` (on a slide that
  carries one: hide decorative art that would collide with it)
- **Theme hooks**: `.decor` and `.decor2` (empty full-slide layers under the text, for shapes,
  frames, blocks and scribbles), and slide attributes for `content: attr(...)`: `data-ghost` (a
  big background word, from the slide's `ghost` field), `data-badge` (circular badge text, from
  `badge`), `data-kicker`, `data-n`, `data-total`, `data-pos` (`first`/`mid`/`last`), `data-type`
- **Variables**: `--bg --text --muted --accent --fill --on-fill --line --grid --pattern
  --pattern-blue --f-display --f-body --f-mono --s-cover --s-headline --s-body --s-label
  --s-number --m --fit`

Keep sizes as `calc(var(--s-...) * var(--fit))` so shrink-to-fit still works.
