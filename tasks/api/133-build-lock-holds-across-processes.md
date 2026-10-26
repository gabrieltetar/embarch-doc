# 133 — Make "one build in flight per build directory" hold across processes, not only inside one

**State:** claimed by agent/api/133-build-lock-holds-across-processes, 2026-10-26 07:43
**Reserve (2026-10-26 leg):** `embarch-api/decisions/client-crate.md` 707 B left (`api/140` filed),
`embarch-api/open.md` 832 B left (`api/144` filed). Record the lock decision in the build topic file, not
`client-crate.md`; if your unit pushes either file further into reserve, say so in your report.
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-api finding 5), verified by Opus against embarch-api@6d664853
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`BuildLocks` is an in-memory map of async mutexes. It serializes two builds of the same lock key only when both run in one process. Every CLI subcommand that builds constructs a fresh `BuildLocks`. Every MCP server process holds its own, and each agent session spawns one. `embarch-ui` holds a third, from the same crate. Two of these can therefore run the build command against one build directory at the same time: an agent's MCP `build` alongside a terminal `embarch-api build`, two agent sessions in one firmware repo, or the UI's build-and-flash alongside either.

When this is done, the guard holds across processes on one machine. One direction: an OS advisory lock on a file keyed by the lock key, taken inside the shared crate's build entry points, so the CLI, the MCP server and `embarch-ui` all get it without changes of their own. A waiting caller says another process holds the build instead of sitting silent. A holder that dies releases the lock. Whether a second caller waits or refuses, and the platform coverage, are the worker's call. Keep it lightweight.

## Why now

- `crates/embarch-firmware-build/src/build.rs:170-191`: per-instance map.
- `src/cli.rs:432, 497, 607, 687, 753, 1381`: a fresh `BuildLocks::new()` per subcommand. `src/tools.rs:37`: the MCP server's own.
- `embarch-ui` `src/main.rs:164-168` holds its own instance, and its comment calls it "the same `BuildLocks` `embarch-api` holds". It is the same type, but a separate lock.
- `spec/implementation.md:18`: "One build in flight per project… guards two calls stomping one output directory". Nothing in the docs limits that to one process.
- Nothing has been recorded going wrong. This is filed because several agent sessions, each with its own MCP server, routinely work on one machine.

## Done when

- [ ] A test starts two separate processes that build the same lock key, using a static project whose build command records its start and end. The two runs never overlap.
- [ ] Builds with different lock keys still run in parallel.
- [ ] A build process killed while holding the lock does not block the next build (test).
- [ ] A caller that has to wait, or is refused, says so in its output or error, naming that another process holds the build.
- [ ] No consumer of `embarch-firmware-build` (CLI, MCP, `embarch-ui`) needs a code change to get the cross-process guard. `embarch-ui` picks it up on its next rebuild.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
