# 037 — Compact `embarch-study-designer/interfaces/types.md`

**State:** blocked — this doc is still in flux (see below); unparks once it has
gone a full leg without a type or field-list edit landing in it.
**Source:** `scripts/check-doc-size.py`, filed by leg landing task 036 (2026-09-13):
`types.md` crossed into its last 10% (91.6%, 1037 B left) from that task's
`StreamRef.records` field-list fix and one-sentence gloss.
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/interfaces/types.md
**Size debt due:** 2026-09-27
**In flux:** yes — this file enumerates every wire/host type's field list, and
it has landed edits from three of the last seven merged units in this scope
(031, 035, and now 036 — the count said four and named three; corrected in
036's fold after the reviewer checked `git log` on this file); a type gaining
or losing a field is exactly what
lands here, and `records`/decision 70 is 2026-09-08, recent enough that
another field is plausible before this parks.

## What

`types.md` is in reserve. No compaction is being done now — this records the
debt per `DOC-COMPACTION.md` §2, since `In flux: yes`.

## Why now

`check-doc-size.py` fails the gate on an unfiled file in reserve.

## Must not delete

The corrected `StreamRef` field list (`name, bytes_written, truncated,
records`) and the one-sentence gloss distinguishing `records` from
`truncated` — task 036 fixed a stale enumeration here once already; losing
the fourth field or the distinction in a future trim reopens the same defect.

## Done when

- [ ] `types.md` compacted (or this task re-parked with a fresh look), such
      that it alone still answers what someone needs to work on this
      component's interfaces today.
- [ ] Gate green.
