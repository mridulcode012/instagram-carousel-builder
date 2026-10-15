# Carousel rubric: how to judge

Weights and the pass rule live in `../rubric.json`. This file is how to score each line so that
two judges on two different days land within a point of each other.

## Contents
1. How to judge
2. Gates (pass/fail) and how to measure by eye
3. The eight lines, anchored
4. judge-rN.json format

---

## 1. How to judge

- **Judge the images, not the intent.** Look at every PNG in `slides/` in order, the way a
  person on a phone would see it. `script.json` tells you what was meant; the slides show what
  shipped. If they differ, the slide wins.
- **Start each line at 3, and move only on evidence you can point to.** A 4 needs a reason you
  can quote from a slide. A 5 is rare: you'd screenshot or send this yourself, and you can say
  exactly why.
- **Cite slides.** Every `evidence` names slide numbers and quotes or describes what's there
  ("Slide 1: '95%' at full width, headline in 9 words"). `score.py` rejects evidence without
  slide numbers. The Caption line is the exception: it quotes the caption ("Caption line 1: ...").
- **Read the caption as part of the post.** `caption.md` is posted with the slides; judge it the way
  it shows in the feed: line 1 alone, then the rest after "...more".
- **Every score under 5 says how to reach 5.** One concrete change: "Slide 4: cut the second
  sentence; it repeats slide 3". This becomes the make workflow's to-do list, so vague notes ("make it
  punchier") waste a round.
- **Read `check/lint.json` first.** Its caps are applied automatically. Don't re-argue them, and
  don't double-penalise a capped problem in a second line unless it really hurts that line too.
- **Score lines, not the verdict.** Don't add up the weights or predict PASS/FIX; `score.py` does
  that, and knowing the outcome tends to pull scores towards it.
- **No render report?** (Canva or hand-made slides.) Then look deliberately for clipped text,
  text running into the edges, tiny type and fonts that look like a default fallback, and score
  Readability and Brand with that in mind.
- **Expect most first drafts to fail at least one line.** That's the loop working. A
  competent-but-generic carousel lands around 3 to 3.5, and the pass bar is 4.0 on purpose.
- **The angle is approved; the wording isn't.** The brief's angle was approved upstream (Step 03).
  Fixes can sharpen how it's said, but they never swap it for a different idea. If you think the
  angle itself is weak, say so in `summary` for the approver, not as a fix.
- **One fix per problem, and no tug-of-war.** If two changes on one slide pull against each other
  (shorter vs. more specific), write a single fix that resolves both.
- **Don't fix anything.** Score and note. The maker fixes.

## 2. Gates (pass/fail) and how to measure by eye

These are Instagram house rules from the account owner. **Any failed gate blocks a pass**, however good the
scores. Lint already measures some of them (missing visual fields, text size, slide count, the counter, promo
phrases, unsourced numbers, bait) and lists them in `check/lint.json → gates_failed`. You rule on what only eyes can
see: write a ruling for every gate marked "judge" in `../rubric.json`.

| gate | fails when |
|---|---|
| G1 Visual on every slide | Any slide is text-only or its visual is decoration that explains nothing; or slide 1 has no **infographic** (a visual with information in it: numbers, comparison, process, labeled diagram) |
| G2 No dead space | Any slide has an empty area over ~20% of the slide that reads as a gap (a full-width band taller than ~270px, or a ~600x600px empty block). Even gaps between elements are fine |
| G3 No overlaps | Text on text, text crossing icons or card edges, objects colliding, anything hidden behind a card, a highlight block touching the line above or below |
| G4 Nothing under 34px | Any text, including labels, chips, diagram text and footer, is under 34px at 1080px width |
| G5 No logo | The Buildable Labs mark or wordmark anywhere. The plain-text footer `BUILDABLELABS.COM` is not a logo |
| G7 No slide numbers | Any counter or page number: "01 / 06", "3/7", numbered slide labels, giant ghost numerals |
| G8 No self-promotion | Any slide or the CTA promotes Buildable Labs or its services ("we help...", "book a call", "free consultation") |
| G10 No engagement bait | "Tag a friend", "comment YES", "comment MOD for the link", "like if", "share if". A plain question to the reader is fine |

