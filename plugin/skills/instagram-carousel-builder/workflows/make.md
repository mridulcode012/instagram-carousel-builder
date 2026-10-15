# Make a carousel

This is Step 04 (Make) of the content pipeline, for carousels. It takes an approved brief and
produces a carousel folder that the check workflow scores in Step 05.

People only supply taste: references, a vision line and answers to a few questions. Claude does
everything else. Every carousel should need fewer questions than the last one, because locked
visions are saved and reused.

## The workspace

All state lives in files, so a fresh session or a scheduled run can pick up where the last one
stopped. Don't rely on conversation memory.

```
<skill-dir>/                     (this skill, read-only)
  assets/brand/brand.json        palette, fonts, voice, rules: the outer limits of every design
  assets/brand/design-rules.md   how the brand looks on slides (from the Brand Foundation)
  assets/themes/<name>/          layout systems: theme.json + theme.css + preview.png   -> references/themes.md
  examples/claude-code-mods/     a finished post (PAS, poster theme) to copy the shape of
  examples/ai-pilots-stall/      a finished post (PPP, cards theme)
<working folder>/                (where the person runs Claude; created as needed)
  visions/<name>.json            locked visions (reuse them; that is how questions shrink)
  carousels/<slug>/
    brief.md              the approved brief + evidence (numbers must trace to this)
    refs/                 reference images the designer dropped in (A, B, C... in file order)
    vision.json           the look: colours, type, layout, decisions   -> references/vision.md
    questions.json        questions waiting for the designer (async mode)
    answers.json          the designer's answers (async mode)
    script.json           every slide's type and copy                   -> references/script.md
    caption.md            the post caption, as it will be posted          -> references/caption.md
    slides/01.png ...     rendered slides, 1080x1350
    board.png             vision panel + all slides at phone size
    render_report.json    what the browser measured (clipping, fonts, type sizes)
    status.json           stage + history (format and stage list: scripts/status.py)
    check/                written by the check workflow
    exports/              PDFs (scripts/export_pdf.py)
```

The brand kit and themes ship inside this skill (`assets/`). A project that keeps its own
`brand/brand.json` (and optionally `themes/`) in a folder above the carousel overrides them; the
scripts look there first and fall back to `assets/`.

Run commands from the working folder. The scripts live in this skill's `scripts/` folder:
`render.py` renders the slides and board, and `status.py` moves the stage and logs why. Call them by
absolute path. `render.py` sets `vision_draft` or `rendered` itself; use `status.py` for every other
move, so the history always says what happened.

## Start by reading status.json

| stage in `status.json` | what to do |
|---|---|
| no folder yet | 1 Intake |
| `vision_draft` | 3 Questions (or 5 Lock, if the person just approved the board) |
| `waiting_on_designer` | if `answers.json` exists or the person answered in chat, go to 4 Apply answers; otherwise say what you're waiting for and stop |
| `vision_locked` | 6 Script and render |
| `rendered` | done; hand to the check workflow |
| `needs_fix` | 8 Fix round |
| `awaiting_approval`, `needs_human`, `approved` | not yours; the check workflow and the approver own these |

## 1. Intake

**First, is this a carousel?** A carousel needs an idea with sequence, worth re-reading: steps, a framework
with parts, a before and after, a checklist. If the idea is one claim, or its payoff has to be seen moving,
say so plainly ("this is one sharp claim; it'll land better as a single image or a Reel") and only build
it if the user still wants a carousel. Stretching one claim across 6 slides is what makes people stop swiping.

Make `carousels/<slug>/` (slug = 2-5 kebab-case words, e.g. `automate-broken-process`) and write `brief.md` with: the idea,
pillar, audience, **our angle** (one opinionated line), the goal/CTA (save, send, follow, read the blog...),
the variant (`standard` or `blog-plug` + blog URL) and an **Evidence** section with links,
numbers and quotes copied verbatim from the brief, and a **`## Search terms`** section: 2-3 phrases people
would actually type into Instagram search for this topic ("claude code plugins", not "#claudecode"). The
caption and alt text carry them as plain words, because Instagram search reads both; lint checks they're there.

If the brief has no evidence, this carousel uses no statistics. That's fine: steps and
frameworks carry value without numbers. The check workflow rejects any number on a slide that
isn't in `brief.md`, because a made-up stat on a company account costs more than a weak slide.
Evidence the brief itself marks as unverified, placeholder or test data **never goes on a slide**,
not even with a disclaimer. Leave it out and mention it in the hand-off. Lint blocks it anyway.

Put reference images in `refs/` and links in `brief.md`. **Look at every reference.** If
a link won't open (Instagram usually needs a login), say so and ask for a screenshot. Never
describe a reference you haven't seen; the whole vision is built on it.

## 2. Vision: reuse or draft

Read `assets/brand/design-rules.md` once per session; it's how the brand looks on a slide. Then
**pick a theme** (`references/themes.md` §2 has a table of what each suits): `foundation`, the website look, is the default.
Read `references/vision.md` for the vision.json fields and how to turn references into decisions
within that theme.

