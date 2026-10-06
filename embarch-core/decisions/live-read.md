# embarch-core decisions: Reading a target's memory

**Status:** active, 2026-10-06.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). HTTP surface: [../interfaces/hardware.md](../interfaces/hardware.md).

### 81 — `POST /live/mem-read`: words read over the role's probe, under one halt

The atlas's live module (`embarch-atlas`, DESIGN.md "Live") decodes MCU registers on a running board: it names addresses, Core reads them, the atlas decodes. Until now an agent read a register with hand-written J-Link command files outside Core and outside its lock, and decoded the bits by hand.

**By role, behind the identity gate.** The request names an enrolled role (default `dut`); Core takes its probe serial and chip from the enrollment and runs the same board-identity gate `/flash` and `/reset` run, then a guarded attach (decision 80). `404` when nothing is enrolled under the role, `409` when the role has a board type but no probe, the gate's own `503`/`409` otherwise.

**One-off reads halt the core.** An STM32G0 idling in WFI with no DMA clock on stops its bus matrix in Sleep, and a debug read of the system bus then returns 0 or the previous word with an OK acknowledge (`embarch-topology` decision 39). A halted core is never asleep, so a halted read is always good. The engineer chose this over keeping a DMA clock on in the firmware, which would change the DUT for the debugger's sake. A running core is halted (100 ms timeout; in Stop mode the halt fails by name, since `DBG_STOP` is a write), every range is read, and the core is let run again; the answer gives `halted` and `halted_us`. A core already halted is left halted.

**Several ranges, one halt.** `ranges: [{address, words}]`, at most 32 ranges and 256 words in all, each address a multiple of 4; checked before `hw_lock` (`400`). A whole peripheral is one snapshot: its registers are read at one instant, and a caller can leave out a register whose read clears something without a second halt.

**Read-only.** Nothing is written but the halt and the resume. Deciding which registers are safe to read (a FIFO data register pops a byte) is the caller's: the atlas has the records that say so, Core has none.

**Rejected: a never-halt read.** It needs the firmware to keep a DMA clock on; the read would otherwise return plausible garbage with no error.
