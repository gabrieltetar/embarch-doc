# 097 — compact `embarch-study-designer/interfaces/hil-run.md`

**State:** blocked — hil-run.md in reserve; HIL Test chain still moving

**Unparks when:** the HIL Test chain unit EMB-376 has landed
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/interfaces/hil-run.md
**Size debt due:** 2026-12-09
**In flux:** yes
**Must not delete:** the key tables of `run.json` and of a test entry with every `(amended)` field; the Expansion statuses table; the Study-export check table (06's checks 0 to 9).

## What

`hil-run.md` is 11,910 of 12,288 B after `study-designer/096` amended it for the bench entry, `run_id` and the expansion. Compact it under `DOC-COMPACTION.md`. Answered by the unit that just worked in it: **the HIL Test chain is still moving** (Core's prepare route EMB-364, the shared verdict function EMB-356 and embarch-api's test plan EMB-376 each read or amend this shape), so every one of them will rewrite lines here.

## Done when

- [ ] `hil-run.md` is out of reserve and every `Must not delete:` item survives.