- **Reuse** when the designer says "usual"/"same as last time", or gives no references and
  `visions/` has a locked vision for this pillar. Start from that file and ask only about what
  this brief changes (often zero or one question).
- **Draft** otherwise. Choose the theme the references sit closest to, then translate the
  references and the vision line into `vision.json` (variant, texture, sizes, colours), staying
  inside `brand.json` (palette and fonts). If a reference depends on something outside the brand,
  such as a neon colour or a font we don't own, ask instead of copying it.

"Us" means `brand.json`: its palette, fonts, `rules` and the `look` paragraph, plus whatever is in
`visions/`. When a vision line says "but still us", that's the yardstick.

Record what you took from each reference in `references[]`, and every choice you made without
asking (case, alignment, size tweaks) in `draft_calls`. The board shows both next to the
reference images, so the designer can see your reasoning without opening anything else.

Then write a draft `script.json` so the board shows real slides. Draft means the right slide types
in the right order, with copy that's close but not polished; it gets finished after the lock.
Default to 6 slides, the house maximum (`references/script.md` §3). Render it:

```bash
python3 <skill-dir>/scripts/render.py carousels/<slug>
```

`board.png` is the vision board: mood, palette with contrast ratios, type, decisions, and every
slide at roughly phone size. A designer can react to that far faster than to a description.

## 3. Questions (3-5, tap-to-answer)

Ask only what the references, the vision line and any reused vision leave open. Each question
gets 2-4 short options, a recommended default and one line on why it matters. The question bank
is in `references/vision.md`. Use it as a starting point and write your own when the references
call for it. Make every option self-contained: if one answer would change what another question
means, merge them into one question. Three good questions beat five; zero is fine for a reused
vision. Copy, slide order and slide count are ours to decide. Only ask about length when the
brief leaves it genuinely open.

- **A person is in the chat:** show `board.png` and ask. If a question tool is available (e.g.
  AskUserQuestion, which takes up to 4 at a time), use it. Otherwise list options as A/B/C.
- **No one is present** (scheduled run, pipeline, or the prompt says async/unattended): write
  `questions.json` (format in `references/vision.md`), run
  `status.py carousels/<slug> waiting_on_designer --event questions_sent --note "round 1, 3 questions"`, and stop.
  The pipeline delivers the questions over Slack/email and drops `answers.json` in the folder.

## 4. Apply answers

Update `vision.json`, record each answer in `decisions` (question, answer, who), and drop any
`draft_calls` the answers settled (a "yes, as on the board" answer settles the calls the board
showed). If `answers.json` says `"use_defaults": true` (nobody answered in time), apply the
recommended options and record them as defaults. Log it:
`status.py carousels/<slug> --event answers_applied --note "..."`.

If nothing is left open, go straight to step 5; there's no need to render in between. Ask a second
round only if an answer created a new ambiguity, and keep it to two questions.

## 5. Lock

When the designer approves the board, or answers leave nothing open, set `status: "locked"` with
`locked_at` and `locked_by`. In async mode, answering the questions *is* the sign-off. The designer
sees the finished slides again at Human check 2, so don't add a round-trip just to approve a board.
The exception: if their answers moved the look a long way from the board they saw (a different
direction, a different background), send one more `questions.json` with the updated board and a
single "Looks right? Yes / Changes" question. Then save a copy to `visions/<name>.json` with this slug in
`used_for`. If the designer changed a library vision, save the result as a new version
(`<name>-v2`) rather than overwriting it, because older carousels still point at the look they used.
Then run `status.py carousels/<slug> vision_locked --event locked`.

## 6. Script and render

**You're writing to the checker's bar.** the check workflow scores shares first: a reader has to want to
DM this to someone specific, and Send-worthy must reach 4 for a pass. Read
`references/rubric.md` §2 once per session, and answer the **share test**
(`references/script.md` §4) in `brief.md` before writing a word of copy.

Write the final `script.json` following `references/script.md`, and `caption.md` following
`references/caption.md`. These are the rules that matter most:

- **The send slide**: one slide that works alone as a screenshot or DM. Build it first.
- **Cover**: the brief's angle, sharpened. 10 words or fewer, specific beats clever, and it
  must make sense at thumbnail size with zero context.
- **Story: PAS or PPP** (`references/script.md` §3). PAS when readers underestimate the problem (you have to
  make them care), PPP when they already feel it and doubt the fix (you have to make them believe). Write the
  pick and one line of why in `brief.md` under `## Story`.
- **Arc**: problem → pain → the obvious fix fails → **BUT** → insight and how → CTA, in 6 slides at most,
  with no part of the answer before the BUT. The headlines alone must tell the story. Slide 2 doubles as a
  second cover, because Instagram re-shows carousels from slide 2 to people who scrolled past.
