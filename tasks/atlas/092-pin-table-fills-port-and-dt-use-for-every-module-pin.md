# 092 — The pin table fills the port and DT use for every module pin

**State:** open
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

- [ ] Every module pin that reaches an MCU port shows its port in `pins.md`
      (test with a module fixture whose map is resolved only in part today).
- [ ] The DT column is filled for those rows from pinctrl and gpios.
- [ ] A pin whose port cannot be resolved says why instead of leaving the cell
      blank.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet), including
      `test_public_guard` running, not skipped.
- [ ] `embarch-atlas`'s docs updated where they describe `pins.md`,
      `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level it made false. Fixtures use generic part and net names only.
