# Visuals: making slides that stop the scroll

A carousel of type-only slides reads as a wall of words in the feed. **Every slide gets one visual**
(house rule, gate G1), taking roughly 40-60% of the slide, and slide 1's is an infographic. A visual is a product-style mockup or diagram that `render.py` draws in brand colours. The brand
bans stock photos, neon and hype gradients, so these are drawn rather than photographed: they look like
the product, a game UI or a whiteboard sketch, never a photo.

## Rules of thumb
- **Cover**: an infographic that shows the promise (the thing in action, a number, a comparison, a
  process), kept clear of the left and right edges for the profile-grid crop.
- **No slide without one.** A `visual`, an `image` or a big sourced `number` counts; a quote alone doesn't.
- **Nothing inside a visual under 34px** (gate G4). The built-in kinds are sized for that; keep labels short so
  they fit.
- **One visual per slide, and it must explain something.** Don't use it as decoration. If the
  reader would understand the slide without it, it's decoration.
- **Don't repeat a visual.** Tease on one slide and reveal on the next (cover shows the health
  bar, slide 2 explains it), but don't show the same mockup twice.
- **Text inside a visual is still copy.** Lint checks it for numbers that aren't in the brief and
  for banned phrasing. Never invent command output, UI text or figures: show the real command, or
  describe what it does in a `# comment` line.
- **Keep reading copy short** when a slide has a visual: headline + one line of body. The visual
  carries the rest.
- `tilt` (-3 to 3 degrees) makes a mockup feel like a sticker on a poster. Use it on
  2-3 slides, not all of them.

## Kinds (`"visual": {"kind": ...}` on any slide)

| kind | looks like | fields | good for |
|---|---|---|---|
| `window` | a terminal or app window, with an optional sticker and HUD strip | `title`, `lines[]` (`{"t": text, "s": "cmd"·"shell"·"out"·"dim"·"hl"·"ok"}` or plain strings), `hud[]` (rows as in `hud`), `toast` + `toast_icon` | commands, settings, "here's what it looks like" |
| `hud` | a game-style status panel | `rows[]`: `{"label", "tag"?, "hearts": [full, total]}` or `{"label", "tag"?, "bar": 0-1}` | usage, progress, before/after levels, anything you can show as a meter |
| `flow` | input → your thing → outcomes | `from`, `from_icon`, `via`, `via_icon`, `to[]` (`{"t", "icon"}`) | how something works, decision points, pipelines |
| `slots` | a game inventory grid (2x2 or 3 across) with one slot "equipped" | `items[]` (`{"icon", "label"}`), `active` (1-based), `caption`? | options, toolkits, "pick your..." lists |
| `dialog` | a confirm dialog with ticks and buttons | `title`, `icon`, `rows[]` (strings or `{"t", "icon"}`), `buttons[]` (last is primary), `primary` (false on a CTA slide so the CTA button stays the only solid one) | checklists, before-you-X slides, CTA slides with something to save |
| `funnel` | stages narrowing to one outcome | `stages[]` (strings or `{"t", "icon"}`, widest first), `out` (`{"t", "icon"}`) | drop-off, "most X never become Y", pipelines that lose things |
| `tags` | a cloud of pills, one or more filled | `tags[]` (strings), `active` (1-based, or a list), `caption`? | crowded options, buzzwords, "everyone's chasing...", the one that matters |
| `compare` | two cards side by side: before (crosses) and after (ticks) | `left`/`right`: `{"title", "rows": [...]}` (3 short rows each) | before/after, demo vs production, myth vs fact, the obvious fix vs the real one |
| `chart` | horizontal bars, one highlighted | `title`?, `bars[]` (`{"label", "value", "display"?}`), `highlight` (1-based) | where time or effort goes, relative size |
| `timeline` | steps down a rail, one current | `steps[]` (`{"t", "when"?, "icon"?}`), `active` (1-based) | phased plans, what happens when, week-by-week |

Common fields: `tilt` (degrees). Meter and bar values (`hearts`, `bar`, a chart's `value`) are drawn,
not printed, so lint doesn't treat them as numbers. Use them for an honest *shape* ("sign-off takes the
longest"), never to imply a statistic. A figure printed on a bar goes in `display`, and lint checks it
against the brief's evidence like any other number.

**Pick the kind by what the slide has to explain**: a loss or drop-off is a `funnel`; a choice among many is
`tags` or `slots`; a turn ("the obvious fix fails, BUT") is `compare`; effort or size is `chart`; a plan is
`timeline`; how something works is `flow`; what it looks like is `window`. Don't use the same kind twice in
one carousel unless the second one reveals something the first teased.

**Icons** (`icon`, `*_icon`): `layout`, `shield`, `slash`, `gamepad`, `terminal`, `eye`, `alert`, `zap`,
`play`, `heart`, `check`, `x`, `plug`, `sparkle`, `bookmark`, `code`. These are outline icons in the Lucide
style. Add new ones to `VIS_ICONS` in `render.py`.

**Colours**: visuals are dark "screens" (`--ui-bg` #0A0B0E, accent #6789EC, brand-blue fill) so
they pop on blue, light and dark slides alike. A theme can restyle `.visual` or override
the `--ui-*` variables in its `theme.css`.

## Example (cover)

```json
{"type": "cover", "headline": "You can now *mod* Claude Code like a video game.",
 "sub": "Fun, until you remember they run with your permissions.",
 "visual": {"kind": "window", "title": "claude", "tilt": -2,
   "hud": [{"label": "Usage", "tag": "Health", "hearts": [7, 10]}],
   "lines": [{"t": "/plugin install <mod>@<marketplace>", "s": "cmd"}],
   "toast": "Mod loaded", "toast_icon": "gamepad"}}
```

`examples/claude-code-mods/script.json` uses window, hud, flow, slots and dialog; `examples/ai-pilots-stall/script.json`
uses funnel, tags, compare, chart and timeline.
