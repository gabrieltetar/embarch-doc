# 075 — `q parts` returns value, tolerance and rating by reference

**State:** claimed by agent/atlas/075-q-parts-returns-tolerance-and-rating-by-reference, 2026-11-17 23:43
**Source:** Fleet Ready issue: a worst-case divider calculation needed each part's tolerance, and `parts.md` drops it, so a session parsed `bom.json` by hand.
**Issue:** EMB-180
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A new lookup, `embarch-atlas q parts <board> <ref>...` with a matching read-only MCP tool, prints one row per reference: MPN, value, tolerance, rating (voltage and power, where the part has them), DNP flag, and the net on each pin. It says which references it did not find. Tolerance and rating are parsed into `bom.json` at `schematic` time — from a dedicated field when the schematic has one, otherwise from the BOM description (descriptions read like `RES SMD 86.6K OHM 1% 1/16W 0402`) — and are recorded as unknown, never guessed, when neither carries them. `parts.md` rows carry the tolerance too.

The parsing rules are the worker's call within `embarch-atlas`: which description shapes it recognises (resistors, capacitors, inductors at least), how a rating is written in the row, and whether the lookup reads `bom.json` directly or goes through the existing parts code. Follow the shape `q net-find` and `q net-trace` already use for arguments, output budget and the MCP tool list.

## Why now

The owner moved the issue to Fleet Ready. Every firmware limit derived from a divider, RC filter or sense resistor needs each part's tolerance, and today that means reading the raw BOM.

## Dispatch notes

- `embarch-atlas` keeps no numbered decisions; document the lookup where the other lookups are documented (`DESIGN.md`, `README.md`, the `MAP.md` tools line in `mapgen.py`, the atlas-use skill's table, `embarch-doc/embarch-atlas/design.md`) and update every place that states the lookup count, including the test that pins `len(TOOLS)`.
- Test with synthetic BOM records, including a description with no tolerance (must read unknown) and a reference that is not on the board.
- No file of this sub-project is in reserve.

## Done when

- [ ] `embarch-atlas q parts <board> <ref>...` prints MPN, value, tolerance, rating and DNP for each reference, and says which references it did not find; the MCP tool returns the same.
- [ ] Tolerance is parsed from the BOM description when no dedicated field exists, and shows as unknown rather than guessed when neither has it.
- [ ] `parts.md` rows carry the tolerance.
- [ ] Tests cover the cases above; gate green (`../../embarch-fleet/gate.md`); docs updated, `changelog.d/` fragment dropped.
