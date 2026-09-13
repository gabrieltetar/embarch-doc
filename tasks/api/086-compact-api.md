# 086 — `embarch-api/decisions/shape.md` is in reserve after decision 64's "Ends when" fired

**State:** open
**Source:** suite task 038 amended decision 64 in place (`embarch-umbrella` stopped scaffolding
`artifact_path_for_core`, so the first clause of that decision's "Ends when" has fired), which put
this file into its reserve band; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/shape.md
**Size debt due:** 2026-09-27
**In flux:** no — this is a decisions file, not a "what is true now" doc. Its entries are settled
records, and the one entry currently moving (64) has just been amended and is now parked on a
condition only the owner can check. The right first move is **the split**, not a rewrite: a
verbatim split restates nothing, and `DOC-BUDGET.md`'s split-first rule applies cleanly to a file
that is many independent decisions rather than one sprawling one. Run
`python3 scripts/check-doc-size.py --decisions` before choosing.

**Must not delete:**
- Decision 64's **two-clause** "Ends when" and its 2026-09-13 amendment. The whole value of that
  entry now is that the first clause has fired and the second has not, and that the second is a
  fact about real machines rather than about this suite. Collapsing it to "tolerated" loses the
  unpark condition, which is one grep.
- The **"Default for the next retired key: refuse by name"** sentence. That is the general rule the
  entry exists to establish; `artifact_path_for_core` is the exception to it, not the subject.
- The `[verified 2026-09-10]` tag and what it was verified against. A verification date on a claim
  about another repo's source is the thing that tells a later reader whether to re-check it.

## Why now

`python3 scripts/check-doc-size.py` names `embarch-api/decisions/shape.md` at 11731/12288 B
(95.5%, 557 B left) — inside the last 10% reserve band (`RESERVE_FLOOR` = 1200 B). It was already
well inside before this amendment; the amendment is what made it worth filing rather than what
caused it.

## Done when

- [ ] `embarch-api/decisions/shape.md` is back under its reserve band with every "must not delete"
      fact intact — a verbatim split along decision boundaries is the first thing to try.
- [ ] If it is split, every decision number that moves keeps its own size pin (`tasks/doc/052`
      records that a verbatim split drops those silently).
- [ ] Gate green (`../../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
