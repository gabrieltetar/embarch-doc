# 174 — The zephyr-west scan takes a board's CPU clusters from its SoC

**State:** done
**Source:** Fleet Ready issue, a session setting up a project with a custom nRF54L15 board
**Issue:** EMB-231
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`list-targets` on a `discovery = "zephyr-west"` project finds the targets of a
board whose `board.yml` lists only the SoC (`socs: - name: nrf54l15`, no
`variants` or `cpucluster`). Today the scan reads CPU clusters from
`board.yml` alone, so for such a board it looks for `<board>_nrf54l15.dts` or
`<board>.dts`, finds neither, and drops the board with
`board '<board>' (soc nrf54l15): looked for … found neither`. Zephyr itself
builds the board as `<board>/nrf54l15/cpuapp` from
`<board>_nrf54l15_cpuapp.dts`, because the SoC's own `soc.yml`
(`soc/<vendor>/…/soc.yml`, `cpuclusters`) supplies the clusters. When
`board.yml` names none, the scan takes them from the SoC's `soc.yml` and looks
for `<board>_<soc>_<cluster>.dts`, the way Zephyr's board qualifiers do.

## Why now

A project with such a board had to fall back to `discovery = "static"` to be
flashed through EmbArch at all.

## Where

- `crates/embarch-firmware-build/src/zephyr.rs` `scan_boards`: reads clusters
  from `board.yml` only.
- The same file, around the `looked for {long} or {short}` drop: the DTS names
  it tries.
- Where the scan finds the Zephyr tree's `soc/` directory is the worker's to
  decide and record; if no `soc.yml` is reachable, the scan keeps today's
  message and says it found no SoC definition.

## Dispatch note

No `embarch-api` file is in size reserve. Per-decision caps close to their
limit in this scope: `ledger` #98 (15 B), `bench-exchange` #89 (122 B),
`failure-reporting` #67 (192 B); none should need touching here. If this needs
a new decision, number it per `DOC-CONVENTIONS.md`.

## Done when

- [x] A board whose `board.yml` lists only `nrf54l15` yields
      `<board>/nrf54l15/cpuapp` targets in `list-targets`.
- [x] A test covers a SoC-defined cluster, with a fixture `soc.yml`.
- [x] A board whose `board.yml` does name its clusters scans as before (test).
- [x] Gate green (`../../embarch-fleet/gate.md`).
- [x] `spec.md`/`decisions.md`/`open.md` updated where they describe the
      zephyr-west scan, `changelog.d/` fragment dropped, `status.d/` fragment
      for anything suite-level it made false.
