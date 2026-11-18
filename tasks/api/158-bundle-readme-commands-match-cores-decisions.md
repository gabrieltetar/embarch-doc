# 158 — The bundle README's commands match what Core's decisions record

**State:** claimed by agent/api/158-bundle-readme-commands-match-cores-decisions, 2026-11-17 18:34
**Source:** EMB-202, a reviewer finding on `api/157`: the bundle README presents a full-chip-erase program command as what embarch-core records, against `embarch-core` decisions 36 and 32
**Issue:** EMB-202
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api bundle` (landed in `api/157`) writes a README for a bench
engineer. Its family table (`FAMILIES` in `src/bundle.rs`) gives the nRF54L
program command as `nrfutil device program ... --options
chip_erase_mode=ERASE_ALL`, its recover line calls "the vendor's erase-all" the
recovery the suite recorded, and its preamble (`render_readme`) says every
command below is what embarch-core's flash backends and its decisions on
flashing record for the family. `embarch-api/interfaces/tools-bundle.md`
repeats that claim.

None of that is true. `embarch-core` decision 36
(`embarch-doc/embarch-core/decisions/flash-backend.md`) says Core invokes
nrfutil with `chip_erase_mode=ERASE_RANGES_TOUCHED_BY_FIRMWARE`, "never
`ERASE_ALL`", and calls it a construction-time contract nobody has confirmed on
a board. Decision 32 (`flashing.md`) records the recovery as the vendor's own
runner with `--erase`, which decision 36 maps to the range erase.

Make the README say only what the suite records:

- Every command line in the family table matches what Core's flash backend
  actually invokes for that family. Read Core's nrfutil backend source and
  decisions 32 and 36 for it (read only: `embarch-core` is not yours to edit).
  A command Core does not run is dropped, the way the table already leaves out
  a family the suite records nothing for.
- The preamble does not claim more than the decisions do: where a decision
  calls a command a contract not yet confirmed on hardware, the README says so
  in one short line rather than presenting it as known good.
- `interfaces/tools-bundle.md` says the same.
- A test pins it: no rendered README contains `ERASE_ALL`, and the nRF54L
  program line carries the range erase.

**No new numbered decision** (burndown). A real design fork goes to
`scripts/fleet-linear.py file --from decision`.

**What you may change.** Only `embarch-api` and `embarch-doc/embarch-api/`.

**Doc reserve.** Nothing of `embarch-api`'s is in reserve. Three of its
decision topic files sit within 256 B of their limit (`ledger` 15 B,
`bench-exchange` 122 B, `failure-reporting` 192 B); this unit has no reason to
touch any of them.

## Why now

The owner's Fleet Ready holds it, and the bundle reaches no bench engineer
before the owner rebuilds and redeploys `embarch-api`, so fixing it now means
the wrong command never ships.

## Done when

- [x] No README line claims `ERASE_ALL` is what Core records, or the recovery the suite recorded.
- [x] Each remaining command matches Core's backend for that family, and an unconfirmed one is labelled as such.
- [x] `interfaces/tools-bundle.md` matches the README.
- [x] A test fails if `ERASE_ALL` comes back.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
