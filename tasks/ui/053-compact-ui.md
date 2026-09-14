# 053 — Compact `embarch-ui/open.md` back out of reserve

**State:** open
**Source:** leg 112's `ui/051` fold, 2026-09-13. A reviewer finding on `ui/051` required restoring a
record that half of suite decision 4's move is still outstanding; I wrote that bullet into
`embarch-ui/open.md` in the fold, and it put the file back in reserve at **4,033 / 5,120 B**, 113 B
over the 3,920 B line. **`ui/050` had compacted this same file out of reserve four units earlier**,
which is the uncomfortable part and is addressed below.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`embarch-ui/open.md` is **4,033 / 5,120 B with 1,087 B left**; the reserve floor for a 5,120 B cap is
**1,200 B**. Get it to **3,920 B or less** — 113 bytes.

**Compacts:** embarch-ui/open.md
**Size debt due:** 2026-09-20
**In flux:** no — every question in the file is a standing unresolved item, and the newest of them
(the trace-analysis split) is *more* settled than it was this morning, not less: what moved and what
did not is now a fact rather than a plan.
**Must not delete:**
- **The trace-analysis bullet's three load-bearing facts**, in whatever form: that the aggregation
  moved and the span/gap classification did not; that `Lane`/`Span`/`Gap` and the four exclusion
  flags are derived in **both** `embarch-ui/src/trace.rs` and `embarch-core/src/outpost_load.rs`; and
  that closing it needs per-span data from Core or a recorded decision that it stays split. **This
  bullet exists because a reviewer caught its predecessor being deleted** — reducing it to a bare
  citation re-creates exactly the gap `ui/051` was corrected for.
- **Every other bullet's own trigger and decision citation**, per `ui/050`'s own must-not-delete
  list: the seven open questions in this file were squeezed once already and each kept its trigger
  deliberately.

## Why this is not simply `ui/050` being undone

**`ui/050` squeezed; it did not create headroom for new content, and there was none to create.** Its
own entry records the file landing at 3,841 B — **78 B clear of the line**, described there as
"further out than the file was before `suite/018` pushed it in". A 78-byte margin cannot absorb a new
open question, and this repo acquired one the same day.

**So the honest reading is that `open.md`'s 5,120 B cap is tight for the number of live questions
`embarch-ui` carries, and the next pass should consider a split rather than a third squeeze.**
`DOC-COMPACTION.md` §2 prefers a split where one fits, and `DOC-BUDGET.md`'s split-first rule applies:
a verbatim split restates nothing. `ui/050` explicitly judged there was no seam — the file "holds one
kind of thing" — and that judgement was right for a squeeze-or-split question asked about seven
questions of the same shape. **Ask it again with the trace bullet in hand**: the trace/outpost
questions (this one, the placement-against-a-second-stream one, the row-cap one) may now be a seam
the file did not have this morning. If they are not, squeeze 113 bytes and say so.

## Done when

- [ ] `python3 scripts/check-doc-size.py` exits 0 with `embarch-ui/open.md` no longer listed — **that
      check, not an arithmetic target of your own** (`tasks/doc/058` is why: the reserve line is
      `max(1200 B, 10% of cap)`, and for a 5,120 B cap the floor wins).
- [ ] Nothing on the `Must not delete:` list above is gone or reduced to a bare citation.
- [ ] **The split-vs-squeeze question above answered explicitly in the commit message**, either way.
- [ ] The compactor answers `DOC-COMPACTION-PASS.md`'s question: can `open.md` alone tell someone what
      is unresolved in `embarch-ui` today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
