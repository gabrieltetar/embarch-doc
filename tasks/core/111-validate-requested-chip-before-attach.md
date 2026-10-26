# 111 — Core calls `validate_serial_for_chip` so a probe moved to another chip family is refused before any attach

**State:** done — branch agent/core/111-validate-requested-chip-before-attach, 2026-10-26 (decision 89; hardware-verification debt in `embarch-core/open.md`)
**Dispatch note (2026-10-26):** no `embarch-core` doc is in reserve. The worktree parent links `embarch-study-designer`, `embarch-topology` and `embarch-smp`. Topology's half is on `main` at `62c188d`. The native Windows build is the owner's debt, not your gate. `study-designer/075` runs beside you and may add a study-validation refusal Core links; gating that against Core is mine at landing, not yours.
**Source:** `tasks/topology/059` (field use 2026-09-30: an STM32G0B1VE flash through a J-Link still enrolled on an nRF54L15 board was refused as a failed FICR read; six days of bypassing EmbArch). Topology shipped the half it owns (`embarch-topology` `62c188d`, topology decision 44). Filed from the worker's inbox drop `core-validate-requested-chip.md`, 2026-10-26.
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

`embarch-topology` now exports `hardware::validate_serial_for_chip(serial, requested_chip) -> Result<Validation>` and the pure `hardware::check_requested_chip(&EnrolledBoard, &str)`. A differing chip (case-insensitive, whitespace-trimmed; empty either side passes) returns a downcastable `hardware::RequestedChipMismatch` before the probe is opened, naming the probe, enrolled role/bench board and chip, the requested chip and the re-enroll call. `validate_serial`/`validate_serial_timed` are unchanged.

Core must call the new function wherever a project's `chip` reaches the gate: `embarch-core/src/hardware.rs:180` and `:391`, `live.rs:93` and `:141` (flash, reset, bootload paths). Use `.board` where the old `validate_serial` result was used. Map `RequestedChipMismatch` to its own refusal (not `"mismatch"`/`"not_attached"`; it is a caller-visible 4xx-style refusal carrying the Display text). Check that a project's `chip` string spells the same as an enrolled `chip` (e.g. `nRF54L15` vs a `_cpuapp` variant); normalise in Core if not (topology decision 44 records this as assumed).

## Why now

Until Core calls it, a moved probe still reads as a failed identity read. Any caller passing a requested chip should get the clear refusal.

## Result

Decision 89. All four call sites use `validate_serial_for_chip`; `RequestedChipMismatch` -> `409` in `describe_topology_error` and `describe_gate_error`. Test is mapping-level: topology's store path is fixed so no test can enroll. **Hardware-verification debt:** flash a different-family project through a probe enrolled for another chip; expect `409 chip-mismatch`, no attach. Chip-spelling equality (project vs enrolled) is assumed, no normalisation added.

## Done when

- [x] All four call sites pass the project's chip through `validate_serial_for_chip`.
- [x] A test: probe enrolled with chip A, flash requested for chip B, refused with the topology text and no attach.
- [x] Equal-chip paths and the identity gate's refusals behave as before.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
