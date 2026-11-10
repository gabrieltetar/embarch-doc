# 020 — A Start work worktree builds its own Zephyr module

**State:** claimed by agent/desk/020-a-start-work-worktree-builds-its-own-zephyr-module, 2026-11-10 03:15
**Source:** Linear issue EMB-19; `embarch-desk/open.md`, last item ("A worktree of a repo built inside a west workspace")
**Issue:** EMB-19
**Scope:** desk
**Hardware:** verify-only
**Owner:** no

## What

Start work makes a worktree beside the main clone (`src/worktree.rs` `worktree_path`, `<repo>-<issue key>`). When that repo is a project in a west workspace it is also a Zephyr module, and west lists the **main clone's** path for it. So a `west build` run in the worktree takes its app from the worktree but its drivers, bindings, Kconfig and board files from the main clone, and edits made in the worktree to those are silently ignored.

Make a build in the worktree use the worktree's module files, **with this direction (decided at the split):**

- **Share the workspace, replace one module.** The worktree does not need its own `west update`: every other module stays the workspace's. Only the firmware repo's own entry in the module list is replaced by the worktree. This is the answer to the `open.md` question; move it out of `open.md` into the decision.
- **The mechanism is Zephyr's `ZEPHYR_MODULES`.** It replaces west's module list outright, so it must name every module: the workspace's list (`west list -f '{abspath}'`, or what the worker finds equivalent) with the main clone's path swapped for the worktree's. `embarch-atlas` already builds this way (its `DESIGN.md`, "Building from the worktree": `-DZEPHYR_MODULES=<every other west module>;<worktree>`). Zephyr reads it through `zephyr_get` in `cmake/modules/zephyr_module.cmake`; confirm from any Zephyr tree's `cmake/modules/extensions.cmake` that `zephyr_get` reads the environment before relying on it. Read only; never write to a Zephyr tree or any repo but `embarch-desk`.
- **Where the desk puts it: the worktree's `.claude/settings.local.json` `env`**, which Claude Code applies to a session started in that folder and to the commands it runs. Start work writes `ZEPHYR_MODULES` there, merging into the file if it already exists and keeping every other key, and git-excludes it as `link_local_files` does its names. If the worker finds that Claude Code does not apply that `env` to a session's shell commands, stop and say so in this file rather than picking another mechanism silently.
- **Not in a west workspace, nothing is written.** A repo with no `.west/` above it, or one west does not list as a project, gets no override and no warning. `west` not found is a warning in Start work's answer, never a failure of Start work.
- **A module with no `name:` changes name.** Zephyr names a module without `name:` in `zephyr/module.yml` after its directory, and the worktree's folder is `<repo>-<key>`, so the override would rename the module (and its `ZEPHYR_<NAME>_MODULE_DIR`). The worker decides what Start work does then (warn and still write, or warn and write nothing), and the decision says which. Never silent.
- **A suite desk is out of scope** (decision 70's `.dev-worktrees/<key>/<repo>` layout keeps the repo's basename and holds no Zephyr repo today).

## Why now

EMB-19: a driver or board edit in a Start work worktree has no effect on its build and nothing says so, which is a wrong answer from the bench rather than a missing one.

## Where to look

- `src/worktree.rs` `prepare`, `link_local_files`, `exclude_from_git` — the worktree and the local files it gets from the main clone
- `src/server.rs` `start_work` — Start work's route, and its answer's `warnings`
- `embarch-doc/embarch-desk/open.md` (last item), `decisions/sessions.md` and `decisions/built.md` for where Start work's decisions live
- `embarch-atlas/DESIGN.md`, "Building from the worktree" — the same override, read only

## Dispatch notes

- Normal mode: a new numbered `embarch-desk` decision is expected. Number it per `DOC-CONVENTIONS.md`; check `main` before you commit.
- `atlas/062` runs beside you: it makes the atlas resolve its `fw` to the worktree a session runs in (the other half of EMB-19). Do not touch `embarch-atlas`.
- If `embarch-api`'s `build` tool, called from a session in a worktree, builds the main clone and not the worktree at all, that is an `embarch-api` gap: say so here and file it with `scripts/fleet-linear.py file --from worker --project embarch-api`. Do not reach into that repo.
- Tests use a fake workspace (a `.west/` folder and a stand-in for `west list`); nothing runs a real west build.
- No `embarch-desk` doc in `embarch-doc` is in doc-size reserve at the split.
- Edit files with your Edit and Write tools, not inline Python or shell redirects.

## Done when

- [ ] Start work on a repo that west lists as a project writes `ZEPHYR_MODULES` (the workspace's module list with the main clone swapped for the worktree) into the worktree's `.claude/settings.local.json` `env`, merging, and git-excludes it; a repo outside a west workspace gets nothing.
- [ ] A module with no `name:` gets a warning in Start work's answer, and the decision says what is written then.
- [ ] Tests cover the swap, the merge into an existing file, the no-workspace case and the missing-`west` warning.
- [ ] `open.md`'s worktree-in-a-west-workspace item is answered and removed; a new `embarch-desk` decision records the mechanism.
- [ ] Hardware-verification debt recorded here: a board-file edit in a real Start work worktree, `west build` there, and the build reading the worktree's file.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.
