# 117 — Core's signal callers say a direct signal's declared serial is ambiguous, in their own words

**State:** open
**Source:** topology/062 (decision 46, `embarch-topology@62d776e`). Filed from `inbox/core-exchange-names-signal-ambiguous.md` by the 2026-10-26 leg, in topology/062's fold.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch_topology::hardware::resolve_signal_port` can now return `SignalAmbiguous` (downcastable, `hardware` feature, which Core builds with; candidates with port name and interface) when a direct signal's declared USB serial matches several ports. Core needs no change for correctness: `exchange.rs::resolve_port_waiting` waits only on `SignalMismatch` with `declared_port_serial` set, so an ambiguity falls through to its `Err(e)` arm at once. But `api.rs` (~1555, 1653, 1662), `outpost_preflight.rs` (~207) and `study.rs` (~2641) map errors to HTTP statuses or messages by generic path; check each gives an ambiguity a sensible status (a configuration problem, not a 500 or a 404) and surfaces the candidate list. Add a Core test that the exchange wait returns immediately on it.

## Why now

Decision 46 refuses instead of guessing; the refusal must reach an agent legibly.

## Done when

- [ ] A test pins that `resolve_port_waiting` does not wait on `SignalAmbiguous`.
- [ ] Each of the four callers reports it with its candidate ports.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
