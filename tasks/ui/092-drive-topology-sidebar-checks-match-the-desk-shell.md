# 092 — `drive_topology.py`'s sidebar checks describe the shell the page has now

**State:** open
**Source:** `ui/091`'s worker, 2026-10-26: two checks in `tests/browser/drive_topology.py` fail on its run and are untouched by its diff. The supervisor read both against `main` at `26ed2ec`; both are stale since the Desk shell (`d414560`, 2026-10-22) and the Atlas tab, not regressions.
**Scope:** ui
**Hardware:** none — the drive runs against its own stub Core, isolated from the live desk since `ui/091`.
**Owner:** no

## What

- `"the sidebar is five tabs"` asserts five `.nav-item`s; `assets/index.html` has six (desk, topology, study-designer, live-study, atlas, debug).
- `"and where it is under that"` asserts `project-current-path` reads `/tmp`; with no desk open `renderShellDesk()` writes `no desk · /tmp`, and with a desk it writes the short name and the path. The drive runs with no desk since `ui/091` isolated it, so the expected text is the no-desk form.

A third check, `"the box's title is the role and the board type is under it"`, failed once on `ui/091`'s run and passed on a rerun. Look for a timing cause (a fixed `sleep` racing a render) while the file is open; say what was found, or that it did not reproduce.

Fix the checks to assert what the page is meant to show (decision text where one exists), not whatever it shows today. Do not reintroduce a dependency on the owner's desk on :4891 or his real `XDG_DATA_HOME`: keep `ui/091`'s isolation.

## Done when

- [ ] `drive_topology.py` passes end to end against a release build, isolated as it is now, twice in a row.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment if anything user-visible changed (likely none).
