# embarch-core decisions: Reading a target's memory

**Status:** active, 2026-10-06.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). HTTP surface: [../interfaces/hardware.md](../interfaces/hardware.md).

### 81 — `POST /live/mem-read`: words read over the role's probe, under one halt

The atlas's live module (`embarch-atlas`, DESIGN.md "Live") decodes MCU registers on a running board: it names addresses, Core reads them, the atlas decodes. Until now an agent read a register with hand-written J-Link command files outside Core and outside its lock, and decoded the bits by hand.

**By role, behind the identity gate.** The request names an enrolled role (default `dut`); Core takes its probe serial and chip from the enrollment and runs the same board-identity gate `/flash` and `/reset` run, then a guarded attach (decision 80). `404` when nothing is enrolled under the role, `409` when the role has a board type but no probe, the gate's own `503`/`409` otherwise.

**One-off reads halt the core.** An STM32G0 idling in WFI with no DMA clock on stops its bus matrix in Sleep, and a debug read of the system bus then returns 0 or the previous word with an OK acknowledge (`embarch-topology` decision 39). A halted core is never asleep, so a halted read is always good. The engineer chose this over keeping a DMA clock on in the firmware, which would change the DUT for the debugger's sake. A running core is halted (100 ms timeout; in Stop mode the halt fails by name, since `DBG_STOP` is a write), every range is read, and the core is let run again; the answer gives `halted_us` and, since decision 97, the state found and left. A core already halted is left halted.

**Several ranges, one halt.** `ranges: [{address, words}]`, at most 32 ranges and 256 words in all, each address a multiple of 4; checked before `hw_lock` (`400`). Measured on the first DUT over a J-Link: 15–18 ms halted for one to 14 words. A whole peripheral is one snapshot: its registers are read at one instant, and a caller can leave out a register whose read clears something without a second halt.

**Read-only.** Nothing is written but the halt and the resume. Deciding which registers are safe to read (a FIFO data register pops a byte) is the caller's: the atlas has the records that say so, Core has none.

**Rejected: a never-halt read.** It needs the firmware to keep a DMA clock on; the read would otherwise return plausible garbage with no error.

### 97 — `POST /live/core-state`, and every halt a live read makes is counted

Field use (a USB PD charger board hung, 2026-10-14) showed the suite could not say where a core was: a vendor device profile reset the board on connect and the hang was gone, raw `DCRSR` writes returned one word for five registers, and six `DWT_PCSR` reads finally gave the PC. **`POST /live/core-state {role, halt?=false, samples?=8}`** is that read, read-only, behind decision 81's gate and guarded attach, `hw_lock`, lease-gated. **Default: never halts.** `DHCSR` (decoded: halt, sleep, lockup, retire, reset), then 1..=64 `DWT_PCSR` samples 1 ms apart, then `DHCSR` again, so `s_retire_st` says whether instructions retired; `null` is a sample the core withheld (asleep). PPB reads need no DMA clock, so a sleeping G0 answers. A halted core is not sampled (`DWT_PCSR` gives nothing then) and a part whose `DWT_PCSR` read fails says so in `pc_note`. **`halt=true`:** one halt, `R0`-`R12`, `SP`, `LR`, `PC`, `xPSR`, `CONTROL`, `PRIMASK`, `SCB_ICSR` (decoded), then back to the state found; a core found halted is read and left halted, never resumed.

**Found, left, `halt_count`.** Both routes now answer `found` and `left` (`running`|`halted`) and `halt_count`: every halt the request made, **the identity gate's included**. The gate halts for an STM32G0 UID read when it finds the core running (`embarch-topology` `read_halted`), then resumes, so Core sees the true state found after the gate and adds the gate's share from `Validation.halts` (`embarch-topology` decision 47: 0 when the core was already halted or the family reads without halting; it also counts the Nordic last-resort halted read, decision 39). Core no longer infers it by chip prefix. `halted_us` stays this request's own halt only. **`MemReadResponse.halted` is kept one release** (removal after 2026-11-30): it meant "the core was running and this read halted it", so `false` read as "running" to callers when it meant the opposite. New callers read `found`/`left`.

**Verified:** unit tests over a scripted core only. **Hardware debts:** (1) on a running STM32G0 the default mode returns PCs inside the image, leaves the core running, `halt_count` 1 (the gate's, from `Validation.halts`; 0 on a non-G0), with `halt=true` `halt_count` 2; (2) on a core halted by a debugger, `found`/`left` both `halted`, registers read, no resume, `halt_count` 0; and that `DWT_PCSR` exists on the target.