(G6, 6 slides max, and G9, every number sourced, are lint-only.)

**Measuring by eye.** Slides are 1080 x 1350; if an image is another width, scale by width / 1080.
- **Text size**: capitals and digits are about 0.73x the font size tall, lowercase x-height about 0.55x.
  34px text has capitals about 25px tall and x-height about 19px; 44px is about 32/24; 88px is about 64/48. Capitals under
  ~24px mean the text is under 34px. Condensed display faces have taller capitals, so allow a little.
- **Visual weight**: on every slide the visual takes roughly 40-60% of the slide.
- **Contrast**: grey or secondary text must read clearly on a phone (about 4.5:1). Pale grey on white and dim
  grey on black both fail.
- **Overlaps**: zoom in wherever elements meet.
- **Grid crop**: slide 1 also shows in the profile grid as a narrower crop, so the hook and key visual must
  stay clear of the left and right edges.

## 3. The eight lines, anchored

The lines are ordered by weight. The weights favour **shares first**: on Instagram a DM send is the
strongest signal for reaching people who don't follow us yet, and Send-worthy has to score **4 or
more** for any carousel to pass. Why each line exists, with sources: `engagement-research.md`.

### Send-worthy (20%, must be 4+): would someone DM this to a specific person?

Ask four questions, and write the answers into `reason`:
1. **Who exactly would they send it to?** ("my cofounder", "our ops lead", "the friend who just installed Claude Code"). If you can't name one, it isn't send-worthy.
2. **Is there one slide that works alone as a screenshot or DM?** (a checklist, a framework, a before/after, a stark reveal)
3. **Does it surprise or genuinely help?** (high-arousal: "wait, really?", awe, amusement, a useful fix) Mild agreement doesn't get forwarded.
4. **Does sending it make the sender look sharp?** (early, insightful, practical). A post that reads as an ad for us makes the sender look like they forward ads.

| score | looks like |
|---|---|
| 5 | All four, clearly. The recipient is obvious from the cover, one slide is a perfect standalone send, and it carries a real surprise or a fix someone needs this week. You would send it yourself |
| 4 | Clear recipient and a strong sendable slide, but the surprise is mild or the useful bit is generic in places |
| 3 | Interesting to the reader but not *for someone else*: no obvious recipient, or no slide that stands alone |
| 2 | Reads as information or as our promotion, with nothing to pass on. Also the cap for engagement bait |
| 1 | Nobody would send this |

### Hook slide (18%): stops the scroll

| score | looks like |
|---|---|
| 5 | Understood in 0.5 seconds: a specific, slightly surprising claim or promise the target reader feels, in 10 words or fewer, bold and conversational. It opens a curiosity gap only swiping answers, and the slide-1 infographic shows the promise and makes it pop in the feed (clear of the grid-crop edges). *"Your AI pilot didn't fail. Your handoff did."* |
| 4 | Clear, specific and legible at thumbnail size, but the tension is mild, the claim is familiar, or the cover is busy enough that the eye doesn't know where to land |
| 3 | The topic is clear but generic ("5 tips for AI adoption"), or a good line weakened by small type, a busy layout or decoration that explains nothing |
| 2 | Vague, or clever but unclear: the reader can't tell what they get |
| 1 | A label, not a hook ("AI Pilots"), or illegible |

### Story flow (14%): swipe-through, from slide 2 to the payoff

| score | looks like |
|---|---|
| 5 | **Read only the headlines, in order: they tell the story on their own.** The arc lands in six slides: problem, amplify the pain, the obvious fix fails, **BUT** (the turn), the insight and how, CTA. No part of the answer appears before the BUT. Slide 2 hooks on its own as a second cover (Instagram re-shows carousels from slide 2). Every slide picks up the previous one's thread, and nothing repeats |
| 4 | A clear arc with one idea per slide, but one transition is flat, the BUT is weak, slide 2 leans on slide 1, a visual repeats instead of revealing something new, or the framework in `brief.md → ## Story` doesn't fit the reader (PAS spends slides amplifying a pain readers already feel; PPP's proof slide has no real proof) |
| 3 | Logical but flat: the answer comes before the turn, slides read as independent points, a filler slide, or slide 2 is setup ("So here's why...") |
| 2 | Two ideas crammed on a slide, or the order wanders |
| 1 | A caption chopped into pieces; slides in no particular order |

