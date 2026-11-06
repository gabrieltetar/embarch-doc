# 036 — `codecheck` keeps a hex-addressed register whose name ends in OFFSET

**State:** claimed by agent/atlas/036-codecheck-keeps-a-hex-addressed-offset-register, 2026-11-06 13:32
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

- [ ] A hex-addressed register define ending in OFFSET (generic part prefix, a value such as `0x12`) classifies as `register` (unit test).
- [ ] A bit-offset define ending in OFFSET or OFS with a small value still classifies as `encoding` (unit test).
- [ ] A test on a source excerpt with a bit-offset define followed by masks asserts no `reg-field-in-other-register` or `reg-mask-vs-field` against the phantom address.
- [ ] `DESIGN.md` says the rule if it describes `classify`'s tokens.
- [ ] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `changelog.d/` fragment dropped.

## Notes for the worker

Fixture part prefixes and names must be generic: `test_public_guard` rejects real part names.
