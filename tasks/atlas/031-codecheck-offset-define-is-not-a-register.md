# 031 — `codecheck` does not take a bit-offset define for a register address

**State:** done
**Source:** a worker's finding, filed to Fleet Ready
**Issue:** EMB-52
**Scope:** atlas
**Hardware:** none — `classify` and the mask association run on C source text a test can write.
**Owner:** no

## What

`codecheck` (`src/embarch_atlas/codecheck.py`) reads a bit-offset define as a register address and then attributes the masks that follow it to that register by position. In the Zephyr BQ2518x driver, `BQ2518X_SYS_REG_CTRL_OFFSET 5` is a bit offset; it is read as register 0x05, so `BQ2518X_DEVICE_ID_MSK` (used on the MASK_ID read) and `BQ2518X_SHIP_RST_EN_RST_SHIP_MSK` (bits 6:5 of SHIP_RST, 0x09) are both reported as `reg-field-in-other-register` and `reg-mask-vs-field` against 0x05. Both are false. In `classify`, a name containing `REG_` takes the register branch (`is_regish`), and the last token `OFFSET` is in neither `BOUND_TOKENS` nor `ENCODING_TOKENS` (which has `SHIFT` and `POS`), so it ends as `register`. `UnitCheck._assoc0` then ties the masks to it by its final `position (under ...)` rule, `strong=False`.

When this is done, `*_OFFSET`, `*_SHIFT` and `*_POS` defines are not register addresses, and a mask is tied to the register named in its own prefix (`<PART>_<REG>_...`) or to the register it is used with at the access site, in preference to its position under the last register define. `_check_masks` and `_mask_finding` raise nothing from a positional association that a prefix or an access site contradicts.

## Why now

Two false findings on one small driver, both against a register the driver never touches, and the same rule applies to every driver that names its bit offsets this way.

## Done when

- [x] `BQ2518X_SYS_REG_CTRL_OFFSET` is not listed as register 0x05 (unit test on a source excerpt shaped like the driver's).
- [x] `BQ2518X_DEVICE_ID_MSK` and `BQ2518X_SHIP_RST_EN_RST_SHIP_MSK` raise no `reg-field-in-other-register` or `reg-mask-vs-field` against 0x05.
- [x] A real register define whose name ends in a different token is still found.
- [x] Any design doc that states the classify or association rule says the new one.
- [x] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [x] `changelog.d/` fragment dropped.

## Done

`ENCODING_TOKENS` in `codecheck.py` gained `OFFSET` and `OFS`, so a `REG_`-named define ending in one classifies as `encoding`, not `register`; with no phantom register, the masks that followed it have no positional association to it. Prefix and access-site association were already preferred over position in `_assoc0`. No design doc states the classify rule, so none changed. Tested at the `classify` level (`test_offset_define_is_not_a_register_address`); no end-to-end driver excerpt was run.
