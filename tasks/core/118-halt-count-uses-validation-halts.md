# 118 — Core's `halt_count` uses `Validation.halts` instead of inferring the gate's halt

**State:** claimed by agent/core/118-halt-count-uses-validation-halts, 2026-10-28 13:46
**Dispatch note (2026-10-28 13:46 leg):** core reserve — `open.md` 5,028/5,120 (92 B left), `spec.md` 9,760/10,240 (480 B), `decisions/probes.md` 11,263/12,288 (1,025 B), all parked under `tasks/core/112` (`In flux: yes`). Decision 97 lives in `decisions/live-read.md`, which is not in reserve: amend it there. Do not add to `open.md` or `spec.md`; if you must, compact that file in this unit carrying `core/112`'s `Must not delete:` list. `suite/047` (installed binary names its commit) runs after you in `embarch-core` — stay out of `--version` and `/status`.
**Source:** `topology/067` (topology decision 47, `embarch-topology@b4d1b0a`), box 2. Filed from `inbox/core-use-validation-halts.md` by the 2026-10-26 09:03 leg, in topology/067's fold.
**Scope:** core
**Hardware:** none — host half only; a real STM32G0 read through `POST /live/core-state` reporting the gate halt (`halts == 1` on a running core) is a hardware debt for a bench leg or the owner.
**Owner:** no

## What

`embarch-topology` now returns `Validation.halts: u32` (topology decision 47): how many times the identity gate halted the core, 0 when it was already halted or the family reads its ID without halting. It also counts the Nordic last-resort halted read (topology decision 39), which Core's inference never covered. Core's `halt_count` (`POST /live/core-state` and `/live/mem-read`, decision 97) should add that field instead of `embarch-core/src/live.rs` `gate_halts`, which infers the gate's halt from chip prefix `stm32g0` plus found-running. Delete `gate_halts` and its mirror comment; where Core calls `validate_serial_for_chip` it already holds a `Validation`, so use its `halts`. Add a test that a gate halt reaches `halt_count`.

Core takes `embarch-topology` by path (`../embarch-topology`), not by pin, so nothing needs bumping: `main` already carries the field.

## Why now

The count is an assumption today: a new halting family, or the Nordic last-resort read, makes Core's number wrong while callers weigh it against a roughly 1 ms USB PD GoodCRC deadline.

## Done when

- [x] `live::gate_halts` is gone; `halt_count` uses `Validation.halts`.
- [x] Decision 97 says where the gate's share of the count comes from.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Verification debt

Hardware: a real STM32G0 read through `POST /live/core-state` on a running core should report `halt_count == 1` (default mode) and 2 with `halt=true`; run on a bench leg or by the owner. Host tests use scripted gate values only.
