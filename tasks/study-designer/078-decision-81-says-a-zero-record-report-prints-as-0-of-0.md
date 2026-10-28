# 078 — Decision 81 says a zero-record report prints as "0 of 0", and its two consumers now say "no records found"

**State:** claimed by agent/study-designer/078-decision-81-zero-record-wording, 2026-10-28 13:28
**Dispatch note, 2026-10-28 leg — reserve in `embarch-study-designer`:** `open.md` 647 B left, parked under `tasks/study-designer/026` (`blocked`, overdue since 2026-10-04). This task should not touch it; if it does, compact `open.md` in this unit carrying `026`'s `Must not delete:` list. `decisions/seals.md` (6,955 B) has room.
**Source:** `api/141`'s reviewer, 2026-10-26 (below its bar; filed by the supervisor so it is not lost when the log folds).
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-study-designer/decisions/seals.md`, decision 81's **Record check** paragraph, ends: *"A `Some`
report with `total 0` now prints as "0 of 0", not "all verified"."* Since then Core's log text says "no
records found" (`embarch-core` decision 86, `core/109`) and so does the `embarch-api` CLI
(`embarch-api@9e8d8bd`, `api/141`: `record_summary` in `src/cli.rs`). Find what, if anything, in this
crate still prints "0 of 0" (a `Display` impl, a doc comment, a test name). If nothing does, the sentence
describes consumers, not the crate: reword it to say what the crate guarantees (`all_verified()` is false
at `total == 0`) and point at core 86 for the wording, as an amendment line rather than a rewrite of the
history. If the crate does print it, say which and leave the decision true.

## Done when

- [ ] Decision 81 no longer states a print the suite does not make, or a note says which crate path still makes it.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
