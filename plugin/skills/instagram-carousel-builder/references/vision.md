# Vision: fields, references, questions

## Contents
1. vision.json fields
2. Reading references
3. Reusing a locked vision
4. Question bank
5. questions.json / answers.json

---

## 1. vision.json fields

Anything you leave out comes from the theme's `defaults`, then the renderer's. Most visions
only need `theme`, maybe `variant`, `mood`, `decisions` and one or two overrides.

```json
{
  "name": "insight-weave",
  "pillar": "Founder's Dilemma",
  "status": "draft",
  "theme": "foundation",
  "variant": null,
  "mode": "dark",
  "mood": ["technical", "calm", "confident", "editorial"],
  "colors": {
    "bg": "#0A0B0E",
    "text": "#F5F6F8",
    "muted": "#7A8296",
    "accent": "#6789EC",
    "fill": "#0B3FDE",
    "on_fill": "#FFFFFF"
  },
  "type": {
    "display": "Instrument Serif",
    "body": "Manrope",
    "mono": "JetBrains Mono",
    "display_case": "none",
    "scale": {"cover": 132, "headline": 84, "body": 40, "label": 24, "number": 280}
  },
  "layout": {
    "align": "left",
    "margin": 96,
    "texture": "weave",
    "counter": true,
    "handle": true,
    "progress": true,
    "swipe_cue": true,
    "cta_fill": false
  },
  "references": [{"ref": "B", "file": "ref-b.png", "source": "pinterest.com/pin/...", "took": "big serif numerals, near-black, lots of air"}],
  "draft_calls": [{"call": "Uppercase serif, left-aligned", "why": "B and C agree; A is the outlier"}],
  "decisions": [{"q": "Dark or light background?", "answer": "Dark", "by": "Designer name"}],
  "notes": "Anything the designer said that doesn't fit a field.",
  "custom_css": "",
  "locked_at": null,
  "locked_by": null
}
```

| field | what it controls |
|---|---|
| `theme` | the layout system from `assets/themes/` (default `foundation`, the website look). Its `defaults` fill in anything below that you leave out |
| `variant` | a named variant of the theme, e.g. `light` or `blue` |
| `colors.bg / text / muted` | background, reading text, labels and sub-lines |
| `colors.accent` | highlighted words (`*like this*`), big numbers, kicker, list numerals. **Must reach 4.5:1 on bg**, since it's used for small labels too |
| `colors.fill / on_fill` | progress bar, rules, CTA fill slide, any slide with `"fill": true` |
| `type.display` | headlines and numbers; `display_case: "upper"` or `"none"` |
| `type.scale` | px sizes at full 1080 width. Keep body at 36px or more and labels at 22px or more |
| `layout.align` | `left` (editorial, easier to scan) or `center` (poster-like, fewer words) |
| `layout.margin` | px from the edge to the text; 80 minimum so the profile-grid crop never bites |
| `layout.texture` | brand patterns `weave` (crossing diagonals), `loop` (circles), `ascent` (rising blue lines), or `grid`, `dots`, `none`. A single slide can override it with `"texture"` |
| `layout.counter`, `layout.kicker` | off by default and should stay off: house rules ban slide numbers and anything above the headline |
| `layout.min_text_px` | 34 (house rule): the renderer lifts any smaller text to this |
| `layout.last_cue` | optional cue on the last slide instead of the swipe cue, e.g. `"YOUR TAKE ↓"` |
| `layout.cta_fill` | CTA slide on the fill colour: a strong visual stop at the end |
| `pillar` | the content pillar this look was made for; used to find a vision to reuse |
| `references[]` | what you took from each image in `refs/` (A, B, C in file order). Shown under each reference on the board |
| `draft_calls` | choices you made without asking, each with a one-line why. Shown on the board as "not yet confirmed"; drop them as answers settle them |
| `custom_css` | escape hatch for a designer request the fields can't express. Use sparingly; the check workflow judges brand match from the result |

Colours come from `brand.json`. Picking a colour outside the palette is flagged by
The check workflow. Do it only when the designer explicitly asks, and record that in `decisions`.

**Contrast trap:** a saturated brand blue that's fine as a fill usually fails as text on a dark
background. The board shows every pair's ratio. Use a lighter tint from the palette as `accent`
and keep the saturated one as `fill`.

## 2. Reading references

For each reference you can actually see, note in `references[]` what you're taking from it:

