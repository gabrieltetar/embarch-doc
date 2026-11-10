# 040 — Check U finds a unit as a token and reads a symbol whole

**State:** done 2026-11-09. The font case (µ/Ω printed as `m`/`W`) was not confirmed and no fixture shows it: left out of scope.
**Source:** Linear issue EMB-41, filed by a session
**Issue:** EMB-41
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Check U's two tests stop passing or failing on accidents of spelling:

- **The unit-on-page test finds the unit as a token.** `record_checks` decides a unit is on the cited page with `any(f in page for f in _unit_forms(rec["unit"]))` (`check.py:638` at the split), a plain substring test on the normalised page, so a record in `µA` passes because `ua` sits inside "guaranteed".
- **A symbol is read as a whole.** `check_unit` takes a symbol's expected dimension from its first character (`SYM_DIM.get(sym[0])`, `check.py:562`), so the symbol `LoadReg` is read as an inductance and a unit `A` or `V` on it is reported `unit ... does not fit symbol LoadReg`. A multi-letter name that is not a known electrical symbol gets no dimension from its first letter.

The issue also reports a font that prints µ and Ω as `m` and `W` failing the same test. That case is not confirmed: treat it as out of scope unless a fixture shows it, and say in the task which way it went.

## Why now

Filed from distilling a real datasheet. A false pass on U is the worse half: it certifies a unit nobody checked.

## Where to look

- `src/embarch_atlas/check.py` `record_checks` — the `U` block, `on_page`
- `src/embarch_atlas/check.py` `_unit_forms` — the spellings tried
- `src/embarch_atlas/check.py` `check_unit` — symbol to dimension, `SYM_DIM`, `PARAM_DIM`

## Dispatch notes

- **Burndown leg: no new numbered decision.** Refining an existing `DESIGN.md` decision in place is fine; if the fix needs a new one, stop and say so in this file.
- No `embarch-atlas` doc is in its size reserve.
- Close by rewriting the `State:` line so `done` (or `blocked`) is its first word with nothing glued to it — `done,` and a left-over `claimed` are both refused by `check-task-state.py`.

## Done when

- [x] A record with unit `µA` on a page that has `guaranteed` and no `µA` fails U.
- [x] A record with symbol `LoadReg` and unit `A` or `V` is not reported by U for its symbol.
- [x] Units already on a page as `µA`, `uA` or `ohm` still pass; tests in `tests/test_check.py` cover all of these.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [x] `DESIGN.md` updated where it describes check U, `changelog.d/` fragment dropped.
