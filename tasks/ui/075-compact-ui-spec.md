# 075 — `embarch-ui/spec.md` is in reserve

**State:** done — landed 2026-09-29.
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

## In flux: no longer

`tasks/ui/070` landed 2026-09-17, before this task started — its invariants (four new ones) are
already in `spec.md`'s current text, not still incoming. Unblocked.

## Done when

- [x] `tasks/ui/070` has closed, or is confirmed not to add to `spec.md`. — landed 2026-09-17.
- [x] `spec.md` is back under 90% of cap, by squeeze or split, per `DOC-COMPACTION.md` §2's
      preference order. — squeezed 9,275 B → 9,031 B (88.2%), clear of `check-doc-size.py`'s actual
      reserve line (9,040 B = `cap - max(RESERVE_FLOOR, 10%)`). No further split seam was clean (see
      `## What` above); a squeeze cut only redundant words, no fact, invariant or clause.
- [x] `DOC-COMPACTION-PASS.md`'s human question answered in the report. — yes: `spec.md` alone still
      answers what someone needs to work on this component today. Nothing was cut but filler words
      ("also", "still", duplicated articles); every invariant, constraint and pointer survives verbatim
      in substance. Squeezed hunks: "merged action list" → "action list" (Shape diagram, filler);
      "one implementation of" → "one impl of" (Shape diagram); "the caps, the advisory" → "caps,
      advisory" (vocabulary invariant, list-formatting only); "two of the three being" → "two of three"
      (advisory-capacity invariant); no clause, name or number was dropped.
- [x] Gate green, `changelog.d/` fragment dropped. — `check-docs.py`: all 11 checks green;
      `check-ownership.py --scope ui` and `--code-repo`: OK; `check-client-names.py`: clean.
      `changelog.d/ui-075-compact-spec.changed.md` dropped.
