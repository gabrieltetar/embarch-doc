# 025 — Done or Canceled tells the issue's window to end its chat

**State:** open
**Source:** Linear issue EMB-73
**Issue:** EMB-73
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

An issue's folder, `<suite root>/.dev-worktrees/<key>/`, lives from Start work until the owner removes it by hand. The owner wants the issue's status to end it instead: Done or Canceled ends the issue's chat with a message and one button that closes the window, and the folder goes once the window is closed. Nothing closes in front of the owner without a click.

EMB-73 is split three ways. **This task** is the desk's first half: notice the move, run the checks, and tell the window. `tasks/desk/026` is the second half (remove the folder once no window shows it), dispatched after this one lands. `tasks/chat/023` is the chat's half, running in parallel with this one against the same contract.

**Direction, decided at the split:**

- **Triggers.** The `/linear/status` route, at once: the Work tab's status menu and a chat's `linear_set_status` both go through it. A move made in Linear itself, when the reference index's refresh sees it (decision 56, at most five minutes). Done and Canceled mean Linear's `completed` and `canceled` state types, whatever the team names them.
- **Only an issue with a `.dev-worktrees/<key>/` folder** (`src/suite.rs`). A Start work worktree made outside a suite is untouched; the decision says so.
- **The checks**, for every worktree in the folder: no uncommitted files, untracked ones included; and for Done, the worktree's branch is on `origin/main` after a fetch. Each failure is one blocker: the repo's folder name and a one-line reason. Write the checks as one function: `tasks/desk/026` runs them again before it removes anything.
- **Once per move.** The desk records each item's close-out (outcome, blockers) so a refresh does not post again for a move it already handled. Moving the issue back to an open state clears the record.
- **The close-out is readable from the desk's answer for the item**, outcome and blockers, so the Work tab can show the repo and reason with a Finish button. The Work tab itself is outside the fleet's repos; say in `interfaces.md` where the field is.

## The contract between the desk and the chat (fixed at the split; implement it as written)

Both halves are written against this in parallel, and either may land first. A chat that knows these kinds before any desk sends them does nothing new. An older chat takes an entry it does not know and drops it (`deskService.ts`'s poll takes every entry, and `extension.ts` acts only on the kinds it knows), so its window simply stays open. Change the contract in neither half; if it cannot be implemented as written, stop and say why in this file.

1. **Two new mailbox kinds, written only by the desk, server-side.** `POST /mailbox` refuses both, as it refuses `start` (decision 46).
   - `end`: `{"kind":"end","id","folder","item_id","issue_key","outcome"}`, `outcome` `"done"` or `"canceled"`. The issue is Done or Canceled and every check passed. The window on `folder` ends the issue's chat.
   - `unfinished`: the same fields plus `"blockers":[{"repo":"<repo folder name>","reason":"<one line>"}]`. The issue is Done or Canceled but a check failed: nothing closes and nothing is removed. The window shows each blocker and a Finish button.
   - Both carry the existing `created_ms`, `expires_ms` and `taken_ms`. Neither expires on the 10-minute launch clock: an entry waits until a window takes it or the folder is gone. A newer `end` or `unfinished` for a folder replaces an untaken older one.
2. **One new desk route, `POST /items/{id}/finish`.** It re-runs the checks for the item's issue, posts a fresh `end` or `unfinished` for its folder, and answers `{"ended":true}` or `{"ended":false,"blockers":[…]}`. The chat's Finish button calls it and then acts on the mailbox entry, not on the answer, so a Finish pressed anywhere reaches the window the same way.
3. **A window shows a folder while it polls `GET /mailbox?folder=` for it.** The chat already polls every 3 s per window folder, and backs off to 60 s while the desk is unreachable. The chat's Close window button only closes the window and calls no route; the desk reads the polls stopping as the window gone (`tasks/desk/026`).

## Why now

EMB-73: a landing that deleted the folder under a live chat left the chat unreachable on its next resume. Landing now keeps the folder, so nothing removes it.

## Where to look

- `src/server.rs` — `linear_status`, the mailbox routes, `start_work` (how a suite folder is made and its `start` entry posted)
- `src/store.rs` — `MailboxEntry`, `post_mail`, `mail_for`, `take_mail`, `LAUNCH_CLAIM_MS`
- `src/refs.rs` — the reference index refresh; `src/linear.rs` — `state_type`
- `src/suite.rs` — `.dev-worktrees/<key>/`, `issue_dir`; `src/worktree.rs` — git helpers
- `embarch-doc/embarch-desk/interfaces/chat-routes.md` (the mailbox rows), `decisions/` (46, 56, 70), `spec.md`, `spec/constants.md`

## Dispatch notes

- Normal mode: a new numbered `embarch-desk` decision is expected. Number it per `DOC-CONVENTIONS.md`.
- No `embarch-desk` doc in `embarch-doc` is in doc-size reserve at the split.
- Tests use temporary git repos and a temporary suite root; never the real `.dev-worktrees/` or the real desk config.
- Do not edit `embarch-chat` or anything outside `embarch-desk` and `embarch-doc/embarch-desk/`.
- Edit files with your Edit and Write tools, not inline Python or shell redirects.

## Done when

- [ ] Moving an issue with a `.dev-worktrees/<key>/` folder to Done or Canceled through `/linear/status` posts an `end` for that folder when every check passes, and an `unfinished` naming each failing repo and reason when one fails; a test covers each, and uncommitted files and (for Done) a branch not on `origin/main` each produce a blocker.
- [ ] A move made in Linear itself does the same on the reference index's next refresh, once per move.
- [ ] `POST /mailbox` refuses `end` and `unfinished`.
- [ ] `POST /items/{id}/finish` re-runs the checks and posts a fresh `end` or `unfinished`, answering as the contract says.
- [ ] The desk's answer for the item carries its close-out outcome and blockers, and `interfaces.md` lists the field, the two kinds and the route.
- [ ] A new `embarch-desk` decision records the triggers, the checks and the contract; `spec.md` updated.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.
