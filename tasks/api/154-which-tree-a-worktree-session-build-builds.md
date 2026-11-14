# 154 — Which source tree a build asked from a worktree session builds

**State:** claimed by agent/api/154-which-tree-a-worktree-session-build-builds, 2026-11-14 11:12
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

## Why now

It is the one Fleet Ready issue, and a worktree session that builds the main
clone without saying so ships a firmware image from the wrong tree.

## Done when

- [ ] The four items above are named under `## Found`, each with the file and
      function it comes from, and whether it was run or read.
- [ ] If the answer is the main clone, a `bug` is filed against `embarch-api`
      naming the fix's place, and its key is in this file.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `changelog.d/` fragment dropped if anything shipped (a test, a spec
      sentence).
