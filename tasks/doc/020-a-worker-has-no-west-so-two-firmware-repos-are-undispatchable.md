# A worker has no runnable `west`, so `dev-bench` code work cannot be dispatched at all

**State:** open
**Source:** owner's repo survey, 2026-09-06 — two real dev-bench defects had to be filed `Hardware: required` for a toolchain reason
**Scope:** doc
**Hardware:** none
**Owner:** required

## What

`../../embarch-fleet/protocol.md` §7 draws the fleet's boundary at *hardware*: workers are host-side
only, and anything needing a board is not a task. `embarch-dev-bench` has a large host-side half —
`workspaces/native_sim` is a host build and `app/tests/serial_protocol` is a ztest suite that runs as
an ordinary process — so on the protocol's own terms that work is dispatchable.

It is not, and the reason is invisible from the protocol: **`west` is not on bare `PATH` on this
machine, and none of `workspaces/*` carries its own `.venv`** (`embarch-dev-bench/CLAUDE.md` says so
explicitly and tells a caller to pass an absolute path, the way `embarch-api`'s config declares
`west_binary` per project). A worker also gets a git worktree of the app repo, which does not carry
`workspaces/native_sim`'s modules at all.

So `Hardware:` is carrying two different meanings — "needs a board" and "needs a toolchain a worker
does not have" — and only the first is written down. Two real defects
(`dev-bench-protocol-state-indices-reach-a-c-array-unchecked`,
`dev-bench-pc-skip-len-prefixed-wraps-past-its-own-bounds-check`) were filed `required` for the
second reason, which reads to any later reader as though they need the bench.

## Why now

It costs a whole sub-project's worth of dispatchable work. The 2026-09-06 throughput audit found the
queue at one or zero dispatchable tasks for 53% of a 7.2 h run, and scope collision costing another
9% — `dev-bench` is one of the eight scopes that would relieve both, and it is dark for a reason
nobody chose.

This is the same family as `tasks/doc/012` (the Windows-target build no leg can run): a gate item
that is unrunnable in a worker's environment rather than wrong.

## Done when

- [ ] It is decided and written down whether a worker can be given a runnable `west` for
      `workspaces/native_sim` from a worktree — and if so, how (an absolute `west` path a task can
      name, the way `embarch-api`'s `west_binary` does, or a worker that works in the main checkout
      for this repo).
- [ ] If it cannot: `../../embarch-fleet/protocol.md` §7 or `tasks/README.md` says that a
      toolchain a worker lacks is also non-dispatchable, and says which value of `Hardware:` records
      it — so `required` stops silently meaning two things.
- [ ] The two dev-bench drops above are reclassified to match whichever answer lands.
- [ ] `embarch-outpost` is checked for the same gap — `tests/run-all.sh` hard-fails on unset `WEST`
      for three of its four legs, though its Python half runs clean today.
