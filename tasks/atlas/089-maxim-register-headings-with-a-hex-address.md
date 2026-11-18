# 089 — Read Maxim register headings with a `0x..` address and a summary table carrying defaults

**State:** open
**Source:** Fleet Ready issue: `doc regparse --template maxim` found 0 registers on a Maxim fuel-gauge datasheet ("no line came close"), while a third Maxim fuel gauge parses with 235 registers, so the template reads one Maxim layout and misses others.
**Issue:** EMB-34
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The `Maxim` template in `src/embarch_atlas/regparse.py` reads the layout the owner pasted from a MAX17048-style datasheet:

- **Heading:** `STATUS Register (0x1A)`, `VALRT Register (0x14)`, `CMD Register (0xFE)`. The address is a `0x`-prefixed hex byte, where the template expects `(<NNN>h)`.
- **Summary table** (one per document): columns `ADDRESS`, `REGISTER NAME` (wrapped over two header lines), `16-BIT LSb`, `DESCRIPTION`, `READ/WRITE`, `DEFAULT`; rows like `0x0C CONFIG — Compensation to optimize ... R/W 0x971C`, with `—` for no LSb and `—` for no default.

Each register found by its heading takes its default from the summary table's `DEFAULT` column, and a register named in the table with no heading, or a heading with no table row, is reported the way the template reports any other mismatch.

## Why now

The owner pasted the headings and the summary table on the issue, which is what the earlier send-back asked for. The second Maxim layout on the issue, a single bit-column register map with no per-register headings, is `atlas/090`.

## Dispatch notes

- This layout's registers are 16-bit words like the layout the template already reads; whether its bit diagrams (if any) use the existing D15..D0 form is not known from the issue. Read what the template already does with a register that has no bit diagram, and say it in `DESIGN.md`.
- The issue's second symptom, flash command headings taken as registers, is not seen on these datasheets and stays open on the issue: do not guess at it. If tightening the heading regex for `0x..` makes a command heading less likely to match, say so; do not claim it fixed.
- `Maxim` reads the source PDF with PyMuPDF, not the text layer. Fixtures are **synthetic** PDFs built the way `tests/regparse_synth.py` builds its Maxim ones, with invented register names; no vendor text goes into the repo.
- The layout the template reads today must parse exactly as before.
- No file of this sub-project is in reserve.
- **Owed, owner-side, not a Done-when item:** `doc regparse --template maxim` on the real datasheet. Write that into the task file's closing note as a debt.

## Done when

- [ ] A synthetic document with `Name Register (0x..)` headings and the summary table above yields its registers, each with its address and its `DEFAULT`.
- [ ] A table row with no heading, and a heading with no row, are each reported.
- [ ] The existing Maxim fixtures' output is unchanged (`tests/test_regparse.py` stays green).
- [ ] `DESIGN.md` says which Maxim layouts the template reads.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
