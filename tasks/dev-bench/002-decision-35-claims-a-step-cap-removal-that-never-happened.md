# Reconcile decision 35 with a step cap that was never removed

**State:** open
**Source:** owner's repo survey, 2026-09-06 — a decision asserting an SRAM refactor that is not in the tree
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-dev-bench/decisions/link.md:41` says "One step decoded at a time from the
retained span, and the local step cap goes away… the ceiling disappears, and the crate's constant
goes back to being the one authority", and `decisions/dispatch.md:27` repeats it as done. The code
still holds the cap: `app/src/serial_protocol.h:55` `#define DBM_MAX_STEPS_PER_STUDY 16` with a
20-line comment defending it, `:714` `struct dbm_step steps[DBM_MAX_STEPS_PER_STUDY];`,
`app/src/serial_protocol.c:1419` refusing `steps_len > 16`, and
`app/tests/serial_protocol/src/main.c:1164` pinning that refusal.

**Doc-only: do not implement the refactor.** The doc stops asserting a change that is not in the
tree — decision 35's reasoning preserved but restated as unimplemented, either moved to `open.md`
under a named trigger or kept in `link.md` with an explicit "not implemented as of `<date>`; the
16-step ceiling and the host/wire divergence it names are both still live". `dispatch.md:27`'s
parenthetical is split, since decision 40's half (the retired `gatt_activity` field) genuinely did land.

## Why now

`embarch.md` §3 makes `spec.md`/`decisions.md` the source of truth for what is true now. A decision
claiming an SRAM refactor happened is the divergence `../../embarch-decision-reversals.md` exists to
make visible, and it currently hides a real host-accepts-20 / wire-refuses-20 gap.

## Done when

- [ ] No doc states the 16-step cap was removed.
- [ ] The still-live divergence (crate `MAX_STEPS_PER_STUDY` = 64, bench = 16) is stated once, where
      an author of a long study would find it.
- [ ] Decision 35's number is not reused or renumbered; `scripts/check-decision-refs.py` still
      resolves every reference to it.
- [ ] `decisions/dispatch.md:27` no longer bundles an unimplemented change with an implemented one.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
