# 094 — `embarch-umbrella/open.md` is inside its reserve floor

**State:** blocked — until the open.md debts named on In flux close (verification legs for checks 13, 15, 17, 5, decisions 51 and 58)
**Source:** `umbrella/093`, 2026-10-28. Its owner-debt bullet for decision 58 took `open.md` to 4,098 B of 5,120 B, 80% of cap, 1,022 B left.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

**Compacts:** embarch-umbrella/open.md
**Size debt due:** 2026-11-11
**In flux:** yes — `open.md` is a list of hardware debts that close as legs verify them (checks 13, 15, 17, 5; decisions 51 and 58); each one that closes deletes its own bullet, so the file shrinks without a pass.
**Must not delete:** any bullet whose debt is still unverified, and the hardware-debt protocols they quote (check 17's three-step protocol pointer, decision 51's, decision 58's owner run).

## What

`embarch-umbrella/open.md` is 4,098 B against a 5,120 B cap. Fold verified or settled bullets out; do not trim a live debt to make room.

## Done when

- [ ] `open.md` is clear of its reserve floor, every `Must not delete:` item still readable.
- [ ] `changelog.d/` fragment. Gate green.
