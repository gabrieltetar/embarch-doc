# 103 — Read where a running or hung core is without resetting it, and report every halt a live read makes

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — one hang hunt took 17 J-Link Commander, J-Link GDB server and probe-rs calls; the first one reset the board and lost the hang; 4 raw `mem_read`s of `SCB_ICSR` and 1 `halted: false` answer that meant the core was already stopped
**Scope:** core
**Hardware:** verify-only — reclassified from `bench` on filing by the 2026-10-25 leg: the route, its two modes and the `halt_count` reporting are host-side code a worker can build and unit-test; the two bench checks are its hardware-verification debt, collected by a supervisor.
**Owner:** no

## What

Core's live surface reads memory words only (`POST /live/mem-read`, `embarch-core/src/live.rs`). When a console goes silent, the next question is where the core is, and nothing in the suite answers it. When done, a read-only `POST /live/core-state {role}` answers it in two modes. The default never halts: it reads `DHCSR` (run, sleep, lockup, reset state) and samples the PC N times through `DWT_PCSR` where the core has one (PPB reads, correct on a sleeping STM32G0 with no DMA clock). With `halt=true` it stops the core once, reads the core registers (`R0`-`R12`, `SP`, `LR`, `PC`, `xPSR`, `CONTROL`, `PRIMASK`) and `SCB_ICSR`, and lets it run again. The attach is topology's guarded attach, never a vendor device profile that resets on connect. The atlas resolves the PCs against the ELF the board runs (the `live_stacks` flash check), but that is a follow-up. In the same change, `MemReadResponse` (`live.rs:56-65`) stops being ambiguous: `halted: false` today means "the core was already halted", and the MCP `mem_read` tool returns that JSON raw (`embarch-api/src/tools.rs:1401-1414`), where it reads as "running". The answer gives the state found and the state left, and counts every halt the request made, the identity gate's included: the gate reads the STM32G0 UID with the core halted (`embarch-topology/src/hardware/hardware_id.rs:126-131`, `361-375`) after `live.rs:93` calls the gate and before `live.rs:103-122` halts again, and only the second halt is reported in `halted_us`.

## Why now

On 2026-10-14 the DUT went silent after a USB PD message. J-Link Commander's STM32G0B1VE device profile reset the board on connect (uptime 8.5 s afterwards, PC in the reset handler), so the hang was gone. Raw `DHCSR`/`DCRSR` writes through probe-rs then returned one word for five different core registers, and probe-rs gdb, the J-Link GDB server and `probe-rs profile` followed. Six reads of `DWT_PCSR` finally showed the PC in the idle loop. Each live read also halts the core twice, the reported 15-20 ms for the read and an unreported one for the gate's UID read; no USB PD disturbance was seen, but a caller weighing a halt against a GoodCRC deadline of about 1 ms is told about one halt of two.

## Done when

- [ ] Unit tests for request checks and for the response shape, including "already halted, left halted" and "running, halted, let run" with a halt count.
- [ ] Bench: on a running STM32G0 the default mode returns PCs inside the image and leaves the core running with `halt_count` 0; with `halt=true` it returns registers and `halt_count` 1 plus the gate's.
- [ ] Bench: on a core halted by a debugger, the answer says "found halted, left halted" and reads the registers without resuming it.
- [ ] `mem-read`'s answer names the state found and the state left; the old `halted` field stays one release for compatibility and its doc says what it meant.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated (decision 81 amended), `changelog.d/` fragment dropped; follow-ups filed for the `embarch-api` tool and CLI and the atlas symbol decode.
