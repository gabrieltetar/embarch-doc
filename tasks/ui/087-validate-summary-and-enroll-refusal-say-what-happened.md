# 087 — Validate's summary never says "passed" over a warning or an empty bench, and enroll refuses an unanswerable chip itself

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-ui findings 8 and 10), verified by Opus against embarch-ui@aa5ffdaa
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Two places on the Topology tab where the answer contradicts what its own rows and its sibling route say.

**The validate summary.** `api_validate` sets `"ok": failed == 0` (`src/topology.rs:1383`), and the tab draws `ok` as a green "every check passed" badge (`assets/app.js:6465-6469`). If the dev-bench port was a lowest-interface guess (`warn`, `:1245`), the report reads "every check passed" next to "1 to look at". If both roles are empty and no link resolved (`empty`, `:1138-1168`, `:1256-1263`), it reads "every check passed" with nothing checked at all.

**Enroll with no chip.** `api_enroll` turns a board whose chip cannot be looked up into an empty string and sends that to Core (`src/main.rs:672-679`). The sibling route `api_set_role_board` refuses the same state here, with a message saying where to set the chip (`src/topology.rs:880-897`). The drag-and-drop dialog blocks an empty chip in the browser (`assets/app.js:735`), but its message, "pick a board type for this role first", is wrong when a board type *is* picked and only the chip is missing. The saved-bench proposal path sends whatever chip the bench file holds (`:6664`), so it can reach Core with none, and the engineer gets back a 502-wrapped failure from the attach.

Suggested direction: a summary that distinguishes passed, passed with warnings, and nothing to check; and one refusal for an unanswerable chip, shared by both enroll paths and the role route.

## Why now

spec.md:63: "one missing either binding is *empty*, not failed; **a guessed dev-bench port is a warning, never a pass**". spec.md:58 and decision 48: a chip is "looked up, never typed … and an unanswerable one refuses here".

## Done when

- [ ] The validate response, or the tab's reading of it, never shows "every check passed" when any check is `warn` or every check is `empty`. A browser check (`tests/browser/drive_topology.py`) covers a warn-only bench and an all-empty bench.
- [ ] `POST /api/enroll` with an empty chip and a board type whose chip cannot be resolved answers 400 with the same guidance as `api_set_role_board`, and makes no Core call. Unit test with a stub Core.
- [ ] The drag-and-drop dialog's refusal names the missing chip when a board type is picked.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` and `open.md` are in reserve with parked compaction debts (`tasks/ui/078`, `tasks/ui/074`).