- **One idea per slide, 30 words max** of reading copy. If it needs more, it's two slides.
- **Numbers only from `brief.md` evidence**, with a source line on stat slides.
- **One CTA**, matching the brief's goal and tied to the payoff ("Save this before your next
  pilot kickoff", not "Follow for more"). Send CTAs name the recipient. Never engagement bait.
- **Caption**: line 1 is a second hook (125 characters max, not the cover again), the body adds
  context and search keywords, one ask, 3-5 precise hashtags.
- **Sound like a person**: contractions, plain words, numerals not number words ("3 steps"), no em dashes,
  no stock AI phrasing, and none of the machine-written shapes lint flags: "It's not X, it's Y", "not only
  X but also Y", one-word question lines ("The result?"), runs of shouted words. Never paste text with
  invisible characters in it. If the `ig-human` skill is installed, you can also run its humanizer.
- **House rules (hard gates in the check workflow)**: a visual that explains the point on every slide (slide 1
  an infographic), no dead space, no overlaps, nothing under 34px, no logo, 6 slides max, no slide numbers,
  no kicker above the headline, footer `BUILDABLELABS.COM`, no self-promotion. The renderer's defaults already
  do the layout ones; the copy and visuals are on you. `references/visuals.md` has the visual kinds.

**Show the copy before rendering.** Once `script.json` and `caption.md` are written, show the user a
numbered list they can read in ten seconds: per slide, the headline, the support line and the visual in
a few words, then the caption's first line, the ask and the hashtags. Words are cheap to change now and
costly after a render. Render once they approve or edit. Skip this step only when the user has said not
to wait for approvals, or when running unattended (a scheduled pipeline); then note in the hand-off
that the copy wasn't reviewed.

```
CAROUSEL · 6 slides · PAS (builders treat mods as toys) · theme poster
1  You can now mod Claude Code like a video game.   There's a catch.   [terminal: /plugin install]
2  Your coding session can have a health bar.        Usage as hearts, context as XP.   [HUD]
...
Caption: "Claude Code mods can rewrite or skip what Claude does next..." · ask: send · 4 hashtags
```

Render, then **look at `board.png` and any slide the summary flags** before handing off.
`render.py` shrinks text that doesn't fit and reports it; "shrunk to 79%" means the slide is too
dense, so cut words rather than accepting small type.

## 7. Hand off

Stage is now `rendered`. Tell the person (or the pipeline) the carousel is ready for
The check workflow, with the board, a one-line summary per slide, the caption, and the share test
answers (who sends it to whom, and which slide is the send). Don't score your own work.
The check workflow runs in a fresh context because the session that made the slides is the worst
placed to judge them.

## 8. Fix round

Read the newest `check/round-N.json` (`fixes`) and any `approver_notes` in `status.json`.

- Change **only** the slides and lines listed. Slides that weren't flagged were scored; touching
  them risks new failures and makes rounds impossible to compare.
- If a fix says split a slide, split it and re-render everything. Otherwise re-shoot just the
  changed slides: `render.py carousels/<slug> --only 3,5`.
- Re-rendering sets stage `rendered`. Then log what changed:
  `status.py carousels/<slug> rendered --event fixed --note "round 1: slide 1 headline cut to 8 words; slide 3 split"`,
  and hand back to the check workflow.


## Redo a carousel in another theme

1. Copy the folder to a new slug (`carousels/<slug>-<theme>`) so the original and its check history stay intact.
2. In the copy's `vision.json`: set `"theme"`, set `"variant"` to null (or one the new theme offers), replace
   `draft_calls` with one entry for the new theme and why, and add a `decisions` entry. An off-brand
   (`"brand": "free"`) theme needs the person's okay, recorded there.
3. Delete the copy's `check/` and `exports/`, render, and look at every slide: a theme can shrink copy or
   collide with a visual that fit the old one.
4. Hand it to the check workflow as a new carousel (a fresh judge; scores don't carry over between themes).

## Themes

The look of a carousel is mostly its theme. New house styles, for example from template photos
someone shares, become new themes, not one-off visions: `references/themes.md` §3 is the
procedure, and `scripts/theme_preview.py <name>` renders a preview to compare against the photos.

## Variants and options

- **Blog-plug** (`variant: "blog-plug"`): four slides. Slides 1-3 explain the topic and slide 4
  sends people to the full blog ("Full breakdown on the blog · link in bio"). Feed links aren't
  clickable on Instagram, so the URL belongs in the caption or bio, not on the slide.
- **PDF**: `scripts/export_pdf.py carousels/<slug>` writes `exports/<slug>.pdf`, one slide per page,
  built from the rendered PNGs so it looks identical in every viewer (WhatsApp, phones, LinkedIn
  document posts). `--vector` prints the HTML instead for selectable text, but phone and chat
  viewers mis-draw its gradients and shadows, so never share that one.
- **Canva**: to build the final slides in the team's Canva template instead of `render.py`, see
  `references/canva.md`. Vision and script work the same either way; only the renderer changes.
