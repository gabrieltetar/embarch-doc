# 079 — The build log says when the DUT role could not decide the board, and the stored log keeps that line

**State:** open
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

- [ ] Unit tests cover each branch of the board choice: role resolved and same as the study, role resolved and different, the study's variant or revision overridden, a role holding a board type absent from the catalog, an unreadable catalog, and an empty role. Each branch emits a line naming the study's board, the role's board and the one built.
- [ ] The stored build log contains those lines and the flash and reset lines. A run whose flash fails has the failure in the stored log.
- [ ] A browser check (`tests/browser/drive_build.py`) finds the board line in the builds source after a run.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` and `open.md` are in reserve with parked compaction debts (`tasks/ui/078`, `tasks/ui/074`), so prefer `decisions/firmware-build.md` and `decisions/topology-roles.md`.
