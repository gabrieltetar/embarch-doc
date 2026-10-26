# 087 — Validate's summary never says "passed" over a warning or an empty bench, and enroll refuses an unanswerable chip itself

**State:** done agent/ui/087-validate-summary-and-enroll-refusal-say-what-happened, 2026-10-26
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-ui findings 8 and 10), verified by Opus against embarch-ui@aa5ffdaa
**Scope:** ui
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 05:14 leg

**Doc reserve in your scope (the Done-when below names stale task numbers):** `embarch-ui/spec.md` 9,099 / 10,240 B (1,141 B left), filed under `tasks/ui/089` (open). `embarch-ui/open.md` 4,366 / 5,120 B (754 B left), filed under `tasks/ui/088`, blocked `In flux: yes`. `embarch-ui/interfaces.md` 13,679 / 15,360 B, 145 B under its reserve line. `decisions/topology-boards.md` 10,645 / 12,288 B. Prefer amending decision 48 or a topology decision file with room over growing `spec.md`; do not grow `open.md` unless you close something in it. If your work pushes `interfaces.md` into reserve, file `tasks/ui/<NNN>-compact-ui.md` in the same commit.

**Isolation, not optional — this is the scope where it went wrong.** A browser drive starts the UI with `EMBARCH_DESK_PORT` set to a free scratch port (check it), and `EMBARCH_DESK_CONFIG_DIR`, `XDG_DATA_HOME`, `XDG_CONFIG_HOME` and `HOME` pointing at scratch dirs, as `tests/browser/drive_topology.py` does since `ui/091`; the stub Core runs on its own scratch port. Never let a UI run use the desk on :4891 or the owner's real config, never point the UI at the live Core (the WSL2 gateway, `:4884`), never call the `mcp__embarch-api__*` or desk tools, never touch a real probe, and never `pkill` by name. Note `tasks/ui/092`: two of `drive_topology.py`'s sidebar checks are already stale on `main`, so read a failure there against `main` before blaming your change.

## What

Two places on the Topology tab where the answer contradicts what its own rows and its sibling route say.

**The validate summary.** `api_validate` sets `"ok": failed == 0` (`src/topology.rs:1383`), and the tab draws `ok` as a green "every check passed" badge (`assets/app.js:6465-6469`). If the dev-bench port was a lowest-interface guess (`warn`, `:1245`), the report reads "every check passed" next to "1 to look at". If both roles are empty and no link resolved (`empty`, `:1138-1168`, `:1256-1263`), it reads "every check passed" with nothing checked at all.

**Enroll with no chip.** `api_enroll` turns a board whose chip cannot be looked up into an empty string and sends that to Core (`src/main.rs:672-679`). The sibling route `api_set_role_board` refuses the same state here, with a message saying where to set the chip (`src/topology.rs:880-897`). The drag-and-drop dialog blocks an empty chip in the browser (`assets/app.js:735`), but its message, "pick a board type for this role first", is wrong when a board type *is* picked and only the chip is missing. The saved-bench proposal path sends whatever chip the bench file holds (`:6664`), so it can reach Core with none, and the engineer gets back a 502-wrapped failure from the attach.

Suggested direction: a summary that distinguishes passed, passed with warnings, and nothing to check; and one refusal for an unanswerable chip, shared by both enroll paths and the role route.

## Why now

spec.md:63: "one missing either binding is *empty*, not failed; **a guessed dev-bench port is a warning, never a pass**". spec.md:58 and decision 48: a chip is "looked up, never typed … and an unanswerable one refuses here".

## Done when

- [x] The validate response, or the tab's reading of it, never shows "every check passed" when any check is `warn` or every check is `empty`. A browser check (`tests/browser/drive_topology.py`) covers a warn-only bench and an all-empty bench.
- [x] `POST /api/enroll` with an empty chip and a board type whose chip cannot be resolved answers 400 with the same guidance as `api_set_role_board`, and makes no Core call. Unit test with a stub Core.
- [x] The drag-and-drop dialog's refusal names the missing chip when a board type is picked.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` and `open.md` are in reserve with parked compaction debts (`tasks/ui/078`, `tasks/ui/074`).

## Done, 2026-10-26

- Validate response gains `verdict` (failed/warned/empty/passed); the tab draws it. Warn-only and all-empty benches covered in `drive_topology.py`.
- `resolve_chip_or_refuse` (src/topology.rs) shared by `/api/enroll` and the role route; Rust test `enroll_refuses_a_board_with_no_chip_without_calling_core` counts stub-Core connections (0). Dialog names the missing chip.
- Decision 48 amended (decisions/board-row.md); interfaces.md updated. spec.md and open.md untouched. A saved-bench proposal sends the same route, so it is refused the same way (no separate fix needed).
- `drive_topology.py` now sets HOME to scratch and takes `EMBARCH_UI_BIN`. Two checks fail there, both the known `tasks/ui/092` ones (sidebar five tabs; its sibling).
