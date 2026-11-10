# 041 — Check S reads a dimension cell as one value

**State:** claimed by agent/atlas/041-check-s-reads-a-dimension-cell-as-one-value, 2026-11-09 20:03
**Source:** Linear issue EMB-37, filed by a session
**Issue:** EMB-37
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A value cell whose numbers are joined by `×` (`1.5 × 2.0`) is one dimension, and check S no longer flags it as several values packed into one cell. A cell of two bare numbers (`1.0 2.0`) is still flagged.

Today `check_tables` flags a value cell as `packed` when it holds more than one number, has no `<br>`, and matches no `[A-Za-z=x]` (`check.py:1141` at the split). `×` is not in that exclusion, so under a `Min`, `Typ` or `Max` column `1.5 × 2.0` gives `{'check': 'packed', 'cell': '1.5 × 2.0'}`, and an S failure makes `doc check` exit 1.

## Why now

Filed from distilling a real datasheet, where a package dimension failed the check.

## Where to look

- `src/embarch_atlas/check.py` `check_tables` — the `packed` test

## Done when

- [ ] A cell like `1.5 × 2.0` is not reported by S; a cell like `1.0 2.0` still is.
- [ ] A test in `tests/test_check.py` covers both, from a pipe table with header `| Param | Sym | Min | Typ | Max |`.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `DESIGN.md` updated if it describes the packed-cell rule, `changelog.d/` fragment dropped.
