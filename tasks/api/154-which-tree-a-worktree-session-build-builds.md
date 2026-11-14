# 154 — Which source tree a build asked from a worktree session builds

**State:** done
**Source:** EMB-128, filed by an audit while `desk/020` (EMB-19) landed: that task asked its worker to check this and file it, and the worker did not check
**Issue:** EMB-128
**Scope:** api
**Hardware:** none
**Owner:** no

## What

A Start work worktree carries `ZEPHYR_MODULES` in its
`.claude/settings.local.json` `env` (`embarch-desk` decision 80), and a
`west build` typed into that session's shell picks it up. A build asked through
the `embarch-api` MCP server goes through `embarch-api`'s own project
resolution instead, and nobody has checked which source tree that resolution
builds when the session's folder is a worktree. If it builds the main clone,
decision 80's override never reaches it.

Find out, and say which. For a project configured on the **main clone** and an
`embarch-api` server **started in a worktree of that clone**, name:

1. the directory the assembled `west build` runs in;
2. the source/app path it passes (`-s` or the positional app dir);
3. the build directory it passes (`-d`), if any;
4. whether `ZEPHYR_MODULES` from the server's own environment reaches the
   spawned `west`, or the plan sets its own environment.

Where to start, from the filer: `src/tools.rs` `build` resolves the configured
project and runs its plan; `src/main.rs` finds the config upward from the
working directory when none is given; the plan itself is assembled in
`crates/embarch-firmware-build/` (`resolve.rs`, `zephyr.rs`, `config.rs`).
`embarch-desk` links the main clone's `embarch/` folder and `.mcp.json` into a
Start work worktree (`embarch-desk/src/worktree.rs` `LOCAL_FILES`), so the
server starts with the main clone's config. The atlas resolves its firmware
checkout from the working directory since `atlas/062`; `embarch-api` has no
equivalent the filer found.

**Prefer a run to a reading.** Where the plan can be assembled without running
`west` — a unit test over a temporary config and a temporary working
directory, or a CLI path that prints the plan — establish the answer that way,
and keep the test if it pins the behaviour. Say in this file which you did. Do
not run a real `west build` and do not build any configured project's sources.

**Do not fix it in this task.** This is the investigation. If the answer is
the main clone, file a bug with
`python3 /home/gabriel/Github/embarch/embarch-fleet/scripts/fleet-linear.py file --from worker --project embarch-api --title "…" --body-file <file>`,
per `LINEAR-PROTOCOL.md`, naming where the fix belongs, and put its key here.
If it is the worktree, nothing is filed.

**Where the answer goes.** Here, under a `## Found` heading, with the four
items above and the file and function each comes from. If `spec.md`'s build
section does not already say which tree is built, add the sentence there. The
supervisor copies the answer onto the issue at the fold.

**What you may change.** Only `embarch-api` and `embarch-doc/embarch-api/`.

**Doc reserve.** Nothing of `embarch-api`'s is in reserve. Decision topic
files near their limit: `ledger` 15 B left, `bench-exchange` 122 B,
`failure-reporting` 192 B; this task should need none of them.

## Found

**The main clone.** Established by a run: a unit test (`resolve.rs`,
`a_zephyr_build_runs_in_and_builds_the_configured_source_path_not_the_working_directory`)
assembles the plan over a temporary config and fixture with the test's own cwd
elsewhere; the config-discovery and spawn lines are read. Bug filed: **EMB-181**
(fix belongs in `resolve.rs` `resolve_zephyr_build`/`resolve_static`, with
`src/main.rs` startup supplying the working directory).

1. **Directory:** `project.source_path`, verbatim from the config (`resolve.rs`
   `resolve_zephyr_build`, `cwd: project.source_path.clone()`; `build.rs`
   `.current_dir(&plan.cwd)`). Run.
2. **Source/app path:** positional `<source_path>/app/<app>` (or `apps/`), from
   `zephyr::app_path` (`zephyr.rs`) called in `resolve_zephyr_build`. Run.
3. **`-d`:** `<build_dir_root>/<target dir name>`, `build_dir_root` verbatim from
   the config (`resolve_zephyr_build`; `zephyr::build_command`). Run.
4. **Environment:** the plan sets only the project's `env` table
   (`env: project.env.clone()`; `build.rs` `.envs(&plan.env)` adds it to the
   server's inherited environment). `ZEPHYR_MODULES` set in the server's process
   reaches `west` by inheritance; the plan sets none and never removes one.
   Read for `build.rs`, run for the plan's `env`. Whether Claude Code puts a
   worktree's `settings.local.json` `env` into the MCP server's environment was
   not checked and is the desk's side.

Why: `src/main.rs` uses the working directory only to find the config
(`find_config_upward`); the config linked into a worktree is the main clone's,
whose `source_path` is absolute, and nothing rebases it. The working directory
is never consulted for a build. So decision 80's override cannot change which
tree is built, and west locates its workspace from the main clone's cwd as well.
A relative `source_path` would resolve against the process cwd, but configs
carry absolute ones. Hardware: none.

## Why now

It is the one Fleet Ready issue, and a worktree session that builds the main
clone without saying so ships a firmware image from the wrong tree.

## Done when

- [x] The four items above are named under `## Found`, each with the file and
      function it comes from, and whether it was run or read.
- [x] If the answer is the main clone, a `bug` is filed against `embarch-api`
      naming the fix's place, and its key is in this file.
- [x] Gate green (`../../embarch-fleet/gate.md`).
- [x] `changelog.d/` fragment dropped if anything shipped (a test, a spec
      sentence).
