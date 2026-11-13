# 152 — Subprocess CLI tests fail when `cargo test` runs from outside the repo

**State:** open
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

- [ ] The cause is named in this file.
- [ ] The suite passes from the repo and from the suite root
      (`--manifest-path`), and a test or the fix's comment says why the
      working directory matters.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
