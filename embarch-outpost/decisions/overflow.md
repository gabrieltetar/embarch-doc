# embarch-outpost decisions: Overflow

**Status:** active, 2026-09-02.

What the ring does when it is full: drop, count, say so, and block only by opt-in.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The ring and the drain loop: [transport.md](transport.md).

### 5 — Overflow policy: drop, count, and emit an explicit gap record. Never overwrite; blocks only by opt-in (28)

When the ring is full the record is dropped and a counter increments; **the next frame opens with a gap record naming how many were lost.** **A host renders the gap as a gap** — a labelled band — **rather than drawing a continuous, plausible, wrong picture across it.**

**Drop-the-newest rather than overwrite-oldest:** overwriting **discards the beginning of a busy burst and keeps the aftermath, which is backwards for a continuous timeline.** Zephyr's own tracing increments a drop counter **that never reaches the wire; closing that is this module's job, because the losses correlate with load, which is exactly when the trace matters.**

**A gap record is always the first record of its frame** — emitted directly into the frame, never through the ring, **the ring being full being the reason it exists.** That position is a **bound**: a host places the losses between the previous frame's arrival and that frame's. **The DUT's own clock narrows it further, stating the interval outright.**

**Two honest consequences.** On the host's clock the band is **wider than one frame whenever a header frame arrived in between**, because a rendered trace carries only frames that held records **and cannot see the header's arrival — too wide is still a bound, too narrow would be a claim.** And **a gap's own stamp legitimately runs ahead of the records printed after it**, because the ring is FIFO and records reserved before the overflow are still draining — **which is why the band's end comes from the firmware's own figure and never from "the next row."**

### 28 — Blocking overflow sleeps where a thread can, and the ring's floor is 320 bytes

Amends decision 5: "never block" holds by default only. `OVERFLOW_BLOCK=y` looped on `k_yield()`, **which reaches only equal or higher priority, and the drain thread runs at 10**, so a producer on a full ring spun forever and the drain thread never made room. It now `k_sleep()`s 1 ms and retries. **It still drops, counted, where waiting is impossible:** ISR, pre-kernel, idle, interrupts locked, the drain thread itself. `BIT(5)` stays: it says the run could block.

*Rejected: removing the mode*: a run that must lose nothing has no other way to say so. **[Measured on native_sim only: 8 rings of records from a priority-1 producer, none dropped, 0.16 s.]**

**`RING_BYTES` starts at 320, not 256.** Below it the 16-slot floor allocated 320 B past the budget; a `BUILD_ASSERT` now holds slots × 20 B under the setting.
