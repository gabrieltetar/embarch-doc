# 117 — Core's signal callers say a direct signal's declared serial is ambiguous, in their own words

**State:** claimed by agent/core/117-signal-callers-report-an-ambiguous-declared-serial, 2026-10-26 07:43
**Reserve (2026-10-26 leg):** `embarch-core/open.md` 50 B left, `spec.md` 474 B, `decisions/probes.md`
1,025 B, all parked under `core/112` (`In flux: yes`). This task should need none of them; if it must
write into one, compact that file in this unit carrying `core/112`'s `Must not delete:` list.
**Source:** topology/062 (decision 46, `embarch-topology@62d776e`). Filed from `inbox/core-exchange-names-signal-ambiguous.md` by the 2026-10-26 leg, in topology/062's fold.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch_topology::hardware::resolve_signal_port` can now return `SignalAmbiguous` (downcastable, `hardware` feature, which Core builds with; candidates with port name and interface) when a direct signal's declared USB serial matches several ports. Core needs no change for correctness: `exchange.rs::resolve_port_waiting` waits only on `SignalMismatch` with `declared_port_serial` set, so an ambiguity falls through to its `Err(e)` arm at once. But `api.rs` (~1555, 1653, 1662), `outpost_preflight.rs` (~207) and `study.rs` (~2641) map errors to HTTP statuses or messages by generic path; check each gives an ambiguity a sensible status (a configuration problem, not a 500 or a 404) and surfaces the candidate list. Add a Core test that the exchange wait returns immediately on it.

## Why now

Decision 46 refuses instead of guessing; the refusal must reach an agent legibly.

## Done when

- [x] A test pins that `resolve_port_waiting` does not wait on `SignalAmbiguous`.
- [x] Each of the four callers reports it with its candidate ports.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
