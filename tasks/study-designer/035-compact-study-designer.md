# 035 — Compact `embarch-study-designer/decisions/declares.md`

**State:** done — 2026-09-13
**Source:** `scripts/check-doc-size.py`, filed by leg 104 in the same commit that spent the
reserve (`tasks/suite/010`, decision 74). The file went 7,472 B → 11,309 B, 92.0% of cap, 979 B
left.
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/decisions/declares.md
**Size debt due:** 2026-10-13
**In flux:** no — the file holds three decisions and all three are settled. 40 and 45 have not been
edited since 2026-09-02; 74 is new, and what makes it *settled* rather than fresh is that the one
question it deliberately left open is filed elsewhere as `tasks/suite/036` rather than expected to
land here.

## What

`declares.md` is in reserve. No compaction is done here — this records the debt per
`DOC-COMPACTION.md` §2.

## The split is obvious and should be preferred over squeezing

`DOC-COMPACTION.md` §2 says split first, and a verbatim split restates nothing. This file's index
row already names two unrelated subjects — "firmware versions **and** the GATT table" — and the
seam runs exactly between its decisions:

- **Firmware versions:** 40 (what a study declares and how each version is verified) and 74 (whose
  build `firmware_version` names on each surface). 74 is a direct continuation of 40 and cites it
  repeatedly; they belong together.
- **The GATT table:** 45, which is **designed, never built** and has no code behind it at all.

Splitting 45 out — to `decisions/declared-gatt.md`, say — moves ~2.9 KB verbatim and leaves both
files well clear, with an index row each that says one thing. **Prefer that to squeezing 40**,
which is the largest single decision in this crate (4,409 B, over the per-decision cap and
currently pinned) and which the size ledger has already chosen not to shave.

## Must not delete

- Decision 40's **verification asymmetry** paragraph and its four `VersionSource` variants — it is
  the load-bearing limitation, and three other decisions and two repos cite it.
- Decision 40's "**a consequence this decision did not anticipate**" paragraph: supplying the
  flashed version is what makes the DUT requirement checkable. That is the only place the
  implementation's own discovery is written down.
- Decision 45's "**what building it would take**" paragraph and its named deferral trigger — the
  whole value of a designed-never-built decision is that someone can build it.
- Decision 74's **reversal condition** (the next wire-schema bump taken for another reason is when
  the rename becomes free) and its pointer to `tasks/suite/036`.

## Done when

- [x] `declares.md` is out of reserve. Decision 45 moved verbatim to
  `decisions/declared-gatt.md`; `declares.md` now 8,676/12,288 B (70.6%).
- [x] `decisions.md`'s index table names whatever file the split produced and the decisions in it.
  Split into two rows: `declares.md` (40, 74) and `declared-gatt.md` (45).
- [x] Gate green.

## Dispatch note (leg 105)

**Answer `DOC-COMPACTION-PASS.md`'s human question in your report, in your own words:** can
`embarch-study-designer/spec.md` alone answer what someone needs to work on this crate today?
No script answers it and the gate does not either.

**Also in reserve for `study-designer`, and both parked — do not spend either:**
`embarch-study-designer/spec.md` 9350/10240 (890 B left, `tasks/study-designer/032`, blocked)
and `embarch-study-designer/open.md` 4659/5120 (461 B left, `tasks/study-designer/026`,
blocked). A verbatim split of `declares.md` should not touch either; if the index row in
`decisions.md` grows, check `decisions.md`'s own headroom before you write it.

**Prefer the split this task already argues for.** It is verbatim, so it restates nothing and
the `In flux:` answer cannot forbid it. Squeezing decision 40 is explicitly the worse move.
