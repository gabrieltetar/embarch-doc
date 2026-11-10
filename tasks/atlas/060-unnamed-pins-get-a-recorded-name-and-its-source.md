# 060 — A pin the netlist left unnamed can be given a name, and every name says where it came from

**State:** done
**Source:** Linear issue EMB-25
**Issue:** EMB-25
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A module's pad names can be missing from a schematic PDF's embedded netlist; today they are read off the rendered symbol by hand. A pin's name is the visible word just past the end of its anchor, on the pin's axis, for parts with 3 or more pins (`MIN_NAMED_PINS`); when that finds nothing the pin keeps `name: null` in `boards/<label>/netlist.json`. There is no step that supplies the missing name, and a name typed in by hand would look exactly like one read from the PDF.

Add both halves, **with this direction (decided at the split):**

- **An engineer-owned overlay per board**, a file beside `netlist.json` that `schematic` never overwrites (as `boards/system.json`'s `interfaces` are never overwritten). It holds names keyed by board, ref and pin, each with a provenance: `engineer-declared`, `engineer-confirmed`, or `llm-unverified` for a name read from a rendered crop (the ladder's rung 4 already says such facts are `llm-unverified` until matched). The worker names the file.
- **A verb writes it**, in the shape of `declare-interface`: it refuses a board with no netlist, a ref the netlist lacks, and a pin number the part lacks, and it does not overwrite a pin the PDF's text already named. The same key again replaces the entry.
- **Every pin name says where it came from.** In `netlist.json` (or in the merged view every later step reads; the worker picks, and says which), a pin's name carries its source: the PDF's text, or the overlay with its provenance. A re-run of `schematic` keeps the overlay's names in effect. `join` (`part_pin_name`) reads the merged name, so `pin_trace` and the join see it.
- **`schematic` reports how many pins on 3-plus-pin parts are still unnamed** after the overlay, beside its existing `pins_named / pins_on_3plus_pin_parts` count.
- **The step is documented** in the skill that runs `schematic` (`atlas-translate-docs` or `atlas-build`, wherever unnamed pins are first seen): render the symbol's crop, read the names, record them through the verb as `llm-unverified`, and have the engineer confirm. Building the vision rung itself (automatic crop and read) stays under "Not yet built".

## Why now

`pin_trace` and the join work from pin numbers only on such a part, and nothing distinguishes a hand-typed name from a printed one.

## Where to look

- `src/embarch_atlas/smartpdf.py` `pin_name_for` (the only source of pin names), `parse_all` (`names_of`, `pins_named`, `pins_on_3plus_pin_parts`; the pin dict is `{"name", "net"}`)
- `src/embarch_atlas/join.py` `part_pin_name`
- `src/embarch_atlas/interfaces.py` `declare` — the verb to model this one on
- `DESIGN.md` "Schematic ingest ladder", "`boards/<label>/netlist.json`", the CLI table and "Not yet built"

## Dispatch notes

- Normal mode. The atlas keeps no numbered decisions; state the overlay, the verb and the provenance rule in `DESIGN.md` in place, as `atlas/055` did for `declare-interface`.
- Nothing touches hardware; tests use synthetic netlists.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.
- Edit files with your edit tool, not inline Python scripts.

## Done when

- [x] A documented step records names for pins the netlist left unnamed, keyed by board, ref and pin, through a verb that refuses an unknown board, ref or pin.
- [x] Every pin name in `netlist.json`, or the merged view later steps read, says whether it came from the PDF's text or from the overlay, with the overlay's provenance.
- [x] A re-run of `schematic` keeps the overlay's names, and `join` reads them.
- [x] `embarch-atlas schematic` reports how many pins on 3-plus-pin parts are still unnamed.
- [x] `DESIGN.md` describes the overlay, the verb and the provenance.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
