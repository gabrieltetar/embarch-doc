# 066 — `decisions.md` says "these seventeen files" and there are nineteen

**State:** claimed by agent/study-designer/066-decisions-md-no-count, 2026-09-29 21:23 — was open — **the number is right again, the defect is not gone.** `study-designer/068`
(2026-09-28) split `decisions/builds.md` out and corrected the sentence to "these twenty files",
which matches the directory. What is left is this task's own preference: rephrase so no count can
go stale, plus the table census. The next split makes "twenty" wrong exactly as it made seventeen
wrong.
**Source:** leg 144's refill sweep, 2026-09-17.
**Scope:** study-designer
**Hardware:** none — one word in one markdown file.
**Owner:** no

## What

`embarch-study-designer/decisions.md:7` reads:

> … which is what let them move from `design.md` §3 to one `decisions.md` and then into **these
> seventeen files** without touching one of the references pointing at them.

`ls embarch-study-designer/decisions/` returns **19**. The count was correct when `registry.md` made
it 17; `ci.md` and `declared-gatt.md` were added afterwards and nothing re-counted.

**Re-derive it**: count the files yourself, and check whether every one of them is a decisions file
the sentence means to include (a README or an index in that directory would change the answer).

## Why now

It is a word, and it is the second time a hardcoded count in this suite has gone stale by exactly the
mechanism that makes counts stale — someone adds a file. Worth doing as a ride-along, not worth a
leg's attention on its own.

## Done when

- [x] The count is correct, **or** the sentence is rephrased so it cannot go stale again (e.g.
      "into the files under `decisions/`"). **Prefer the rephrase** and say why in one sentence: a
      number that no check reads will drift again, and this sentence is about permanence of
      *identifiers*, not about how many files there happen to be.
      Rephrased to "into the files under `decisions/`" — done, since the next split makes any
      number wrong again the same way it made seventeen and twenty wrong.
- [x] While you are in `decisions.md`, check the group table the same way: every decision number
      present in `decisions/*.md` appears in exactly one row, and every number a row claims exists.
      Report the tally either way — a clean result is a useful one.
      Clean: 78 decision numbers total (headers `### N` across `decisions/*.md`), no duplicates
      either in the files or in the table, and the two sets are identical — every number a file
      declares appears in exactly one table row and every number a row claims exists as a file
      header. The table itself also has 20 rows for 20 files, matching 1:1.
- [x] No `changelog.d/` fragment unless the table census turns up something reader-facing; a
      corrected count is not. — census was clean, no fragment filed.
- [x] Gate green per `../../embarch-fleet/protocol.md` §10.

## Not yours

- **Do not amend any decision's text**, and do not renumber anything.
- **`embarch-study-designer/spec.md` (91.3%) and `open.md` (91.0%) are both in the size reserve** and
  already filed against blocked `study-designer/032` and `study-designer/026`. Do not edit either,
  and do not file a new compaction task for them.
