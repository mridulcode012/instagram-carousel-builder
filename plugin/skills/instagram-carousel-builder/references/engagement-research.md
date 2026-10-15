# What makes a carousel spread: the evidence behind the rubric

Collected 2026-10-14. The rubric (`../rubric.json`, `rubric.md`) and the make workflow's writing rules
are built on this file. Every claim is tagged with how much to trust it:

- **[platform]**: said by Instagram itself (Adam Mosseri, Head of Instagram, in his own posts or interviews)
- **[study]**: peer-reviewed research or a large dataset
- **[practice]**: consistent advice across many practitioner sources, not independently verified

Re-check this file every few months. The ranking system changes, and blogs repeat stale
claims long after the platform moves on.

## Contents
1. How Instagram decides who sees a post
2. Why people share
3. What that means for a carousel
4. Things we deliberately don't do
5. Sources

---

## 1. How Instagram decides who sees a post

- **Three signals lead, each measured per person reached: watch time, likes per reach and
  sends per reach.** [platform] Mosseri, January 2025.
- **Sends (DM shares) matter most for reaching people who don't follow you; likes matter slightly
  more with existing followers.** [platform] A send is one person recommending the post to
  another. That makes it the main lever for new reach, and the reason this rubric weights
  "Send-worthy" highest. Blogs quote "a send is worth 3-5x a like". That figure has no primary
  source, so we don't use it.
- **A carousel gets a second chance.** [platform] If someone sees it and doesn't swipe, Instagram
  can show it to them again, opening on slide 2. Slide 2 is effectively a second cover.
- **More slides mean more interactions, which means more reach.** [platform] This is Mosseri's
  explanation for why carousels out-reach single images. Swiping counts as time spent on the post.
- **Original content is favoured; reposting other people's work loses recommendations.** [platform]
  Since 2022, and widened in 2024 and 2026. Our own framing, data and visuals count as original.
  A screenshot of someone else's post with a caption added does not.
- **Engagement bait is a target.** [platform, via press] Instagram's line is that genuine
  interaction is fine, but posts built to inflate engagement counts in order to game reach are not.
  "Tag a friend", "comment YES", "like if..." and "share if you agree" are the classic patterns
  that Meta has demoted since 2017.
- **Captions and alt text feed search.** [platform] Mosseri: keywords in the caption, the profile and
  alt text help Instagram search. Hashtags categorise a post but are "not necessarily a strategy for
  getting more distribution". A few precise ones are enough. Since July 2025, public professional
  posts can be indexed by Google [practice, single source].
- **Carousels win on saves.** [study] Socialinsider's benchmark (millions of posts) finds carousels
  earn the highest save rate of any format, while Reels lead on comments and shares. So a
  carousel has to work harder for shares, which is exactly what this rubric pushes on.
- **Slide count: 7-10 is the common recommendation.** [practice] The evidence is weak and
  conflicting. Past about 10, fewer people reach the end. Treat this as a soft range, not a rule.

## 2. Why people share

- **High-arousal emotion spreads; low-arousal emotion doesn't.** [study] Berger and Milkman
  analysed New York Times most-emailed articles and ran follow-up experiments. Awe,
  amusement, surprise, anger and anxiety drive sharing; contentment and sadness suppress it.
  Positive content beats negative overall. Content that was surprising, interesting or
  practically useful was also shared more.
- **People share what makes them look good.** [practice, from Berger's STEPPS] Sharing is identity
  ("social currency"): being the one who found the smart, early or insider thing. A post that makes
  the sender look sharp gets sent.
- **People share what helps someone specific.** [study + practice] Practical value: "you need this"
  is one of the most common reasons to forward something. The more precisely a reader can picture *who*
  to send it to, the more likely the send.
- **Stories and concrete examples carry ideas.** [practice] A named example or a before/after travels
  further than an abstract principle.

## 3. What that means for a carousel

These are the rubric's lines, and the rules the make workflow writes to.

| lever | what it looks like on slides | rubric line |
|---|---|---|
| A clear *who to send it to* | The reader can name one person ("my cofounder", "our ops lead") the post is for, and sending it says something about the sender | Send-worthy |
| One standalone sendable slide | A single slide that makes sense alone as a screenshot or DM: the framework, the checklist, the before/after | Send-worthy, Value |
| Surprise or awe, not mild agreement | A claim that contradicts what the reader assumed, or a reveal that makes them say "wait, really?" | Hook, Send-worthy |
| Scroll-stopping cover | Specific claim in 10 words or fewer, readable at thumbnail size, a visual that shows the promise, an open question only swiping answers | Hook |
| Slide 2 as a second cover | Works with no context, because people may see it first | Flow |
| Open loops and a payoff | Each slide leaves something unresolved, and the last content slide pays it off | Flow |
| Save-worthy reference | A checklist, steps, a framework or a sourced number someone will come back to | Value |
| One honest ask | Save, or send to a named kind of person for a stated reason. Never bait | CTA |
| Caption that adds, not repeats | A first line that works as a second hook before "...more", keywords people search for, one ask, 3-5 precise hashtags | Caption |
| Original and on-brand | Our angle, our visuals and our evidence; no reposts, no stock | Brand |

## 4. Things we deliberately don't do

These would move numbers short term but cost reach, trust or the brand:

- **Engagement bait**: "tag 3 friends", "comment YES", "like if you agree", "share if...", "follow for part 2" gating.
  Lint blocks these phrases in slides and caption.
- **Rage-bait and fake urgency.** Anger spreads, but the brand voice is calm conviction, and
  an angry audience isn't a client base.
- **Unsourced statistics.** A fake number is the fastest way to lose a technical audience, and
  lint already blocks them.
- **Hype vocabulary.** The brand's `voice.never` list applies to captions too.
- **Reposting other people's work.** It loses recommendations, and it isn't ours.

## 5. Sources

- Mosseri on watch time, likes and sends per reach (Jan 2025), as reported by
  https://kompozy.io/news/instagram-mosseri-ranking-signals-guidance and
  https://www.dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers
- Sends and non-follower reach: https://www.socialync.io/blog/adam-mosseri-shares-instagram-algorithm-2026,
  https://influencermarketinghub.com/instagram-sends-per-reach-playbook/
- Carousel second-slide resurfacing (Mosseri): https://routenote.com/blog/instagram-carousels-perform-better-than-single-photos-according-to-the-head-of-instagram/,
  https://planoly.com/blog/instagram-carousels-are-making-a-comeback
- Originality: https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/,
  https://www.gigazine.net/gsc_news/en/20240502-instagram-updated-algorithm-prioritizes-original-content
- Engagement bait: https://www.socialmediatoday.com/news/instagram-clarifies-advice-on-single-word-ctas-and-longer-reels/718151/,
  https://lowyat.net/2017/150787/facebook-demote-engagement-bait-posts
- Captions, keywords, hashtags: https://www.phable.io/phable-labs/instagram-hashtags-keywords-discovery,
  https://www.kontentino.com/q-and-a/instagram-search-seo/
- Carousel benchmarks: https://www.socialinsider.io/social-media-benchmarks/instagram,
  https://www.socialinsider.io/social-media-benchmarks/instagram-engagement-report
- Berger and Milkman, "What Makes Online Content Viral?" (Journal of Marketing Research):
  https://cssh.northeastern.edu/pandemic-teaching-initiative/wp-content/uploads/sites/43/2020/09/What-Makes-Online-Content-Viral.pdf
- Berger, *Contagious* (STEPPS): https://www.supersummary.com/contagious-jonah-berger/summary/
