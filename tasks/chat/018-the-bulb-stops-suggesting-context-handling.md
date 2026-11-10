# 018 — The chat's 💡 stops suggesting compact, handoff and background agents

**State:** open — unparked 2026-11-09 by `chat/017`'s fold: Promptu's pass now owns the judgement, and a run from the chat passes its context usage (`prep --context-usage`, embarch-chat `a46c5ac`; `embarch-chat` decision 96).
**Source:** Linear issue EMB-66, filed by the owner — owner's call on 2026-11-05
**Issue:** EMB-66
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

The 💡 offers no background, compact or handoff card. Promptu's planning for high-context work (`embarch-promptu` decision 41, built by `tasks/promptu/002` and `tasks/chat/017`) is the one place that judgement is made. The header's context meter and its Compact button stay, and the bulb's other cards still work.

Today decision 36 ("And a card for context handling") has Haiku judge whether a draft calls for a background agent, compacting first or a handoff to a fresh chat, seeing the chat's context usage; decision 97 keeps those cards with the 💡 while Promptu owns missing context and improvement (`embarch-promptu` decision 16).

## Why now

One place decides how high-context work is carried, so two suggestions never disagree. It waits for Promptu's side to exist, so nothing is lost in between.

## Where to look

- `src/assistant/prompts.ts` — the cards prompt and its thresholds
- `src/assistant/edits.ts` — the card kinds, `BACKGROUND_INSTRUCTION`, `handoffRequest`
- `webview/chat/composer.tsx` `applyCard` — the handoff card's path into Promptu's dialog

## Dispatch notes

- `handoffRequest` and `extractHandoff` may still be used by the agent's own handoff (`tasks/chat/007`, decision 103). Remove only what the bulb alone uses.

## Done when

- [ ] The 💡 never offers a background, compact or handoff card, and its other cards still work.
- [ ] Decisions 36 and 97 are amended.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
