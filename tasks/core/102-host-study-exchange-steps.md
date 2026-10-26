# 102 — Run host studies in Core: send-and-read steps against the PD bench and the DUT console

**State:** claimed by agent/core/102-host-study-exchange-steps, 2026-10-26 07:08
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the PD source sequence ran 4 times as a bash script (plus 7 runs of its scratch versions). The scripts made 441 shell exchanges across 2 consoles in 16 e-load runs, about 1.7 s per operation. 2 runs stopped on an empty console reply (2026-10-10)
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## Supervisor note, 2026-10-26 06:30 leg — the landing carries a schema bump, announced

**Announced:** `#embarch-fleet` `ts` `1793017849.375049`, 2026-10-26 06:30 MDT, no `--action`. The 30-minute window runs from that `ts`; poll it with `fleet-read.py --thread 1793017849.375049` before dispatching. A cancel drops this note's plan (quote it here); silence for 30 minutes means go. **Window closed with no reply at 07:01** (thread polled then, 0 actionable); the announcing leg ended at its unit cap before it could run this, so the next leg may dispatch it after one more poll of the thread.

This is the unit where Core first accepts a `HostStudy`, and `embarch-study-designer` decisions 80 and 86 (`decisions/study.md`, `decisions/host-repeat.md`) put the `HOST_TYPE_SCHEMA_VERSION` bump in exactly that unit. The constant lives in `embarch-study-designer/src/schema_version.rs`, so **the worker does not make it** and must not touch that repo; it ships the Core half against 19. **The landing leg makes the bump itself**, 19 to 20 with the file's history comment and any test pinning 19, as a shared-crate commit landed in the same fold as this unit's Core merge, then re-runs the Core and api gates against it. No dev-bench wire bump (`embarch-host-study-proposal.md`: JSON only). `tasks/core/116` (per-pass line counts) and `tasks/core/101` build on this unit.

## Dispatch note, 2026-10-26 07:08 leg

Thread `1793017849.375049` polled again at 07:06: no reply, so the plan above stands. **Do not touch
`embarch-study-designer`** (not the constant, not its tests): build against it as it is, at 19. Do not do
`core/116` or `core/101`. Core's renderer for `line_counts`/`Repeat` is `core/116`'s; if `HostStudy`
carries fields this unit does not execute, refuse them by name or ignore them as the proposal says, and
record which. If you find the unit needs a change in any other repo (topology, study-designer, api),
stop and report it rather than reaching across.

**Reserve, and one file is nearly full.** `embarch-core/open.md` is 5,070 / 5,120 B (**50 B left**),
parked under `core/112` (`In flux: yes`). Put this unit's open points inside its new decision, as
`core/115` did, and leave `open.md` alone. If an open question genuinely must go in `open.md`, compact
`open.md` in this unit to make room, keeping `core/112`'s `Must not delete:` items readable, and say so in
the task file. `embarch-core/spec.md` 9,638 / 10,240 B (602 B left) and `decisions/probes.md` 11,263 /
12,288 B are filed under `core/112` too: a host-study decision belongs in a new topic file
(`decisions/host-study.md` or similar, indexed), and `spec.md` gets at most a short pointer.

**Hardware debts to record, not run:** the native Windows build, and the task's own bench check (PD
source sequence against `pd-bench`, teardown to 5 V after a forced failure).

**Isolation.** Do not reach the owner's live services. No live Core (no request to the Windows service
or any running Core; a Core you start for a test binds a scratch port and gets a fresh temp data dir), no
desk on `:4891`, no geckodriver on `:4444` and no UI on `:4899`, no real serial ports or debug probes
(the scripted fake port only), no owner data directories, and no MCP tools at all. Kill only processes you
started, by PID.

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
