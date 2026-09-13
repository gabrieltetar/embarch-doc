# 038 — Split `embarch-study-designer/interfaces/types.md`'s Results section into its own interface file

**State:** done — leg 108, 2026-09-13, landed on `agent/study-designer/038-split-result-types`
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

1. [x] `embarch-study-designer/interfaces/result-types.md` exists and holds the `Results` section
   **byte-identical** to its text at this task's parent commit. Verified: extracted the section
   (`## Results` to EOF) from both the pre-move `types.md` and the new file and diffed them —
   **exit status 0**. New prose is the title line, a `**Status:** active` header line naming
   "Split out of types.md ... (tasks/study-designer/038)", matching the suite's real split-file
   convention (`embarch-core`, `embarch-api`, `embarch-umbrella`'s own split interface files all use
   this "Split out of X" shape, not literally the words "Current truth:" — none of `types.md`'s own
   siblings in this sub-project carry a `Current truth:` line either; see report), a
   "Current truth for the authoring types ... : types.md"-worded cross-reference line back to the
   authoring types, and, in `types.md`, a one-line `## Results` pointer forward to the new file.
2. [x] `embarch-study-designer/interfaces/types.md` is out of reserve — **8,999 B**, under 11,059 B.
3. [x] The `StreamRef` four-field list (`name, bytes_written, truncated, records`) and its
   `records`-vs-`truncated`-adjacent gloss (the `records: Option<RecordReport>` sentence) are
   present, unchanged, verbatim, in `result-types.md`. Cross-checked against `study-designer/036`'s
   own diff (`git show 5bbc0bc`), which is where the fourth field was added — the moved text matches
   that landed version exactly.
4. [x] Suite-wide citation sweep done. Outcome: swept this repo (docs, `history/`, `tasks/`,
   `embarch-decision-reversals.md`) and every code repo's source/docs for `interfaces/types.md`.
   Found and left alone (name only the type, or cite unmoved `Study`/`Step`/`Action` content):
   `embarch.md:116`, `embarch-glossary.md:24` (both suite-level, untouched regardless),
   `history/study-designer.md:8`, `embarch-study-designer/spec.md:5`,
   `embarch-study-designer/decisions.md:5`, `embarch-study-designer/decisions/declared-gatt.md:14`,
   `embarch-study-designer/decisions/streams.md:31` (a pre-existing `§4.8` numbered reference,
   predating and unrelated to this split), `suite/studies-guide.md:13,100`,
   `tasks/study-designer/031` (historical, closed). Found needing repoint but out of this task's own
   `## Not in scope` (this crate's source): `embarch-study-designer/README.md:23`,
   `src/result.rs:1,23,35,89`, `src/limits.rs:50` — filed as
   `tasks/study-designer/039-repoint-source-doc-comments-to-result-types-md.md`. Found needing
   repoint in a repo this task does not own: `embarch-ui/src/study_designer.rs:780` (a `StreamRef`
   citation) — dropped as
   `/home/gabriel/Github/embarch/embarch-doc/inbox/ui-repoint-streamref-citation-to-result-types-md.md`.
   Its sibling citation at `study_designer.rs:1524` was checked and is unaffected (unmoved `Action`
   content).
5. [x] `python3 scripts/check-docs.py` green in `embarch-doc` — all 11 checks, including
   `check-doc-size.py` and `check-decision-refs.py`.
6. [x] `tasks/study-designer/037` untouched (confirmed: not in this unit's diff). This task's own
   file closed `done`.

## Not in scope

- Any change to the prose beyond moving the section and adding the cross-reference.
- Any change to `embarch-study-designer`'s source. The code branch for this unit is expected to
  carry zero commits.
- Answering any of the `open.md` questions this file's types touch — the sample grain, the FFI
  cross-link, `repeat`/`bitpack`/`crc32`/`fixed`. None of them is a documentation move.
