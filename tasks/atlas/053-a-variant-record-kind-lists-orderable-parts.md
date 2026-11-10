# 053 — A `variant` record kind lists a part's orderable variants

**State:** claimed by agent/atlas/053-a-variant-record-kind-lists-orderable-parts, 2026-11-10 01:45
**Source:** Linear issue EMB-47, filed by a session
**Issue:** EMB-47
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The record schema has no kind for orderable variants, so a regulator's table of orderable part numbers (output voltage, package, options per part number) ends up as free text spread across `rule` records. A `rule` is behaviour (`text`, `cond`, `recover`, `steps`), and `quirk`'s `variant` class flags a datasheet row that differs by variant without listing the variants.

Add a `variant` kind: one record per orderable part, with `mpn` (the orderable part number) and `options` (the settings that differ between variants).

## Why now

A reader or agent asking which orderable part has which output voltage, package or option gets an answer buried in `rule` text. The kind is additive, and no existing record changes.

## Where to look

- `schemas/record.schema.json` — the `kind` enum and the per-kind property blocks
- `src/embarch_atlas/records.py` `KINDS` and `FACT_KEYS` — both list the kinds; `FACT_KEYS` sets the rendering order in `facts.txt`
- `DESIGN.md` — the record-kind table (the `rule`, `quirk` and `strap` rows)
- `skills/atlas-translate-docs/reference/datasheet-procedure.md` — the per-kind instructions (`strap` is the nearest model)

## Dispatch notes

- Burndown is on: no new numbered decision. The atlas has none anyway; add the row to `DESIGN.md`'s record-kind table in place and say when a `variant` is written instead of a `rule` or a `quirk`.
- Grep for every other place that enumerates kinds (validators, renderers, `check.py`, tests) so `variant` is not refused or dropped by one of them.
- The shape of `options` is yours to pick (an object of option name to value reads naturally); state it in the schema and in `DESIGN.md`.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.

## Done when

- [ ] `variant` is in `KINDS`, in the schema's `kind` enum, and has its own property block.
- [ ] The datasheet procedure says when to write a `variant`.
- [ ] A `variant` record validates and renders in `facts.txt`, with a test.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
