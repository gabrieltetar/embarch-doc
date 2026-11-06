# 029 — `atlas join` decodes devicetree pin use on Nordic nRF targets

**State:** claimed by agent/atlas/029-join-decodes-nordic-devicetree-pin-use, 2026-11-06 12:37
**Source:** a worker's finding, filed to Fleet Ready
**Issue:** EMB-50
**Scope:** atlas
**Hardware:** none — `tests/test_dt.py` already drives `extract_edt` with a fake edtlib object; Nordic controllers and `psels` go in the same fake.
**Owner:** no

## What

On a Nordic nRF target `embarch-atlas join` decodes no devicetree pin use at all. On an nRF54L15 board the summary reads `0 MCU pins in DT, 0/0 I/O pins reach a part`, the pin map's DT column is empty, and six pin-level checks ("DT pin reaches the board", "I2C device signals land on the DT pins", "one DT owner per pin", "pinctrl function vs net name", "DT pull vs board pull", "GPIO polarity vs net name") run with nothing to check without saying why. Two false candidates follow: `open-drain-no-pull` reports `DT flags []` for a line whose DT entry has `GPIO_PULL_UP`, because the flags were never read, and `dt-no-driver` lists 11 SoC infrastructure nodes that nrfx drives without a Zephyr device (DPPIC, PPIB, MPC, UICR, GPIOTE).

The cause is in `extract_edt` (`src/embarch_atlas/dt.py`):

1. GPIO controllers are recognised only by an STM32 compatible or a label matching `gpio[a-z]`. Nordic controllers are `nordic,nrf-gpio` with labels `gpio0`, `gpio1`, `gpio2`, so `gpio_controllers` is `{}` and every `*-gpios` phandle is skipped.
2. pinctrl is read only from `pinmux` (decoded by `stm32_pinmux`). Nordic pinctrl uses `psels = <NRF_PSEL(fun, port, pin)>`, which is never read.
3. The pin map names Nordic pins `P0.04`, while the GPIO use builder emits `P{letter}{pin}` (STM32 style), so even a decoded use would not match. `join.py`'s `build_pin_map` already recognises `P\d\.\d{1,2}` in the datasheet-name match.

When this is done, `nordic,nrf-gpio` controllers are decoded by their `port` property (or the label digit), `psels` through the `NRF_PSEL` encoding (function, port, pin; pull flags from `bias-*`), Nordic pins are named `P<port>.<pin:02>`, `checks.md` says when a check had no input because the family has no decoder, and `dt-no-driver` (`src/embarch_atlas/mismatch.py`, the `R.cand("dt-no-driver", ...)` block and `dt_intent` folding) folds SoC infrastructure nodes as expected on Nordic targets.

## Why now

Every pin-level check is silently empty on a whole MCU family, and the two false candidates it does raise are what an engineer would read first.

## Done when

- [ ] On an nRF54L15-shaped fake EDT, `dt.json` has `gpio_controllers` for `gpio0`, `gpio1` and `gpio2`, and pinctrl `psels` uses with pin names `P<port>.<pin:02>`.
- [ ] The pin map's DT column is filled for pins used in devicetree, and the pin-level checks list a non-zero "ran".
- [ ] `open-drain-no-pull` shows the DT flags of a pulled-up line and is not raised for it.
- [ ] `dt-no-driver` does not list DPPIC, PPIB, MPC, UICR or GPIOTE nodes as candidates.
- [ ] On a family with no decoder, `checks.md` says the pin checks had no input because the family is unsupported.
- [ ] The STM32 path is unchanged (its existing tests pass untouched).
- [ ] `DESIGN.md` and `embarch-doc/embarch-atlas/design.md` name the families whose pin use is decoded.
- [ ] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `changelog.d/` fragment dropped.
