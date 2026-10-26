# 052 — A direct signal route declares which serial interface carries it

**State:** open — announced 2026-10-26 08:09 MDT, `ts` `1793023741.728799` (no `--action`); the window closes 08:39. Poll `fleet-read.py --thread 1793023741.728799`; run it as a leg's last unit only if no objection has arrived by then
**Source:** topology/062 (DeepSeek V4 Pro review 2026-10-25, topology findings 1, 4, 8); split off because it changes a public shape (protocol §8). Filed from `inbox/suite-direct-route-declared-interface.md` by the 2026-10-26 leg, in topology/062's fold.
**Scope:** suite
**Hardware:** none — fixture-testable; whether a two-interface direct device exists on this bench is unknown (`embarch-topology/open.md`)
**Owner:** no

## What

`embarch-topology` decision 46 (topology/062) makes a declared direct-route serial that matches several ports a refusal (`SignalAmbiguous`, listing each candidate port and interface). That leaves such a device unusable as a direct route until the route can declare an interface, the way bootload ports do (decision 36). Add an optional `interface` to `Route::Direct` (serde default, skipped when absent, so old `enrollment.toml` rows load and write back unchanged) and make `Filter::for_declared_serial` take it. Consumer sites that build or destructure `Route::Direct { port_serial }` without `..` and break the moment the field lands on topology `main`: `embarch-api` `src/tools.rs` (~751, ~1342; also the `declare_signal` tool and CLI), `embarch-ui` `src/topology.rs` (~1291; the declare form). Check `embarch-core` for exhaustive matches too. Land the three together.

**Build every consumer configuration before landing topology** (2026-10-26 leg): `SignalAmbiguous` and `AmbiguousDeclaredSerial` are `hardware`-only since `embarch-topology@62d776e`, and topology's `Cargo.toml` names `--no-default-features --features software,wire` as a gate item because `embarch-core-client`, `embarch-ui` and `embarch-umbrella` build that way. `9e465cb` skipped it and broke them for five minutes.

## Why now

Without it, a DUT whose console is one of two interfaces under one serial cannot be declared at all. Also update `SignalAmbiguous`'s message, which says a direct route "cannot yet declare" an interface.

## Done when

- [ ] A direct route with a declared interface resolves to that interface (fixture test over a two-interface port list); without one it is still refused by `SignalAmbiguous`.
- [ ] A pre-change `enrollment.toml` signal row loads and is written back without an `interface` key.
- [ ] `embarch-api` (`declare_signal`, CLI) and `embarch-ui` (declare form) can declare it; all three repos build and pass their gates.
- [ ] Docs: topology decision 46 amended, `open.md` item removed; `tasks/topology/066` unparks.
