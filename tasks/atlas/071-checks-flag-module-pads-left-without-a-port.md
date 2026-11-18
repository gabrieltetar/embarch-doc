# 071 — `checks.md` flags module pads left without a port, and DT pins on them

**State:** claimed by agent/atlas/071-checks-flag-module-pads-left-without-a-port, 2026-11-17 18:34
**Source:** EMB-188 and EMB-156, two audit findings about module pad names the schematic reader leaves blank; `atlas/070` added the text-layer recovery both waited on
**Issue:** EMB-188
**Issue:** EMB-156
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

On a board whose MCU is a module symbol, the netlist can leave some pads
without a pin name. `pins.md` then shows those pads with an empty port column,
and an empty DT column too, because the DT-to-pad join goes through the port
name. The pin-versus-schematic check skips them, and nothing in `checks.md`
says so. In the case that produced EMB-188, two SPI signals the devicetree uses
sat on such pads and were never compared.

`atlas/070` now recovers rotated pad names from the PDF text layer and lists a
pad it cannot pair as `pad-name-unpaired` in the ingest's `issues.md`. That is
the ingest's report. What a reviewer reads is the atlas's `checks.md`, and it
is still silent. This unit makes it speak:

- **A module pin row with a net and no port is a finding in `checks.md`**,
  naming the part, the pad and the net. A row the text layer filled (marked
  `text-layer`) is not one.
- **A DT pin that cannot be joined to a pad is listed in `checks.md` as
  unresolved**, naming the DT node and property, so a pin check that could not
  run reads as unresolved, never as passing.
- **Check that `atlas/070`'s recovery covers EMB-188's shape**: a contiguous
  range of pads on one side of a module symbol, names printed beside them. Add
  a synthetic case for it if the existing tests do not have one. If the shape
  is not recovered and the cause is not visible without the real board, say so
  in this file and leave it to the flags above; do not guess at a fix.

The schematic text search EMB-156 also asks for is `atlas/072`, not this unit.

**Public repo.** Tests use synthetic schematics and netlists built in the test;
no client board, no real schematic.

**No new numbered decision** (burndown; `embarch-atlas` keeps none anyway).
Record what the checks prove in `DESIGN.md` beside the other checks. A real
design fork goes to `scripts/fleet-linear.py file --from decision`.

**What you may change.** Only `embarch-atlas` and `embarch-doc/embarch-atlas/`.

**Doc reserve.** Nothing of `embarch-atlas`'s is in reserve.

## Why now

The owner moved both issues to Fleet Ready, and their finding comments sequence
them after EMB-89, which `atlas/070` landed today.

## Done when

- [ ] An atlas whose module symbol has a pad with a net and no port lists that pad in `checks.md`.
- [ ] A DT pin that cannot be joined to a pad appears in `checks.md` as unresolved.
- [ ] A test covers a contiguous range of named pads on one side of a module symbol, and the result is recorded here.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
