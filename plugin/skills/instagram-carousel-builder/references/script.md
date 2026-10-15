# Script: slide types, arcs, copy rules

## Contents
1. script.json shape
2. Slide types
3. Arcs by length
4. Copy rules
5. Worked example

---

## 1. script.json shape

```json
{
  "title": "Your AI pilot didn't fail. Your handoff did.",
  "variant": "standard",
  "blog_url": null,
  "slides": [ { "type": "cover", "headline": "...", "sub": "...", "alt": "..." } ]
}
```

Slides are numbered by position, so don't store `n`. **Every slide carries one `visual`** (a drawn UI
mockup or diagram: `window`, `hud`, `flow`, `slots`, `dialog`; see `visuals.md`), an `image`, or a big sourced
`number`; slide 1's must be an infographic, a visual with information in it. Some themes print `ghost` (a big
background word) and `badge` (circular badge text); other themes ignore them. Optional on any slide: `align`
(override), `fill: true` (put this slide on the fill colour; at most once besides the CTA), and `alt` (alt
text, required on the cover and good on all slides). There's no kicker: house rule, the headline is the first
thing on every slide. Never a slide number either.

Wrap one to three words in `*asterisks*` to set them in the accent colour, once per slide at
most. On a headline it reads as an italic accent; in body text it reads as bold.

## 2. Slide types

| type | use it for | fields |
|---|---|---|
| `cover` | the hook | `headline` (≤10 words), `sub` (one promise line), `number` (optional: lead with a stat), `alt` |
| `stake` | why it matters; slide 2's job | `headline`, `body` |
| `point` | one insight | `headline`, `body` |
| `stat` | one sourced number | `number`, `headline`, `body`?, `source` (required) |
| `steps` | a numbered how-to, 3-5 items | `headline`, `items[]`, `body`? |
| `quote` | a real quote from the evidence | `quote`, `attribution` |
| `recap` | the screenshot slide | `headline`, `items[]` (≤5 items, ≤6 words each), `numbered`? |
| `cta` | the one ask | `headline`, `body`?, `action` (`save`·`follow`·`comment`·`read`·`share`·`dm`), `button` |
| `image` | a screenshot or photo in `refs/` | `image` (path relative to the carousel folder), `headline`, `body`? |

## 3. Arcs (6 slides maximum)

House rule: **6 slides at most**. The arc is problem, amplify the pain, the obvious fix fails, **BUT**, the
insight and how, CTA. No part of the answer before the BUT. Read the headlines alone, in order: they must
tell the story on their own.

### Pick the story: PAS or PPP

The arc's order never changes. The framework decides **where the slides go**, and it depends on the reader:

| | PAS: Problem → Amplify → Solution | PPP: Problem → Promise → Proof |
|---|---|---|
| Use when | readers **underestimate** the problem, or are confidently doing the wrong thing | readers **already feel** the problem and doubt it can be fixed |
| The hard part | getting them to **care** | getting them to **believe** |
| Where the room goes | slides 2-3: the pain and why the usual fix fails | slide 5: the proof (a before/after, a mechanism, a named example, a sourced number) |
| Send-worthy because | "you need to see this before it bites you" | "this actually works, here's how" |
| Example | "Claude Code mods run with your permissions" (people think mods are toys) | "Your AI pilot can ship in 4 weeks" (founders know pilots stall; they doubt the fix) |

Quick test: **care or believe?** If it's both, pick PAS for news and warnings, PPP for how-tos and results.
PPP needs real proof. If the brief has no evidence, the proof has to be a mechanism, a before/after or a
named example, never an invented number; if none of those exist either, use PAS.

Write the choice and one line of why in `brief.md` under `## Story` (e.g. `PAS: builders treat mods as toys,
so the risk is the news`). The copy review and the judge both read it.

**6 slides (default)**

| slide | PAS | PPP |
|---|---|---|
| 1 cover | the problem, as a hook | the problem, as a hook |
| 2 stake | **amplify**: what it costs, made personal (second cover) | the problem's cost in one line, compressed: they already know it hurts (second cover) |
| 3 point | **the obvious fix, and why it fails** | **the promise**: the BUT, stated as a clear outcome |
| 4 point | **the BUT**: the turn | the better way: what changes |
| 5 steps / stat / point | the insight and how (usually the send slide) | **the proof**: before/after, mechanism, example or sourced number (usually the send slide) |
| 6 cta | one ask, calling back to the hook | one ask, calling back to the hook |

**5 slides**: PAS: cover · stake · point (obvious fix fails + BUT) · steps *or* stat · cta.
PPP: cover · point (problem compressed + promise) · point (the better way) · proof · cta.

