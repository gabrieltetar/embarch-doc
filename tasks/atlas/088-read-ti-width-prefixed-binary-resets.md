# 088 — Read TI register resets printed as width-prefixed binary, and a capital-R `[Reset = ...]` heading

**State:** claimed by agent/atlas/088-read-ti-width-prefixed-binary-resets, 2026-11-19 00:12
**Source:** Fleet Ready issue: on one TI charger datasheet `doc regparse --template ti` found 13 registers and 67 fields, carried no reset value on any of them, and wrote no `conflict` record; four other TI and Maxim datasheets now parse with resets, so this is one TI layout variant.
**Issue:** EMB-33
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The `TI` template in `src/embarch_atlas/regparse.py` reads resets from the layout the owner pasted on the issue, and its `_check_document` conflict pass runs on them:

- **Heading:** `7.5.1.10 SHIP_RST Register (Offset = 0x9) [Reset = 0x11]`. The reset bracket has a capital `R`, and the address is `Offset = 0x9`.
- **Bit diagram:** bit numbers `7 ... 0`, a row of field names (a multi-bit one written `EN_RST_SHIP_1:0`), and access-reset tokens `R/W-1b0`, `R/W-2b00`, `R/W-2b10`: a **width-prefixed binary** (`<width>b<bits>`), not `R/W-<n>` with a `b` or `h` suffix as `FIGTOK` expects.
- **Field table:** header `Bit Field Type Reset Description`, rows like `7 REG_RST R/W 1b0 Software Reset` and `6-5 EN_RST_SHIP_1:0 R/W 2b00 ...`, the reset column in the same width-prefixed form.
- **Status registers** on the same pages print `[Reset = X]` and `R X`: an unknown reset, which must read as unknown, not as a value and not as a conflict.

With those read, each register's heading reset, field-table resets and bit-diagram resets are compared as for any other TI layout, so a disagreement among them is a `conflict` record.

## Why now

The owner pasted one register exactly as it prints, which is what the earlier send-back asked for.

## Dispatch notes

- Find which of `HEAD`, `FIGTOK`, `TABLE_HDR`, `_heading_reset`, `_reset_spec` and `_field_reset` drops the value, and name the cause in `DESIGN.md` and the changelog fragment; that is the investigation half of the issue.
- A width-prefixed binary is width `N`, then `b`, then exactly `N` binary digits. Say what the parser does when the digit count disagrees with the width: that is itself a document error worth an `Issue`.
- Fixtures are **synthetic**, in `tests/regparse_synth.py` style, with invented register names: one register printed consistently, one where the heading's `[Reset = ...]` disagrees with its fields (to prove a conflict is written for this layout), and one status register with `[Reset = X]`. No vendor text goes into the repo.
- The three real conflicts on the owner's datasheet are not identified on the issue, so do not claim them.
- No file of this sub-project is in reserve.
- **Owed, owner-side, not a Done-when item:** `doc regparse --template ti` on the real datasheet, to see its resets and its 3 conflicts. Write that into the task file's closing note as a debt.

## Done when

- [ ] A synthetic register in this layout yields its heading, field-table and bit-diagram resets, and a multi-bit `2b10` reset decodes to its value.
- [ ] A synthetic register whose resets disagree writes a `conflict` record; a `[Reset = X]` register writes none and carries no reset.
- [ ] Every existing TI fixture's output is unchanged (`tests/test_regparse.py` stays green).
- [ ] `DESIGN.md` names the cause and the width-prefixed form.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
