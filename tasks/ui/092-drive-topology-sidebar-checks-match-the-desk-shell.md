# 092 — `drive_topology.py`'s sidebar checks describe the shell the page has now

**State:** claimed by agent/ui/092-drive-topology-sidebar-checks-match-the-desk-shell, 2026-10-26 05:37
**Source:** `ui/091`'s worker, 2026-10-26: two checks in `tests/browser/drive_topology.py` fail on its run and are untouched by its diff. The supervisor read both against `main` at `26ed2ec`; both are stale since the Desk shell (`d414560`, 2026-10-22) and the Atlas tab, not regressions.
**Scope:** ui
**Hardware:** none — the drive runs against its own stub Core, isolated from the live desk since `ui/091`.
**Owner:** no

## Dispatch note, 2026-10-26 05:37 leg

**Doc reserve in your scope:** `embarch-ui/spec.md` 9,099 / 10,240 B (1,141 B left), filed under `tasks/ui/089` (open, not yours); `embarch-ui/open.md` 4,366 / 5,120 B (754 B left), filed under `tasks/ui/088`, blocked `In flux: yes`; `embarch-ui/interfaces.md` 13,756 / 15,360 B, 68 B under its reserve line. This task should need none of them; do not grow any. `ui/087` (landed at `fd7f1b6`) changed `drive_topology.py` last: it scratches `HOME`, takes `EMBARCH_UI_BIN`, and toggles the stub's dev-bench port. Build on that.

**Isolation, not optional — this is the scope where it went wrong.** A browser drive starts the UI with `EMBARCH_DESK_PORT` set to a free scratch port (check it), and `EMBARCH_DESK_CONFIG_DIR`, `XDG_DATA_HOME`, `XDG_CONFIG_HOME` and `HOME` pointing at scratch dirs, as `drive_topology.py` already does; the stub Core and geckodriver run on their own scratch ports. Never let a UI run use the desk on `:4891` or the owner's real config, never point the UI at the live Core (the WSL2 gateway, `:4884`), never call the `mcp__embarch-api__*` or desk tools, never touch a real probe, and never `pkill` by name (kill only the PIDs you started).

## What

- `"the sidebar is five tabs"` asserts five `.nav-item`s; `assets/index.html` has six (desk, topology, study-designer, live-study, atlas, debug).
- `"and where it is under that"` asserts `project-current-path` reads `/tmp`; with no desk open `renderShellDesk()` writes `no desk · /tmp`, and with a desk it writes the short name and the path. The drive runs with no desk since `ui/091` isolated it, so the expected text is the no-desk form.

A third check, `"the box's title is the role and the board type is under it"`, failed once on `ui/091`'s run and passed on a rerun. Look for a timing cause (a fixed `sleep` racing a render) while the file is open; say what was found, or that it did not reproduce.

Fix the checks to assert what the page is meant to show (decision text where one exists), not whatever it shows today. Do not reintroduce a dependency on the owner's desk on :4891 or his real `XDG_DATA_HOME`: keep `ui/091`'s isolation.

## Done when

- [ ] `drive_topology.py` passes end to end against a release build, isolated as it is now, twice in a row.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment if anything user-visible changed (likely none).