- **Ground**: dark, light or colour? Flat or textured?
- **Type**: serif or sans, case, how big the headline is relative to the body, how many sizes
- **Layout**: left or centred, dense or airy, where the hook sits, what repeats on every slide
- **Devices**: giant numbers, rules, grids, photos, screenshots, icons, highlight colour on one word
- **Mood**: three to five plain words a designer would agree with

Then map each choice onto the closest thing inside the brand. Where references disagree with
each other (one dark, one light), that's a question, not a guess. Where a reference depends on
something outside the brand, that's a question too. Where they agree, decide it yourself and log
it in `draft_calls`.

With an empty `visions/` folder, "our look" is `brand.json`: the palette, fonts, `rules` and the
`look` paragraph. A vision line like "loud, but still us" means stretching inside those, for
example one big colour block or one giant number, not adding new colours or fonts.

One vague line ("clean, techy, big numbers") is enough to draft from. A detailed spec is
followed as written, and you only ask about gaps.

## 3. Reusing a locked vision

`visions/` holds every locked look, each with `used_for` (slugs) and `locked_at`.

- The designer says "usual", "same as last", or names one: load it, set `status: "draft"`,
  re-render with the new rough script, and ask only about what this brief changes. A topic with
  no numbers doesn't need a number-led cover, for example.
- No references and one obvious candidate for this pillar: propose it with a single question
  ("Use *techy-big-numbers* again? Yes / Yes but light / New look").
- Any change the designer approves gets saved as `<name>-v2`, never overwritten.

## 4. Question bank

Pick at most five, and only ones that are actually open. Phrase options in a few words. Always
mark the recommended one and say why in one line, ideally pointing at a reference. The bank is
a starting point. Write your own question (with your own `id`) when the references call for it.
When references split several ways, a `direction` question with blended options ("Dark like B,
with C's centred layout") usually beats asking each dimension separately.

Keep every option self-contained. If picking A in one question changes what another question
means, merge the two into one question whose options spell out the combinations.

| id | question | options |
|---|---|---|
| `ref` / `direction` | Which reference is closest? / Which direction? | A / B / C, or blends ("Dark like B, centred like C") |
| `bg` | Dark or light background? | Dark · Light |
| `lead` | Lead the cover with a number, a question, or a bold claim? | Number · Question · Claim |
| `length` | How many slides? | 5 · 7 · 10 |
| `template` | Usual template or a new layout? | Usual (`<vision name>`) · New |
| `case` | Headline style? | UPPERCASE serif · Sentence case |
| `align` | Text alignment? | Left (editorial) · Centred (poster) |
| `texture` | Background? | Plain · Blueprint grid · Dots |
| `accent` | Which accent colour? | Two or three palette colours that pass 4.5:1 on the chosen background |
| `highlight` | Accent colour on…? | One key word per slide · Numbers only · Nothing |
| `fill_slides` | Which slides get the full colour block? | Cover and end · End only · None |

Questions the designer shouldn't be asked: anything about copy (that's ours to write), the
slide order, or a choice that's already in their references or the locked vision. Slide count
is ours too, unless the brief leaves it genuinely open.

`fill_slides` maps to `layout.cta_fill` (end slide) and `"fill": true` on the cover in `script.json`.

## 5. questions.json / answers.json

Async mode writes this, sets stage `waiting_on_designer` and stops:

```json
{
  "carousel": "ai-pilot-handoff",
  "round": 1,
  "to": "designer",
  "asked_at": "2026-10-14T10:30:00+05:30",
  "board": "board.png",
  "questions": [
    {
      "id": "bg",
      "text": "Dark or light background?",
      "options": [{"key": "dark", "label": "Dark (near-black)"}, {"key": "light", "label": "Light (paper)"}],
      "recommended": "dark",
      "why": "Refs B and C are both dark, and the big numbers pop more."
    }
  ]
}
```

The pipeline (Slack/email buttons, a form, a person) writes back:

```json
{"answers": {"bg": "dark", "lead": "number"}, "by": "Designer name", "at": "2026-10-14T12:05:00+05:30"}
```

or, when the deadline passes with no reply:

```json
{"use_defaults": true, "at": "2026-10-15T09:00:00+05:30"}
```

Answers may also be free text ("dark, but warmer"). Interpret them, record the original wording
in `decisions`, and ask a follow-up only if you genuinely can't act on it.
