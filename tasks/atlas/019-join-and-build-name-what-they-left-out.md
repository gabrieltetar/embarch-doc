# 019 — An atlas says when a declared board or its Kconfig extraction is missing, and a missing kconfig.json can be filled without a full rebuild

**State:** done
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-atlas findings 10 and 11), verified by Opus against embarch-atlas@0cf93cec
**Scope:** atlas
**Hardware:** none — Fixture atlases with a stamp and some netlists. The Kconfig half is testable by making the extraction fail under monkeypatch. Proving the properties needs no west build.
**Owner:** no

## What

**A declared schematic board with no netlist drops out of the atlas, and nothing says so.**
- `load_boards` (`src/embarch_atlas/join.py:1022-1031`) skips any board in the stamp's `schematic_boards` that has no `boards/<label>/netlist.json`. `load_join` logs only when *no* board loaded (`join.py:1083-1085`).
- Join exits 0. Pins, checks, the MAP and the graph cover only the boards that had netlists.
- `inputs.json` records schematic hashes only for the boards that were loaded (`join.py:1117`), while `joined_stamp` keeps the build's hash for the missing one (`project.py:299-300`), so `status` reads the atlas as fresh (`project.py:317-319`).
- `update`'s stop check skips a board that has no netlist (`update.py:118-120`).
- The MAP header names every declared board (`mapgen.py:61`), but its boards section lists only the loaded ones, with no reason (`mapgen.py:105-107`).

**A failed Kconfig extraction leaves the atlas without kconfig.json, and the answer then gives the wrong way out.**
- `build` turns an extraction failure into a logged warning and a stamp string, `kconfig: "not extracted: …"` (`build.py:503-508`).
- `config` on that atlas then answers "has no kconfig.json (built before it existed); the next /atlas-update writes one" (`buildq.py:78-81`). That is false for this atlas: `update` or `build` of the same commit returns "already built" (`build.py:438-440`), so only `build --force`, a full worktree rebuild, writes the file.

One possible direction:
- Name a declared board that has no netlist in the join's output and in a place the session reads, such as the MAP's boards section or `status`. Decide whether `update` stops for it.
- Have `config` quote the stamp's recorded reason.
- Give an existing atlas a way to get its kconfig.json written short of `--force`. The existing guard that extraction runs only while the workspace's Zephyr matches the build still applies.

## Why now

- DESIGN.md "On-disk layout" says `kconfig.json` is "Written by `build`", and the `[[targets]]` section says `schematic_boards` is "which schematic boards make up this product". An atlas covering part of the product, or missing a file its own answers point to, says neither.
- The case is a normal one: a product gains a second board in `atlas.toml` before anyone runs `schematic` on it, or the build's Python lacks kconfiglib.
- `tasks/atlas/015` (stale reasons on every `src:` line, the MAP's stale line) and `001` (a bump that cannot run says why in the MAP) write to the same MAP and `status` surfaces. The missing-input reasons here should use whatever those land, not invent a third place.

## Done when

- [x] A fixture join with `schematic_boards = ["A", "B"]` and only A's netlist names B as missing in the join's log, and in the MAP or `status` output. A test covers it.
- [x] Whether `update` stops for a declared board that has no netlist is decided, written in DESIGN.md "When `update` stops", and pinned by a test.
- [x] An atlas whose stamp records `kconfig: not extracted: <reason>` answers `config` with that reason and a recovery that works for that atlas. A test uses a stamp carrying the failure string.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `DESIGN.md` updated (embarch-atlas has no `spec.md`, so DESIGN.md is its contract). `changelog.d/` fragment dropped.
