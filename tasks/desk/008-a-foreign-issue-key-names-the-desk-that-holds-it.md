# 008 — A foreign issue key names the desk that holds it

**State:** claimed by agent/desk/008-a-foreign-issue-key-names-the-desk-that-holds-it, 2026-11-09 19:47
**Source:** Linear issue EMB-9, filed by a session
**Issue:** EMB-9
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

When no workspace in a call's scope has an issue key, the error says which case it hit: a key whose team is bound to another desk names that desk and the folder to open; a key whose team no connected workspace has says so, without naming a desk. Today every case gives exactly `no connected Linear workspace has <KEY>`, so an agent cannot tell a wrong key from the wrong desk and asks the user instead of fixing it.

**Read decision 77 first** (`embarch-doc/embarch-desk/decisions/desks.md`, landed 2026-11-09): a call is now scoped to its session's desk, resolved from the session's folder and work item, which makes "the key belongs to another desk" the common case this error has to name. Write the message against that resolution, not against the old one open desk.

## Why now

Decision 29 makes the desk the agents' one access point to Linear, so its errors have to be enough to act on.

## Where to look

- `src/linear.rs` `first_with` — builds the message when no workspace answers and none errored
- `src/linear.rs` the issue lookup at the `find_issue` call, and `create_issue`'s `no connected Linear workspace has a team {team_key}`
- `src/server.rs` `ensure_item` and `link_item` — the same message for a work item
- `src/store.rs` — the desks' `linear` bindings (`LinearBinding`: account, team, project), where the owning desk can be found

## Dispatch notes

- **Burndown leg: no new numbered decision.** Amending an existing `embarch-desk` decision in place is fine; if the work needs a new one, stop and say so in this file.
- **In reserve:** `embarch-desk/decisions/agents.md` (11,455/12,288 B, 833 B left), filed as `tasks/desk/011` (open). Add nothing to it if you can avoid it; if you must, keep it short and say so in your report.
- Close by rewriting the `State:` line so `done` (or `blocked`) is its first word with nothing glued to it — `done,` and a left-over `claimed` are both refused by `check-task-state.py`.

## Done when

- [ ] A key whose team is bound to another desk names that desk and its folder in the error.
- [ ] A key whose team no connected workspace has says so, without naming a desk.
- [ ] A test covers both messages.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `embarch-desk` `interfaces.md` updated where it lists the error, `changelog.d/` fragment dropped.
