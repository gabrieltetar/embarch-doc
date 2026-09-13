# 038 — Split `embarch-study-designer/interfaces/types.md`'s Results section into its own interface file

**State:** claimed — leg 108, 2026-09-13, dispatched to `agent/study-designer/038-split-result-types`
**Source:** supervisor, leg 108, 2026-09-13 — filed against the size-reserve debt parked in
`tasks/study-designer/037`, which is `blocked` on `In flux: yes` and stays blocked. See "Why this is
not that task" below.
**Scope:** study-designer
**Hardware:** none — documentation only. No board, no build, no wire change.
**Owner:** no

## What

`embarch-study-designer/interfaces/types.md` is **11,251 / 12,288 B (91.6%)** — inside the last 10%
of its cap and therefore in reserve. Its four top-level sections are `Study`, `Step`, `Action` and
`Results`.

Move the whole **`Results`** section (line 65 to end of file, 2,434 B), **verbatim**, into a new
`embarch-study-designer/interfaces/result-types.md`, and leave a one-line cross-reference where it
was.

**`Results` is the right seam, and `Action` is not.** `Study` / `Step` / `Action` are the authoring
half — what an engineer writes down before a run — and they nest: a `Study` holds `Step`s and a
`Step` holds an `Action`. `Results` is the other direction entirely: what comes back off the wire
after the run. Splitting `Action` out would cut through the nesting; splitting `Results` out cuts
along it.

`DOC-BUDGET.md` line 25 already covers the new file: `<sub-project>/interfaces/<topic>.md` at 12 KB.
No budget entry needs adding, and no owner-reserved file is touched. The move takes `types.md` to
roughly **8,850 B**, out of reserve with about 2,200 B of headroom.

## Why this is not `tasks/study-designer/037`, and why `In flux: yes` does not forbid it

`037` parks a **compaction pass** — a squeeze that rewrites prose — on the grounds that this file
enumerates every wire/host type's field list and has taken edits from three of the last seven merged
units in this scope (031, 035, 036), so another field arriving is plausible. That reasoning is
correct and it stays correct.

**It does not apply to a verbatim split**, because a split restates nothing: every byte that moves
arrives byte-identical, so there is no way for it to encode a field list that is about to become
wrong. `DOC-COMPACTION.md` §2 names a mission split as the cheaper move where one fits,
`DOC-BUDGET.md` line 47 says outright that a parked compaction task is a deferral and not a wall,
and `tasks/ui/043` demonstrated the argument end to end on 2026-09-13.

So `037` is left exactly as it is, `blocked`, with its `Size debt due: 2026-09-27`. If this task
lands, `types.md` leaves reserve and that debt is discharged rather than paid; say so in the commit,
and do **not** edit `037`'s `In flux:` field to make it dispatchable.

## Must not delete — carried verbatim from `tasks/study-designer/037`

The corrected `StreamRef` field list — `name`, `bytes_written`, `truncated`, `records` — and the
one-sentence gloss distinguishing `records` from `truncated`. Task `036` fixed a stale enumeration
here once already; losing the fourth field or the distinction reopens the same defect. **This item
almost certainly lives in the text that moves**, which makes this split the exact moment it could be
lost. Check it explicitly on the far side of the move and say in the report that you did.

Beyond that: no field row, type name, default, or numbered `../decisions/*.md` citation may be
shortened, reworded, merged or re-ordered in either file.

## The citation problem this move creates, which is the real work

`tasks/doc/044` records it as a class: **a verbatim split is the one move `check-decision-refs.py`
cannot see.** The numbers still resolve, so the gate stays green while a citation now points at a
file that no longer holds the thing cited. `types.md` is a shared crate's type reference, so it is
cited from more repos than most files in this suite. So:

- Sweep the **whole suite** — this repo including `history/`, `tasks/` and
  `embarch-decision-reversals.md`, plus every code repo's source and docs — for references to
  `interfaces/types.md`, and repoint every one whose subject moved.
- A **path-qualified** citation (`interfaces/types.md`'s `StreamRef` row) must be repointed. A
  citation that names only the type, or points at `Study` / `Step` / `Action` content that did not
  move, must be left alone.
- Report the sweep's outcome **either way**, including "I found nothing else". A clean result is the
  only thing that tells the next leg this file's citations are settled, and it is exactly the
  sentence a worker omits when it finds nothing.

## Done when

1. `embarch-study-designer/interfaces/result-types.md` exists and holds the `Results` section
   **byte-identical** to its text at this task's parent commit. Prove it: extract the section from
   both sides and `diff` them, and put the exit status in the report. The only new prose anywhere is
   the new file's title line, a `Current truth:` header line matching its siblings' convention, and
   one cross-reference line in each file pointing at the other.
2. `embarch-study-designer/interfaces/types.md` is out of reserve — under 11,059 B.
3. The `StreamRef` four-field list and its `records`-vs-`truncated` gloss are verified present and
   unchanged on the far side of the move, and the report says so.
4. The suite-wide citation sweep above is done and its outcome reported either way.
5. `python3 scripts/check-docs.py` is green in `embarch-doc`, including `check-doc-size.py` and
   `check-decision-refs.py`.
6. `tasks/study-designer/037` is **untouched**. This task's own file is closed `done`.

## Not in scope

- Any change to the prose beyond moving the section and adding the cross-reference.
- Any change to `embarch-study-designer`'s source. The code branch for this unit is expected to
  carry zero commits.
- Answering any of the `open.md` questions this file's types touch — the sample grain, the FFI
  cross-link, `repeat`/`bitpack`/`crc32`/`fixed`. None of them is a documentation move.
