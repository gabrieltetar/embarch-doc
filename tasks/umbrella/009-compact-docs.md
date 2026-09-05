# 009 — embarch-umbrella's spec.md and open.md are in reserve

**State:** blocked
**Source:** scripts/check-doc-size.py --pressure
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/spec.md, embarch-umbrella/open.md
**In flux:** yes — four open tasks, and every one of them rewrites the doctor table in spec.md
**Must not delete:** spec.md's twenty-row `doctor` table, and in particular which rows are **designed and unbuilt** — four decisions describe checks that do not exist, the doc asserted four of them as shipped for weeks, and that table is now the only place the distinction lives; open.md's note that check 15 is not a hash comparison and must not be read as one.

**Counts refreshed by the supervisor, 2026-09-05, after `umbrella/005` landed** — they were *nineteen rows / five decisions / six open tasks* and are now twenty / four / four. `umbrella/005` built check 16 (so one designed-and-unbuilt decision became built) and renumbered the design-only checks 16-19 → 17-20. Refreshed because a `Must not delete:` clause that preserves a table *by a count* is worse than useless once the count is stale: whoever runs this task would have protected the wrong shape. **Urgency, also from `umbrella/005`: `open.md` is at 5051/5120 B — 69 B left — and `spec.md` at 10089/10240 B, 151 B left.** This task stays `blocked` on `In flux: yes`, which is still true, but the next `umbrella` task to touch either file has effectively no room.

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

**And meanwhile the reserve is not parked with it, 2026-09-05.** Neither file can be
split — 10 KB and 5 KB are role caps on single files — so shortening was the only move.
**`open.md` is already paid**: the owner's live-`doctor` pass took it 5,051 → 4,388 B
(86.2%) while *adding* what the run measured, which is `DOC-COMPACTION.md` §2's new rule
on its first real use. `spec.md` still has 151 B, and `tasks/umbrella/006` and `007` each
carry its compaction as part of their own unit, under this task's `Must not delete:` list.
**Refresh the counts above before trusting them.**

**This task got further away, not closer, on 2026-09-05.** Its unpark condition is "the
umbrella queue is down to one open task", and that queue went from two to five: the
owner's live `doctor` run filed `010`, `011` and `012`. That is the condition working —
three of sixteen checks were found dark on the primary topology, and every one of them
rewrites a row of the table this task would be compacting.

## Done when

- [ ] Both files out of reserve.
- [ ] The unbuilt/built distinction survives, per row.
- [ ] No question disappears from `collect-open-questions.py` unless you can
      name it as answered.
- [ ] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
