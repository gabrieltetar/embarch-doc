# 157 — Core keeps definitions, premade suites and confirmations

**State:** open
**Source:** EMB-363 — Core holds no definition, premade suite or confirmation
**Issue:** EMB-363
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core never reads a firmware repo and keeps no test definition, and nothing
records a confirmation. The HIL design: a custom or derived test is confirmed
whole, by the hash of its definition; each DUT input field by field; an
unmodified premade test needs none, unmodified meaning identical to Core's own
copy of that suite version; a Core in the engineer's own account reads its
premade suites from a suite checkout its configuration names; a confirmation
binds the hash of exactly what was confirmed and is kept by Core
(`embarch-doc/notes/hil/03-test.md`, "The DUT's inputs"). An act is submitted
with a nonce Core issued for that card's rendering, and only the person's token
obtains one (`notes/hil/12-prevention.md`, items 4 and 5). When this is done:

- `POST /definitions` (either token): a test, suite, plan, bench, capability or
  hook mapping, checked by `embarch-study-designer`'s `hil-test` checks
  (`TestDef::check`, `SuiteManifest::check`, `Plan::check`, and
  `hil_check::check_test` where the inputs exist), kept as
  `definitions/<sha256>.json` in Core's data folder, the hash being the crate's
  `definition_hash`; `GET /definitions/{hash}`. Posted twice, kept once.
- **Premade suites** read from the checkout `EMBARCH_SUITES_DIR` names,
  indexed by suite id and version with each manifest's hash. The owner may
  strike the variable: a Core config key is the alternative (plan choice 11).
- `GET /confirmations/pending` lists what waits; **the card's data** comes with
  a nonce issued only to the person token, single use.
- `POST /confirmations` with the person token and the nonce binds a hash; the
  agent's token is refused `403` even on an unattested (development) Core, as
  a discard of a failing run already is (decision 112). Each confirmation is an
  entry in the run log, with the scope and the surface. The owner may strike
  this: a chain of its own is the alternative (plan choice 7).
- **A suite version Core does not hold** is confirmed once, as a unit, by its
  manifest hash; the report then says the suite was not Core's (03, review
  round 4).
- Route names are the plan's; the owner may strike them (plan choice 8). The
  decision must name plan choices 7, 8 and 11 as the owner's to strike.

Core's build enables `embarch-study-designer` with `std,reducers,hil-image`
today; adding `hil-test` to that list is in scope (Core's own `Cargo.toml`). If
you find you need a change inside `embarch-study-designer` itself, stop and say
so in this file: that is another sub-project.

## Why now

EMB-363 is on the HIL Test chain's critical path: Core's prepare route and the
go (EMB-364), embarch-api's proposals and test plan (EMB-376) and the UI's
confirmation card (EMB-383) wait on it. Design:
`embarch-doc/notes/hil/14-implementation-plan.md`.

## Where to look

- `src/run_log.rs` — the chain an entry joins; `discard` for the `403`
  precedent.
- `src/token_store.rs` — `Scope`, and `PERSON_ROUTES` with its
  `person_middleware` (decision 132): the nonce route and the confirmation post
  are person-only on every Core, which is stricter than 132's service-only
  table, so say in the decision how the two relate.
- `embarch-doc/embarch-core/interfaces/run-log.md`; decisions 109, 111, 112,
  132.

## Where the doc goes

A new decision (a new topic file is fine, e.g. `decisions/definitions.md`),
and `interfaces/` for the routes and the run-log entry shape. **Decisions near
or over their per-decision limit (`check-doc-size.py --pressure`):**
`run-log.md` 111 (120 B left), `instruments.md` 104 (144 B left),
`lease.md` 93, `stopping-a-study.md` 128, `host-study.md` 95,
`analog-capture.md` 127, `signing.md` 110 (all over); do not grow any of them,
and point at them from your new decision instead. No `core` file is in
reserve. If your work pushes one into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md`.

## Done when

- [ ] A definition posted twice is kept once, by its hash; an invalid one is
      refused with the crate's reason.
- [ ] A confirmation with the agent's token is refused `403`; with the
      person's token and a fresh nonce it is entered in the run log; the same
      nonce again is refused.
- [ ] An edited definition, a new hash, reads unconfirmed.
- [ ] A premade test identical to the checkout's copy needs no confirmation;
      one byte changed needs one.
- [ ] A decision and `interfaces/` docs give the routes and the entry shape.
