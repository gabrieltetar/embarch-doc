# 026 — The issue's folder goes once no window shows it

**State:** claimed by agent/desk/026-the-issues-folder-goes-once-no-window-shows-it, 2026-11-10 06:25 — 025 landed (desk `9a32975`), its checks are `closeout::check` in `src/closeout.rs`, decision 83
**Source:** Linear issue EMB-73
**Issue:** EMB-73
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

The desk's second half of EMB-73. `tasks/desk/025` makes Done or Canceled post an `end` (or an `unfinished`) to the issue's window, and the chat closes the window on a click (`tasks/chat/023`). **This task removes the folder once no window shows it**: the worktrees, their local branches and `.dev-worktrees/<key>/` itself. It reuses `tasks/desk/025`'s checks and close-out record, so it waits for 025 to land; `embarch-desk`'s decision for 025 records the desk-chat contract (two mailbox kinds, `end` and `unfinished`; `POST /items/{id}/finish`; a window shows a folder while it polls for it).

**Direction, decided at the split:**

- **A window shows a folder while it polls `GET /mailbox?folder=` for it.** The desk records the last poll per folder. A folder has no window once no poll for it has arrived for longer than a grace that covers the chat's 60 s back-off; pick the grace, and put it in `spec/constants.md` tagged [chosen].
- **A desk restart is not a window closing.** Absence is measured from the later of the folder's last poll and the desk's own start.
- **Only when the desk can see windows at all.** With the chat setting (`settings.chat_panel`) off, a window may never poll, so the desk removes nothing and the item's close-out says the folder is left for the owner.
- **The trigger is any of three, read the same way:** the chat's Close window button, the window closed any other way, or no window open when the status moved. All three are polls stopping, so there is one mechanism.
- **The checks run again immediately before removing anything**, since the chat may have worked between the status move and the window closing. A failure posts an `unfinished` and removes nothing.
- **Removal**, for each worktree in the folder: `git worktree remove` from its main clone, then delete its local branch; for Canceled, also delete the branch on the remote (a remote that does not have it is not an error). Then remove the folder **without following symlinks**: the folder holds symlinked siblings (`src/suite.rs` links them), and their targets must be untouched.
- **The close-out record says what happened**: waiting for the window, removed, or left for the owner and why.

## Why now

EMB-73. Landing keeps the folder, so today nothing ever removes it.

## Where to look

- `src/server.rs` — the mailbox routes (where a poll is seen), the settings, and 025's close-out code
- `src/suite.rs` — how a folder and its symlinks are made; `src/worktree.rs` — git helpers
- `embarch-doc/embarch-desk/interfaces/chat-routes.md`, `decisions/` (025's decision), `spec/constants.md`

## Dispatch notes

- Normal mode: a new numbered `embarch-desk` decision, or an extension of 025's if it reads as one decision; your call, and say which.
- **Two `embarch-desk` docs are in reserve after 025** (`tasks/desk/027`, blocked on `In flux: yes`): `decisions/sessions.md` 12,177 of 12,288 B (111 B left) and `spec.md` 9,197 of 10,240 B. You are the actor making the flux, so this is yours: **before extending decision 83, move it verbatim out of `sessions.md` into a new topic file under `decisions/`** (pointer stub and index row, per `DOC-COMPACTION.md` §2's split-first rule; a verbatim split restates nothing). Then extend it there, or add your own decision beside it. Carry 027's `Must not delete:` list (decision 83's contract with the chat; decision 80's **Unverified** note). If `sessions.md` is then out of reserve, delete it from 027's `Compacts:` line and say so in 027's body; keep `spec.md` under its cap and leave 027 open for it if it is still in reserve.
- 025's reviewer noted that code comments in `src/closeout.rs` and `src/server.rs` cite "decision 77" for the close-out; it is 83 (77 is the per-session desk decision). Fix them while you are in those files.
- Tests use temporary git repos, a temporary bare remote and a temporary suite root; never the real `.dev-worktrees/`, a real remote or the real desk config.
- Do not edit `embarch-chat` or anything outside `embarch-desk` and `embarch-doc/embarch-desk/`.
- Edit files with your Edit and Write tools, not inline Python or shell redirects.

## Done when

- [ ] After an `end`, once no poll for the folder has arrived for the grace, the worktrees are removed, their local branches deleted and the folder gone; a test with a symlinked sibling in the folder shows the symlink's target untouched.
- [ ] Canceled also deletes the branches on the remote; a test against a temporary bare remote covers it, and a branch the remote lacks.
- [ ] With uncommitted files at removal time, nothing is removed and an `unfinished` names the repo and reason.
- [ ] A desk that has just started does not read every folder as windowless; a test covers it.
- [ ] With the chat setting off, nothing is removed and the close-out says why.
- [ ] `embarch-desk` decisions, `spec.md`, `spec/constants.md` and `interfaces.md` updated.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.
