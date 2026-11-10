# 009 — The start hook takes the work item from the prompt before it asks

**State:** done
**Source:** Linear issue EMB-16, filed by a session
**Issue:** EMB-16
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A session on no work item, on a desk with time on, is told to look for an issue key in its opening prompt or a handoff first, and to call `desk_set_work_item` with it; it asks the user only when there is none. A session with no key anywhere is still asked, on every prompt, as today.

Today `ask_text` tells the agent to ask the user before anything else and to "Ask again on every prompt until it is answered" (decision 7). The hook never reads the prompt: `HookEvent` carries no prompt field, and the only ways an item is set without asking are a card's launch and `claim` (a branch naming a card's issue). Checked on `main` at the split (`0c44f9d`): the text is unchanged since decision 77.

## Why now

A prompt that already names the issue, or a handoff that decides it, still gets a question the user has answered.

## Where to look

- `src/events.rs` `ask_text` — the text
- `src/events.rs` `apply` — the `("SessionStart" | "UserPromptSubmit", None)` arm
- `src/events.rs` `claim` — what sets an item without asking
- `src/events.rs` `HookEvent` — the payload; reading the prompt for a key is the alternative the issue names, and needs a `prompt` field
- `embarch-doc/embarch-desk/decisions/` — decision 7

## Dispatch notes

- Either route meets the issue: the text change alone, or the hook reading the prompt for a key. Pick one and say why in decision 7's amended text; this is an amendment, not a new decision.

## Done when

- [x] A session whose first prompt names an issue key ends on that item without the user being asked (a test drives the route you chose).
- [x] A session with no key in the prompt or a handoff is still asked.
- [x] Decision 7 amended; `spec.md` or `interfaces.md` updated where they quote the hook's behaviour.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
