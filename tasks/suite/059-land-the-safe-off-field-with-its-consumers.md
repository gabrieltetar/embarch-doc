# 059 — Land the safe-off field with its consumers

**State:** open — announced 2026-11-24 09:00, ts 1795536052.967279; runs after 09:30 if no objection in that thread
**Source:** `topology/072`'s worker report: `Instrument` and `SignalLink` gained a field, so every consumer that builds one with a struct literal stops compiling the moment the topology branch lands
**Issue:** EMB-321
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`topology/072` added `Instrument.safe_off: Vec<String>` and
`SignalLink.safe_off: Option<String>` to `embarch-topology`, gated green on all
four of the crate's feature sets, and pushed
`agent/topology/072-an-instrument-and-a-signal-declare-a-safe-off` in both repos.
Landing it alone turns three consumers red on `main`, because they construct
both types with struct literals: `embarch-core` (`src/api.rs`, `src/study.rs`),
`embarch-api` (`src/tools.rs`, `crates/embarch-core-client/src/client.rs`,
`tests/core_client_http.rs`) and `embarch-ui` (`src/topology.rs`), by the
worker's grep. The build is the real list.

When this is done, in one sequenced pass: each consumer's literals carry
`safe_off: Default::default()` (no behaviour change; Core's use of the field is
later work), each consumer is gated on its own against the topology branch, and
the pushes go topology first, then `embarch-core`, `embarch-api`, `embarch-ui`
in quick succession, so no consumer `main` stays red. The topology unit's doc
branch lands with it, and `topology/072` is closed `done` in this task's fold.

## Why now

A shared-crate field addition that breaks literal construction is a cross-repo
change, which `protocol.md` §8 gives to the supervisor alone, announced first.
The topology half is finished and waiting.

## Done when

- [ ] `embarch-topology` at the `topology/072` tip on `main`, its doc branch
      landed.
- [ ] `embarch-core`, `embarch-api` and `embarch-ui` build, test and clippy
      green against it, each pushed.
- [ ] `topology/072` and this task closed in one fold.