**Blog-plug, 4 slides**: cover · stake *or* stat · point (the sharpest takeaway, left a little
open) · cta (`action: "read"`, "Full breakdown on the blog · link in bio").

### Bridges: every slide hands off

Each slide leaves a small open loop the next one closes. If you can't write the bridge between two
slides, the order is wrong or a slide is missing.

- **Question, then answer**: a slide ends on a question; the next headline answers it.
- **"But", "So", "Which means"** opening the next headline.
- **Escalation**: "That costs a week." then "Now multiply it by every team."
- **Contrast**: "What most teams do" then "What the ones who ship do".
- **An evolving visual**: the funnel loses another stage, the bar fills, the timeline moves on.
- **Callback**: the CTA uses the hook's words ("mod" on the cover, "first modder" on the CTA).

## 4. Copy rules

**Write to the checker's rubric.** the check workflow scores shares first (`references/rubric.md`,
evidence in `engagement-research.md`). Before writing, answer the **share test** in one line each, and
put the answers in `brief.md` under `## Share test`:

1. **Who sends it to whom?** "A founder sends it to their ops lead." If you can't name the pair, the
   angle isn't specific enough yet.
2. **Which slide is the send?** The one slide that works alone as a screenshot or DM: a checklist, a
   framework, a before/after, a stark reveal. Build it first, then build the rest around it.
3. **What's the "wait, really?"** The surprise, or the fix someone needs this week. Mild agreement
   doesn't get forwarded.
4. **Why does sending it make the sender look sharp?** Early, insightful, practical. If the post reads as
   an ad for us, it won't be sent.

Then the line-by-line rules:

These are the rules the check workflow scores against, so following them here saves a round.

**Cover (hook).** Take the brief's angle and sharpen it. Ten words or fewer.
Make a specific claim or promise the target founder feels, not a topic label ("AI Pilots" is a
label; "Your AI pilot didn't fail. Your handoff did." is a hook). It has to read at
profile-grid thumbnail size, so fewer, bigger words win. The `sub` line says what they get by
swiping.

**Slide 2 is a second cover.** Instagram re-serves carousels starting at slide 2 to people who
skipped the first time, so it can't be setup ("So here's why..."). It has to hook on its own:
the stake, the surprising stat, the cost of getting it wrong.

**Flow.** One idea per slide. Every slide should leave a reason to swipe: a question
opened, a list started, a "but". If a slide could be deleted without anyone noticing, delete it.

**Readability.** 30 words of reading copy per slide at most (headline + body + items). If it
needs more, it's two slides. Headlines read best under 12 words, and body copy should be one or
two sentences.

**Value.** Something worth saving: a step, a framework, a number, a line people would
screenshot. The recap slide exists for that. **Numbers come only from `brief.md` evidence**, and a
stat slide always has a `source`. No evidence means no stat: use a step or a framework instead.
Evidence the brief marks as unverified, placeholder or test data doesn't count, so leave it off
the slides entirely. Quotes are real quotes from the evidence with attribution, never invented
testimonials. You can quote one complete clause or sentence on its own. Don't change its words,
and mark any cut inside it with "...". Capitalising the first word is fine.

**CTA.** One action, matching the brief's goal, tied to the payoff: "Save this before your
next pilot kickoff" beats "Follow for more". If you'd write two verbs (save *and* follow), pick
one. A **send** CTA (`action: "share"`) names the recipient and the reason: "Send this to whoever's
installing mods this week". Never bait: no "tag 3 friends", "comment YES", "comment MOD for the
link", "like if". Instagram demotes it and lint blocks it. For blog-plug, the action is `read`.

**Caption.** Write `caption.md` with the slides; it's scored too. Line 1 is a second hook, and the
body adds what the slides don't. Format and rules: `caption.md`.

**Voice.** Write like a founder talking to a founder: contractions, plain words, concrete nouns,
our real opinion. No em dashes. No stock AI phrasing ("unlock", "leverage", "game-changer",
"in today's fast-paced world", "it's not just X, it's Y", "here's the thing"). If the
`ig-human` skill is installed, run its humanizer over the joined copy before rendering.

## 5. Worked example

`examples/claude-code-mods/script.json`: 6 slides, a visual on every slide (window, hud, flow, slots, window,
dialog), a send goal, the share test in its `brief.md`, and a `caption.md`. It passed the check workflow at 4.08.
Read its headlines alone: "You can now mod Claude Code like a video game." → "Your coding session can have a
health bar." → "A mod runs inside Claude Code." → "Pick your loadout." → "Mods aren't sandboxed. Check first."
→ "Send this to your team's first modder."
