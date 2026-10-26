# 070 — Host-run study model: Exchange, Prompt, Instrument and Wait steps, with teardown

**State:** claimed by agent/study-designer/070-host-study-model, 2026-10-26 00:58
**Done 2026-10-26:** `src/host_study.rs`, decision 80, fixture `tests/fixtures/host_pd_source_sequence.json`. `HOST_TYPE_SCHEMA_VERSION` deliberately not bumped (decision 80); the Core unit that accepts `HostStudy` owns it. `open.md` untouched. Tests are `alloc`-gated: run `cargo test --features std` (plain `cargo test` skips them).
**Reserve, for the worker (2026-10-26):** `embarch-study-designer/open.md` 647 B left, parked on
`tasks/study-designer/026` with nothing live payable. Put new open points in the decision or
`spec.md` where they belong; if `open.md` must take a line, delete an answered one first, and
file `tasks/study-designer/<NNN>-compact-study-designer.md` if you leave it tighter than you found it.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 0 studies run against 96 logged bench tests: every PD and e-load run was a bash script over `signal-exchange` (16 logged e-load runs, 972 commands), because `Action` (`embarch-study-designer/src/study.rs:715`) has only BLE steps
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-study-designer` has the host-run study type that `embarch-host-study-proposal.md` (2026-10-09, §Shape, "Study model") describes, plus the teardown list that the field scripts needed and the proposal leaves out. `HostStudy { name, steps, teardown, streams }`, where `streams` holds `Signal` taps only. `HostStep { name, action, timeout_ms, continue_on_fail, delay_before_ms }`. `HostAction` is `Exchange { signal, line, until, match_after_echo }`, `Prompt { text }`, `Instrument { instrument, line, query }` and `Wait { ms }`. **`teardown` is a list of host steps that runs on every exit path.** That covers the end of the run, a step that fails without `continue_on_fail`, a timeout and a cancel. Every field script carried this exit path by hand: load input off, PD partner back to 5 V, DUT settings restored, even on Ctrl-C. The type is JSON only and never goes on the dev-bench wire: a host-type schema bump with no wire bump, so decision 60 still holds for bench studies. Names are checked against topology when Core accepts the study, not here.

## Why now

The field project wrote 1,736 lines (72 KB) of bash, including a simulated bench, to run 3 sequences and 9 e-load cases. Each script reimplements the step list, its timeouts, the raw log and the abort path. Nothing the suite gives a study covers any of it.

## Done when

- [x] `HostStudy`, `HostStep`, `HostAction` and `HostStepResult { step_name, outcome, reply, reply_truncated, answered_by, elapsed_ms }` exist, serde round-trip, and reject unknown fields.
- [x] `teardown` is validated like `steps`. A teardown step that fails is recorded and the rest of the teardown still runs.
- [x] **No step type carries an expected value or a range.** The study philosophy (2026-09-25) is that a study collects and the engineer interprets, and the schema enforces it.
- [x] `decisions.md` settles one open point: whether `Exchange` may declare a refusal marker that makes the step `Fail`. The PD bench ends every command with `pd: ok` or `pd: error <reason>` (`embarch-dev-bench` decision 48). A refusal means the action was not carried out, which the philosophy already counts as a failure. A value in the reply is never compared.
- [x] A host-study step cap is set as its own constant, sized from field sequences. The PD source sequence is 49 host steps: 14 requests, 17 status reads and 18 waits. Studies on the dev-bench wire keep 16 (`DBM_MAX_STEPS_PER_STUDY`) and 64 (`limits.rs:10`).
- [x] A fixture study, the PD source sequence (fixed 5/9/15/20 V, then PPS 5 to 21 V at 1 A, then back to 5 V), validates and lives in the crate's test fixtures.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
