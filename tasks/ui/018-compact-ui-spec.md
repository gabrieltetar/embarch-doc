# 018 — `embarch-ui/spec.md` is in reserve

**State:** done — leg 059, 2026-09-09, burndown
**Source:** `scripts/check-doc-size.py`'s reserve floor, added 2026-09-07
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/spec.md
**Size debt due:** 2026-10-12

## Supervisor note — leg 059, doc-size reserve in `ui`

**Current numbers, which are worse than the body below records:** `spec.md` is
**9613/10240 B, 627 B left** (the body says 1,027 B — that reading is two days old).
`embarch-ui/open.md` is also in reserve at **4191/5120, 929 B left**, filed under
`tasks/ui/021-compact-ui.md`, which is **blocked** — leave `open.md` alone unless this unit has to
write there, in which case compact it too, carrying `021`'s `Must not delete:` list.

**Answer the human question in your report, in your own words** —
`DOC-COMPACTION-PASS.md`: *can `spec.md` alone answer what someone needs to work on this
component today?* No script answers it and the gate does not either. **This leg runs in burndown,
which forbids authoring a new numbered decision**; a compaction pass should not need one.

## What

`spec.md` is **9,213 / 10,240 B (90.0%), 1,027 B left** — the tightest of the
five sub-project `spec.md` files, and it crossed on the rule change rather than
on an edit: reserve was 90% of a limit, and reserve is now
`max(1200 B, 10%)` from the top so that a file is warned while it still has a
seam to cut rather than 22 bytes before the wall.

**Prefer a split.** [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split
restates nothing, so it costs no argument. A `spec.md` splits by surface — the
way `embarch-umbrella` split `decisions/projects.md` into `integration.md` and
`embarch-api` split `decisions.md` by mission — and the seam has to be checked
for inbound links before it is cut, which is the step
`tasks/umbrella/022` records getting right and nearly getting wrong.

Run `scripts/check-duplication.py embarch-ui` first: a `spec.md` in reserve
next to a `decisions/` directory in reserve usually means one of them is
re-arguing what the other owns, and deleting a duplicate is cheaper than either
a split or a squeeze.

## Why now

The debt is real once a file is within one amendment of its cap, and recording
it is the whole mechanism: an unfiled file in reserve is what
`check-doc-size.py` fails on, not the reserve itself. Two other `ui` size debts are
already open — `011` on `decisions/study-designer.md` at 224 B left, and `016`
on `decisions/trace-chart.md`, filed by a leg in the same hour as this one — so
a `ui` worker should read all three before choosing where to spend a unit.

## In flux: no

Nothing in `spec.md` is mid-argument as of 2026-09-07. `ui/015` is open against
the trace view's rendering, not the spec.

## Done when

- [x] `spec.md` is out of reserve, or the task says why it cannot be and what
      was done instead.
- [x] Whichever it was — split, delete a duplicate, or squeeze — is stated,
      with the byte numbers before and after, and the seam's inbound links
      named if it was a split.

## Resolution — 2026-09-09

**Split, not squeeze or dedup.** `check-duplication.py embarch-ui` first: the 12
overlaps it found were all the expected shape (a spec invariant a decision
explains), not a genuine two-copies-of-one-claim error — nothing to delete.

Moved the whole **"The trace chart"** section out of `spec.md` into a new
`embarch-ui/interfaces.md` (`DOC-COMPACTION.md` §3: endpoints/constants
reference that doesn't fit `spec.md`), leaving one paragraph behind stating
the two load-bearing invariants (bounded element count; filtering doesn't
touch the load repartition) and a pointer. Checked for inbound links to that
section first (`grep` across the repo for `the-trace-chart` and for
`embarch-ui/spec.md`) — none anchor into it, only whole-file references, so
nothing else needed fixing.

`spec.md`: **9,613 B → 8,354 B** (81.6%, was 93.9%/reserve). `interfaces.md`
(new): **1,915 B**. One duplicate sentence the split itself introduced
(the "filtering changes the drawing" clause landed in both files) was caught
by a second `check-duplication.py` run and removed from `spec.md`'s pointer
paragraph, keeping the full statement only in `interfaces.md`.

`embarch-ui/open.md` (929 B left, filed under `021`, blocked) was not touched —
this unit did not need to write there.

**Human question (`DOC-COMPACTION-PASS.md`):** yes, `spec.md` alone answers
what someone needs to work on this component today. What moved was reference
detail — exact row/lane counts, the bin-fetch endpoint shape, the two cap
constant names — that a reader needs only when touching the trace view
specifically, not to orient on the six tabs, the shape, the invariants, or the
design system, all of which stayed put untouched. `spec.md`'s own invariants
paragraph for the trace chart (bounded element count, filtering vs. load
repartition) survived the split intact, so a reader scanning `spec.md` top to
bottom still gets the one fact that would cause a wrong move (redrawing the
whole capture client-side) without following the pointer; the pointer exists
for the exact numbers and wire shape, which nobody needs to *change* this
component without first opening `interfaces.md` anyway.
