# 152 — Subprocess CLI tests fail when `cargo test` runs from outside the repo

**State:** done
**Source:** EMB-158, filed by a worker on 2026-11-11, measured against a branch based on `origin/main` `d36be9e`
**Issue:** EMB-158
**Scope:** api
**Hardware:** none
**Owner:** no

## What

From the repo or a worktree of it, `cargo test --no-fail-fast` passes all 400
tests. From the suite root, `cargo test --no-fail-fast --manifest-path
<worktree>/Cargo.toml` fails 20, every one a test that runs the `embarch-api`
binary against `tests/support`'s mock Core: all of `tests/bench_exchange_cli.rs`,
`tests/signal_exchange_cli.rs` and `tests/serial_log_truncation.rs`, plus
`tests/dev_bench_hello_success.rs` and `tests/run_study_unreported_bench.rs`.
For example `serial_log_truncation.rs` `truncated_true_reaches_json_output`
reads `Null` where it expects `true`.

Each test passes `--config <tempdir>/api.toml` and sets `XDG_DATA_HOME` and
`LOCALAPPDATA`. The child inherits the parent's working directory, the only
input that differs between the two runs.

**Next check.** Run one failing test from the suite root with the child's
stderr printed, and see what the binary reads from its working directory.
Candidates: a config or `embarch/embarch.toml` found by walking up from the
working directory, or the session-desk lookup (decision 85) resolving the suite
root as a desk folder.

**The fix, either of two.** The tests set the child's working directory to a
temp folder, or the binary stops reading the parent's when `--config` is given.
If the second changes what a user sees, it is a decision; say which you chose
and why. **Run from the suite root only with `--manifest-path` and a
`--target-dir` beside your worktree**, so nothing builds into another repo.

**What you may change.** Only `embarch-api` and `embarch-doc/embarch-api/`.

**Doc reserve.** `embarch-api/open.md` is 4,502 of 5,120 B, in reserve, and
filed as `tasks/api/150-compact-api.md`. Add nothing to it unless a bullet goes
out in the same edit. Decisions near their own limit: `ledger` (98) 15 B,
`bench-exchange` (89) 122 B, `failure-reporting` (67) 192 B.

## Why now

A gate run from the wrong folder reads red for a reason no diff explains, and
twenty failures at once look like a broken branch.

## Done when

- [x] The cause is named in this file (below).
- [x] The suite passes from the repo and from the suite root
      (`--manifest-path`), and a test or the fix's comment says why the
      working directory matters.
- [x] Gate green (`../../embarch-fleet/gate.md`).

## Cause and fix

Not the working directory the binary reads. `embarch-api/.cargo/config.toml`
blanks `EMBARCH_REQUIRE_LEASE` (`force = true`) for test runs, and cargo finds
that file by walking up from the *invoking* working directory, not from
`--manifest-path`. From the suite root it is not read, so a session that
exports `EMBARCH_REQUIRE_LEASE=1` (this one does) leaks it into every spawned
binary; the lease gate then asks the mock Core for `/lease`, gets a body with
no `holder`, and the call fails (`missing field holder`). It was the child's
inherited environment, not its cwd, that differed.

Fix: `tests/support/mod.rs` gains `api_command(exe)`, a `Command` with
`EMBARCH_REQUIRE_LEASE` removed and a comment saying why; the five failing
files spawn the binary through it. No user-visible change, so no decision.
Passes from the worktree and from the suite root (`--manifest-path`,
`--target-dir` beside the worktree), `--workspace`, no failures.

Tests that spawn the binary without the mock Core (e.g. `version_line`,
`patches_cli`) were not hit and were left alone. Task 153 (clock-named scratch
dirs) shares no cause with this one: it is about directory names, this about an
inherited variable.
