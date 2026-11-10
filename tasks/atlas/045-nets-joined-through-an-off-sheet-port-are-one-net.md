# 045 — Nets joined through an off-sheet port are one net in the netlist

**State:** done (agent/atlas/045, 2026-11-09)
**Source:** Linear issue EMB-24, filed by a session
**Issue:** EMB-24
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`embarch-atlas schematic <pdf> --board <label>` joins two sheets' nets that meet through the same off-sheet port into one board net in `boards/<label>/netlist.json`, carrying the pins of every sheet, even when the two sheets name the net differently. A port that has no partner on another sheet is listed in the netlist's `issues`. `net_trace`, `pin_trace`, the pin map and the graph then see the whole net.

Today `parse_all` builds one board net per net *name* (the "board nets: one per name" block): every sheet's `Nets > <name>` outline entry is merged into the board net of the same name, and nothing else joins nets. The ports a net touches are only counted (`ports`), never used to join, and `read_outline` keeps each sheet's port names in `S["ports"]` unused. A net that leaves one sheet through a port under one name and arrives on another under a different name is therefore two board nets, each with one side's pins, and no issue is raised. This follows from the code; it was not reproduced against a real PDF.

## Why now

Filed as the most serious gap found in the schematic parse: every tool that reads `netlist.json` answers from half a net without a warning.

## Where to look

- `src/embarch_atlas/smartpdf.py` `parse_all` — the "board nets: one per name" block
- `src/embarch_atlas/smartpdf.py` `read_outline` — reads `Nets > <net> > Pins | Ports | NetLabels` and each sheet's `Ports` list
- `src/embarch_atlas/geom.py` — the geometric cross-check; whether it has the same gap is not known, so say what you find rather than assume
- `tests/test_smartpdf.py` — the synthetic outline fixture shape
- `DESIGN.md` "Schematic ingest ladder" (rung 2, the embedded outline netlist, is the source of truth) and the `boards/<label>/netlist.json` description

## Dispatch notes

- **Synthetic fixtures only.** No vendor or project PDF goes in this public repo. Build the two-sheet outline in the test, as the existing fixtures do.
- **Which name the joined net takes is yours to choose and state** in `DESIGN.md`; this repo has no numbered decisions, so amending `DESIGN.md` in place is the record. Keep a same-named join working exactly as it does now.
- No `embarch-atlas` doc in `embarch-doc` is in reserve at the split.

## Done when

- [x] A synthetic two-sheet fixture whose nets are joined only through an off-sheet port of the same name, under different net names, yields one net with both sheets' pins in `boards/<label>/netlist.json`.
- [x] A port with no partner on another sheet is listed in the netlist's `issues`.
- [x] `net_trace` on that fixture shows the pins from both sheets.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `DESIGN.md` says how nets join; `changelog.d/` fragment dropped.

## Notes

- Joined net takes the first non-auto-named name in natural order (else the first); the rest are `aliases` on the net. Stated in `DESIGN.md` ("How nets join").
- Port names come from each net's `Ports > <title>` outline children (`port_names`). Whether a real export titles those with the port name, as the synthetic fixtures do, is unverified against a real PDF.
- An unpartnered port is one whose name is on no other sheet's port/sheet-level port list and is no other sheet's net name (so a hierarchy sheet entry on the parent counts as a partner when it is a net there).
- `geom.py` has the same gap in kind: it compares per sheet and per name and never joins across a port. Left as is; a joined net's `crosscheck` mark is the picked name's sheet net only (stated in DESIGN.md).
