# 092 — The pin table fills the port and DT use for every module pin

**State:** done
**Source:** Fleet Ready issue, an audit finding while listing a board's free interrupt-capable pins
**Issue:** EMB-237
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`pins.md` shows the MCU port and the devicetree use for every module pin that
reaches an MCU port. Today, for a board built on a pre-certified radio module,
module pins 15 to 31 carry a net and a far end but no port and no DT use,
although the devicetree assigns them (I2C, PWM, GPIO outputs, an alert line);
pins 1 to 14 and 32 onwards have both. The fault is in the module-pin to
MCU-port join when `pins.md` is built, for a module whose pin map is only
partly resolved.

## Why now

Questions such as "which interrupt-capable pins are free" depend on the port of
every pin; with half the rows blank the table answers them wrongly.

## Where

The module-pin to MCU-port join in `pins.md`'s build. Find first why the map
resolves for some module pins and not others (a second pin-map source, a
page or table the distillation stopped at, a naming mismatch), and record the
cause in the change.

## Done when

- [x] Every module pin that reaches an MCU port shows its port in `pins.md`
      (test with a module fixture whose map is resolved only in part today).
- [x] The DT column is filled for those rows from pinctrl and gpios.
- [x] A pin whose port cannot be resolved says why instead of leaving the cell
      blank.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet), including
      `test_public_guard` running, not skipped.
- [x] `embarch-atlas`'s docs updated where they describe `pins.md`,
      `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level it made false. Fixtures use generic part and net names only.

## Outcome

**Cause (measured on a real module board, pads 15 to 31).** It is not the join: the symbol prints a pin name for only
some pads of the module, and the 17 unnamed pads (15 to 31) have `name: None` in `netlist.json`. `port_of_key` reads the
name, so it finds no port; the datasheet fallback (`ds_by_num`) has no row either, because the translated datasheet is
the SoC's, whose pin numbers are not the module's pads. No port means `uses_by_pin.get(port)` is never consulted, so the
DT column stays empty, and `pins.md` printed `port or name or ''`: a blank cell.

**Change.** `build_pin_map` (src/embarch_atlas/join.py): a pad with no port takes one from a net named after it
(`P1.05/RX`, whole segment, `net_port`), recorded as `port_source` and printed `P1.05 (from net name)`; the DT column then
fills from pinctrl and gpios as for any pad. A non-rail, connected pad still without a port carries `port_why` and prints
`(no port: ...)` naming the remedy. DESIGN.md updated; test in tests/test_join_nordic.py.

**Not closed.** A pad whose net is not port-named (the bus, GND-less signal nets) still has no port until the engineer adds
`pin_names.json` or the module's own pad table is translated: the information is not in any atlas input. It now says so.
Suggest an issue: a module pad table (pad -> SoC port) as a translated record kind. Not filed from here.
