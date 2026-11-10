# 045 — Nets joined through an off-sheet port are one net in the netlist

**State:** claimed by agent/atlas/045-nets-joined-through-an-off-sheet-port-are-one-net, 2026-11-09 20:58
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

- [ ] A synthetic two-sheet fixture whose nets are joined only through an off-sheet port of the same name, under different net names, yields one net with both sheets' pins in `boards/<label>/netlist.json`.
- [ ] A port with no partner on another sheet is listed in the netlist's `issues`.
- [ ] `net_trace` on that fixture shows the pins from both sheets.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `DESIGN.md` says how nets join; `changelog.d/` fragment dropped.
