# 143 — Core refuses every lease-gated call while a study runs, bar its cancel

**State:** done — lease_middleware refuses every gated call but cancel while a study runs; decisions 93 and 95 amended; open.md out of reserve
**Source:** notes/hil/12-prevention.md — "What stays outside prevention": while a study or a test runs, Core refuses every hardware call that is not the run's own, Live reads included
**Issue:** EMB-253
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`study_lock` is checked today by the instrument route, `GET /dev-bench/hello`
and a second study. Reset, flash, mem-read, core-state, serial log and signal
exchange take only `hw_lock`, which a study takes per step, so the lease
holder's call lands between a study's steps. When this is done:

- One check beside `lease_middleware`: while `study_lock` holds a study, a call
  to a `LEASE_GATED` route is refused `409` naming the study, whatever its
  token, the lease's own included.
- Admitted: `POST /study/{id}/cancel`. The prompt answer and the study's status
  reads are lease-open already and stay admitted.
- The person's setup calls between benches belong to the Test phase's route and
  are not admitted here.
- Where the call log (`tasks/core/140`) has landed, the refusal is in it like
  any refused call.

Also read `embarch-api`'s `run_study` and `run_host_study` (`src/study.rs`,
`src/host_study.rs` in that repo) and say, in the new decision, whether either
makes a lease-gated call while its run is in flight. **Read only**: if one does,
name it in this task file and your report, and the supervisor files it for
`embarch-api`.

## Why now

The owner put this rule in the HIL Live phase on 2026-11-23
(`notes/hil/05-live.md`, "Never during a run"; `notes/hil/03-test.md`, "A run",
item 4). A halted debug read disturbs the DUT the run is measuring, and the HIL
guide's Live section already says Live never runs during a run.

**Doc headroom:** decision 93 (`decisions/lease.md`) has about 70 B left.
`decisions/signing.md` decision 110 is already over its cap; leave it alone.

**Dispatched in a burndown leg (2026-11-23): no new numbered decision.** The rule
is the owner's (the HIL notes above), so record it by amending existing
decisions in place: replace decision 93's paragraph "A study in flight is not
interrupted …", which this rule overturns, with a shorter pointer, and put the
rule, its exceptions and the `embarch-api` finding in decision 95
(`decisions/host-study.md`, which has room) or decision 19's `study_lock`
(`decisions/studies.md`). Read "a Core decision records the rule" below as that
amendment. If it cannot be recorded without a new decision, stop and say so here
and in your report.

**`embarch-core/open.md` is in reserve** (4,260 of 5,120 B; out of reserve at
3,919 B or less), and its compaction `tasks/core/144` is parked until this task
lands, because Core's lease and gated-call surface was moving under it. This
task is the last of that movement, so **compact `open.md` as part of this
unit**: bring it out of reserve without dropping a fact or a decision pointer,
and keep everything 144's `Must not delete:` names (the scope-enforcement
bullets for decisions 109 to 112 and 118, the Windows ACL debt, and the call-log
`board` bullet for decision 122). Do not edit 144; the supervisor closes it at
the fold.

## Done when

- [x] A test with a study in flight walks `LEASE_GATED` and gets `409` for every
      route but `POST /study/{id}/cancel`, with the lease's own token too.
- [x] The existing dev-bench and host study tests pass.
- [x] The decision states whether `embarch-api`'s `run_study` and
      `run_host_study` make a lease-gated call while their run is in flight,
      naming any that does.
- [x] A Core decision records the rule and its exceptions.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
