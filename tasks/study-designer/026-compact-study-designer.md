# 026 — Compact `embarch-study-designer/open.md`

**State:** open
**Source:** the surviving half of `tasks/study-designer/006-compact-study-designer.md`, closed
`done` by leg 064 on 2026-09-10 once its `spec.md` item was paid. Filed as a fresh task rather
than left on 006's `Compacts:` line, because `fold-commit.py` (correctly) refuses to fold a unit
whose own task file still reads `open`, and 006's remaining file is a real debt that must keep a
clock rather than be closed with it.
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/open.md
**Size debt due:** 2026-10-04

*The date is carried over unchanged from 006 — this is the same debt with a new file number, not a
new deferral, and re-dating it would be a park with extra steps.*

## In flux: no

**Leg 064's supervisor asserted this, against its own worker's read, and the reasoning belongs
here rather than only in the log.** 006's worker wanted to leave the task `blocked` on the grounds
that `open.md` is "still in flux". An open-questions file is edited every week in every
sub-project, so "in flux" applied to one is a property of the filename rather than a fact about a
subsystem settling down — and accepting it parks the debt permanently. It is also the wrong test
for the work available: the compaction move for an `open.md` is **striking questions that have
since been answered**, which restates nothing, and which no amount of flux forbids
([DOC-BUDGET.md](../../DOC-BUDGET.md)'s own wording for a 5 KB `open.md` role cap says the same).
If the owner disagrees, this is his call to make in his files, not a leg's.

## What

`embarch-study-designer/open.md` is **4,662 / 5,120 B — 458 B left**, inside the reserve floor. It
has been in reserve since `study-designer/008` tombstoned decision 45 there on 2026-09-08, and
`study-designer/019` left it untouched.

## Why now

It is the last file on 006's ledger entry, it has a clock, and it is the file every new open
question in this sub-project lands in — so it is the one place in `embarch-study-designer` where
the cap will refuse an edit that is *not* about the cap.

## Done when

- [ ] `embarch-study-designer/open.md` is out of reserve (`scripts/check-doc-size.py` clean), or
      this task says in its own words why it cannot be.
- [ ] Whichever it was is stated with the byte numbers before and after.
- [ ] **Every question deleted was actually answered**, with the decision number or task that
      answered it named in the same edit. A live question shortened to fit is the failure this
      task exists to avoid; a question whose answer nothing records is *not* answered.
- [ ] `DOC-COMPACTION-PASS.md`'s human question answered in the worker's own words.
- [ ] Gate green ([protocol](../../../embarch-fleet/protocol.md) §10); `changelog.d/study-designer-*`
      fragment.
