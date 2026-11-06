# 035 — A `join` test runs a Nordic project end to end

**State:** open
**Source:** a reviewer's finding on `atlas/029`, filed to Fleet Ready
**Issue:** EMB-78
**Scope:** atlas
**Hardware:** none — a synthetic netlist and a synthetic `dt.json`; no board, no west.
**Owner:** no

## What

`atlas/029` taught `dt.py` to decode Nordic devicetree pin use, and each step has a unit test: `tests/test_dt.py` drives `extract_edt` with a Nordic-shaped fake EDT; `tests/test_mismatch.py` checks the SoC infrastructure fold, but on the STM32 `make_project` fixture with injected peripherals; `test_mcu_port_spellings` checks that a datasheet's `P0.4` matches the devicetree's `P0.04`. Nothing joins a Nordic `dt.json` with a Nordic board netlist, so nothing asserts that the pin map's DT column is filled or that "DT pin reaches the board" and the other pin-level checks report `ran > 0`. The `port_of_key` and `build_pin_map` changes in `src/embarch_atlas/join.py` that make this work have no Nordic fixture, and `atlas/029` ticked that criterion on how the code is structured rather than on a test.

When this is done, a synthetic Nordic project fixture exists — a small netlist with `P0.xx` and `P1.xx` MCU pins and a Nordic `dt.json` — and a `join` test on it asserts both.

## Why now

The fix landed on 2026-11-06 with this one criterion resting on reading; a fixture is the cheapest way to keep it true, and it is the fixture any later Nordic check will need.

## Done when

- [ ] A `join` test on a synthetic Nordic project asserts the pin map's DT column is filled for pins used in devicetree.
- [ ] The same test asserts the pin-level checks report a non-zero "ran".
- [ ] The STM32 fixtures are unchanged.
- [ ] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `changelog.d/` fragment dropped. If the test finds a real defect, fix it in the same unit and say so in `decisions.md` only if the fix is a design choice.

## Notes for the worker

The fixture's part and board names must be generic: `test_public_guard` rejects real part names.
