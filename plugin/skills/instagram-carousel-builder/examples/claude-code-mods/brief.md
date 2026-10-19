# Claude Code mods

## Idea
If you build with Claude Code, you can now mod it like a video game.

## Pillar
Product news for builders (Claude Code)

## Audience
Founders and engineers who build with Claude Code every day.

## Our angle
Mods make Claude Code feel like a game you can customise, but under the fun they are plugins that run unsandboxed, so treat them like code you run.

## Goal / CTA
Send (to the teammate who will install the first mod). Changed from save on 2026-10-14: the rubric is now shares-first.

## Share test
- Who sends it to whom: a developer who uses Claude Code sends it to the teammate or lead who will install the team's first mod.
- The send slide: slide 6, the 'Before you install' checklist (works alone as a screenshot), backed by slide 5's validate command.
- The 'wait, really?': mods can rewrite or skip what Claude does, you can play Doom while it works, and they run unsandboxed with your permissions.
- Why the sender looks sharp: early on a new feature, and the one who spotted the safety catch before anyone installed something.

## Variant
standard, 6 slides

## Evidence
Collected 2026-10-14 from secondary coverage. The official docs page was not reachable (404), so slides use only claims that at least two sources agree on, and no version numbers or statistics.

- Mods are plugins whose small JavaScript or TypeScript functions run inside Claude Code and react to events such as tool calls and prompts. (developersdigest.tech guide; stork.ai; search coverage)
- Unlike hooks, which observe events or trigger side effects, mods run in the runtime loop and can rewrite payloads or skip events. (search coverage; developersdigest.tech)
- What a mod can change: draw panels above the prompt, redraw parts of Claude Code's own interface, hold or answer a tool call, add a /command. (developersdigest.tech)
- Installed like any plugin: /plugin install <name>@<marketplace>. Check one first with: claude plugin validate <directory>, which lists the events it hooks and the API calls it makes. (developersdigest.tech; runtimewire.com)
- Game-style examples: a Minecraft-style HUD where usage becomes a health bar and the context window fills an XP bar; a shared Doom lobby to play while Claude works. (stork.ai/blog/claude-mods-turn-waiting-into-a-minecraft-game; wearedevelopers.com Doom article)
- Anthropic sample mod blast-radius pauses risky shell commands (rm -rf, force push) and shows a pane with Proceed and Cancel. (developersdigest.tech; runtimewire.com)
- Security: mods are not sandboxed, run with your permissions, and Anthropic says to install only from sources you trust. (developersdigest.tech; search coverage)

Sources
- https://www.developersdigest.tech/blog/claude-code-mods-guide-2026
- https://www.stork.ai/blog/claude-mods-turn-waiting-into-a-minecraft-game
- https://www.wearedevelopers.com/magazine/780-play-doom-with-developers-while-claude-code-works
- https://runtimewire.com/article/anthropic-claude-code-mods-typescript-permissions

## Story
PAS: builders treat mods as a fun toy, so the risk (they run with your permissions) is the news. The hard part is getting them to care before they install one.

## Search terms
- claude code mods
- claude code plugins
