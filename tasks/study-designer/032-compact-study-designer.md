# 032 — Compact `embarch-study-designer/spec.md`

**State:** done — 2026-09-28. Split §4 ("What a study carries") verbatim to
`spec/carriage.md`, per the dispatch note's split-first instruction; renumbered the remaining
sections (5→4, 6→5, 7→6) since nothing in this suite's own docs cited them by number, and fixed
`embarch-study-designer/src/study.rs:1062`'s own `spec.md §7` comment to `§6` in the same commit.
`spec.md` is now 7,924/10,240 B (out of reserve). Found one cross-repo citation this split made
stale — `embarch-api/src/main.rs:538`'s `spec.md §7` — outside this task's ownership row, dropped
at `/home/gabriel/Github/embarch/embarch-doc/inbox/api-stale-study-designer-spec-section-cite.md`.
**Source:** `scripts/check-doc-size.py`, filed by leg landing task 031 (2026-09-11):
`spec.md` crossed into its last 10% (91.3%, 890 B left) from that task's seal-placement
correction and `record_checks` table row.
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/spec.md
**Size debt due:** 2026-09-25
**In flux:** no — unparked at claim, 2026-09-28, three days past its clock, on this task's own
condition. §4's last edit is `ac9c2116` (2026-09-18), one table cell naming decision 77's build
spec in the `requires` row; nothing has touched `spec.md` in the ten days and every leg since, and
decision 77 itself was split out verbatim to `decisions/builds.md` today (`study-designer/068`)
without touching this file. The old answer, kept as history: *yes — §4 ("What a study carries")
was just edited twice in one week (seal ordering, then `record_checks`), and `record_checks`/
decision 70 is recent (2026-09-08/09) enough that another field could still land there; unparks
once §4 has gone a full leg without a new field or seal-placement edit landing in it.*

## What

`spec.md` is in reserve. No compaction is being done now — this records the debt
per `DOC-COMPACTION.md` §2, since `In flux: yes` for the file's only section that
grew.

## Why now

`check-doc-size.py` fails the gate on an unfiled file in reserve.

## Must not delete

The corrected seal-ordering sentence in §4 (`struct Study`'s actual declaration
order: `steps, streams, steps_crc, streams_crc, protocols, protocols_crc`) — it
replaced a wrong claim (task 031) and losing the specific order in a future trim
would let the same error creep back in.

## Dispatch note (supervisor, 2026-09-28)

**Split first, squeeze second** (`DOC-BUDGET.md`'s split-first rule, `DOC-COMPACTION.md` §2).
`spec.md` is **9,400 / 10,240 B, 840 B left**. If a section has a mission of its own — §7's
constants, or §4's carriage table — a verbatim move to a sibling under `spec/` (the pattern
`embarch-ui/spec/capture-rendering.md` set) restates nothing. A squeeze is legal here too now that
the flux has lapsed, but the §4 seal-ordering sentence above is untouchable either way. Check every
inbound link into `spec.md`'s sections before cutting (`grep -rn 'study-designer/spec.md'` over
`embarch-doc` and the code repo) and repoint any that name a moved section.

**Also in reserve in `study-designer`, not yours to write:** `decisions/gatt-extract.md` **36 B
left** (`tasks/study-designer/069`, open — the next leg's first unit), `open.md` 5,447 / 5,120 B
(`tasks/study-designer/026`, blocked). If your work pushes any other `study-designer` file into
reserve, file `tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit.

## Done when

- [x] `spec.md` compacted (or this task re-parked with a fresh look), such that
      it alone still answers what someone needs to work on this component today.
      Split, not squeezed: §4 moved verbatim to `spec/carriage.md` (the seal-ordering sentence
      under "Must not delete" above travelled with it, unreworded), so `spec.md` alone still
      answers what someone needs today and `spec/carriage.md` is one link away for the carriage
      detail. No inbound link named §4/§5/§6/§7 by number from any current (non-historical,
      non-task) doc in either repo except the two source comments above, both fixed or reported.
- [x] Gate green.
