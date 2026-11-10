# 054 — A register record can state its bank, and lookups key on bank and address

**State:** open
**Source:** Linear issue EMB-46, filed by a session
**Issue:** EMB-46
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`register` records carry `name`, `addr`, `width`, `reset`, `access`, `summary` and `desc`, and nothing that says which page or bank a register is on. On a sensor with paged register maps (an embedded-function page and a sensor-hub page beside the main one), two registers at the same address on different pages read as one address with two names: check G reported 59 duplicate addresses on one such part. Codecheck's register map and the live module also key a register by address alone.

Add an optional `bank` to `register` records (and to the `field` records that point at a banked register), and make check G, codecheck's `RegMap` and the live module key on `(bank, addr)`. A register with no `bank` behaves exactly as today.

## Why now

Every paged-register part fails check G with false duplicates, and an address alone is ambiguous for codecheck and the live module on the same parts.

## Where to look

- `schemas/record.schema.json` — the `register` and `field` kinds; no page property
- `src/embarch_atlas/records.py` `FACT_KEYS["register"]` — rendering order
- `src/embarch_atlas/check.py` `_structure` — `seen[a]` by address, emits `address {a:#x} is also {seen[a]}`
- `src/embarch_atlas/codecheck.py` `RegMap.__init__` (`self.regs_at[a]`) and `RegMap.reg`
- `src/embarch_atlas/live.py` `_addr` — turns a register record into one integer
- `DESIGN.md` — the record-kind table's `register` and `field` rows

## Dispatch notes

- Burndown is on: no new numbered decision. The atlas has none anyway; amend `DESIGN.md`'s `register` and `field` rows in place.
- How a `field` names its register's bank (its own `bank`, or inherited through its register reference) is yours to pick; state it.
- The live module selecting a page on the device is out of scope: it has no hardware here. It must pick the right *record* for a bank and address; writing a page-select register is a separate issue if it is needed, and you file it.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.

## Done when

- [ ] `register` records can state a `bank` and the schema accepts it.
- [ ] Check G reports no duplicate for two registers at one address on different banks, and still reports one on the same bank (tests for both).
- [ ] `codecheck` and the live module pick a register by bank and address; a register with no `bank` resolves as before.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
