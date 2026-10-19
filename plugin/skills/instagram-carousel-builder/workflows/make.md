# Make a carousel

This is Step 04 (Make) of the content pipeline, for carousels. It takes a topic and a hook, and produces a
carousel folder that the check workflow scores in Step 05.

**No questions, no approvals.** The person gives a topic and a hook (and maybe a reference photo); everything else
is your call: the angle, the design, the copy, the slide count. Make each open decision, and list every one of them
in the hand-off (section 8), so the person can overrule it afterwards. The one exception: if the idea isn't a
carousel at all (section 1), say so and ask.

**Every carousel gets its own design.** That is the point of this skill. A design is mixed from the library, or
extracted from a reference photo; it is never picked from a fixed list, and it never repeats one of the last 5 posts
(`references/design-system.md`).

## The workspace

All state lives in files, so a fresh session or a scheduled run can pick up where the last one stopped. Don't rely
on conversation memory.

```
<skill-dir>/                     (this skill, read-only)
  assets/designs/*.design.md     the design library: 8 specs to mix from
  assets/slide-base.html         the HTML contract and starting point for every slides.html
  assets/brand/brand.json        handle, footer and the voice "never" list; assets/brand/voice.md
  examples/                      two finished posts to copy the shape of (brief, script, design, slides.html)
<working folder>/
  designs/                       every design made so far (log.json holds the fingerprints; the last 5 are checked)
  carousels/<slug>/
    brief.md              the brief + evidence (numbers must trace to this) + story + share test + search terms
    refs/                 reference photos the person attached (never committed)
    design.md             this post's design: fingerprint + spec
    script.json           the copy, slide by slide                       -> references/script.md
    caption.md            the post caption, as it will be posted          -> references/caption.md
    slides.html           the slides, written by hand from the design     -> references/design-system.md, visuals.md
    slides/01.png ...     rendered slides, 1080x1350
    board.png             design summary + every slide at phone size, with flags
    render_report.json    what the browser measured (clipping, overlaps, type sizes, contrast, fonts)
    status.json           stage + history (scripts/status.py)
    check/                written by the check workflow
    exports/              PDFs (scripts/export_pdf.py)
```

Run commands from the working folder (in claude.ai chat: `/home/claude/work`, see "Running in claude.ai chat" in
SKILL.md, which also covers delivery to `/mnt/user-data/outputs/` and design history for a fresh chat). Scripts are in this skill's `scripts/` folder: call them by absolute path.
`render.py` sets the stage `rendered` itself; use `status.py` for every other move, so the history says what happened.

## Start by reading status.json

| stage in `status.json` | what to do |
|---|---|
| no folder yet | 1 Intake |
| `designed` | 3 Script and caption, then 4 Build |
| `rendered` | done; hand to the check workflow |
| `needs_fix` | 7 Fix round |
| `awaiting_approval`, `needs_human`, `approved` | not yours; the check workflow and the approver own these |

## 1. Intake

**First, is this a carousel?** A carousel needs an idea with sequence, worth re-reading: steps, a framework with
parts, a before and after, a checklist. If the idea is one claim, or its payoff has to be seen moving, say so plainly
("this is one sharp claim; it'll land better as a single image or a Reel") and only build it if the person still wants
a carousel. Stretching one claim across 6 slides is what makes people stop swiping.

Make `carousels/<slug>/` (slug = 2-5 kebab-case words) and write `brief.md` with: the idea, pillar, audience, **our
angle** (one opinionated line), the goal and CTA (save, send, follow, read the blog...), the variant (`standard` or
`blog-plug` + blog URL), an **Evidence** section with links, numbers and quotes copied verbatim from the brief, and a
**`## Search terms`** section: 2-3 phrases people would actually type into Instagram search ("claude code plugins", not
"#claudecode"). The caption and alt text carry them as plain words; lint checks they're there.

If the brief has no evidence, this carousel uses no statistics. That's fine: steps and frameworks carry value without
numbers. The check rejects any number on a slide that isn't in `brief.md`. Evidence the brief itself marks as
unverified, placeholder or test data **never goes on a slide**, not even with a disclaimer; leave it out and mention it
in the hand-off.

