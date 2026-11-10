# 017 — The chat gives Promptu's pass its context usage

**State:** open — unparked 2026-11-09 by `promptu/002`'s fold: the input is `promptu prep --context-usage <0-100>`, defined in `embarch-promptu` `docs/contract.md` §7.10 (embarch-promptu `95f0d69`); without it the pass judges from the text alone.
**Source:** Linear issue EMB-65, filed by the owner; `embarch-promptu` decision 41 (owner, 2026-11-07)
**Issue:** EMB-65
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

When the chat starts a Promptu run, `beginPromptu` passes the chat's current context usage, in the shape `embarch-promptu/docs/contract.md` defines once `tasks/promptu/002` lands. Promptu's pass uses it to judge whether the work will outgrow one context window.

This is the chat half of EMB-65. Today `beginPromptu` passes only the rough text and the desk item.

## Why now

`embarch-promptu` decision 41 says the pass judges from what it reads "and, run from the chat, the chat's context usage, which `beginPromptu` passes". Without this half, the pass judges from the text alone.

## Where to look

- `src/views/chatHost.ts` `beginPromptu`
- `src/promptu/runs.ts` `BeginOpts`
- `src/wire/chat.ts` — the context-usage refresh the header's meter reads
- `embarch-promptu/docs/contract.md` — the input, as `tasks/promptu/002` defined it (read only)

## Dispatch notes

- **`embarch-promptu` is not yours.** If the contract does not fit what the chat can pass, report that; do not change Promptu.
- When this lands, `tasks/chat/018` unparks: the folding supervisor sets it `open` in the same fold.

## Done when

- [ ] A Promptu run started from the chat receives the chat's context usage, as the contract defines it.
- [ ] A test covers the value reaching the run's options.
- [ ] `embarch-chat`'s docs say what is passed, and its decisions name `embarch-promptu` decision 41 where they describe `beginPromptu`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
