# 091 — net_trace uses the fitted package's pin map

**State:** claimed by agent/atlas/091-net-trace-uses-the-fitted-packages-pin-map, 2026-11-23 13:07
**Source:** Fleet Ready issue, an audit finding while tracing a sensor's supply rail
**Issue:** EMB-236
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`net_trace` names a part's pins by the package actually fitted on the board.
Today, for a part whose datasheet distils more than one package pinout, it
joins datasheet pin records to netlist pins using the first package: a
fixed-output LDO fitted in a 6-pin WSON was read with its SOT-23-5 pinout, so
its pin 1 (OUT in the WSON) showed as `GND … dir=power type=ground`, and
`net_trace` on the 1.8 V rail it feeds reported that no part on the net sources
it. The `parts` tool, which reads the schematic's own pin names, had it right
(`1/VOUT`, `3/GND`, `6/VIN`).

## Why now

A regulator output shown as ground hides where a rail comes from and reads
like a wiring fault during a supply investigation.

## Where

`net_trace`'s join of datasheet pin records to netlist pins, for parts whose
datasheet distillation carries more than one package. How the fitted package is
resolved (footprint name, pin count, schematic pin names agreeing with one
pinout) is the worker's design to record as a decision.

## Done when

- [ ] `net_trace` on a rail fed by a multi-package part names the pins of the
      fitted package (test with a two-package fixture, fitted in the second).
- [ ] A part whose package cannot be resolved shows the schematic pin name and
      says the package was not resolved, rather than guessing the first.
- [ ] The regulator's output is reported as the rail's source in that fixture.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet), including
      `test_public_guard` running, not skipped.
- [ ] `embarch-atlas`'s docs updated where they describe `net_trace`'s pin
      join, `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level it made false. Fixtures use generic part and net names only.
