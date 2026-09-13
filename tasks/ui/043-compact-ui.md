# 043 — `embarch-ui/decisions/trace-view.md` is in reserve

**State:** claimed
**Source:** `scripts/check-doc-size.py`'s reserve floor, hit by `tasks/ui/042`'s fix to decision
10's marker-count sentence
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/decisions/trace-view.md
**Size debt due:** 2026-10-13

## Dispatch note (supervisor, leg 107)

**This is a compaction unit and it is judged differently from every other kind.** Answer
`DOC-COMPACTION-PASS.md`'s human question in your report, in your own words: *can `spec.md` alone
answer what someone needs to work on the trace view today?* No script answers it and the gate does
not either, so a report that only gives byte counts has not finished the task.

**`In flux: no` is already established per file** and this task names exactly one file, so the
split-first rule applies with nothing parking it. `DOC-COMPACTION.md` §2 prefers a **split** over
squeezing, and the task already identifies the seam (decision 10's three sub-arguments vs.
decisions 19 and 21). **A verbatim split restates nothing**, so prefer it; if you split, say which
new file was created and confirm every inbound citation to `decisions/trace-view.md` still
resolves — a decision link surviving a mission split and pointing at the wrong file is a defect
this suite has already paid for (`tasks/doc/022`).

**`embarch-ui/decisions/trace-view.md` is the only `embarch-ui` file in reserve** — 11093/12288 B,
1195 B left, 90.3%. Note the standing, unrelated `embarch-ui` debt: the 18-record stale prefix has
never met a real stale prefix (`tasks/ui/007`, blocked). Decision 19 is the stale-prefix decision;
**do not delete the reasoning that debt is waiting on** while shortening it.

**Report the byte numbers before and after**, for every file you touched — that is what closes the
ledger entry, and `check-doc-size.py` is what the fold will re-run.

## What

`decisions/trace-view.md` is **11,093 / 12,288 B (90.3%), 1,195 B left**. `ui/042` corrected a
stale marker count in decision 10 (132 → naming the fixture it was true of, since regenerated to
155) and did not shorten anything to pay for the added clause, so the file crossed the reserve
floor on that edit.

**Prefer a split** (`DOC-COMPACTION.md` §2) before squeezing. This file already carries three
decisions (10, 19, 21) at very different granularity — decision 10 alone is most of the file's
mass and is itself three sub-arguments (post-hoc rendering and the two-boolean model; the
gap-band/clock-tier axis choice; the load-repartition and idle-double-count reasoning) that a
future split could separate from 19/21 (the stale-prefix drop, the row-cap literal) without
restating anything.

## Why now

The debt is real once a file is within one amendment of its cap, and recording it is the
mechanism (`tasks/topology/014`'s wording, same rule): an unfiled file in reserve is what
`check-doc-size.py` fails on, not the reserve itself.

## In flux: no

Nothing queued against `embarch-ui` as of 2026-09-13 targets this file for further edits.
`tasks/ui/015` (the unknown-outcome-band hatch reuse, also against decision 10) is `done`.
`embarch-ui/open.md` carries live open questions this file's clock/placement claims bear on
(the unmeasured dual-clock-vs-second-stream comparison, the unmeasured 250,000-row cap at
Core-scale) but none of them is a queued edit to `trace-view.md` itself — they are open
measurements, not pending prose changes.

## Done when

- [ ] `decisions/trace-view.md` is out of reserve, or the task says why it cannot be and what
      was deleted instead.
- [ ] Prefer a split per `DOC-COMPACTION.md` §2 if a seam exists (decision 10's three
      sub-arguments vs. decisions 19/21) before deleting live reasoning.
- [ ] Whichever it was — split or delete — is stated, with the byte numbers before and after.
