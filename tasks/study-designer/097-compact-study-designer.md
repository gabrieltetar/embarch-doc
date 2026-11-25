# 097 — compact `embarch-study-designer/interfaces/hil-run.md`

**State:** claimed by agent/study-designer/097-compact-study-designer, 2026-11-25 08:56
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/interfaces/hil-run.md
**Size debt due:** 2026-12-09
**In flux:** no — the three units that were moving it (EMB-364, EMB-356, EMB-376) landed by 2026-11-25 (`api/196`'s fold); it was `yes` until then
**Must not delete:** the key tables of `run.json` and of a test entry with every `(amended)` field; the Expansion statuses table; the Study-export check table (06's checks 0 to 9).

## What

`hil-run.md` is 11,910 of 12,288 B after `study-designer/096` amended it for the bench entry, `run_id` and the expansion. Compact it under `DOC-COMPACTION.md`. Answered by the unit that just worked in it: **the HIL Test chain is still moving** (Core's prepare route EMB-364, the shared verdict function EMB-356 and embarch-api's test plan EMB-376 each read or amend this shape), so every one of them will rewrite lines here.

## Done when

- [ ] `hil-run.md` is out of reserve and every `Must not delete:` item survives.
