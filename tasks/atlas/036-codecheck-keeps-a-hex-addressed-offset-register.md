# 036 — `codecheck` keeps a hex-addressed register whose name ends in OFFSET

**State:** done
**Source:** a reviewer's finding on `atlas/031`, filed to Fleet Ready
**Issue:** EMB-79
**Scope:** atlas
**Hardware:** none — synthetic source excerpts; no board, no west.
**Owner:** no

## What

`atlas/031` added `OFFSET` and `OFS` to `ENCODING_TOKENS` in `src/embarch_atlas/codecheck.py`, so `classify` returns `encoding` for every `REG_`-named define whose last token is one of them. A real register whose name ends in OFFSET — an offset-calibration register, a `X_REG_ADC_OFFSET 0x12` shape — is now `encoding`, gets no address, and is silently never compared. The same hazard already applies to `*_POS`, `*_SHIFT`, `*_BLOCK` and `*_FLAG`; fix it for OFFSET and OFS here, and say in the Done section whether the same value test is safe for the others.

Separately, `atlas/031`'s two mask criteria — a mask that follows a bit-offset define raises no `reg-field-in-other-register` or `reg-mask-vs-field` against the phantom register — were ticked on reading: `test_offset_define_is_not_a_register_address` checks `classify` on four names and never runs `UnitCheck._assoc0`, `_check_masks` or `_mask_finding`.

When this is done, a `REG_`-named define ending in OFFSET or OFS is `encoding` only when it reads as a bit offset (a small value, under 64, or a body that is not a hex address), a hex-addressed one stays `register`, and a source-excerpt test runs the association and the mask checks end to end.

## Why now

The fix landed on 2026-11-06 and traded one false positive for a silent miss, which is the failure `codecheck` exists to prevent; the reviewer named both halves.

## Done when

- [x] A hex-addressed register define ending in OFFSET (generic part prefix, a value such as `0x12`) classifies as `register` (unit test).
- [x] A bit-offset define ending in OFFSET or OFS with a small value still classifies as `encoding` (unit test).
- [x] A test on a source excerpt with a bit-offset define followed by masks asserts no `reg-field-in-other-register` or `reg-mask-vs-field` against the phantom address.
- [x] `DESIGN.md` says the rule if it describes `classify`'s tokens.
- [x] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [x] `changelog.d/` fragment dropped.

## Notes for the worker

Fixture part prefixes and names must be generic: `test_public_guard` rejects real part names.

## Done

`classify` (`src/embarch_atlas/codecheck.py`): a `REG_` define whose last token is OFFSET or OFS stays `register` when its body is a hex literal (`0x12`), unless an earlier token names a bit (BIT, BITS, SHIFT, POS, FIELD, FLD). A decimal, an expression or a `BIT(n)` body is still `encoding`.

- **The "under 64" test was not used.** The task's own example, `0x12`, is under 64, so a value test would have made it `encoding` and contradicted the first Done-when. The test is the body's spelling: a hex literal reads as an address, a decimal as a bit offset. Residual miss: a register written in decimal (`X_REG_ADC_OFFSET 18`) is still `encoding`; a bit offset written in hex without a bit token in its name is still `register`.
- Third box is a real end-to-end test (`test_bit_offset_define_adds_no_phantom_register_findings`) through `cc.run`, so `_assoc0`, `_check_masks` and `_mask_finding` all run. Fixture: an unprefixed mask after a bit-offset define is tied to the last register define above it; with the fix reverted the test fails (measured), so it guards the phantom.
- `DESIGN.md` box ticked on reading: `embarch-doc/embarch-atlas/design.md` and the code repo's `DESIGN.md` do not describe `classify`'s tokens (grep for OFFSET, SHIFT, encoding), so there was no rule to restate.
- **`*_POS`, `*_SHIFT`, `*_BLOCK`, `*_FLAG`:** a value test is not safe for any of them, and no change was made. `POS`/`SHIFT` carry a hex body only by accident of style and a register named `*_POS` is implausible, so they stay `encoding`; `BLOCK` and `FLAG` have no bit-offset meaning in the value at all (a block index or a flag can be any number), so no value or spelling test separates them from a register. Not tested for them, reasoning only; a real hit would need a separate issue.
