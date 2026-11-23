# 094 — A module's pad table gives an unnamed pad its port

**State:** done
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

- [x] A module's pad table translates into a record that maps each pad to its
      SoC port.
- [x] `pins.md` gives the port and DT use of an unnamed pad on a
      function-named net from that record, marked with its source.
- [x] A test covers a module fixture whose unnamed pads resolve only through
      the pad table.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [x] `DESIGN.md` and `embarch-doc/embarch-atlas/design.md` updated,
      `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level it made false.

## Outcome

**Decided.** The record kind is the existing `pin` record with a new optional `port` field (schema + DESIGN.md), keyed to the
module like any pin record (the document covering its MPN, `package` as usual); no new kind, loader or join table. Order in
`build_pin_map`: symbol pin name, pad table `port` (`port_source` `module pad table`), datasheet pin name, net name. The
symbol wins over a disagreeing pad table; `pins.json` carries `port_conflict` and `pins.md` prints `(pad table says X)`.
A port is normalised (`P1.3` -> `P1.03`). `port_why` now names the `port` field as the remedy.

**Tests.** `tests/test_join_nordic.py` synthetic module: pad resolved only via the table (with DT use), table ahead of net
name, symbol-wins conflict, a pad with no row still saying why. Full suite 978 passed.

**Not exercised.** Whether the `atlas-translate-docs` pin-table pass fills `port` from a real module datasheet's pad table
is untried (it needs an LLM pass over a real datasheet); the skill text was not changed, so until it is told to emit `port`
the field is filled by hand or by `engineer-declared` records.
