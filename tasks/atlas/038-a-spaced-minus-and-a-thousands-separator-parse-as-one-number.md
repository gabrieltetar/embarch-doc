# 038 — A spaced minus and a thousands separator parse as one number

**State:** open
**Source:** Linear issue EMB-36, filed by a session
**Issue:** EMB-36
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`numbers` in `src/embarch_atlas/check.py` reads `– 0.3` as -0.3 and `1,000` (and `1 000`) as 1000, everywhere a plain number is found today. Checks N, C and M all read numbers through it, so each stops comparing a sign-dropped or split value against the page.

Today `NUM_RE` takes a sign only when it is directly against the digits, and has no thousands separator. Reproduced on `main` at the split:

```
cd src && python3 -c "from embarch_atlas.check import numbers; from embarch_atlas.pdftext import normalize; print(numbers(normalize('– 0.3')), numbers(normalize('1,000')))"
[0.3] [1.0, 0.0]
```

## Why now

Filed from distilling a real datasheet: a negative limit written with a space after the minus read as positive, and a four-digit value split into two numbers.

## Where to look

- `src/embarch_atlas/check.py` `NUM_RE` — the pattern: the sign lookbehind and the digit groups
- `src/embarch_atlas/check.py` `numbers` — used by N, C and M (`DocText.page_numbers`, `md_claims`)
- `src/embarch_atlas/check.py` `_CELL_NUM` — check K's cell parser, which takes no separator either; make it agree with `numbers`

## Done when

- [ ] The command above prints `[-0.3] [1000.0]`.
- [ ] A hyphen between two numbers (`10-90%`, `3..23`) and `±X` parse as before.
- [ ] Tests in `tests/test_check.py` cover the spaced minus, a comma and a space thousands separator, and the unchanged cases.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `DESIGN.md` updated where it describes number parsing, `changelog.d/` fragment dropped.
