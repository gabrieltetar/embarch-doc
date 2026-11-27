# 182 — Core refuses a hardware call it cannot write to its call log

**State:** claimed by agent/core/182-core-refuses-a-hardware-call-it-cannot-log, 2026-11-26 23:53
**Source:** EMB-328 — Core serves a hardware call it cannot write to its call log
**Issue:** EMB-328
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`src/call_log.rs` writes an entry after the handler has run, and on a failed
append it logs an error and serves the answer anyway; decision 122 says the
fail-closed rule "is a later phase". No reserved tail exists. `core/181`
(decision 156) has since added Core's safe-off and the call log's `start` and
`stop` entries, which this task builds on.

The design this implements (`embarch-doc/notes/hil/12-prevention.md`, item 3):
"when the store cannot be written, Core refuses every new hardware call and
starts no new step (fail closed) and says why, but a cancel and Core's own
safe-off always run"; "a study's own teardown steps, which the agent wrote, run
only while they can be logged; when they cannot, Core runs the safe-off in
their place"; "the safe-off is logged to a reserved tail sized for every output
of the bench".

When this is done, per the issue's direction (the owner moved it to Fleet Ready
with that direction; follow it, and record any deviation in the decision):

- Core keeps a **"cannot log" state**: set when an append fails, or when free
  space in the store falls below the reserved tail; cleared by the next append
  that succeeds.
- In that state **every gated route answers `503`** naming the call log, except
  `POST /study/{id}/cancel`.
- **A study in flight starts no new step.** Its teardown steps run only while
  they can be logged; otherwise Core runs the safe-off (decision 156) in their
  place, and the record says so.
- **The reserved tail:** room for one entry per declared output's safe-off plus
  a `start` and a `stop` entry, computed from the declarations. Were it spent,
  Core still switches off and writes that it could not log to its tracing log.
- The call log stays a file of its own, so a full call log never stops the key
  or the run log being read.

**Not yours:** `embarch-topology` (its `safe_off` declarations are read, not
changed), `embarch-api`, and every other repo. You never touch hardware: every
test uses a writer seam that fails on demand and fake ports, as the existing
call-log and safe-off tests do. EMB-329 (a quota on the call log) waits on this
one and will build on the "cannot log" state, so name it plainly in the
decision.

## Where to look

- `src/call_log.rs` — `call_log_middleware` (around line 428), `record`,
  `append`; the `start`/`stop` entries from decision 156
- `src/safe_off.rs` (decision 156's `Bench` seam), `src/host_study.rs` and
  `src/study.rs` — the step and teardown loops
- `embarch-doc/embarch-core/decisions/call-log.md` (122, 156),
  `interfaces/call-log.md`; `embarch-doc/notes/hil/12-prevention.md` item 3,
  `notes/hil/14-implementation-plan.md`

## Where the doc goes

Amend decision 122 in place in `decisions/call-log.md` (7.7 KB of 12 KB), or
write a new decision there with an index row if the fail-closed rule reads
better standing alone (157 is the next free number at the time of writing; take
the next free one when you write it, by scanning the headings as
`DOC-CONVENTIONS.md` says, and cite only that number in code comments).
`interfaces/call-log.md` gives the `503` body. **Over or near the per-decision
cap, do not grow:** `signing#110`, `analog-capture#127`, `host-study#95`,
`definitions#133`, `lease#93`, `stopping-a-study#128`, `run-log#111` (120 B
left). **`open.md` is 3,917 B, 2 B under its reserve line, and `spec.md`
9,011 B, 28 B under it.** Leave both alone if you can; if your edit puts either
into reserve, file `tasks/core/<NNN>-compact-core.md` in the same commit
(`tasks/README.md` has the shape; number from
`scripts/check-task-numbers.py --next core`).

## Done when

- [ ] With a writer seam that fails on demand, every gated route answers `503`
      naming the call log, and a cancel still cancels.
- [ ] A study in flight when writes fail starts no new step; its teardown is
      replaced by the safe-off, and the record says so.
- [ ] With free space below the reserved tail, the same refusal, and the
      safe-off's entries still land.
- [ ] After the writer recovers, the next call is served and logged.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`).
- [ ] Decision 122 amended (or a new decision written); `interfaces/call-log.md`
      gives the refusal; `changelog.d/` fragment.
