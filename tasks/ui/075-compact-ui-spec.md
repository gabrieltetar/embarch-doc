# 075 — `embarch-ui/spec.md` is in reserve

**State:** claimed by agent/ui/075-compact-ui-spec, 2026-09-29 21:31
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by this task's own tab-table
split (`tasks/ui/069`): the split itself paid down 1,747 B, but that only bought `spec.md` back
to 90.6% of cap — still inside the reserve band — because the file had drifted 971 B over cap
before this pass started.
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/spec.md
**Size debt due:** 2026-10-20

## What

`spec.md` is **9,275 / 10,240 B (90.6%), 965 B left.** `tasks/ui/069` split the five-tab table
verbatim into `spec/tabs.md` (2,435 B) in the same pass, which is what brought this file back
under cap at all — but it started that pass 971 B *over*, so the margin bought is thin.

The remaining content is `## What it is`, `## Shape`, the two paragraphs under `## The five tabs`
(the fragment-navigation rule; the table itself is gone), `## Invariants` (the largest section —
roughly 20 one-line invariants) and `## Verification technique`. No further split seam was
obviously clean at the time of `069`'s pass: the invariants section is dense but each line is a
distinct, load-bearing fact rather than a set that groups by topic the way the tab table or the
capture-rendering facts did.

## Why now

94–965 B of headroom on a file that has needed two compactions in the last six weeks (`069`
itself, and the split-to-`capture-rendering.md` before it) is not a comfortable margin: the next
decision that touches Topology or Study Designer invariants is likely to cross the cap again.
Recording it now rather than waiting for `check-doc-size.py` to go fully red.

## In flux: yes

`tasks/ui/070` (the Study Designer authors-everything-a-study-carries work) is open against this
same sub-project and is exactly the kind of change that adds invariants to `spec.md`. This task is
**blocked** until `070` closes or is confirmed not to touch `spec.md`'s invariants list — compacting
mid-flux risks writing a clean statement of something about to change (`DOC-COMPACTION-PASS.md`
failure modes).

## Done when

- [ ] `tasks/ui/070` has closed, or is confirmed not to add to `spec.md`.
- [ ] `spec.md` is back under 90% of cap, by squeeze or split, per `DOC-COMPACTION.md` §2's
      preference order.
- [ ] `DOC-COMPACTION-PASS.md`'s human question answered in the report.
- [ ] Gate green, `changelog.d/` fragment dropped.
