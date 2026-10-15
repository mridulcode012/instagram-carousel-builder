# Caption: the second hook

`caption.md` in the carousel folder is posted with the slides, exactly as written. It's plain text,
no heading, and no markdown beyond line breaks. The check workflow scores it (Caption, 8%) and lint checks it.

## Why it matters
- **Line 1 is all most people see.** The feed cuts the caption at about 125 characters ("...more").
  For someone who didn't swipe, line 1 is a second chance to hook them.
- **Instagram search reads captions.** Keywords in the caption (and in alt text) are how a post is found
  in search, and public posts from professional accounts can show up on Google. Hashtags only help
  classify the post. A few precise ones are enough.
- Sources and confidence: `references/engagement-research.md`.

## Shape

```
<line 1: a second hook, 125 characters max, different from the cover>

<2-5 short lines: what the slides don't say: why now, a named example, the context,
the one thing to remember. Use the words someone would type into search.>

<one ask: the same single action as the CTA slide>

#tag #tag #tag
```

## Rules
- **Line 1 is not the cover again.** Angle it differently: the stake, the surprising part, or
  who it's for ("If you're installing your first Claude Code mod this week, read slide 5 first.").
- **Add, don't repeat.** If a line is already on a slide, cut it from the caption.
- **One ask**, matching the CTA: save *or* send (to a named kind of person, with the reason).
  Never "tag a friend", "comment YES", "comment MOD for the link", "like if", or "share if". Instagram demotes
  engagement bait, and lint blocks it.
- **Open with the hook.** Never a greeting ("Hey builders"), a hashtag or an emoji as the first thing.
- **Search terms as plain words.** Work the 2-3 phrases from `brief.md → ## Search terms` into the body as
  sentences a person would write ("...the first Claude Code plugins worth installing..."). Instagram search
  reads the caption text; a hashtag doesn't count. Put at least one in the cover's alt text too.
- **No links.** Caption links aren't clickable and read as off-platform. Say "link in bio".
- **Emoji as punctuation, not decoration**: 4 per 100 characters at most, and usually none.
- **3-5 hashtags**, specific to the topic (`#claudecode`, not `#ai #tech #viral`), on the last line.
  Hashtags are labels, not reach (Mosseri), and Instagram caps them at 5. Never `#viral`, `#fyp`,
  `#explorepage` or `#foryou`; they describe nothing.
- **Brand voice**: same `voice.never` list as the slides, no em dashes, no hype. Numbers only from
  `brief.md` evidence (lint checks the caption too).
- **Length**: usually 40-120 words. Instagram's hard limit is 2,200 characters.

Lint prints the first 125 characters exactly as the feed shows them before "...more". Read that line
on its own: if it doesn't make you tap, rewrite it before anything else.
