# embarch-outpost decisions: The bench

**Status:** active, 2026-09-02.

The first consumer, and how its trace reaches the host.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 15 — First consumer: `reference-dut-fw`

The nRF54L15 already enrolled as the DUT, already flashed through Core, **already the target of every milestone here — so the concrete numbers this design defers get measured on a board that is already on the bench rather than estimated.**

What is still unmeasured: **the sustainable record rate at a given baud and the drop rate that follows from it.** Cycle rate and wrap period stopped being questions once the DUT kept its own per-record clock.

### 16 — The trace reaches the Core machine over a USB-UART bridge wired to the DUT's own console UART pins — a direct route in the most literal form

The signal leaves the DUT and **goes straight to the Core machine, around the bench, exactly as the route was drawn.** No third serial device had to be introduced: **the bridge and the DUT board are things the bench already has and already identifies**, so the declared serial names a port that already exists — **dissolving the hazard of a third indistinguishable USB-serial device, which is the shape of the stale-override incident that created `embarch-topology` in the first place.**

**The trace UART is the console UART on this board revision, and the outpost snippet takes the console off it.** That contention is real and is resolved by the snippet's composition order, not by a second peripheral.

**Two board facts that cost three diagnoses between them, and neither is inferable from a schematic.**

- **The schematic's debug-TX label sits on a net that is physically crossed** on both revisions of this board, **so a bridge wired from the schematic reads a dead line and looks exactly like broken firmware.** The board's own devicetree had written down that symptom, in the tree, months earlier.
- **The build target has to match the board revision in hand.** Two revisions put the console UART on different pins, so **a build for the wrong one transmits correctly onto a pad nothing is connected to** — indistinguishable from an emitter that stalls. **Confirm the revision before suspecting the firmware, the wire, or the instrument** ([reversals](../../embarch-decision-reversals.md) rows 83–85).

**Both are settled: the trace works.** A real capture runs at tens of KB/s with zero records lost, and **a study captures it on its own tap and a host renders it named and timed.**
