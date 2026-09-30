# doc/087 — `Must not delete:` lists protect findings but not their citations

**State:** open
**Source:** `tasks/core/089`, 2026-09-29. Compacting `embarch-core/decisions/surfaces.md`
under `tasks/core/079`'s `Must not delete:` list (itself carried forward by
`core/078`'s ride-along compaction) preserved every protected finding in decision
59 but dropped four evidence citations behind two of them — a symbol name, a file
path, a confirmation-trail sentence, and a grep receipt. None of the four
survived anywhere permanent; three were recovered only by re-deriving them from
`core/074`/`077`'s task files, which are `done` and slated for removal. `core/086`
found the same failure shape one notch worse (a squeeze taking named identifiers
out of the corpus entirely) in the leg before this one.
**Scope:** doc
**Hardware:** none
**Owner:** required — `DOC-COMPACTION-PASS.md` is owner-reserved (check-ownership.py --supervisor refuses it).

## What

A `Must not delete:` list, as currently written in a compaction task, names the
*findings* a compaction pass must keep intact, but says nothing about the
*evidence* behind them — a cited symbol, file path, or "confirmed by reading X's
Y" sentence that lets a later reader re-establish the claim without re-reading
the whole source. A squeeze pass reads "shorten without losing the finding" and
correctly keeps the conclusion while dropping the receipt, because nothing told
it the receipt was also protected.

## Why now

This is a second, independent instance of the `core/086` shape (`core/089`'s own
task file calls it "one notch milder"), which is enough to call it a pattern in
how `Must not delete:` lists get written, not a one-off compaction mistake.
`DOC-COMPACTION-PASS.md` is owner-reserved, so the fix — whatever form it takes
(a required second field, a convention note, a checklist item) — belongs there,
not in any one sub-project's task.

## Done when

- [ ] `DOC-COMPACTION-PASS.md` (or whichever doc owns compaction-task authoring)
      says explicitly that a `Must not delete:` list should name citations
      (symbols, paths, "confirmed by" sentences) behind a protected finding, not
      just the finding's conclusion — or explains why that is deliberately left
      to author judgment instead.
- [ ] Gate green.
