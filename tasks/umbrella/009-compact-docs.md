# 009 — embarch-umbrella's spec.md and open.md are in reserve

**State:** blocked
**Source:** scripts/check-doc-size.py --pressure
**Scope:** umbrella
**Hardware:** none
**Compacts:** ~~embarch-umbrella/spec.md~~ (paid 2026-09-05, `umbrella/006`), ~~embarch-umbrella/open.md~~ (paid 2026-09-05)
**In flux:** yes — the open umbrella tasks still rewrite the doctor table in spec.md
**Must not delete:** spec.md's twenty-row `doctor` table, and in particular which rows are **designed and unbuilt** — four decisions describe checks that do not exist, the doc asserted four of them as shipped for weeks, and that table is now the only place the distinction lives; open.md's note that check 15 is not a hash comparison and must not be read as one.

**Counts refreshed by `umbrella/006`, 2026-09-05.** The table is still **twenty rows**, but **three** decisions are designed-and-unbuilt, not four: `umbrella/006` built decision 18, so check 5's row now describes a shipped Fail branch and the unbuilt set is 22(a-c), 27/29 and 17's amendment. A `Must not delete:` clause that preserves a table *by a count* is worse than useless once the count is stale, so whoever runs this task protects **twenty rows / three unbuilt decisions**, not the earlier nineteen/five or twenty/four.

**Both files are out of reserve, so the urgency is gone and only the pass is left.** `open.md` 5051 → 4525 B (88.4%) across two units, `spec.md` 10089 → 9131 B (89.2%) in `umbrella/006`. This task stays `blocked` on `In flux: yes`, which is still true.

## What

`spec.md` is at ~93% of 10 KB and `open.md` at ~94% of 5 KB. Both had a pass on
2026-09-04 whose main find was a duplication rather than cold prose:
`decisions/doctor.md` was re-arguing build status that `spec.md`'s table owns,
worth ~1.2 KB. Run `scripts/check-duplication.py embarch-umbrella` before
anything else — the same class may still be there between `spec.md` and
`decisions/projects.md` or `decisions/release.md`.

## Why blocked

Tasks 003–008 are all open, all in this sub-project, and between them they build
`setup --dry-run`, check 10's handshake, `doctor --prune`, check 5's
not-permitted branch, check 8's shellout and check 11's `embarch-api versions`
read. **Every one of those changes a row of the table this task would be
compacting**, and several close an `open.md` bullet outright. Compacting first
means writing a clean statement of five things about to become false.

**Unparks when the umbrella queue is down to one open task**, whichever it is.
Not on a timer, and not on "enough of them landed".

**And meanwhile the reserve was not parked with it, 2026-09-05 — and is now paid.** Neither
file can be split — 10 KB and 5 KB are role caps on single files — so shortening was the
only move, and `DOC-COMPACTION.md` §2's ride-along rule put it inside the units doing the
rewriting. `open.md` went 5,051 → 4,388 B in the owner's live-`doctor` pass and `spec.md`
10,089 → 9,131 B in `umbrella/006`, which also spent 526 B more of `open.md` and gave it
back. **What `umbrella/006` moved rather than deleted**, since a move restates nothing and
so survives the in-flux objection: `spec.md`'s "Committing a repo integration" section into
[decision 12](../../embarch-umbrella/decisions/projects.md), and `open.md`'s measured v17
reading into [decision 35](../../embarch-umbrella/decisions/schema-skew.md). What it deleted
outright: the runtime-path half of the Shape diagram, and a question `open.md` itself called
closed. **Refresh the counts above before trusting them.**

**This task got further away, not closer, on 2026-09-05.** Its unpark condition is "the
umbrella queue is down to one open task", and that queue went from two to five: the
owner's live `doctor` run filed `010`, `011` and `012`. That is the condition working —
three of sixteen checks were found dark on the primary topology, and every one of them
rewrites a row of the table this task would be compacting.

## Done when

- [x] Both files out of reserve — `open.md` 2026-09-05 (owner), `spec.md` 2026-09-05 (`umbrella/006`). **This is the reserve item only; the pass itself is still owed** and the rest of these boxes are open.
- [ ] The unbuilt/built distinction survives, per row.
- [ ] No question disappears from `collect-open-questions.py` unless you can
      name it as answered.
- [ ] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
