# 067 — Topology reports how many halts its identity gate made

**State:** open
**Source:** core/103 (decision 97): Core's `halt_count` includes the identity gate's halt, which Core can only infer by chip prefix `stm32g0` plus found-running, mirroring `hardware_id.rs` `read_halted` (`:126-131`, `:361-375`). Filed from `inbox/topology-report-gate-halts.md` by the 2026-10-26 08:09 leg, in core/103's fold.
**Scope:** topology
**Hardware:** none — unit-testable over `read_halted` with a stand-in core.
**Owner:** no

## What

`validate_serial_for_chip` (and `Validation`) should say how many times it halted the core while checking identity, so Core stops mirroring topology's `Stm32G0Uid` arm by prefix. When done, `Validation` carries `halts: u32` (0 when the core was already halted or the family reads its ID without halting), and a new halting family cannot make Core's count wrong.

`embarch-topology` is a shared crate: build it under `--no-default-features --features software,wire` as well as the default before landing, because `embarch-core-client`, `embarch-ui` and `embarch-umbrella` build it that way. `embarch-topology/decisions/enrollment.md` and `links.md` are both under 170 B from their caps (`topology/060` blocked, `066` open); record the decision elsewhere or say why.

## Why now

Core's `POST /live/core-state` and `mem-read` report `halt_count` to callers weighing a halt against a roughly 1 ms USB PD GoodCRC deadline; today the gate's halt is counted by an assumption (`embarch-core/src/live.rs` `gate_halts`).

## Done when

- [ ] `Validation` (or its timed variant) exposes the gate's halt count, unit-tested over `read_halted` for a running and an already-halted core.
- [ ] A Core follow-up task (via `inbox/`) replaces `live::gate_halts` with that field.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
