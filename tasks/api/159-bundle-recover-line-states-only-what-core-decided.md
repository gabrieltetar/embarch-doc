# 159 — The bundle README's recover line states only what Core decided

**State:** claimed by agent/api/159-bundle-recover-line-states-only-what-core-decided, 2026-11-17 19:19
**Source:** EMB-203, a reviewer finding on `api/158`: the bundle README's nRF54L recover line says Core's decisions map the vendor runner's `--erase` to the range erase, and no Core decision says that
**Issue:** EMB-203
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`src/bundle.rs` (`FAMILIES`, the `nrf54l` entry's `recover` text and its
comment) tells a bench reader to run the program command again, because "Core's
decisions record the vendor runner's `--erase` as the recovery and map it to
that range erase". `embarch-api/interfaces/tools-bundle.md` repeats the claim.

What the two Core decisions actually say:

- `embarch-core` decision 32 (`embarch-core/decisions/flashing.md`): a plain
  non-erase flash does not recover the board; the vendor's own runner with
  `--erase`, on the same image, does. That recovery is measured.
- `embarch-core` decision 36 (`embarch-core/decisions/flash-backend.md`): when
  Core's own flash asks for an erase, the vendor runner is invoked with
  `chip_erase_mode=ERASE_RANGES_TOUCHED_BY_FIRMWARE`. Nobody has confirmed that
  mode on silicon. It does not say decision 32's `--erase` is that mode.

Reword the recover line and its `tools-bundle.md` bullet so they state only
that: decision 32 measured the vendor runner's `--erase` as the recovery, and
the range-erase program line is Core's own erase request, unconfirmed on a
board. Read both decisions' text before writing; the last two units on this
README were written from summaries and each drew a reviewer finding. Keep the
program line and its "not yet confirmed on a board" label as they are
(`api/158`). Add or extend a test so the README no longer says decision 36 maps
anything.

**No new numbered decision** (burndown). If the honest recover line needs a
decision Core does not have, file it with `scripts/fleet-linear.py file --from
decision` and say so in the task file.

**What you may change.** Only `embarch-api` and `embarch-doc/embarch-api/`. Core's
decisions are read, never edited.

**Doc reserve.** No `embarch-api` file is in reserve at filing. Decisions near
their limit: `ledger` #98 (15 B left), `bench-exchange` #89 (122 B),
`failure-reporting` #67 (192 B). This unit should touch none of them.

## Why now

The owner moved EMB-203 to Fleet Ready. The README is the bench reader's
recovery instruction for a bricked board.

## Done when

- [ ] The README's recover line and `tools-bundle.md` say only what decisions 32 and 36 say.
- [ ] No text says decision 36 maps decision 32's `--erase` to the range erase.
- [ ] A test fails if that claim comes back.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
