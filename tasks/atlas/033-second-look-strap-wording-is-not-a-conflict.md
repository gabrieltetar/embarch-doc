# 033 — `second-look compare` does not call agreeing strap readings a conflict over wording

**State:** done
**Source:** a worker's finding, filed to Fleet Ready
**Issue:** EMB-55
**Scope:** atlas
**Hardware:** none — `compare_one` takes two readings and returns a verdict; `tests/test_secondlook.py` already drives it.
**Owner:** no

## What

`second-look compare` (`src/embarch_atlas/secondlook.py`) marks strap readings as `conflict` when the address values agree and only the free-text `condition` is worded differently. For a `strap` item, `compare_one` compares the value with `_same_address`, then sends `condition` through `_condition`, which calls `text_value_verdict`; with no quantity on both sides that takes the share of the second reading's words found in the first, and at or under one third, with no common quantity, it is a `conflict`. Examples with the same value: first pass `fixed` against reader `fixed 7-bit address; no address pin or strap shown on this page`, both 0x6A; `SDO/SA0 = GND` against `SDO/SA0 pin connected to ground (LSb = 0)`, both 1101010b. In one round of 20 items that gave 15 conflicts, every one a wording difference — and recording them would freeze 15 false document-reading conflicts into the mismatch report, since the queue skips an item with a frozen verdict and it would never be looked at again.

When this is done, a strap item compares the address or mode value normalised (0x6A = 1101010b = 106), and treats the `condition` as matching when both name the same pin state or both say the address is fixed. `READER_RULES`'s `strap {"value","condition"}` line tells the reader to keep `condition` to the pin state only, with no commentary. Optionally, `compare` (and `cmd_compare`'s printout) flags "values agree, wording differs" separately from a real conflict.

## Why now

A frozen false conflict is never revisited, so each round that runs under the current rule writes errors into the report permanently.

## Done when

- [x] A strap reading with an equal address value and a differently worded `condition` is `confirmed`, or flagged "wording differs", and is not `conflict` (unit tests on both examples above).
- [x] A strap reading with different address values is still `conflict`.
- [x] The reader prompt tells the reader to state only the pin state in `condition`.
- [x] Any design doc that states the strap compare rule says the new one.
- [x] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [x] `changelog.d/` fragment dropped.

## Done

Strap conditions now compare by named pin state (`pin_states`, `_strap_condition` in `secondlook.py`). An address strap with an agreeing value and no common named state is `unresolved` ("values agree, wording differs"), not `conflict`; the two examples (fixed, GND) are `confirmed`. Mode straps keep the old word-overlap rule. Tests in `tests/test_secondlook.py` cover each box; the design-doc box is `DESIGN.md` in the code repo (no doc-repo text states the rule). Gate run results below in the report.
