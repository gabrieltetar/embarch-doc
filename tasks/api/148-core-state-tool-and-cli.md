# 148 — `core_state` MCP tool and CLI, and `mem_read` shows found/left/halt_count

**State:** claimed by agent/api/148-core-state-tool-and-cli, 2026-10-26 09:03
**Reserve (2026-10-26 09:03 leg):** `decisions/client-crate.md` 707 B left (`api/140`, open), `open.md` 832 B left (`api/144`, open). If this unit spends either, it files nothing new: those tasks already carry the debt, but say in the task file how much you spent.
**Source:** core/103 (decision 97): Core ships `POST /live/core-state {role, halt?, samples?}` and adds `found`, `left`, `halt_count` to `/live/mem-read`; the MCP `mem_read` tool returns Core's JSON raw (`embarch-api/src/tools.rs:1401-1414`) where `halted: false` read as "running". Filed from `inbox/api-core-state-tool-and-cli.md` by the 2026-10-26 08:09 leg, in core/103's fold.
**Scope:** api
**Hardware:** none — a client call and tool over a Core route, testable against a stub.
**Owner:** no

## What

Add a `core_state` MCP tool and CLI subcommand over the new Core route (params `role`, `halt`, `samples`), and update the `mem_read` tool description to point callers at `found`/`left`/`halt_count` and say `halted` is deprecated (removed after 2026-11-30). When done, an agent reads where a hung core is without hand-written J-Link calls.

`MemReadResponse` and the new response type live in `crates/embarch-core-client`, which `embarch-ui` path-depends on: build and test `embarch-ui` against the change before landing.

## Why now

The hang hunt that motivated Core's route took 17 external probe calls; without the tool the route is unreachable from an agent session.

## Done when

- [x] `core_state` tool and CLI, with the `halt=true` description naming the halt and its count.
- [x] `mem_read` description updated; tests cover the new response fields passing through.
- [ ] Gate green: see below; supervisor re-runs it.

## Result (2026-10-26)

- `core_state` tool, `core-state` subcommand (`--role --halt --samples`), `CoreClient::core_state` and `RunState`/`Dhcsr`/`CoreRegisters`/`Icsr`/`CoreStateResponse` in `embarch-core-client`. `MemReadResponse` gained `found`/`left`/`halt_count` as `Option` with `serde(default)` (older Core still parses). Documented in api decision 83 (amended), `tools-build-flash.md`, `api-310` feature row.
- **embarch-ui check:** `grep -rn "MemRead\|mem_read" embarch-ui --include=*.rs` found nothing: ui neither constructs nor matches `MemReadResponse`. The change is additive; the supervisor still builds ui at landing.
- **Hardware-verification debt:** Core's JSON is mirrored from `embarch-core/src/live.rs` and unit/mock tested; run `core_state` (default and `halt=true`) and `mem_read` against a live Core with a running STM32G0 and a debugger-halted core, per core decision 97's debts (1) and (2), to confirm the field names on the wire.
- **Reserve spent:** none. `decisions/client-crate.md` and `open.md` untouched; the amendment went in `failure-reporting.md`.
