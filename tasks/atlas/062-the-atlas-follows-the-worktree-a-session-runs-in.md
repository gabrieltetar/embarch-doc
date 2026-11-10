# 062 — The atlas follows the worktree a session runs in

**State:** done
**Source:** Linear issue EMB-19 ("The atlas `fw` path resolves to the worktree")
**Issue:** EMB-19
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`embarch-desk`'s Start work makes a git worktree of a firmware repo beside its main clone and links the main clone's untracked `embarch/` folder and `.mcp.json` into it (`embarch-desk` `src/worktree.rs` `LOCAL_FILES`). So a session in the worktree starts the atlas MCP server with the main clone's `--atlas-dir`, and `atlas.toml`'s `[project] fw` names the main clone: `status`, staleness and `build` all read the main clone's commit, not the branch the session is working on.

Make the atlas follow the worktree, **with this direction (decided at the split):**

- **The worktree is found from the working directory.** When an `embarch-atlas` command or the MCP server runs with its working directory inside a linked git worktree of the configured `fw` repo (the same `git rev-parse --git-common-dir`), `fw` resolves to that worktree's top for that process. Anywhere else, `fw` resolves exactly as today. `atlas.toml` is not edited.
- **The build worktree keeps the repo's name.** `build` names its worktree `.work/<commit12>/<fw basename>` so the Zephyr module keeps its name (`DESIGN.md`, "Building from the worktree"). A linked worktree's folder is usually named differently (Start work uses `<repo>-<issue key>`), so that basename must stay the configured `fw` repo's, not the linked worktree's.
- **Say which `fw` was used.** `status` and anything else that reports the firmware commit name the worktree when one was picked, so a reader can tell a main-clone answer from a worktree answer.
- **One atlas folder, shared.** The `embarch/` folder is the main clone's in every worktree, so a `build` run from a worktree writes the same atlas folder the main clone's sessions read. The worker states in `DESIGN.md` what that does (the expected answer: it is one atlas pinned to whichever commit was built last, and `status` in the other checkout then reports it stale); changing it to one atlas per worktree is out of scope.
- An explicit override (a `--fw` option or an environment variable) is the worker's call; if added, it wins over the working directory.

## Why now

EMB-19: in a Start work worktree the atlas answers about the main clone's commit, so a session checking its own branch's devicetree or pins against the hardware gets another branch's answer.

## Where to look

- `src/embarch_atlas/project.py` `fw_dir`, `git_head`, `status`
- `src/embarch_atlas/stale.py` — the staleness check's `fw`
- `src/embarch_atlas/build.py` — `.work/<commit12>/<fw basename>` and where `fw` is read
- `src/embarch_atlas/mcp` entry and `live.py`, `inventory.py` — other `fw_dir` callers
- `DESIGN.md` — "Building from the worktree", the `atlas.toml` section

## Dispatch notes

- `desk/020` runs beside you: it makes a `west build` in a Start work worktree use the worktree's module (the other half of EMB-19). Do not touch `embarch-desk`.
- Tests use a temporary git repo with a linked worktree; nothing runs a real west build.
- The atlas has no numbered decisions: amend `DESIGN.md` in place, and note it briefly in `embarch-doc/embarch-atlas/design.md` only if that doc says something this changes.
- Your worktree has its own venv; run `pytest -rs` from it. `test_public_guard` needs `../.atlas-local`, which is linked.
- Edit files with your Edit and Write tools, not inline Python or shell redirects.

## Done when

- [x] Run from a linked worktree of the configured `fw` repo, `fw` resolves to that worktree; from the main clone or elsewhere, unchanged. A test covers both with a real temporary git worktree.
- [x] `build`'s worktree folder keeps the configured repo's basename when `fw` is a linked worktree, with a test.
- [x] `status` names the worktree when one was used.
- [x] `DESIGN.md` says how `fw` is resolved and what a build from a worktree does to the shared atlas folder.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.

## What landed

`project.resolve_fw` (env `EMBARCH_ATLAS_FW` wins, else the git worktree of the configured repo the cwd is in, else the configured `fw`); `fw_dir` goes through it, so `status`, staleness, inventory, live and `build` follow. `status` prints and returns the worktree (`fw_is_worktree`, `fw_configured`). `build` keeps the configured repo's basename, excludes the main clone from the west modules, and treats both checkouts as leak sources. Override choice: an environment variable only, no `--fw` form. DESIGN.md "Which `fw` a process uses" also states the shared-atlas-folder effect. No hardware debt: nothing ran a real west build.