Put any reference photos the person attached in `refs/` and links in `brief.md`. **Look at every reference.** If a link
won't open (Instagram usually needs a login), say so and ask for a screenshot. Never describe a reference you haven't
seen.

## 2. Design

Read `references/design-system.md` once per session.

**A reference photo was attached** → follow `references/reference-mode.md`: extract the design exactly and write
`design.md` with `kind: "reference"`. No mixing.

**No reference** → mix a new design:

Fresh sandbox and the person attached earlier design files? Run `python3 <skill-dir>/scripts/design_log.py import <files>`
first, so the last-5 check has its history.

```bash
python3 <skill-dir>/scripts/design_log.py library        # the specs you can mix from
python3 <skill-dir>/scripts/design_log.py recent         # what the last 5 posts looked like
```

1. Read the last 5 fingerprints. Decide what the new post must *not* look like.
2. Pick 2-3 sources by fit (the topic's tone, the visual the story needs); at least one that none of the last 5 used.
3. Read each chosen spec in full. Take each of the six dimensions (layout, type, colour, emphasis, devices, visual
   style) from one source, or make your own colour; at least 2 dimensions from a second source; change at least one
   value so the result is new. Colours are open (any hex). Fonts are fixed except the headline: body Manrope, labels
   JetBrains Mono, and any Google Font for the display (headline) face (`references/design-system.md` §3a).
4. Make it cohere: one display font and at most two others, one accent colour, a visual style that suits the type.
5. Write `design.md` in the format of `references/design-system.md` §2, with the CSS starter filled in for this design
   and a `## Decisions` section: what came from which source, and why.
6. Run `python3 <skill-dir>/scripts/design_log.py check carousels/<slug>`. If it fails, change the dimensions it names
   and run it again. Don't build anything until it passes.

If the person asks to **reuse a saved design** ("use the design from the AI pilots post"), copy it from `designs/` into
the carousel as `design.md`, add `"reuse": true` to its fingerprint (this exempts it from the no-repeat check), and skip
the mixing.

Then: `python3 <skill-dir>/scripts/status.py carousels/<slug> designed --event designed --note "<sources>"`.

## 3. Script and caption

**You're writing to the checker's bar.** The check scores shares first: a reader has to want to DM this to someone
specific, and Send-worthy must reach 4 for a pass. Read `references/rubric.md` §3 once per session, and answer the
**share test** (`references/script.md` §4) in `brief.md` before writing a word of copy.

Write `script.json` following `references/script.md`, and `caption.md` following `references/caption.md`. The rules that
matter most:

- **The send slide**: one slide that works alone as a screenshot or DM. Build it first.
- **Cover**: the brief's angle, sharpened. 10 words or fewer, specific beats clever, and it must make sense at
  thumbnail size with zero context.
- **Story: PAS or PPP** (`references/script.md` §3). Write the pick and one line of why in `brief.md` under `## Story`.
- **Arc**: problem, pain, the obvious fix fails, **BUT**, insight and how, CTA, in 6 slides at most, with no part of the
  answer before the BUT. The headlines alone must tell the story. Slide 2 doubles as a second cover.
- **One idea per slide, 30 words max** of reading copy. If it needs more, it's two slides.
- **Numbers only from `brief.md` evidence**, with a source line on stat slides.
- **One CTA**, matching the brief's goal and tied to the payoff. Send CTAs name the recipient. Never engagement bait
  ("comment MOD", "tag a friend"): lint blocks it.
- **Caption**: line 1 is a second hook (125 characters max, not the cover again), the body adds context and search
  keywords, one ask, 3-5 precise hashtags.
- **Sound like a person**: contractions, plain words, numerals not number words, no em dashes, no stock AI phrasing, none
  of the machine-written shapes lint flags. If the `ig-human` skill is installed, run its humanizer.

## 4. Build the slides

Write `slides.html` by hand: start from `assets/slide-base.html` (its header comment is the contract), paste in the
CSS starter from `design.md`, and write one `<section class="slide">` per slide in the order of `script.json`. Then draw
the visuals (`references/visuals.md`) in the design's visual style.

The contract `render.py` measures (everything else is yours): `.slide` exactly 1080x1350; one `.headline` per slide,
the first text on it; a `.visual`; `.foot` with `.site` = `BUILDABLELABS.COM` and, on every slide but the last, a `.cue`;
decoration only inside `.decor`. House rules (gates): nothing under 34px (SVG text as drawn), no weight under 400, no
overlaps or clipped text, no dead space, no logo, no slide numbers, no kicker, 6 slides at most.

Vary the layout between slide types within the design (the cover, a point slide, a steps slide and the CTA shouldn't be
the same arrangement), but keep the margins, headline position and footer fixed so the set reads as one system.

## 5. Render and fix what the browser measured

```bash
python3 <skill-dir>/scripts/render.py carousels/<slug>
```

It screenshots every slide and prints what it measured. **Fix every flag in `slides.html` and render again** until it
prints "all slides clean". Then **look at `board.png` and every slide image**: lint can't see an ugly composition, a
visual that doesn't explain anything, or a design that drifted from `design.md`. For a reference design, run the
fidelity check (`references/reference-mode.md` §6) too.

## 6. Save the design and hand off

```bash
python3 <skill-dir>/scripts/design_log.py save carousels/<slug>
```

This logs the design so the next post won't repeat it. Stage is now `rendered`. Tell the person (or the pipeline) the
carousel is ready for the check workflow, with:

- the board, a one-line summary per slide, the caption, and the share-test answers (who sends it to whom, which slide
  is the send)
- **the design**: its name, what it was mixed from (or the reference it copies), and the one-line reason for each
  dimension taken
- **every decision made without asking**: angle, story (PAS or PPP), slide count, evidence left out, fonts and colours
  chosen, anything you changed to satisfy the no-repeat check or the house rules

Don't score your own work. The check runs in a fresh context because the session that made the slides is the worst
placed to judge them.

## 7. Fix round

Read the newest `check/round-N.json` (`fixes`) and any `approver_notes` in `status.json`.

- Change **only** the slides and lines listed. Slides that weren't flagged were scored; touching them risks new
  failures and makes rounds impossible to compare.
- If a fix says split a slide, split it (and update `script.json`). Re-render with `render.py` (`--only 3,5` re-shoots
  just those images; the report still covers all).
- Keep `script.json` and `slides.html` in step, and `design.md` too if the design itself changed. Then log what changed:
  `status.py carousels/<slug> rendered --event fixed --note "round 1: slide 1 headline cut to 8 words; slide 3 split"` and
  hand back to the check workflow.

## Redo a carousel in another design

1. Copy the folder to a new slug (`carousels/<slug>-<n>`) so the original and its check history stay intact.
2. Delete the copy's `check/`, `exports/`, `design.md` and `slides*`, then go back to section 2 and make a new design
   (a new mix, or the person's reference). It must pass the no-repeat check against the last 5, **including the
   original**: that's the point of redoing it.
3. Rebuild the slides (section 4) from the same `script.json`, fixing copy where the new design needs shorter lines.
4. Hand it to the check workflow as a new carousel (a fresh judge; scores don't carry over between designs).

## Variants and options

- **Blog-plug** (`variant: "blog-plug"`): four slides. Slides 1-3 explain the topic and slide 4 sends people to the full
  blog ("Full breakdown on the blog · link in bio"). Feed links aren't clickable on Instagram, so the URL belongs in the
  caption or bio, not on the slide.
- **PDF**: `scripts/export_pdf.py carousels/<slug>` writes `exports/<slug>.pdf`, one slide per page, built from the
  rendered PNGs so it looks identical in every viewer (WhatsApp, phones, LinkedIn document posts). `--vector` prints the
  HTML instead for selectable text, but phone and chat viewers mis-draw its gradients and shadows, so never share that
  one.
