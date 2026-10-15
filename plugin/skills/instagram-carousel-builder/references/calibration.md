# Calibrating the rubric against real posts

A rubric is only useful if high scores predict posts that do well. Until that's tested, the
4.0 pass bar is a guess. Do this once before relying on the gate, and again whenever Learn
(Step 07) says high-scoring posts are flopping.

## One-time calibration (about an hour)

1. Pick 10-15 carousels you've already posted: a mix of clear winners, clear flops and some in
   between. Export each one's slides to `calibration/<slug>/slides/01.png ...`, with a short
   `script.json` (the copy per slide) and `brief.md` (the evidence you had at the time).
2. For each, note the real numbers from Instagram Insights in `calibration/results.csv`:
   `slug,saves,shares,reach,profile_visits,follows`. Use saves + shares per 1,000 reach as the
   main outcome, since those are the signals the rubric is trying to predict.
3. Run lint and a judge on each one (fresh context, as in SKILL.md) and score it with `score.py`.
   **Don't show the judge the results.**
4. Line up the rubric's weighted score against the outcome:
   - Do winners score higher than flops? If the ranking is mostly right, keep the weights.
   - Does one line separate winners from flops better than the rest? Weight it up.
   - Does a line score high on everything? Its anchors are too soft. Tighten the 4 and 5 rows.
   - Where do most past winners land? If good posts score 3.6, the 4.0 bar is set too high
     for your account; if flops score 4.2, it's too low.
5. Change `rubric.json` and/or the anchors in `rubric.md`, bump `version`, add a `changelog`
   line saying what you changed and why, and re-run on the same set to confirm.

## Ongoing

Every scorecard (`check/round-N.json`) records the rubric version and each line's final score.
Once posts are live, Learn can join those scores to Insights by slug. Review every 4-6 weeks,
not every week: at four carousels a week, one week of data is noise.
