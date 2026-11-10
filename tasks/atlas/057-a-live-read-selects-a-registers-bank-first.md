# 057 — A live read selects a register's bank before reading it

**State:** claimed by agent/atlas/057-a-live-read-selects-a-registers-bank-first, 2026-11-10 02:22
**Source:** Linear issue EMB-124, filed by the `atlas/054` worker
**Issue:** EMB-124
**Scope:** atlas
**Hardware:** verify-only
**Owner:** no

## What

Since `atlas/054`, a `register` record may state a `bank`, and `embarch-atlas live` reads `<label>.<REG>@<bank>` from that bank's record (`src/embarch_atlas/live.py` `_ext_regs`, `ext_reg_read`). It then reads the address alone: nothing selects the page on the part first, so the value comes from whatever page the part is on. Which register selects a page, and the value per bank, is in no record.

Add both halves: a record (a new field on an existing kind, or the part's `bus` record, the worker's pick) stating how a bank is selected on the part — the select register and its value per bank — and, in `ext_reg_read`, a select, read, restore sequence that puts the previous page back afterwards.

## Why now

A live read of a paged part's banked register returns a value from the wrong page, silently.

## Where to look

- `src/embarch_atlas/live.py` `_bank`, `_pick_bank`, `_ext_regs`, `ext_reg_read`, and how `allow_clear` guards a read that changes the part
- `DESIGN.md` record-kind table (`register`, `field`, `bus`) and the live-read section
- `src/embarch_atlas/schema` (or wherever the record schema lives) and `tests/` for the fake shell the live tests use

## Dispatch notes

- **A page select is a write, and the read tool declares itself read-only.** So: no write without the caller opting in, the way `allow_clear` gates a read that clears. Without the opt-in a read of a banked register on a part that states how to select a bank refuses and names the opt-in; a part that states none reads as today and says the page was not selected. Restore the previous page even when the read fails. Say in the report what the opt-in is called and how the restore reads the previous page.
- Burndown is on: no new numbered decision. The atlas has none; describe the field and the sequence where `DESIGN.md` describes `register` and the live read, in place.
- Nothing touches hardware: tests run against the fake shell. Verification on a board with a paged part is a debt for the log, not yours.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.

## Done when

- [x] A record states how a bank is selected on the part, in the schema and `DESIGN.md`.
- [x] `ext_reg_read` selects the bank, reads and restores the previous page, behind an explicit opt-in, with tests against the fake shell (opt-in absent, present, read failing).
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
- [ ] Verified on a board with a paged part (debt, recorded at the fold).

## Done

`bus.bank_select` = `{reg, values: {<bank>: <value>}}` (schema, `records.py`, DESIGN.md in place). Opt-in `allow_bank_select` (CLI `--allow-bank-select`; MCP `reg_read_bank`, a write tool). Sequence: `read_byte` of the select register (previous page, once), `write_byte` bank value, reads, `write_byte` previous page back, in every exit path. Tests in `tests/test_live.py` against the fake shell (extended with `write_byte` and `_fail`).

**Hardware-verification debt:** run `embarch-atlas live reg-read <label>.<REG>@<bank> --allow-bank-select` on a board with a paged I2C part whose `bus` record states `bank_select`; confirm the value is from the bank and the page register reads its old value afterwards. Assumes an 8-bit, readable select register.
