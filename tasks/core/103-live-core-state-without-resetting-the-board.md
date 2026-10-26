# 103 — Read where a running or hung core is without resetting it, and report every halt a live read makes

**State:** done — host side; the two bench boxes below are the hardware-verification debt
**Reserve (2026-10-26 08:09 leg):** `embarch-core/open.md` **50 B left**, `spec.md` 474 B, `decisions/probes.md`
1,025 B, all filed on `tasks/core/112`, which is `blocked` on `In flux: yes`. Put this unit's bench debts in
this task file and in the decision you amend, not in `open.md`. If you must write to `open.md` or `spec.md`
anyway, compact that file inside this unit first, keeping `core/112`'s `Must not delete:` list, and delete
that file from `core/112`'s `Compacts:` line (say so in its body). `decisions/live-read.md` is 2,441 B.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — one hang hunt took 17 J-Link Commander, J-Link GDB server and probe-rs calls; the first one reset the board and lost the hang; 4 raw `mem_read`s of `SCB_ICSR` and 1 `halted: false` answer that meant the core was already stopped
**Scope:** core
**Hardware:** verify-only — reclassified from `bench` on filing by the 2026-10-25 leg: the route, its two modes and the `halt_count` reporting are host-side code a worker can build and unit-test; the two bench checks are its hardware-verification debt, collected by a supervisor.
**Owner:** no

## What

Core's live surface reads memory words only (`POST /live/mem-read`, `embarch-core/src/live.rs`). When a console goes silent, the next question is where the core is, and nothing in the suite answers it. When done, a read-only `POST /live/core-state {role}` answers it in two modes. The default never halts: it reads `DHCSR` (run, sleep, lockup, reset state) and samples the PC N times through `DWT_PCSR` where the core has one (PPB reads, correct on a sleeping STM32G0 with no DMA clock). With `halt=true` it stops the core once, reads the core registers (`R0`-`R12`, `SP`, `LR`, `PC`, `xPSR`, `CONTROL`, `PRIMASK`) and `SCB_ICSR`, and lets it run again. The attach is topology's guarded attach, never a vendor device profile that resets on connect. The atlas resolves the PCs against the ELF the board runs (the `live_stacks` flash check), but that is a follow-up. In the same change, `MemReadResponse` (`live.rs:56-65`) stops being ambiguous: `halted: false` today means "the core was already halted", and the MCP `mem_read` tool returns that JSON raw (`embarch-api/src/tools.rs:1401-1414`), where it reads as "running". The answer gives the state found and the state left, and counts every halt the request made, the identity gate's included: the gate reads the STM32G0 UID with the core halted (`embarch-topology/src/hardware/hardware_id.rs:126-131`, `361-375`) after `live.rs:93` calls the gate and before `live.rs:103-122` halts again, and only the second halt is reported in `halted_us`.

## Why now

On 2026-10-14 the DUT went silent after a USB PD message. J-Link Commander's STM32G0B1VE device profile reset the board on connect (uptime 8.5 s afterwards, PC in the reset handler), so the hang was gone. Raw `DHCSR`/`DCRSR` writes through probe-rs then returned one word for five different core registers, and probe-rs gdb, the J-Link GDB server and `probe-rs profile` followed. Six reads of `DWT_PCSR` finally showed the PC in the idle loop. Each live read also halts the core twice, the reported 15-20 ms for the read and an unreported one for the gate's UID read; no USB PD disturbance was seen, but a caller weighing a halt against a GoodCRC deadline of about 1 ms is told about one halt of two.

## Done when

- [x] Unit tests for request checks and for the response shape, including "already halted, left halted" and "running, halted, let run" with a halt count.
- [ ] Bench: on a running STM32G0 the default mode returns PCs inside the image and leaves the core running with `halt_count` 0; with `halt=true` it returns registers and `halt_count` 1 plus the gate's.
- [ ] Bench: on a core halted by a debugger, the answer says "found halted, left halted" and reads the registers without resuming it.
- [x] `mem-read`'s answer names the state found and the state left; the old `halted` field stays one release for compatibility and its doc says what it meant.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated (decision 81 amended), `changelog.d/` fragment dropped; follow-ups filed for the `embarch-api` tool and CLI and the atlas symbol decode.

## Hardware-verification debt

Run by a supervisor on the first DUT (an STM32G0 board), over a Core built from this branch, on a scratch instance:

1. Running core: `POST /live/core-state {"role":"dut"}` returns `pc_samples` inside the flashed image, `left` `running`, `halt_count` 1 (the identity gate's halt; 0 on a non-G0 part). With `halt=true`: registers and `scb_icsr` returned, `halt_count` 2, `halted_us` in the low milliseconds, core running afterwards.
2. Core halted by a debugger: both modes answer `found` and `left` `halted`, `halt_count` 0, registers read, and the debugger still sees the core halted. Also confirm `DWT_PCSR` (0xE000101C) exists on that part (`pc_note` is empty).
3. `/live/mem-read` on the same board shows `found`/`left`/`halt_count` and the old `halted` unchanged.

The native Windows build of `embarch-core` was not run (not the worker's to run).

Drops: `inbox/topology-report-gate-halts.md`, `inbox/api-core-state-tool-and-cli.md`, `inbox/atlas-core-state-symbol-decode.md`. `open.md` and `spec.md` were not touched (reserve line); the debts live here and in decision 97.
