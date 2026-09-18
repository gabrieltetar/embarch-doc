# 117 — `embarch-api/decisions.md`'s index omits decision 72, and one size cell is 70% low

**State:** claimed by agent/api/117-decisions-index-census, 2026-09-17 18:57
**Source:** leg 144's refill sweep, 2026-09-17 — a mechanical check of every sub-project's
`decisions.md` index against the decision numbers and file sizes actually on disk.
**Scope:** api
**Hardware:** none — one markdown table.
**Owner:** no

## What

Two defects in the same table, `embarch-api/decisions.md`:

1. **Decision 72 is in no row.** `embarch-api/decisions/client-crate.md:54` carries
   `### 72 — The seven mirrored embarch-topology types are retired; the tests that pinned them are
   kept and re-scoped` (landed in `suite/035`'s fold, 2026-09-12). The index's client-crate row
   (line 26) lists `36, 37, 38, 55, 58, 62, 66` — no 72 — and no other row claims it. A reader
   walking the index has no route to the decision that retired seven mirrored types.

2. **The `decisions/logging.md` row's size cell reads `1.6 KB` and the file is 2,724 B (2.7 KB).**
   That is not a rounding difference; it is off by ~70%, which means the cell was written once and
   never re-measured. A stale size column is worse than none: `check-doc-size.py` reads the real
   files, so a reader planning a compaction off this table plans against a file that does not exist.

**Re-derive every coordinate above — line numbers, the decision number, both byte counts — before
editing. "This does not hold" is a correct outcome to report.**

## Why now

Both are cheap, both are in one file, and the size column is the kind of defect that gets *worse*
silently: nothing measures it, so the only thing that ever corrects a cell is somebody happening to
look.

## Done when

- [ ] The client-crate row's *Decisions* cell lists 72 in its existing convention, and that row's
      description names what 72 settles if the cell's phrasing has room for it — do not stretch the
      row into a paragraph.
- [ ] `decisions/logging.md`'s size cell is corrected to the measured value.
- [ ] **Re-verify all 21 size rows and every decision number in the table while you are there**, and
      report the tally in your status fragment: how many rows were right, how many you corrected,
      and how many decisions present on disk were missing from the index. A row that is already right
      is a result worth stating — the point of the census is the rate, not just the fixes.
- [ ] Pick one spelling convention for sizes and apply it to every cell you touch (the table
      currently mixes precisions); say which you chose and why in one sentence.
- [ ] A `changelog.d/` fragment if you judge any of it reader-facing. An index repair usually is not;
      saying so plainly is a fine answer.
- [ ] Gate green per `../../embarch-fleet/protocol.md` §10.

## Not yours

- **Do not amend decision 72, or any decision's text.** This is the index.
- **Do not compact anything.** If a size you measure pushes a file into its 90% reserve and nothing
  has filed for it, file `tasks/api/<NNN>-compact-api.md` per `tasks/README.md` in the same commit —
  recording the debt, not paying it.
- **Do not renumber anything.**
