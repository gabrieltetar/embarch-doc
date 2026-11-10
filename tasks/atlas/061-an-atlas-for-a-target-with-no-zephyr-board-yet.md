# 061 — An atlas for a target whose PCB has no Zephyr board yet

**State:** done
**Source:** Linear issue EMB-21
**Issue:** EMB-21
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`embarch-atlas build <target>` always runs `west build -b <board>` for one target at one commit, and the rest of the atlas (`join`, `config`, `dt_node`, `footprint`, `stacks`, `MAP.md`) hangs off that build's artifacts. A project whose custom PCB has no Zephyr board yet cannot build an atlas at all, and that is when one would help most: the schematic and datasheets exist, and the board files are the thing being written.

Several steps already need no build (`inventory`, `schematic`, `interfaces`, `missing`, `doc prep`), and since `atlas/058` `q part_card` and `q mismatch_report` answer from netlists and coverage before an atlas exists.

**Direction (decided at the split):**

- **A target can say it has no board yet, explicitly.** A forgotten or misspelt `board` must still fail as it does today, so this is a stated opt-in in `atlas.toml` (the worker names the key or value, and the matching flag if any).
- **`build` on such a target skips the west build and every step that reads its artifacts**, runs every step that does not, and writes an atlas whose stamp (`atlas.json`) says there is no build and why, rather than leaving `board` and `build` silently empty. It is still pinned to one target and one firmware commit.
- **`status` and `MAP.md` say which outputs are absent because there is no build**, each by name, so a session reading `MAP.md` knows not to ask for them. A query that needs a build (`config`, `dt_node`, `footprint`, `stacks`, a code lookup) on such an atlas answers that the target has no board yet, not with a traceback or a missing-file error.
- **Principle 6 is amended in place** to say what a no-board atlas is pinned to and what it lacks. When the target later gains a board, a normal `build` supersedes it; the staleness check sees the stamp's board change.
- Which of the build-dependent outputs can degrade rather than be absent (part of `join` may run without a build) is the worker's call: list each one in `DESIGN.md` under the rule, with what it does without a build.

## Why now

Bring-up of a new board is the moment the atlas has most to answer and the one moment it cannot be built.

## Where to look

- `src/embarch_atlas/build.py` `target_config` (merges `atlas.toml` and flags; `board` comes from the target), `run_build`, `stamp`, `west_command`, `cmd_build`
- whatever runs after the build in the `atlas-build` flow (`join`, the `MAP.md` writer, `status`)
- `skills/atlas-build/SKILL.md` — step 2 is the build, steps 3 to 7 join and report from it
- `DESIGN.md` principle 6, "The stamp (`atlas.json`)", "How a session sees the atlas", `atlas.toml`, the CLI table
- `src/embarch_atlas/` `part_card` and `mismatch_report`'s no-atlas paths from `atlas/058`, which this should reuse rather than duplicate

## Dispatch notes

- Normal mode. The atlas keeps no numbered decisions; state the rule in `DESIGN.md` in place, principle 6 included.
- Nothing touches hardware and nothing runs a real `west build`; tests use a synthetic project with netlists and records and no board.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.
- Edit files with your edit tool, not inline Python scripts.

## Done when

- [x] A project with schematics and datasheets, whose target states it has no Zephyr board, produces an atlas without `build` failing, and a target with a missing `board` still fails as before.
- [x] `status` and `MAP.md` name each output absent because there is no build.
- [x] A build-dependent query on that atlas says the target has no board yet.
- [x] `DESIGN.md` states the rule, principle 6 included.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.

## Result

- Opt-in: `no_board = true` on the `[[targets]]` entry in `atlas.toml`, or `build --no-board` for one run. A missing `board` still fails naming `--board`; `no_board` with a `board` is refused.
- `build` writes only the stamp (`board: null`, `build: {built: false, reason, fw, west_topdir}`); `join`, `update`, `status`, `MAP.md`, `stale=` and the lookups read it through `common.no_build`. Lists of absent and reduced outputs are `common.NO_BUILD_ABSENT` / `NO_BUILD_DEGRADED`, also written into `DESIGN.md`.
- A normal `build` for the same target and commit supersedes the no-board atlas; staleness says the target now names a board.
- `features.d/`: no row, since `atlas` has no section in the feature inventory.
- Hardware verification debt: none. Unverified on a real project: the stamp's recorded west project list when a workspace is configured (best effort; a failure is a warning).
