# 094 — Every browser drive script takes its geckodriver and UI addresses from one environment convention

**State:** claimed by agent/ui/094-drive-scripts-one-port-convention, 2026-10-26 07:09
**Source:** the 2026-10-26 leg, landing `ui/085`: its worker passed scratch ports through environment variables to `tests/browser/drive.py` and `drive_race.py`, which read none, so both ran once against `127.0.0.1:4444` and `127.0.0.1:4899`, the owner's own geckodriver and UI. `drive.py` opened a headless session on the owner's geckodriver and failed on its first navigation; nothing was left running. Earlier legs tonight had workers reach live services too, so this is a harness gap, not one worker's slip.
**Scope:** ui
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 07:09 leg

**This task is the isolation gap itself, so do not test it the way `ui/085` did.** You do not need a
browser to prove the convention: the check this task asks for (a grep-style test or a gate-runnable
script) and a unit-level test of the address helper prove it without a geckodriver. **Do not run any drive
script whose source you have not just converted**, and never one with the variables unset. If you do run
one end to end, start your own geckodriver and UI on scratch ports (not 4444, 4899, 4891), record their
PIDs when you start them (not `$!` of a subshell: `ui/081`'s leg leaked one that way), confirm with `ss
-ltnp` that your script connected to yours, and kill them by those PIDs. A process on 4444 or 4899 is the
owner's: leave it alone. Do not do `ui/093` (the Desk Slack toggle) here.

**Reserve.** `embarch-ui/spec.md` 9,099 / 10,240 B (filed under `ui/089`), `embarch-ui/open.md` 4,366 /
5,120 B (parked under `ui/088`). This is a test-harness change; the convention belongs in
`tests/browser/README.md`, and a decision only if you change the defaults' behaviour (record it in the
topic file with room, not `spec.md`).

**Isolation.** Do not reach the owner's live services. No live Core, no desk on `:4891`, no geckodriver on
`:4444` and no UI on `:4899`, no real serial ports or debug probes, no owner data directories (any UI or
stub you start gets a fresh temp dir), and no MCP tools at all. Kill only processes you started, by PID.

## What

Five drive scripts hardcode `GECKO = "http://127.0.0.1:4444"` and `UI = "http://127.0.0.1:4899"` with no override (`drive.py`, `drive_race.py`, `drive_live.py`, `drive_switch.py`, `drive_chart_field.py`, as of `embarch-ui@81bde80`); the rest read an override, under more than one name (`drive_topology.py` takes `EMBARCH_GECKO_PORT`, `ui/085`'s `drive_table_refresh.py` takes `GECKO`/`UI`). When done, every `tests/browser/drive*.py` reads the geckodriver and UI addresses through one shared convention (one helper or one pair of variable names), `tests/browser/README.md` states it, and a script started with the convention's variables set never touches 4444 or 4899. Whether the defaults stay 4444/4899 (the owner's interactive use) or a script refuses to start without the variables is this task's call; record it.

## Why now

A fleet worker can only isolate itself from the owner's live UI through these variables, and a script that silently ignores them is the one way a careful worker still lands on his ports.

## Done when

- [x] Every `tests/browser/drive*.py` takes both addresses from the one convention; none hardcodes them without an override.
- [x] `tests/browser/README.md` names the convention and the scratch-port recipe a worker uses.
- [x] A test or a check (a grep in `cargo test`, or a pytest-free script the gate can run) fails if a drive script hardcodes either address without the override.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment only if a reader-facing behaviour changed.

## Shipped

`tests/browser/addr.py` is the one reader: `EMBARCH_GECKO_PORT` (default 4444) and `EMBARCH_UI_PORT` (default 4899, or a script's own where it starts the UI); all 15 `drive*.py` use it. Defaults kept; the retired names (`GECKO`, `UI`, `WEBDRIVER`, `ATLAS_UI_PORT`, `LINKS_UI_PORT`, `DESK_UI_PORT`) exit with an error (embarch-ui decision 65, `decisions/browser-drive.md`). `tests/browser/README.md` states it with a scratch-port recipe; `tests/drive_addresses.rs` is the guard and runs the helper with no browser.

**Not verified:** no drive script was run end to end (no geckodriver or UI started); the change to each script is its address lines plus `import addr`, and all compile (`py_compile`).
