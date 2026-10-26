# 102 — Run host studies in Core: send-and-read steps against the PD bench and the DUT console

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the PD source sequence ran 4 times as a bash script (plus 7 runs of its scratch versions). The scripts made 441 shell exchanges across 2 consoles in 16 e-load runs, about 1.7 s per operation. 2 runs stopped on an empty console reply (2026-10-10)
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## Supervisor note, 2026-10-26 06:30 leg — the landing carries a schema bump, announced

**Announced:** `#embarch-fleet` `ts` `1793017849.375049`, 2026-10-26 06:30 MDT, no `--action`. The 30-minute window runs from that `ts`; poll it with `fleet-read.py --thread 1793017849.375049` before dispatching. A cancel drops this note's plan (quote it here); silence for 30 minutes means go. **Window closed with no reply at 07:01** (thread polled then, 0 actionable); the announcing leg ended at its unit cap before it could run this, so the next leg may dispatch it after one more poll of the thread.

This is the unit where Core first accepts a `HostStudy`, and `embarch-study-designer` decisions 80 and 86 (`decisions/study.md`, `decisions/host-repeat.md`) put the `HOST_TYPE_SCHEMA_VERSION` bump in exactly that unit. The constant lives in `embarch-study-designer/src/schema_version.rs`, so **the worker does not make it** and must not touch that repo; it ships the Core half against 19. **The landing leg makes the bump itself**, 19 to 20 with the file's history comment and any test pinning 19, as a shared-crate commit landed in the same fold as this unit's Core merge, then re-runs the Core and api gates against it. No dev-bench wire bump (`embarch-host-study-proposal.md`: JSON only). `tasks/core/116` (per-pass line counts) and `tasks/core/101` build on this unit.

## What

Core runs a host-run study (study-designer task "host-study-model"), as `embarch-host-study-proposal.md` §Core describes. `POST /host-studies` takes the same `study_lock` as a bench study, validates the study against topology and runs the steps on one executor thread. It emits the existing `StepCompleted` per step. **`Exchange` runs the code path of `POST /signals/{name}/exchange`** (decision 79): write one line, then read until `until` or the timeout, with `match_after_echo` taken as declared. The reply is recorded raw, escape codes kept, capped and marked truncated. `Wait` sleeps. **Teardown runs on every exit:** after the last step, after a failing step, on a timeout and on a new `POST /study/{id}/cancel`. A step that cannot find its signal's port fails with the port names seen, like the exchange route's own 409.

## Why now

Each field script took its own bench lock and reimplemented abort and safe state. A run that dies part-way leaves the load sinking and the partner at 20 V. Two runs of the PD sequence were lost to an empty reply the script could not tell apart from a dropped command.

## Done when

- [ ] `POST /host-studies` accepts a valid host study and answers 409 while any study holds `study_lock`.
- [ ] `Exchange` and `Wait` execute, and `GET /study/{id}/steps` returns each reply with its byte count and elapsed time.
- [ ] **A zero-byte reply is reported as its own outcome detail**, separate from a reply that never showed `until` before the timeout.
- [ ] Teardown runs after a failed step, after a timeout and after `POST /study/{id}/cancel`. Unit tests over a scripted fake port prove all three.
- [ ] No step compares a value. Only "written", "marker seen" and "port present" decide the outcome.
- [ ] Bench check, run by the supervisor: the PD source sequence as a host study against `pd-bench` gives the same contract lines as the bash run, and teardown leaves the partner at 5 V after a forced failure.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
