# 037 — `second-look` reads a high-impedance strap as floating, not VDD

**State:** done
**Source:** a reviewer's finding on `atlas/033`, filed to Fleet Ready
**Issue:** EMB-80
**Scope:** atlas
**Hardware:** none — unit tests on strap conditions; no board, no west.
**Owner:** no

## What

`pin_states` in `src/embarch_atlas/secondlook.py` (added by `atlas/033`) splits a strap `condition` into `[a-z0-9]+` tokens and maps them through `_PIN_STATES`. `high` is a VDD word and `open` a floating word, so "high-impedance" names VDD and "open-drain" names floating. Two readings that both mean a floating pin, "floating" and "high-impedance", then name disjoint states and `_strap_condition` records a `conflict` — and a conflict frozen into a round is never revisited. Negations ("not floating") are not seen either, and the match is a set intersection, so "GND or VDD" matches "VDD".

When this is done, "high-impedance", "hi-z" and "high-Z" name the floating state, "open-drain" names no pin state, a negated state is not counted as that state, and two readings that mean the same pin state never conflict on wording.

## Why now

The strap rule landed on 2026-11-06 to stop false conflicts on wording; the reviewer found this as a new source of exactly that, and a frozen false conflict outlives the round that made it.

## Done when

- [x] A strap read as "floating" by one pass and "high-impedance" by the other is not `conflict` (unit test).
- [x] "open-drain" in a condition names no pin state (unit test).
- [x] A negated state ("not floating") is not counted as that state (unit test).
- [x] "SEL = GND" against "SEL = VDD" is still `conflict` (the existing test passes).
- [x] `DESIGN.md`'s compare paragraph says the new rule if it lists the pin-state words.
- [x] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [x] `changelog.d/` fragment dropped.

## Notes for the worker

Fixture part and strap names must be generic: `test_public_guard` rejects real part names. Do not bump `CHECKED_VERSION`; `DESIGN.md` names a deliberate bump as the route for re-checking frozen rounds.

## Done

`pin_states` now rewrites high-impedance/hi-z/high-Z to floating, drops open-drain/collector, and drops a negated word before tokenizing. Unit tests cover each box; the DESIGN.md box was ticked on reading (paragraph edited). "GND or VDD" matching "VDD" (set intersection) is unchanged, not required by Done-when.
