# 153 — Test scratch directories named from the clock can collide

**State:** claimed by agent/api/153-test-scratch-dirs-named-from-the-clock, 2026-11-13 13:34
**Source:** EMB-169, filed by the `api/151` worker on 2026-11-12, after `tests/lease_client.rs` was fixed
**Issue:** EMB-169
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Several `embarch-api` test files name a per-call scratch directory from the
process id and the nanosecond clock. Tests are threads of one process, so two
that read the clock in the same tick share one directory: the second writes
over the first's config, and whichever finishes first deletes the directory
under the other. `api/151` found this in `tests/lease_client.rs` (about 1 run in
100 failed under load, 0 in 700 after) and replaced the clock with a
process-wide `AtomicUsize` counter.

The issue names five files with the same pattern: `tests/build_each.rs`,
`tests/bench_exchange_cli.rs`, `tests/serial_log_truncation.rs`,
`tests/build_verdict.rs` and `tests/signal_exchange_cli.rs`. A grep of
`origin/main` finds the nanosecond clock in five more —
`tests/dev_bench_hello_success.rs`, `tests/json_surface.rs`,
`tests/run_study_unreported_bench.rs`, `tests/smoke_harness.rs` and
`tests/study_follow_cli.rs` — not yet read to see whether each names a
directory or does something else with the time. Read every one; fix each that
names a directory, and say in this file which you left and why.

One helper in `tests/support/` that every file calls is better than ten copies
of the counter, if the files can share it.

**Runs after `api/152`.** That task (subprocess CLI tests fail from the suite
root) touches the same files, and its cause may change what these helpers look
like. If `api/152` has not landed when this is dispatched, say so and stop.

**What you may change.** Only `embarch-api` and `embarch-doc/embarch-api/`.

**Doc reserve.** `embarch-api/open.md` is in reserve and filed as
`tasks/api/150-compact-api.md`. Add nothing to it unless a bullet goes out in
the same edit.

## Why now

A test that fails once in a hundred runs reads as a broken branch at the gate,
and the fleet re-runs the gate on every unit it lands.

## Done when

- [ ] No test file names a scratch directory from the clock alone.
- [ ] Each changed file passes 50 runs under CPU load (parallel batches, as
      `api/151` did, are acceptable), with the numbers in this file.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `changelog.d/` fragment dropped.
