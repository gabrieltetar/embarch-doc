# 039 — A step marker in a rule is not a numeric claim

**State:** claimed by agent/atlas/039-a-step-marker-in-a-rule-is-not-a-numeric-claim, 2026-11-09 19:24
**Source:** Linear issue EMB-38, filed by a session
**Issue:** EMB-38
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Check M stops reading a parenthesised step marker inside a clause, `(1)`, `(2)`, as a number the page has to anchor. A real number in parentheses still counts.

Today `md_claims` and `_clause_claims` strip `_STRIP_BEFORE_NUMBERS` before reading numbers, and `NOT_CLAIMS` covers `3.` or `3)` at a line start, `Tier N`, token counts and backticked identifiers, but not `(n)` mid-clause. A number on no cited page and in no verified record is `unanchored` in `check_markdown_file`, and any unanchored number makes `doc check` exit 1, so a non-chip document with numbered steps fails outright. Reproduced on `main` at the split:

```
cd src && python3 -c "from embarch_atlas.check import md_claims; print(md_claims('(1) set A (2) set B'))"
[(1.0, None), (2.0, None)]
```

## Why now

Filed from distilling a real document: numbered steps in a rule were reported as unanchored numbers.

## Where to look

- `src/embarch_atlas/check.py` `NOT_CLAIMS` — the patterns for what is not a claim
- `src/embarch_atlas/check.py` `md_claims` — reads one line's numbers
- `src/embarch_atlas/check.py` `check_markdown_file` — reports `unanchored` and `record_elsewhere`

## Done when

- [ ] The command above prints no claim for `(1)` and `(2)`.
- [ ] A footnote reference such as `fn 13`, a bit range `[7:5]` and a real number in parentheses, `(5 V)`, behave as before.
- [ ] Tests in `tests/test_check.py` cover the markers and the three unchanged cases.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `DESIGN.md` updated where it lists what is not a claim, `changelog.d/` fragment dropped.
