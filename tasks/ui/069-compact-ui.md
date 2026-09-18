# 069 — `embarch-ui/decisions/shape.md` and `spec.md` are in reserve

**State:** open
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decision 28 (the launcher's
focus-the-existing-tab change) and its one-line `spec.md` body edit
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/decisions/shape.md, embarch-ui/spec.md
**Size debt due:** 2026-10-17

## What

`decisions/shape.md` is **12,194 / 12,288 B (99.2%), 94 B left** and `spec.md` is
**9,227 / 10,240 B (90.1%), 1,013 B left**. Both are out of reserve when this closes, or the task
says why not and what was deleted instead.

`shape.md` is the file that matters: it now carries decisions 1, 2, 3, 9 and 28, and **28 alone is
most of its mass** — the measured focus round trip, four UI Automation invariants, the strategy
registry, the page title as a load-bearing interface, and four rejected alternatives.
`DOC-COMPACTION.md` §2 prefers a **split** over a squeeze and there is a clean seam here: 1, 2 and
9 are what the project *is* (one consolidated process, zero-build, the repo), while 3 and 28 are
both about the **VS Code launcher** and cite each other — 28 extends 3's thin-launcher stance
directly. A verbatim split of 3 + 28 into `decisions/launcher.md` restates nothing.

`spec.md` is one line over the floor and wants a squeeze, not a split.

## Why now

The debt is real once a file is within one amendment of its cap, and recording it is the
mechanism (`tasks/topology/014`'s wording, same rule): an unfiled file in reserve is what
`check-doc-size.py` fails on, not the reserve itself. 94 B left means the next correction to any
of the five decisions in `shape.md` cannot land without paying first.

## In flux: no

Nothing queued against `embarch-ui` targets either file for further edits as of 2026-09-17.
Decision 28 landed with its code in the same pass, and the only work it left open is a human's
manual pass over the launcher — a verification step, not a pending prose change.

## Done when

- [ ] `decisions/shape.md` and `spec.md` are both out of reserve, or the task says why not.
- [ ] A split along the launcher seam (3 + 28) was preferred over deleting live reasoning, per
      `DOC-COMPACTION.md` §2 — or the report says why the seam was rejected.
- [ ] If it split: every inbound citation to `decisions/shape.md` still resolves, and
      `decisions.md`'s group table gained the new row.
- [ ] Decision 28's four invariants, the page-title interface and its four rejected alternatives
      survive in full — each one is a defect that was measured, not reasoned, and the title
      paragraph is what stops a later rename from silently restoring the original bug.
- [ ] Byte numbers before and after, for every file touched.
- [ ] `DOC-COMPACTION-PASS.md`'s human question answered in the report, in your own words: can
      `spec.md` alone answer what someone needs to work on the launcher today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment dropped.
