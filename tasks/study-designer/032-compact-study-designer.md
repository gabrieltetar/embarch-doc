# 032 — Compact `embarch-study-designer/spec.md`

**State:** blocked — §4 is still in flux (see below); unparks once §4 has gone
a full leg without a new field or seal-placement edit landing in it.
**Source:** `scripts/check-doc-size.py`, filed by leg landing task 031 (2026-09-11):
`spec.md` crossed into its last 10% (91.3%, 890 B left) from that task's seal-placement
correction and `record_checks` table row.
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/spec.md
**Size debt due:** 2026-09-25
**In flux:** yes — §4 ("What a study carries") was just edited twice in one week
(seal ordering, then `record_checks`), and `record_checks`/decision 70 is recent
(2026-09-08/09) enough that another field could still land there.

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

## Done when

- [ ] `spec.md` compacted (or this task re-parked with a fresh look), such that
      it alone still answers what someone needs to work on this component today.
- [ ] Gate green.
