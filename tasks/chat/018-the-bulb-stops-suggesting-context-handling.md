# 018 — The chat's 💡 stops suggesting compact, handoff and background agents

**State:** done
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
- Burndown is on: no new numbered decision. Amend 36 and 97 in place (both in `decisions/assistant.md`, 9,848 of 12,288 B).
- Doc-size: `embarch-chat/spec.md` is 9,027 B, 12 B under its reserve line (9,039). Edit, do not append; if your change still pushes it into reserve, file `tasks/chat/<NNN>-compact-chat-spec.md` in the same commit (`tasks/README.md` has the shape). Decision 96 (`decisions/promptu.md`) is 204 B under its per-decision limit; leave it alone unless this task needs it.
- Gate: `npm ci`, `build`, `typecheck`, `test`, `test:webview`. If you add or change a webview check, its own PASS line must be in the output.

## Done when

- [x] The 💡 never offers a background, compact or handoff card, and its other cards still work.
- [x] Decisions 36 and 97 are amended.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.

## Result

The 💡's cards call asks Haiku for desk references only (none, no call); the context card kinds, the handoff request, the "Fresh chat with this handoff" chip, `freshChat`, and the Promptu `handoff` origin are gone. Kept: `splitCompact` and `sendAfterCompact` (a typed `/compact` first line still sends first) and the agent's own handoff (103). Decisions 36 and 97 amended in place; spec line 20 shortened. `spec.md` 9,011 B, `decisions/assistant.md` 9,346 B. Webview e2e lost the compact-card, handoff-card and chip checks and gained one asserting a context answer from Haiku yields no card.
