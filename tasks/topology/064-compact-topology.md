# 064 — `decisions/link-declares.md` is in reserve after decision 42

**State:** open
**Source:** `scripts/check-doc-size.py`, 2026-10-26, after `tasks/topology/063` added decision 42 (11,155 / 12,288 B, 1,133 B left).
**Scope:** topology
**Hardware:** none
**Owner:** no

**Compacts:** embarch-topology/decisions/link-declares.md
**Size debt due:** 2026-11-09
**In flux:** no — decisions 20, 27, 36 and 42 are settled; `topology/059`, `061` and `062` touch validation, parity and the signal route, not a role's declared link facts.
**Must not delete:** decision 20's interface finding (the DK's lower VCOM accepts bytes and never answers; the guess was invisible) and its rejected handshake alternative; decision 42's note that the vacated-row choice is reasoned, not measured.

## What

Bring `link-declares.md` out of the reserve band. A verbatim split of decision 42 or 36 into a file named for what it settles is the cheapest move (`DOC-BUDGET.md`).

## Done when

- [ ] `scripts/check-doc-size.py --pressure` no longer lists the file in reserve.
- [ ] Answer in the commit message: can `spec.md` alone answer what someone needs to work on this component today?