### Value (12%): worth saving and coming back to

| score | looks like |
|---|---|
| 5 | A reader could act on it today and would save it as a reference: a checklist, named steps, a framework or a sourced number, plus at least one concrete specific (a real command, a named example, a figure from the brief). **A complete beginner gets every slide immediately**: plain words, numerals not spelled-out numbers, no jargon walls |
| 4 | Useful and specific; the takeaway is slightly less sharp or not quite reference-worthy |
| 3 | Sensible but generic ("communicate clearly", "start small"), or the examples are unnamed |
| 2 | Thin; mostly restating the hook |
| 1 | No takeaway, or claims that aren't backed (unsourced numbers are capped by lint anyway) |

### Readability (10%): easy on a phone

| score | looks like |
|---|---|
| 5 | Every slide is read in about 3 seconds at phone size: one focal point, an obvious reading order (headline, visual, support line), the visual taking roughly 40-60% of the slide, space shared evenly with no awkward gaps, and the type scale held (headline about 88px, hook up to 120px, body 44, main line 40, card text 36, labels and footer 34; no light weights, at most one highlighted phrase per headline) |
| 4 | Easy everywhere; one slide is a little dense, its hierarchy is soft, or one element is low contrast |
| 3 | Readable but several slides near the word limit, or hierarchy unclear (everything the same weight) |
| 2 | Walls of text, cramped margins, or low contrast somewhere |
| 1 | Clipped text, unreadable sizes, or the wrong dimensions |

### Brand match (10%): original, and recognisably ours (brand themes)

| score | looks like |
|---|---|
| 5 | A clean render (crisp, aligned, no clutter or faded ghost words behind cards) that looks exactly like the locked vision on `board.png` and its theme (`assets/themes/<theme>/preview.png`): the headline is the first element on every slide, the footer reads `BUILDABLELABS.COM` bottom-left with a swipe cue bottom-right, and every rule in `brand.json` → `rules` and `assets/brand/design-rules.md` holds (check them one by one: palette and usage ratio, emphasis style, type roles, labels, buttons, patterns, the imagery "never" list). Consistent across all slides. Original: our angle, visuals and evidence, nothing reposted. The voice is calm conviction, not hype |
| 4 | On-brand; one inconsistency (a slide with a different alignment, an extra accent, a rule miss) |
| 3 | On palette but drifting: sizes jump between slides, the accent is overused, or the locked vision is loosely followed |
| 2 | An off-brand font or colour, hype voice, or it reads like a different account |
| 1 | Unrecognisable as ours, or someone else's content |

### Design (10%, replaces Brand match on free themes)

Use this table instead of Brand match when the theme's `theme.json` says `"brand": "free"` (lint adds a
`free_theme` note). These themes leave the brand on purpose, so don't mark them down for off-brand colour
or type. Ask whether the look will do well on Instagram:

| score | looks like |
|---|---|
| 5 | Stops the scroll on its own: a bold, distinctive visual system you'd recognise in the grid with the handle covered. Colour, type and devices feel deliberate and consistent across every slide, and it matches its theme preview. Every slide reads at thumbnail size. Type is legible (display faces only for display), contrast is strong, nothing looks cheap or templated. Original: no stock photos, nothing that looks like someone else's post |
| 4 | Strong and consistent; one weak slide, one device overused, or a display face pushed into body text |
| 3 | Pleasant but generic or template-like; or busy enough that the eye doesn't know where to land |
| 2 | Inconsistent between slides, hard to read in places, or clashing colours |
| 1 | Looks broken, cheap or unreadable |

### Call to action (8%): one honest ask

| score | looks like |
|---|---|
| 5 | One short, specific action tied to the payoff and the brief's goal, ideally a callback to the hook, with no explanation and no promotion: a **send** ask that names the recipient and the reason ("Send this to whoever's installing mods this week"), a **save** ask that names the moment, or a **question** a founder can answer in a few words ("Which one would you install first?"). Visually the only primary button |
| 4 | One clear action, slightly generic, or another element competes with the button |
| 3 | Generic ("Follow for more") or two asks |
| 2 | Implied but never stated, or bait ("tag 3 friends", "comment YES") |
| 1 | No CTA |

