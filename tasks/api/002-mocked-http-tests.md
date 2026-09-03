# 002 — Write the specified-but-missing mocked HTTP test suite

**State:** claimed by agent/api/002-mocked-http-tests, 2026-09-02 21:39
**Source:** [embarch-api/open.md](../../embarch-api/open.md) — "The mocked unit-test suite is specified and unwritten. The acceptance criteria are recorded ... and no test files exist."
**Scope:** api
**Hardware:** none

## What

`embarch-api/tests/` holds two JSON fixtures and **zero `.rs` files** (verified
2026-09-03; the 59 `#[test]` in `src/` are inline unit tests and are not this).
Write the suite `open.md` already specifies, against a mock HTTP server rather
than a live Core.

The acceptance criteria are already recorded and are the task — do not invent
new ones:

- bearer token injection on every outbound call
- per-endpoint timeout independence
- plain-text body surfaced on a non-2xx response
- the two-pipe drain invariant (a child writing heavily to one of stdout/stderr
  while barely touching the other must not hang)
- truncation on a UTF-8 character boundary, never mid-codepoint
- an untouched pre-existing artifact **not** counted as fresh

## Why now

Entirely host-side, fully verifiable without a board, and it closes a gap the
doc has been carrying rather than adding a new surface. The two-pipe invariant
in particular is a real hang this crate already fixed once and nothing guards.

## Done when

- [x] `embarch-api/tests/` contains real `.rs` tests covering all six criteria.
      `core_client_http.rs` (8 tests: bearer sweep over 23 endpoints, timeout
      independence, three plain-text-non-2xx surfaces) and `build_capture.rs`
      (12 tests: two-pipe drain both directions, UTF-8-boundary truncation,
      freshness), plus `tests/support/mod.rs`, a mock Core hand-rolled on
      `tokio::net`. **No new dependency, dev- or otherwise.**
- [x] Each test fails if its invariant is broken — check by breaking it locally.
      Six mutations, one per criterion, each reverted afterwards: drop
      `.bearer_auth`; point `serial_log` at `status_timeout`; parse a non-2xx
      body as JSON; drain the two pipes sequentially; drop the
      `is_char_boundary` search; return `true` for a pre-existing artifact.
      All six went red, including the sequential-drain one, which deadlocked
      and was caught by its own outer timeout at 60 s.
- [x] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`.
      81 tests pass (61 pre-existing inline + 20 new); clippy silent. Run three
      times over for the timing-sensitive test; no flake.
- [x] `embarch-api/open.md` updated — the smoke harness bullet stands and now
      says only the harness is unwritten.
- [x] `changelog.d/api-mocked-http-suite.added.md` and
      `changelog.d/api-capture-cap-is-tail-only.fixed.md` dropped;
      `status.d/api-build-rs-verified-column.md` written.

## What this turned up

Two things worth the supervisor's attention, neither of them the task:

- **`spec.md` described truncation that has never existed.** It said the build-log
  cap "keeps head *and* tail (~32 KB each side)"; `truncate_tail` has kept the
  64 KB tail only since the initial commit. Corrected in `spec.md` §3 and §7;
  the behavioural gap is logged in `open.md` rather than silently fixed, since
  building the head-and-tail split is a design call, not this task.
- **`suite/features.md` claimed `Verified: unit` for two rows backed by no test
  at all** — `src/build.rs` had no `#[cfg(test)]` module from the initial commit
  until now. Freshness is now genuinely unit-verified; `BuildLocks` still is
  not. That is the `status.d/` fragment.

## Structural change, flagged deliberately

`embarch-api` was a pure binary, so `tests/*.rs` could reach **nothing** in
`src/` — three of the six criteria were untestable, not merely untested. This
adds a one-module `lib` target (`src/lib.rs`, `pub mod build;`) and `main.rs`
imports `build` from it instead of declaring it. One compiled copy; the rest of
`main.rs` is untouched. Rationale: `embarch-api` decision 46.

## Debt

- **Windows coverage.** The four end-to-end tests need a POSIX shell and are
  `#[cfg(unix)]`. Truncation and freshness also have direct tests that run
  everywhere; **the two-pipe drain invariant has no portable form and is
  uncovered on Windows.** Not hardware debt — no board is involved — but it is
  a real hole, and it is recorded in `open.md` and decision 46.
- **The bearer sweep is a list.** A `CoreClient` endpoint added without
  `.bearer_auth(…)` is caught only if the sweep's route list is extended to
  call it. `post_study` is deliberately absent from the list (it calls
  `status()` first, so it would double-count); `flash`'s multipart branch is
  absent because a declared `base_url` always resolves `Local`.

## Environment note for the supervisor

Sibling path dependencies do not resolve inside a worktree: `embarch-api`'s
`Cargo.toml` names `../embarch-study-designer` and `crates/embarch-core-client`
names `../../../embarch-topology`, which under
`.worktrees/embarch-api/<branch>/` point at paths that do not exist. Two
symlinks in the worktree parent (`.worktrees/embarch-api/embarch-study-designer`
and `…/embarch-topology`, both to the main checkouts) were created to build at
all. **They are outside every repo and are not part of this branch**, but any
future `embarch-api` worktree needs them.
