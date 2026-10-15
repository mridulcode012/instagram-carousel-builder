# Buildable Labs: design rules for social slides

Source: *Buildable Labs Brand Foundation*, Version 01, July 2026. Typography and Color are
**locked** there. The machine-readable values are in `brand.json`; this file explains how to use
them on Instagram slides. carousel-make designs inside these rules, and carousel-check's judge
scores Brand match against them.

## 1. Who we sound like

An execution-first AI studio that ships outcomes, not proposals. One voice, three registers:

- **Precise.** Technical authority without jargon walls. Every sentence earns its place.
  *"We architect the system, prototype the hard part, and ship on milestones."*
- **Partner-first.** We talk to founders as peers and co-architects, never as a vendor.
  *"We don't wait for a brief. We sit in discovery with you until we both see the architecture."*
- **Conviction-led.** We state a point of view plainly, with confidence but not arrogance.
  *"When AI collapses execution time, judgment is the differentiator. Not headcount."*

**Never:** transactional language, time-based thinking (hours, timesheets), "out of the box",
marketing spin, SOW-only rigidity, "leverage synergies". Lint flags the phrases listed in
`brand.json → voice.never`.

Core lines to echo, not copy: *Anything is buildable, with the right human in place.* ·
*Critical thinking is the moat.* · *Building AI Systems That Ship & Scale.*

## 2. Type

| role | font | on a 1080px slide | notes |
|---|---|---|---|
| Display / headline | Instrument Serif **italic** | 72-140px, line-height 1.0-1.1 | sentence case; the signature of the brand |
| Bold headline (H1) | Manrope Bold | 56-76px, line-height 1.12 | for data-led and announcement slides |
| Subhead (H2) | Manrope SemiBold | 40-48px | |
| Body | Manrope Regular | 36-42px, line-height 1.4-1.6 | |
| Label / metadata | JetBrains Mono, UPPERCASE | 34px minimum, tracking 0.04-0.08em | source, footer, visual labels |
| Button | Manrope SemiBold | 34-40px | sentence case |

Themes (`themes/`) may change case, layout and patterns, but never the palette or the three fonts.
**Exception: free themes** (`theme.json` → `"brand": "free"`) leave the palette and fonts on purpose, for posts
where the person asks for a look outside the brand. They still keep the handle, the voice rules and the truth
rules (sourced numbers, no bait), and they're judged on Instagram design quality instead of brand match.
The web scale (Display 72-128, Body 16-18) is for screens read at arm's length. A slide is
seen at about a third of its size on a phone, so body and labels are scaled up here.

## 3. Colour: Alloy

Blue for authority, chrome for craft, deep neutrals for the engineering substrate.

- **Usage ratio:** 70% deep neutrals (black #0A0B0E, graphite #1A1D24) · 18% brand blue #0B3FDE ·
  7% steel #7A8296 · 5% off-white #F5F6F8.
- **Brand blue #0B3FDE is a fill**: full-colour slides (quote, CTA), the highlight block behind
  one word, buttons, rules and the progress bar. On black it's only 2.5:1, so **never use it for small
  text on dark**. Blue text on dark uses **#6789EC**; on light, brand blue is fine (7:1).
- **Chrome gradient** is for the occasional hairline only. Never for text or
  large fills.
- One accent family per slide: blue and its tints. No other hues.

## 4. Emphasis

One key word or short phrase per slide sits on a **solid brand-blue block** with white text,
like *That **Ship** & Scale* in the tagline. In script copy it's written `*Ship*`. Use it on
the word that carries the angle, not for decoration.

## 5. Layout

- Dark substrate by default. Light slides (off-white #F5F6F8, text #0A0B0E, icons #2C3444) are
  allowed for contrast moments.
- **The headline is the first element on every slide.** No kicker, eyebrow or mini-headline above it, and
  no slide or page numbers anywhere (no "01 / 06", no giant numerals).
- Footer on every slide: `BUILDABLELABS.COM` bottom-left in mono (plain text, not a logo), a swipe cue
  bottom-right; the last slide may use a CTA cue ("YOUR TAKE ↓") or nothing. No logo or brand mark.
- **Nothing under 34px**, labels and footer included. Scale: headline about 88px (hook up to 120px),
  body 44px, main line 40px, card text 36px, grey/secondary, labels and footer 34px.
- **6 slides maximum, a real visual on every slide**, taking roughly 40-60% of the slide; slide 1 carries
  an infographic (a visual with information in it, not decoration).
- Thin dividers (#22242B on dark) between list items; square corners, 4px at most.
- Lots of air. A slide that feels busy is off-brand even if every colour is right.

## 6. The four social templates (from the foundation's Applications page)

| template | look | slide type here |
|---|---|---|
| **Insight** | dark, blue mono kicker, serif italic statement | `cover`, `point`, `stake` |
| **Case study** | dark, Manrope bold headline, big blue number as data ("6 wks") | `stat` |
| **Quote** | full brand-blue slide, white serif italic, small quote mark | `quote` |
| **Announcement** | dark, Manrope bold headline, square blue button | `cta` |

## 7. Pattern language (backgrounds only, 5-12% opacity)

- **The Loop**: scattered circles. Feedback, iteration. Hero and cover backgrounds.
- **The Weave**: crossing diagonals. Integration, craft. Slide backgrounds.
- **The Ascent**: ascending parallels in brand blue. Growth, velocity. Growth or results slides.

## 8. Icons

Lucide, outline only, 1.5px stroke at 24px (scale the stroke with the size), rounded caps and joins,
no fills. Steel #7A8296 by default, brand blue for the active or primary item, #2C3444 on light.

## 9. Imagery

Two pillars only: the **3D chrome mark** (soft directional light, black or navy background, no
coloured lighting) and **abstract geometry** (dark substrate, one accent colour per render).

**Never:** stock photography · AI-hype gradients · neon glow · busy photographic backgrounds ·
generic tech imagery.