### Caption (8%): the second hook, and what search reads

Read `caption.md`. Evidence quotes the caption ("Caption line 1: ...").

| score | looks like |
|---|---|
| 5 | Line 1 (before "...more", about 125 characters) is a second hook that is different from the cover and pulls non-swipers in. The body adds what the slides don't (context, why now, a named example), in the words people would search for. It ends on the same single ask as the CTA, then 3-5 precise hashtags. Brand voice, no hype |
| 4 | Good line 1 and one ask, but the body mostly repeats the slides, or keywords and hashtags are generic |
| 3 | Line 1 is a label or repeats the cover; or the caption is long without earning it |
| 2 | Hashtag soup, several asks, or hype voice |
| 1 | Missing, or bait |

## 4. judge-rN.json format

Write `check/judge-r<N>.json` exactly like this:

```json
{
  "judge": "subagent",
  "lines": {
    "share":       {"score": 4, "reason": "Recipient: a cofounder about to run a pilot. Slide 6 checklist stands alone. Surprise is mild.",
                    "evidence": "Slide 1: 'Your AI pilot didn't fail. Your handoff did.'; Slide 6: three-item checklist",
                    "to_reach_5": "Slide 3: lead with the counter-intuitive fact from the brief so the post carries a real surprise."},
    "hook":        {"score": 4, "reason": "...", "evidence": "Slide 1: ...", "to_reach_5": "..."},
    "flow":        {"score": 4, "reason": "...", "evidence": "Slides 2-3: ...", "to_reach_5": "..."},
    "value":       {"score": 3, "reason": "...", "evidence": "Slide 4: ...", "to_reach_5": "..."},
    "readability": {"score": 5, "reason": "...", "evidence": "Slides 1-7: ...", "to_reach_5": ""},
    "brand":       {"score": 4, "reason": "...", "evidence": "Slide 5: ...", "to_reach_5": "..."},
    "cta":         {"score": 5, "reason": "...", "evidence": "Slide 7: ...", "to_reach_5": ""},
    "caption":     {"score": 4, "reason": "...", "evidence": "Caption line 1: '...'", "to_reach_5": "Caption line 1: ..."}
  },
  "gates": {
    "G1":  {"pass": true,  "evidence": "Slides 1-6 each carry an explaining visual; slide 1 shows the 95% stat as a bar."},
    "G2":  {"pass": false, "evidence": "Slide 4: empty band ~320px tall between the list and the footer."},
    "G3":  {"pass": true,  "evidence": ""},
    "G4":  {"pass": true,  "evidence": ""},
    "G5":  {"pass": true,  "evidence": ""},
    "G7":  {"pass": true,  "evidence": ""},
    "G8":  {"pass": true,  "evidence": ""},
    "G10": {"pass": true,  "evidence": ""}
  },
  "risks": [
    {"reason": "The angle is familiar to founders who've run a pilot.", "fix": "Slide 3: lead with the counter-intuitive cost from the brief."},
    {"reason": "...", "fix": "..."},
    {"reason": "...", "fix": "..."}
  ],
  "fixes": [
    {"slide": 4, "line": "value", "note": "Make step 2 concrete: name the metric type (hours saved, tickets closed)."},
    {"slide": null, "line": "caption", "note": "Rewrite line 1 as a second hook: lead with the cost of skipping the handoff."}
  ],
  "summary": "One or two sentences: the verdict in plain words and the single most important fix."
}
```

`judge` is one of `subagent`, `fresh-session` or `same-session`. Scores are integers from 1 to 5. `gates` needs a
ruling for every gate marked `"judge": true` in `../rubric.json`; a failed gate's evidence names the slide. `risks`
is 3-5 honest reasons this might **not** get engagement on Instagram, each with a fix.
`fixes` should cover every line under 4, one note per change, each on a specific slide where
possible. Lint's own findings are added to the fix list automatically, so don't repeat them.
