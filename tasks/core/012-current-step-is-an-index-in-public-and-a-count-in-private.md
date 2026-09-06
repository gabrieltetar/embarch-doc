# 012 — `current_step` is a 0-based index on the API and a count internally, set two lines apart

**State:** claimed by leg 023, 2026-09-06 — `agent/core/012-current-step-semantics`
**Source:** observed live by the supervisor running `tasks/api/029`'s study, 2026-09-06
**Scope:** core
**Hardware:** none
**Owner:** no

## Doc-size reserve for `core` (supervisor, leg 023)

**No `embarch-core` doc is in reserve** — `spec.md`, `interfaces.md` and every
`decisions/` file have room, and `core/011` paid `open.md` down last leg. Write
where the content belongs.

**One suite-level file is at a hard wall and it is not yours to fix:**
`suite/features.md` is at **20,259 / 20,480 B — 221 bytes left**, and its
compaction task `suite/004` is `blocked` on the owner (an assembled file no agent
may write). **So do not write a `features.d/` fragment for this unit unless the
change genuinely ships a new user-visible capability** — a documented meaning for
an existing field is a `changelog.d/` entry, not a feature row. If you conclude a
feature row is genuinely owed, say so in your report and let the supervisor
assemble it; do not pad it.

Standing rule either way: if your work pushes an `embarch-core` doc into its last
10%, file `tasks/core/<NNN>-compact-core.md` in the same commit
(`tasks/README.md` has the shape).

## What was observed

A **completed** two-step study reported, verbatim from `GET /study/{id}`:

```json
{ "current_step": 1, "status": "completed", "total_steps": 2 }
```

with both steps' `outcome` reading `Pass`. So a caller rendering the obvious
"step `current_step` of `total_steps`" shows **"1 of 2" on a run where both steps
finished** — the progress display is permanently one short, and it is one short
*at the moment it matters*, when the run is done.

**This is a real observation, not a source read**: study
`3785bd198cc3a62dccd1780fd552e988`, the two-step `BleAdvertise` self-test, run
against the live bench with `reflash` at its `none` default.

## Where it comes from

`embarch-core/src/study.rs`, in the step-completion block, **on adjacent lines**:

```rust
next_expected = step_index as usize + 1;
capture.current_step.store(next_expected as u32, Ordering::Relaxed);
update_job(&jobs, &study_id, |job| job.current_step = Some(step_index));
```

Two counters with the same name and different conventions. The **capture's**
`current_step` is a count of steps finished and is what the tap machinery uses
to scope a stream to a step range — that one is right for its job and must not
move. The **job's** `current_step`, the one that reaches the API and every
client through it, is the 0-based index of the last step that finished.

Neither convention is wrong on its own. What is wrong is that they share a name,
sit two lines apart, and only one of them is public.

## Why nothing caught it

`embarch-core/interfaces.md`'s `GET /study/{id}` row lists `current_step?` **with
no semantics at all** — not "steps completed", not "index of the current step".
There is nothing for a test or a reader to disagree with, so both conventions
satisfy the documented contract and a client picks whichever it guesses.

## Done when

- [ ] The public `current_step` has one stated meaning, written into
      `embarch-core/interfaces.md`'s row rather than left to the reader.
- [ ] Whichever convention is chosen, a completed study and a running one are
      both checked against it — the off-by-one is invisible mid-run and only
      shows at completion.
- [ ] The internal capture counter is either renamed or commented so the next
      reader of that block does not have to re-derive which is which.
- [ ] Decide explicitly whether changing the public field is a breaking change
      for `embarch-ui` and the shared Core client, and say so; if it is,
      **document the current meaning instead of changing it** — this is a
      progress indicator, not a correctness property.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
