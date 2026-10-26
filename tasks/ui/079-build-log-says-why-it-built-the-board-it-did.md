# 079 — The build log says when the DUT role could not decide the board, and the stored log keeps that line

**State:** claimed by agent/ui/079-build-log-says-why-it-built-the-board-it-did, 2026-10-26 04:32
**Dispatch note:** the compaction tasks named under Done when are renumbered: `spec.md` (9,099/10,240 B, 1,141 B left) is filed under `tasks/ui/089` (open, `In flux: no`), and `open.md` (4,366/5,120 B, 754 B left) under `tasks/ui/088` (blocked). Put the decision in `decisions/firmware-build.md` (8,047 B) or `decisions/topology-roles.md` (7,762 B); if you must add to `spec.md`, add no more than a phrase. The browser drive must stay isolated from the live desk the way `ui/091` made `drive_topology.py` isolated (scratch `EMBARCH_DESK_PORT`, `EMBARCH_DESK_CONFIG_DIR`, `XDG_*`), and must never reach a live Core or the desk on :4891.
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-ui findings 4 and 12), verified by Opus against embarch-ui@aa5ffdaa
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

**The fallback is silent.** `build_and_flash` announces the role when `role_target` returns one (`src/firmware_build.rs:326-351`). When it returns `None`, it falls back to the study's own stored board, variant and revision with no line at all (`:353-357`). `None` covers a role with no board type, but also a board type that is in the role and absent from the catalog, and a catalog that would not load (`src/topology.rs:586-624`; `load_catalog(..).ok()`). `role_target`'s own comment says that in this case "the caller says so and builds what the study asked for" (`:618-623`). The caller does not say so. A study that names the same board as the role but a different variant or revision gets "building for the DUT role's board" and is not told that its own variant was replaced. The log does print the resolved descriptor and command (`:368-375`), so what was built is visible; why is not.

**The stored log loses those lines.** The durable copy collects only west's stdout and stderr (`:378-397`). Every `info` line goes to the live stream only: the working-tree version, the role announcement or its absence, flashing, reset, and the error when flash or reset fails. A log read in the Debug tab's builds source an hour later cannot show which board the role overrode. The `ok`/`failed` in the file name and header is the build's own verdict, which matches decision 39 ("a build log is a log").

Suggested direction: one line for every path through the board choice, naming what the study stored, what the role held, and which one won and why. Also keep those lines, plus the flash and reset outcome, in the stored file. Whether the stored log should also say how the run ended is the worker's call to make and record against decision 39.

## Why now

Decision 45 (`decisions/topology-roles.md`): a study that still carries a board "is neither obeyed nor silently dropped. The role wins, and the build log says so by name before anything is built." spec.md:64: "the override is announced on the build log." When the role cannot be resolved, the study's board is obeyed, with no announcement. If that board shares the role's chip, Core's identity gate lets the flash through.

## Done when

- [x] Unit tests cover each branch of the board choice: role resolved and same as the study, role resolved and different, the study's variant or revision overridden, a role holding a board type absent from the catalog, an unreadable catalog, and an empty role. Each branch emits a line naming the study's board, the role's board and the one built.
- [x] The stored build log contains those lines and the flash and reset lines. A run whose flash fails has the failure in the stored log.
- [x] A browser check (`tests/browser/drive_build.py`) finds the board line in the builds source after a run.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` and `open.md` are in reserve with parked compaction debts (`tasks/ui/078`, `tasks/ui/074`), so prefer `decisions/firmware-build.md` and `decisions/topology-roles.md`.

## Result

Decision 62 (`decisions/firmware-build.md`). `topology::role_target` now returns `Result<RoleTarget, RoleMiss>`; `firmware_build::choose_board` writes the line for every path; every `info` line is kept in the stored log with an `[embarch-ui] ` marker, and flash/reset lines and failures are appended after the build. File name and header stay the build's own verdict. Tests: 7 in `firmware_build.rs`, 1 in `topology.rs`. Browser: `drive_build.py` run against a debug binary, stub west, stub Core, all PASS, including the failed-flash line. `spec.md`/`open.md` untouched (reserve).
