# 039 — Two different `embarch-core` decisions are both numbered 54

**State:** open
**Source:** leg 077, 2026-09-10, found while picking the next free decision number for `api/044`.
A live instance of the gap `tasks/doc/033` describes — nothing checks that a decision number is
unique — so this is the defect, not the missing check.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Two decisions in `embarch-core` carry the number 54:

- `embarch-core/decisions/flashing.md:46` — *"`Backend::NrfJprog` retired: a fourth backend no
  bench, doctor run, or record ever selected"*
- `embarch-core/decisions/surfaces.md:45` — *"`EnrolledBoardResponse` does not grow a persisted
  validation timestamp; the existing field gets an honest label instead (`tasks/core/027`)"*

They are unrelated, and both are cited elsewhere in the suite. **"decision 54" in `embarch-core`
currently resolves to whichever file the reader opened first**, and `check-decision-refs.py` is
green on both because it resolves a number against the sub-project rather than against a file —
the same blind spot leg 076 hit from the other direction with `umbrella/042`.

## What to do

**Renumber exactly one of them, and the citation sweep is the work.** Whichever moves, every
reference to it across the suite has to move with it, and a reference that says only "decision 54"
without a file has to be read for which one it meant — that reading is the part no script can do.

Prefer renumbering the **later-written** one to the next free number (57, after `core/037` took 55 and `api/044` took 56),
and leave a one-line note at the old number's home saying it moved, so a stale citation lands
somewhere that explains itself rather than somewhere plausible and wrong.

**Do not add the uniqueness check here** — `scripts/` is the owner's, and `tasks/doc/033` already
holds that half.

## Done when

- [ ] Exactly one of the two is renumbered; both numbers are unique within `embarch-core`.
- [ ] Every citation of the moved decision, in every repo, points at the new number — the body of
      this task names each one found and says how it was read.
- [ ] `scripts/check-decision-refs.py` green, and a manual grep for the bare old number is recorded.
- [ ] `changelog.d/` fragment.
