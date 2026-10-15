# Check a carousel

This is Step 05 (Check) of the content pipeline, for carousels. It scores every carousel on its own
rubric and sends weak ones back to the make workflow with exact fixes. After 3 failed rounds it
hands the carousel to a person. A pass still goes to a human approver (Human check 2) before
Publish.

**The problem this skill exists to solve:** Claude grading Claude's work drifts high. Three
things keep the score honest, and all three matter:

1. **Facts go to scripts, not opinion.** `lint.py` checks everything measurable, and its
   findings cap the rubric lines they touch. A judge can't give Readability a 5 when text is
   clipped.
2. **The judge is someone else.** Judge in a fresh context that didn't make the slides.
3. **The math is a script.** `score.py` applies weights, caps and the pass rule identically
   every time.

## Inputs

A carousel folder made by the make workflow (layout: `workflows/make.md`). It needs `slides/` (PNG
per slide), `script.json`, `vision.json`, `brief.md`, `caption.md` and ideally `render_report.json`. Run
commands from the working folder. Scripts are in this skill's `scripts/` folder; call them by absolute path.
The brand kit and themes come from this skill's `assets/` (or a project's own `brand/` above the carousel).

**Check `status.json` first.** Check runs when the stage is `rendered`.
- `vision_draft` / `waiting_on_designer`: the designer hasn't signed off the look yet. Say so and
  stop. If a person explicitly asks for a check anyway, run it; lint will cap Brand at 3.
- `needs_fix`: the make workflow hasn't done the fix round yet. Stop.
- `awaiting_approval` / `approved`: already checked. Only re-check if asked.

## 1. Lint

```bash
python3 <skill-dir>/scripts/lint.py carousels/<slug>
```

This writes `check/lint.json`. **Fatal** findings (missing or stale slides, more than 20 slides)
mean the slides need re-rendering. Stop and send the carousel back to the make workflow; there's
nothing to score yet. Errors and warnings feed the judge and cap the score.

## 2. Judge, in a fresh context

Work out the round: `N` = number of existing `check/round-*.json` + 1.

**If you can start a subagent (Agent/Task tool), do.** Give it this brief and nothing from the
current conversation:

> You are the carousel judge. You did not make this carousel, so score it cold.
> Folder: `<absolute path to carousels/slug>`. Rubric anchors: `<skill-dir>/references/rubric.md`.
> Read the rubric first, then `brief.md`, `script.json`, `caption.md`, `<skill-dir>/assets/brand/brand.json`, `<skill-dir>/assets/brand/design-rules.md`,
> the theme's `<skill-dir>/assets/themes/<theme>/theme.json` and `preview.png` (the theme name is in `vision.json`), and `check/lint.json`.
> If that theme.json says `"brand": "free"`, score the brand line with the rubric's **Design** table (Instagram
> craft), not Brand match.
> Then **look at every image in `slides/` in order**, at full size, and at `board.png`. Rule on every
> judge gate (G1-G10, rubric §2) before scoring the lines, and list 3-5 reasons it might NOT get engagement. Score the eight lines
> exactly as the rubric says, and write `check/judge-r<N>.json` in the format the rubric gives. Judge it as a
> stranger scrolling Instagram would: would you stop, swipe to the end, and send it to someone?
> Don't read `status.json`, `vision.json → notes` or earlier rounds in `check/`; judge what's on
> the slides. Set `"judge": "subagent"`. Don't work out the verdict or the weighted score; a script
> does that. Don't change any other file. Reply with only the eight scores on one line, e.g. `share 4, hook 4, flow 3, value 3, readability 4, brand 4, cta 5, caption 4`.

If you can't start a subagent, judge it yourself, following `references/rubric.md` to the letter,
and set `"judge": "same-session"`. The approver will see that label and give the score less weight.
In a scheduled pipeline, the check step is already its own session; use `"judge": "fresh-session"`.

## 3. Score

```bash
python3 <skill-dir>/scripts/score.py carousels/<slug> --judge carousels/<slug>/check/judge-r<N>.json
```

The script re-runs lint, applies the caps, computes the weighted average, applies the pass rule
(**every gate passes, then 4.0 or more, no line below 3, and Send-worthy at 4 or more**), and writes `check/round-N.json`, `check/round-N.md` and
`status.json`. The script owns the round number. If it rejects the judge file (no slide numbers in
the evidence, a missing `to_reach_5`, the wrong round), send it back to the judge with the error.
Don't edit the scores yourself, and don't loosen the check.

## 4. Act on the verdict

- **PASS** → stage `awaiting_approval`. Put together the approval packet: `board.png` plus
  `round-N.md`. Any notes under "Optional polish" go to the approver, not back to the make workflow,
  unless the approver asks for them. If a person is in the chat, show both and ask: approve, request changes, or kill.
  - Approve: `score.py carousels/<slug> --approve "Name"` → stage `approved`, ready for Publish.
  - Request changes: `<skill-dir>/scripts/status.py carousels/<slug> needs_fix --event approver_notes --note "..."`
    (one call per note), then hand back to the make workflow.
- **FIX** → stage `needs_fix` (score.py sets it). The fix list in `round-N.md`, one item per slide
  and line, is the make workflow's to-do list. Stop there. In a chat, offer to run the make workflow's fix
  round next; in a pipeline, the orchestrator routes on the stage. Don't fix the slides yourself:
  keeping the maker and the checker separate is what keeps the score honest.
- **ESCALATE** (failed the last allowed round, 3 by default) → stage `needs_human`. Summarise in
  three lines what still fails and why, for the approver to decide: approve as is, edit by hand,
  or kill.

When reporting back, lead with the verdict and score, then the line table, then the fix list
(already grouped). If the fix list is long, show the five that move the score most (lines below
3 first) and point to `round-N.md` for the rest. The person reading it is deciding, not studying.

## Built to win on Instagram

The check exists to get posts that win on Instagram. It has two layers:
1. **Gates** (pass/fail, `rubric.json → gates`): the account owner's house rules. A real visual on every slide
   with an infographic on slide 1, no dead space, no overlaps, nothing under 34px, no logo, 6 slides max, no
   slide numbers, no self-promotion. Plus ours: every number sourced, no engagement bait. Any failure blocks a pass.
2. **Weighted lines** (shares first): what makes a post spread once the basics hold.

## What the rubric rewards, and why

Shares first. A DM send is Instagram's strongest signal for reaching people who don't follow us yet, so
**Send-worthy** carries the most weight and must reach 4 for a pass. Next come the hook (stop the
scroll), flow (swipe-through, with slide 2 as a second cover), save value, then the craft lines
and the caption (second hook, search keywords). Lint blocks engagement bait outright, because Instagram
demotes it. The research and its sources are in `references/engagement-research.md`. Read it when a
scorecard needs defending, or when Step 07 (Learn) suggests the weights are wrong.

## The rubric is a file, and it should change

`rubric.json` holds the weights, pass rule, limits (words per slide, minimum type size, contrast)
and caps. Step 07 (Learn) is meant to adjust it: if carousels that score high keep flopping on
saves and shares, the weights are wrong. When you change it, bump `version` and add a
`changelog` line, so every scorecard records which rubric scored it. Before trusting the
4.0 threshold at all, calibrate it against posts you've already published:
`references/calibration.md`.

## Slides made in Canva or by hand

These work too. Export PNGs at 1080x1350 into `slides/` as `01.png`, `02.png` and so on, with a
`script.json` holding the copy (write it from the slides if needed, since lint reads words and
numbers from it). There's no `render_report.json`, so lint can't detect clipping, type size or
font fallback. The judge has to look for those deliberately; the rubric says how.
