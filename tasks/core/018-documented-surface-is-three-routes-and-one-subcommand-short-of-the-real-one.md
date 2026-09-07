# 018 — Core's documented surface is three routes and one subcommand short of its real one, while the auth sweep already holds the complete list

**State:** done
**Source:** suite review pass 2026-09-06, dimension 3 (one philosophy). Code-confirmed.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-core/src/api.rs:71-96`'s `build_router` registers **27** method/path pairs.
`embarch-core/interfaces.md` documents **22**, missing `GET /dev-bench/port`,
`GET /logs/recent` and `GET /logs/stream`.

`embarch-core/src/main.rs:42+` has **11** subcommands; `embarch-core/spec.md:19` enumerates ten
and omits `flash-backend` — which appears in **no doc in the corpus**, while
`embarch-umbrella/src/doctor.rs:3045` runs `embarch-core flash-backend` as check 14 and `:3109`
tells the operator to run it themselves.

**The complete list already exists in this repo, derived mechanically.**
`embarch-core/src/api.rs:1292` `const ROUTE_MARKER` and `:1299` `const AUTH_CASES` are a
27-row table derived from and checked against the router's own source. Core's `spec.md` §2
boasts about it: *"'every' is asserted mechanically: the test sweep derives its route list from
`build_router`'s own source, so a route added without an auth case fails the build rather than
shipping open."* That mechanism is pointed at auth only.

Candidate direction: make it hold that Core's documented surface inventory cannot be shorter than
its registered one — the existing `ROUTE_MARKER` scan is the obvious lever — and add the missing
CLI subcommand to `spec.md` §1's list.

## Why now

Auditing Core's surface for reach is exactly how `tasks/api/036` was found, and it was done
against a table three rows short. An operator following `doctor` check 14's advice is pointed at an
undocumented command. `check-links.py` validates paths and `check-doc-size.py` counts bytes;
nothing compares `interfaces.md`'s table to the router.

## Done when

- [x] `embarch-core/interfaces.md` has a row for every route `build_router` registers. Added
      `GET /dev-bench/port` (Hardware table), and a new `## Logs` section for `GET /logs/recent`
      and `GET /logs/stream`.
- [x] `embarch-core/spec.md` §1 lists every subcommand `main.rs` accepts. Added `flash-backend`
      to the CLI list.
- [x] Adding a route without a doc row fails something, or the reason it should not is written
      down. `src/api.rs`'s test module now carries `DOCUMENTED_ROUTE_COUNT` (26, one behind
      `AUTH_CASES.len()`'s 27 because `/signals` is one `.route()` call for two methods) and a
      new test `every_registered_route_has_a_row_in_interfaces_md` asserting it against
      `registered_route_paths().len()`. It is a pinned literal, not a cross-repo file read — decision
      46 (`embarch-core/decisions/platform.md`) writes down why a relative path to `interfaces.md`
      is not reliable under the fleet's one-branch-two-worktrees model, and what this convention
      does and does not catch.
- [x] Gate green; `changelog.d/core-*` fragment. `changelog.d/core-surface-doc-gap.fixed.md`.

## Notes from this pass

- Also fixed two now-stale "26 registered routes" references that predate this task
  (`embarch-core/decisions/platform.md`'s decision 42 entry, `embarch-core/open.md`'s
  "route sweep proves rejection, not reach" bullet) — both now say 27, the real current count.
- `embarch-core/interfaces.md` landed in the doc-size reserve (94.6%, 833 B left) as a direct
  result of the three added rows. Filed `tasks/core/022-compact-core.md` in the same commit,
  blocked on `tasks/core/021` (retire `GET /logs/stream`) and `tasks/api/032` landing first, since
  either would change the very rows a compaction pass would otherwise touch.
- **Windows build debt, not attempted**: this unit changed `src/api.rs`/`main.rs`-adjacent test
  code and docs only; `cargo build --target x86_64-pc-windows-msvc` was not run from this worktree
  (WSL has no MSVC `cc` for `hidapi`'s `build.rs`, and Windows `cargo.exe` cannot follow this
  worktree's Linux symlinks to `embarch-topology`/`embarch-study-designer`). Linux
  build/test/clippy are green; per protocol this is a recorded debt, not a gate failure.
- No `features.d/` fragment: this is a documentation-accuracy fix, not a new user-visible
  capability, matching the supervisor's own read in the dispatch note.

**Adjacent, not the same:** `tasks/api/032` notes that `embarch-core/interfaces.md:30`'s
`/probes/enrolled` row omits a **field**. This is three absent **rows** plus a subcommand, and the
mechanism that would prevent both. **Also note:** the
`core-retire-logs-stream-which-has-no-consumer-anywhere` drop in this batch may delete one of the
three missing routes outright. Land that first if both are worked.
