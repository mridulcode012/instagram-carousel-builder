# Building the slides in Canva instead

The pipeline guide plans to build final slides in the team's Canva template through the
Canva connector. That works with this skill. Canva only replaces the renderer; the vision,
questions, lock and script steps don't change.

1. Do steps 1-6 as usual, up to a final `script.json` and a locked `vision.json`. Keep rendering
   with `render.py` while the vision is a draft, because the board is how the designer reacts.
2. With the Canva connector available in the session, open (or duplicate) the team's carousel
   template and fill **one page per slide** from `script.json`: kicker, headline, sub/body/items,
   number and source. Apply the vision's colours and fonts where the template allows.
3. Export every page as PNG at **1080x1350** and save them into the carousel folder as
   `slides/01.png`, `slides/02.png` and so on, so the check workflow finds them exactly as it would
   a `render.py` output.
4. Note in `status.json` history that the slides came from Canva, with the design link.

What you lose: there's no `render_report.json`, so the check workflow can't machine-check clipped
text, type size or font loading. It tells the judge to look for those by eye. Contrast,
word counts, numbers and the CTA are still checked from the files.

Before committing the pipeline to Canva, run one carousel end to end and confirm the connector
fills **your** template reliably: text boxes in the right places, nothing overflowing, fonts
intact. If it doesn't, keep `render.py` as the renderer and use Canva for one-off hand edits.
