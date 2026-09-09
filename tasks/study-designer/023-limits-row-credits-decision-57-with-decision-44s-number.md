# study-designer — `MAX_DISCOVERED_SERVICES` row attributes decision 44's finding to decision 57

**State:** done — leg 050, 2026-09-08
**Promoted** from `inbox/study-designer-022-decision-57-cited-for-a-number-it-does-not-state.md`
by leg 048, unchanged apart from this line and the number. The supervisor read the same row at the
merge, asked the reviewer four questions about it, and did **not** see this one — the reviewer did.
**Source:** `embarch-reviewer` on `study-designer/022` (code merge `c58f592`, doc merge `4ff55eb`)
**Scope:** study-designer
**Hardware:** none — this is a citation-accuracy finding; confirming it needs no hardware

## What

`embarch-study-designer/interfaces/limits.md`'s `MAX_DISCOVERED_SERVICES` row, as
landed in `4ff55eb` (`embarch-study-designer/interfaces/limits.md` line 28), reads:

> decision 57's validated GATT table: `reference-dut-fw` declares 3 services, 7
> in total once an encrypted link reaches the rest (same DUT as
> `MAX_MONITOR_TARGETS` below), transcribed from `src/limits.rs:80-84`...

The whole clause is attributed to **decision 57**
(`embarch-study-designer/decisions/gatt-extract.md`), but decision 57's own text
validates only the 3-declared figure: *"Validated against the real checkout:
three services where a bounded read found two, every characteristic named."*
Decision 57 (a static, source-extraction decision, explicitly `std`-only,
"never something dev-bench or Core links") says nothing about a 7-service total
or an encrypted link.

The "7 total once an encrypted link reaches the rest" figure is decision **44**'s
(`embarch-study-designer/decisions/ble.md`, `Action::BleSecurity`), whose own
validated-on-hardware note reads: *"connect passed, elevation passed reporting
the level asked for, then discovery returned 7 services... Discovery of that
table had never once succeeded before this pass."* That is a live-discovery
result behind an encrypted link — a different decision, a different mechanism
(live BLE discovery, not the static extractor decision 57 governs), reached
independently and already carried, uncredited to 57, in the neighboring
`MAX_MONITOR_TARGETS` row.

## Why this is a contradiction rather than a refinement

The row does not just borrow a true number from elsewhere — it asserts that
number as part of "decision 57's validated GATT table," which is false: decision
57 never validated a 7-total or an encrypted-link figure. This is the same
failure shape decision 57 itself exists to fix (a stale/incorrect provenance
claim standing as fact in a doc), reintroduced one hop later: a reader who
checks `gatt-extract.md` decision 57 to confirm the "7" will not find it there,
and may reasonably conclude decision 57 was edited or is being mis-cited
elsewhere too.

## What it would take to undo

Merge SHA `4ff55eb` (`embarch-doc`). A plain revert of this hunk is clean — it
only touches this one row — but reverting would restore the *prior* problem
(the stale "2 services" count decision 57 was filed to retire), so the right
fix is forward: split the row's sourcing into two clauses, crediting decision 57
for "3 declared" and decision 44 (or the existing `MAX_MONITOR_TARGETS` note) for
"7 total once an encrypted link reaches the rest," rather than folding both
under one citation.

## Not filed as findings (checked, no action needed)

- The header ("Every bound the crate declares, each marked `[measured <date>]`
  or `[assumed]`") now reads as mildly self-contradicted by this row carrying
  neither bracket — but this is an internal wording inconsistency in one file's
  own prose, not a contradiction of a locked decision, and the task file
  (`tasks/study-designer/022-...md`) already records the deliberate reasoning
  (no third `DOC-CONVENTIONS.md` bracket invented, flagged instead). Leaving
  this to the follow-up already planned.
- `src/limits.rs`'s untouched `design.md §3 decisions 31/32, §4.3a` citation
  (line 80-81, unchanged by this diff) is stale — `design.md` was split
  2026-09-04 — but this is pre-existing and already tracked, not introduced by
  this unit: `tasks/study-designer/018-design-md-citations-repo-wide-sweep.md`
  (state: open) explicitly lists `limits.rs` among the 23 files carrying this
  exact defect class (35 occurrences), filed before this unit landed.

## Done

Verified against the sources rather than trusting this file's own reading:
decision 57 (`decisions/gatt-extract.md`) validates only "three services where
a bounded read found two" — a static-extraction result, `std`-only, no live
link involved. Decision 44 (`decisions/ble.md`, `Action::BleSecurity`)'s
"[Validated on hardware 2026-08-26]" note is the one stating "discovery
returned 7 services" behind an elevated (encrypted) link. The task file's
reading was correct.

`interfaces/limits.md`'s `MAX_DISCOVERED_SERVICES` row now credits "3
declared" to decision 57 (transcribed from `src/limits.rs:80-84`) and "7 in
total once an encrypted link reaches the rest" to decision 44's
validated-on-hardware discovery, as two clauses under one row rather than one
citation covering both. No other line touched. `check-docs.py`: all 10 checks
green. `interfaces/limits.md` is 10,334 B, not in reserve, no size debt to
file. No `changelog.d/` fragment filed — this is a citation-accuracy
correction to an existing row's prose, not a capability change or anything a
changelog reader would need to know about.
