# 153 — Test scratch directories named from the clock can collide

**State:** done
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

- [x] No test file names a scratch directory from the clock alone.
- [x] Each changed file passes 50 runs under CPU load (parallel batches, as
      `api/151` did, are acceptable), with the numbers in this file.
- [x] Gate green (`../../embarch-fleet/gate.md`).
- [x] `changelog.d/` fragment dropped.

## Outcome

`api/152` had landed. Added `support::unique_dir(tag)` in `tests/support/mod.rs`
(process id plus a process-wide `AtomicUsize`, not the clock); all ten files
that named a directory from the clock now call it: the five the issue named
and the five the grep found (`dev_bench_hello_success`, `json_surface`,
`run_study_unreported_bench`, `smoke_harness`, `study_follow_cli`). All ten
named a directory; none was left. `json_surface`, `build_verdict` and
`build_each` gained `mod support;`. The same pattern in the unit-test helper
in `src/main.rs` (it cannot reach `tests/support`) got an inline counter.

Left alone: directories named from the process id plus a fixed tag
(`patches_cli`, `stack_cli`, `core_client_http`, `src/ledger.rs`, ...). They
are not clock-named, and collide only if one tag is used twice in a process.
`build_capture` and `lease_client` already used counters.

**Load runs.** Each of the ten changed test files: 50 runs (5 parallel batches
x 10 runs, 14 `yes` CPU burners on 14 cores, `EMBARCH_REQUIRE_LEASE=1`
exported): 500 runs, 0 failures. Gate green: build, test, clippy `-D warnings`.
