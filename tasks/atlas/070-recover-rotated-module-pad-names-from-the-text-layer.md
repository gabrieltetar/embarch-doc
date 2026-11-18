# 070 — Recover a module symbol's rotated pad names from the PDF text layer

**State:** claimed by agent/atlas/070-recover-rotated-module-pad-names-from-the-text-layer, 2026-11-17 18:09
**Source:** EMB-89, filed by an audit after a second-reader pin check paired 16 bottom-row module pads to their port names by hand from the schematic's text layer
**Issue:** EMB-89
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

When a module symbol prints its pad names as rotated text (typically the bottom
row of pads), the schematic reader leaves those pads' port column empty in
`pins.md`, and nothing says the names are on the page.

Add a recovery step to the schematic ingest:

- Read every word on the page with its box (`pdftotext -bbox`, or whatever the
  ingest already uses for word positions; check before adding a tool). Inside
  the symbol's outline, a rotated pad-name row and the pad-number row beside it
  share x columns, so each pad number pairs with the name over it; side columns
  pair by y.
- Fill only pads the netlist left without a name. Mark every recovered name
  with its provenance (for example `src=text-layer`) in `netlist.json` and in
  `pins.md`, so a reader sees which ports came from the drawing.
- A pad whose name cannot be paired (no word in its column, two candidates) is
  listed in the atlas report instead of left blank.

This is the first of three issues about blank module pad names. EMB-156 (a
schematic text search, and a `checks.md` flag for a pin row with a net and no
port) and EMB-188 (a `checks.md` entry for a DT pin on an unresolved pad) follow
it and are not this unit. Leave both alone.

**Public repo.** Tests build a synthetic schematic PDF with rotated pad names in
the test; no client board, no real schematic.

**No new numbered decision** (burndown; `embarch-atlas` keeps none anyway).
Record the step in `DESIGN.md` where the schematic ingest is described. A real
design fork goes to `scripts/fleet-linear.py file --from decision`.

**What you may change.** Only `embarch-atlas` and `embarch-doc/embarch-atlas/`.

**Doc reserve.** Nothing of `embarch-atlas`'s is in reserve.

## Why now

The owner moved EMB-89 to Fleet Ready, and the finding comments on EMB-156 and
EMB-188 put it first in their sequence.

## Done when

- [x] An atlas built from a schematic whose module symbol prints pad names as rotated text shows a port for every named pad in `pins.md`, each marked as recovered from the text layer.
- [x] A pad whose name cannot be paired is listed in the atlas report.
- [x] A test builds such a PDF and checks both.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.

## Notes

Unpaired pads are listed in the netlist `issues` (so `issues.md`, kind `pad-name-unpaired`), the schematic ingest's own report; a `checks.md` flag is EMB-156/EMB-188 and untouched. Vertical pads: rotated words in the pad number's x column; side pads: upright words on the pad's row, own side of the outline. Tested on a synthetic PDF only; real symbols with other layouts (numbers inside, mirrored columns) are unmeasured.
