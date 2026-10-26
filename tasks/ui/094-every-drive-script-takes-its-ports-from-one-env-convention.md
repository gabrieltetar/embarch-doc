# 094 — Every browser drive script takes its geckodriver and UI addresses from one environment convention

**State:** open
**Source:** the 2026-10-26 leg, landing `ui/085`: its worker passed scratch ports through environment variables to `tests/browser/drive.py` and `drive_race.py`, which read none, so both ran once against `127.0.0.1:4444` and `127.0.0.1:4899`, the owner's own geckodriver and UI. `drive.py` opened a headless session on the owner's geckodriver and failed on its first navigation; nothing was left running. Earlier legs tonight had workers reach live services too, so this is a harness gap, not one worker's slip.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Five drive scripts hardcode `GECKO = "http://127.0.0.1:4444"` and `UI = "http://127.0.0.1:4899"` with no override (`drive.py`, `drive_race.py`, `drive_live.py`, `drive_switch.py`, `drive_chart_field.py`, as of `embarch-ui@81bde80`); the rest read an override, under more than one name (`drive_topology.py` takes `EMBARCH_GECKO_PORT`, `ui/085`'s `drive_table_refresh.py` takes `GECKO`/`UI`). When done, every `tests/browser/drive*.py` reads the geckodriver and UI addresses through one shared convention (one helper or one pair of variable names), `tests/browser/README.md` states it, and a script started with the convention's variables set never touches 4444 or 4899. Whether the defaults stay 4444/4899 (the owner's interactive use) or a script refuses to start without the variables is this task's call; record it.

## Why now

A fleet worker can only isolate itself from the owner's live UI through these variables, and a script that silently ignores them is the one way a careful worker still lands on his ports.

## Done when

- [ ] Every `tests/browser/drive*.py` takes both addresses from the one convention; none hardcodes them without an override.
- [ ] `tests/browser/README.md` names the convention and the scratch-port recipe a worker uses.
- [ ] A test or a check (a grep in `cargo test`, or a pytest-free script the gate can run) fails if a drive script hardcodes either address without the override.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment only if a reader-facing behaviour changed.
