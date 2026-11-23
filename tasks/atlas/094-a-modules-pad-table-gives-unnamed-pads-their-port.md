# 094 — A module's pad table gives an unnamed pad its port

**State:** open
**Source:** Fleet Ready issue, filed by `atlas/092`'s worker for the part of its issue that unit could not meet
**Issue:** EMB-243
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A pre-certified radio module's pad-to-SoC-port map becomes an atlas input. Today
a pad's port comes from the schematic symbol's pin name, the SoC datasheet's
pin number (which is not the module's pad number), or, since `atlas/092`, a net
named after a port (`P1.05/RX`). A pad on a bus or a PWM gate whose net is named
for its function (`I2C_SDA`, `PWM_GATE`) has none of these, so its `pins.md` row
prints `(no port: …)` and the engineer adds `pin_names.json` entries by hand.
When this is done the module datasheet's pad table translates into a record
mapping each pad to its SoC port, the way the SoC's pin table is translated, and
`build_pin_map` takes a pad's port from it ahead of the net-name inference,
marking the source in `pins.json`'s `port_source`. How the record is keyed to
the module part, and which wins when it disagrees with the symbol's pin name, is
the worker's to decide and record.

## Why now

On a real module board 17 pads carried no name, and the net-name inference
resolved only some; the rest leave an engineer unable to ask which pins of a
port are free or interrupt-capable.

## Where

- `embarch-atlas/src/embarch_atlas/join.py` `build_pin_map`: the port sources
  and `port_why`.
- `embarch-atlas/DESIGN.md`: the record kinds and the `pin` row; `atlas/092`'s
  "an empty port" line.
- `embarch-doc/embarch-atlas/design.md`.

## Done when

- [ ] A module's pad table translates into a record that maps each pad to its
      SoC port.
- [ ] `pins.md` gives the port and DT use of an unnamed pad on a
      function-named net from that record, marked with its source.
- [ ] A test covers a module fixture whose unnamed pads resolve only through
      the pad table.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `DESIGN.md` and `embarch-doc/embarch-atlas/design.md` updated,
      `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level it made false.
