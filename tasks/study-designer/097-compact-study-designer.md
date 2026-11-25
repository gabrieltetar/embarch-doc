# 097 — compact `embarch-study-designer/interfaces/hil-run.md`

**State:** done — hil-run.md split verbatim; Study export moved to hil-study-export.md
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

- [x] `hil-run.md` is out of reserve and every `Must not delete:` item survives.

## Done

Verbatim split (nothing deleted, so no squeeze list): the "A Study's export and check" section moved to `interfaces/hil-study-export.md` (4,851 B); `hil-run.md` is 7,602 B with a pointer. Both `Must not delete:` items survive: `run.json` and test-entry tables and the Expansion statuses table stay in `hil-run.md`; the Study-export check table (checks 0 to 9) is in the new file. Links updated in `hil-shapes.md`. Does `spec.md` alone answer what someone needs to work on this component today? Yes for what exists and where each shape lives: it indexes the HIL shapes and names both files; the shape details are deliberately in the interface files, which are the loaded-on-purpose tables, and no spec content was touched. In flux: no.
