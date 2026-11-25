# 063 — An instrument's declaration carries its metrology

**State:** claimed by agent/suite/063-an-instruments-declaration-carries-its-metrology, 2026-11-25 07:12 — run by the supervisor; window ts 1795612302.163159 closed with no reply
**Source:** EMB-358 — an instrument's declaration carries no resolution, uncertainty or calibration
**Issue:** EMB-358
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`Instrument` in `embarch-topology`'s identity store holds its line facts (port,
baud, terminators, pacing, acknowledgements, safe-off) and nothing about what
it measures. The HIL design has each instrument declare its resolution, its
uncertainty `U` with its coverage factor and basis, its range, and its
calibration (`embarch-doc/notes/hil/03-test.md`, "The verdict";
`notes/hil/06-report-and-publish.md`, "The audit appendix";
`notes/hil/12-prevention.md`, "The root of trust"). When this is done:

- `Instrument` has an optional `metrology` list, one entry per quantity it
  measures: `{quantity, unit, resolution, U, k, basis, range {min, max}}`, and
  an optional `calibration {serial, certificate_ref, due,
  certificate_sha256}`. Both default when absent and are omitted when empty,
  so a store written today loads and is rewritten unchanged.
- `Instrument::check` refuses a negative `U` or resolution, an inverted range
  or a malformed date, naming the field.
- The owner may strike this: keeping metrology in Core's own store instead,
  with no topology change, is the alternative (plan choice 14).

## Why this is a suite task

Three consumers build `Instrument` by struct literal, so a new field breaks
their compile: `embarch-core/src/instrument.rs` (a test helper),
`embarch-api/src/instrument.rs` (`declare_instrument`'s builder) and
`embarch-ui/src/bench/live.rs` (Make live). Each gets the defaults and nothing
more; passing metrology through `declare_instrument` is EMB-375, and Core
stamping it on measurements is EMB-360, both later. Land in order: topology,
then core, api and ui, each `main` compiling on its own, the way `suite/059`
landed `safe_off`.

## Where the doc goes

`embarch-topology/decisions/instruments.md` holds decision 49 with 208 B left:
a new decision beside it, with a dated pointer on 49 if it fits.
`interfaces/` for the new fields. No consumer decision changes.

## Done when

- [ ] A store fixture written before the change loads unchanged.
- [ ] An instrument with a metrology block and a calibration round-trips.
- [ ] A negative `U` or resolution, an inverted range, or a malformed date is
      refused with the field named.
- [ ] Core, embarch-api and embarch-ui build and test against the new topology.
- [ ] Decision 49 amended or pointed at by the new decision.
