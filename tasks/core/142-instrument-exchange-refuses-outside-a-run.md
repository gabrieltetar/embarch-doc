# 142 — Core refuses instrument_exchange outside a run

**State:** open
**Source:** notes/hil/05-live.md — "Reach and permission": instruments are reached only through a Study or a Test, and Core refuses `instrument_exchange` outside a run (owner 2026-11-19)
**Issue:** EMB-252
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`instrument_exchange_handler` refuses only while `study_lock` is held and admits
every caller otherwise, the opposite of the design. When this is done,
`POST /instruments/{name}/exchange` refuses every caller with `409`, before any
port is opened, with a text naming the way in: a host study with an
`Instrument` step. During a run the route is already refused, so after this it
has no admitted caller.

- The route stays, so an older client reads a reason rather than a `404`
  (the owner's choice, 2026-11-23).
- `run_instrument_exchange`, which a host study's `Instrument` step calls
  directly, is unchanged.
- Declaring, listing and removing an instrument are unchanged.

Updating `embarch-api`'s `instrument_exchange` tool to match is a separate unit
(EMB-257); this task changes Core and Core's docs only.

## Why now

The owner's HIL Live phase (`notes/hil/14-implementation-plan.md`). The engineer
then sees an instrument switched only by a study file they can read before it
runs, and the HIL guide's Live section states that reach.

## Done when

- [ ] `POST /instruments/{name}/exchange` answers `409` with no study in
      flight, naming a host study's `Instrument` step, and opens no port.
- [ ] The host study tests with an `Instrument` step still pass.
- [ ] Decision 104 (`decisions/instruments.md`) and `interfaces/instruments.md`
      are amended.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
