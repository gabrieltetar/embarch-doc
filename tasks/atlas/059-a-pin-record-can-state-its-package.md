# 059 — A pin record can state its package

**State:** done (2026-11-10)
**Source:** Linear issue EMB-45
**Issue:** EMB-45
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A part whose pinout changes with its package makes the join's pin-number lookup ambiguous: on one logic gate pin 5 is VCC on most packages and N.C. on two. A `pin` record holds only the number or ball (`schemas/record.schema.json`), and the join takes the first record whose `pin` contains the number (`Join.part_pin_name`, `Join.part_pin_record`, and `build_pin_map`'s `ds_by_num.setdefault`), so on such a part it can name the wrong signal.

Add both halves, **with this direction (decided at the split):**

- `pin` records take an optional `package` (a non-empty string as the datasheet names it), in the schema, `records.FACT_KEYS["pin"]`, the renderer and the datasheet procedure. Records without it validate and render as today.
- The board side states the package per board part in `boards/bindings.json`, engineer-declared, keyed by ref (a new optional key beside `compat_parts`; the worker names it). Reading the package from the BOM's footprint string or from `variant` records (`atlas/053`) is **not** in scope; name it under `DESIGN.md` "Not yet built" if it fits there.
- When the board part's package is known, lookups use the records for that package plus any record with no `package`. When it is not known and the records for one pin number differ by package, the join does not silently take the first: it says the pin is ambiguous (where, and in what words, is the worker's pick; say it in the report). A part with one pinout resolves exactly as today.

## Why now

The join can name the wrong signal on any part with two pinouts, and nothing says so.

## Where to look

- `schemas/record.schema.json` (`pin` kind), `src/embarch_atlas/records.py` `FACT_KEYS["pin"]`, the `pin` renderer
- `src/embarch_atlas/join.py` `Join.part_pin_name`, `Join.part_pin_record`, `build_pin_map`, and where `bindings.json` is loaded (the module docstring describes its keys)
- `DESIGN.md` record-kind table (`pin`), the `boards/bindings.json` line in "On-disk layout", and the join's description
- `skills/atlas-translate-docs/reference/datasheet-procedure.md` for where a distiller would write `package`

## Dispatch notes

- Burndown is on: no new numbered decision. The atlas has none; describe the field and the lookup rule in `DESIGN.md` in place, as `atlas/054` did for a register's `bank`.
- Nothing touches hardware; tests use synthetic records and netlists.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.

## Done when

- [x] A `pin` record can state its package, and the schema accepts it.
- [x] With two pin records for one number on different packages and the board part's package declared in `bindings.json`, the join resolves the one for that package.
- [x] With the same records and no declared package, the join reports the pin as ambiguous instead of taking the first.
- [x] A part with a single pinout and no `package` on its records resolves as before.
- [x] `DESIGN.md` describes the field, the `bindings.json` key and the lookup rule.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
