# 067 — A session in a worktree finds the main clone's atlas

**State:** claimed by agent/atlas/067-worktree-sessions-find-the-main-clones-atlas, 2026-11-17 13:42
**Source:** EMB-90, filed by an audit after a session planning a driver change in a worktree read a datasheet with an inline `pdftotext` script before finding the atlas in the main clone
**Issue:** EMB-90
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The atlas lives in `embarch/atlas/` of a firmware repo's main clone, and that
folder is excluded from git (`.git/info/exclude`), so `git worktree add` does not
carry it. `common.atlas_dir()` defaults to `<git toplevel>/embarch/atlas`, which
in a worktree is a path that does not exist; the `@embarch/atlas/MAP.md` import
that `project.py` writes is not there either; and the `atlas-use` skill's trigger
("an `embarch/atlas/MAP.md` exists") does not fire. The session falls back to
grepping the PDF, when `find_text` already does that job with page and section
citations.

Make the atlas reach a worktree session. `project.resolve_fw()` already detects
"a worktree of the configured repo" by `git rev-parse --git-common-dir`; the
issue's direction, which you may improve on and must say so if you do:

- `atlas_dir()` falls back to the main clone's `embarch/atlas` when the current
  tree has none and the two share a git common dir;
- the `atlas-use` skill's trigger and first steps say how to find the atlas from
  a worktree (the CLI and MCP lookups resolving it, or the main clone's path), so
  the skill fires there.

Linking the folder into each new worktree at creation is the other direction the
issue names; that is a worktree-creation change, not this repo's. If you find the
atlas side cannot meet the first Done-when item alone, say so here and file the
other half as a worker issue rather than reaching across.

**Public repo.** Tests use synthetic repos made with `git init` and `git worktree
add` in a temp dir; `test_public_guard` must run, not skip (the worktree's parent
carries the `.atlas-local` link).

**Burndown leg: no new numbered decision** (`embarch-atlas` keeps none, so this is
about `DESIGN.md`: describe the lookup order, do not open a new design question).

**What you may change.** Only `embarch-atlas` and `embarch-doc/embarch-atlas/`.

**Doc reserve.** Nothing of `embarch-atlas`'s is in reserve.

## Why now

The owner moved it to Fleet Ready; a worktree is the default for desk work items,
which is where the hardware questions behind a driver or devicetree change are asked.

## Done when

- [ ] A session started in a fresh worktree of an atlas-equipped repo can run `find_text` and read `MAP.md` without opening the main clone by hand.
- [ ] The `atlas-use` skill's trigger fires in that worktree.
- [ ] A test covers the fallback over a synthetic repo and worktree, and the explicit `--atlas-dir` still wins.
- [ ] Gate green (`../../embarch-fleet/gate.md`, Python bullet).
- [ ] `changelog.d/` fragment dropped; `DESIGN.md` or `embarch-atlas/design.md` updated where the atlas location is described.
