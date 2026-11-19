# 090 — Read a Maxim register map printed as one bit-column table with no per-register headings

**State:** claimed by agent/atlas/090-maxim-bit-column-register-map, 2026-11-19 04:06 — resumed: the 00:25 claim's worker died with its leg at 00:30; its uncommitted tree is `d80aa9f` on the branch
**Source:** Fleet Ready issue: `doc regparse --template maxim` found 0 registers on a Maxim optical-sensor datasheet and noted three bit diagrams that name no register address.
**Issue:** EMB-34
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The `Maxim` template (or a sibling template, if that is cleaner, and `DESIGN.md` says which) reads the MAX30102-style layout the owner pasted: **one register-map table** with columns `REGISTER`, `B7` through `B0`, `REG ADDR`, `POR STATE`, `R/W`, and **no heading per register**. A row names the register (wrapped over two lines, `Interrupt` / `Status 1`, `FIFO` / `Configuration`), places each field under the bits it occupies (`A_FULL` under B7, a name split over two lines like `PPG_` / `RDY`, a multi-bit field written `SMP_AVE[2:0]` or `FIFO_A_FULL[3:0]` spanning its columns), then gives the address `0x00`, the power-on state `0X00` (either case of `x`) and the access.

Each row becomes a register record with its address, reset (the POR state) and access, and fields with bit ranges taken from the `[m:n]` suffix where printed and from the column span otherwise. These registers are **8-bit**, where the template's existing layouts are 16-bit words.

## Why now

The owner pasted the table on the issue, which is what the earlier send-back asked for. The other Maxim layout on the issue is `atlas/089`.

## Dispatch notes

- `Maxim` reads the source PDF with PyMuPDF, so the column positions are available from word coordinates rather than from the text layer's spacing. Use them for the column span; say in `DESIGN.md` what a field whose span disagrees with its `[m:n]` suffix produces (that is a document error worth an `Issue`).
- Register width is per layout, not per template: the 16-bit layouts must keep reading as 16-bit.
- Fixtures are **synthetic** PDFs, built the way `tests/regparse_synth.py` builds its Maxim ones, with invented register and field names; no vendor text goes into the repo.
- No file of this sub-project is in reserve.
- **Owed, owner-side, not a Done-when item:** `doc regparse --template maxim` on the real datasheet. Write that into the task file's closing note as a debt.

## Done when

- [ ] A synthetic bit-column register map yields one 8-bit register per row with address, POR state and access, and its fields with correct bit ranges, including a wrapped register name and a wrapped field name.
- [ ] A field whose column span disagrees with its `[m:n]` suffix is reported.
- [ ] The existing Maxim fixtures' output is unchanged (`tests/test_regparse.py` stays green).
- [ ] `DESIGN.md` says which Maxim layouts are read and how register width is chosen.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
