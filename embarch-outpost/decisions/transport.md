# embarch-outpost decisions: The transport

**Status:** active, 2026-09-02.

A lock-free ring, a drain thread, and what happens when it overflows.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 3 — The outpost owns its own transport: a lock-free record ring, a low-priority drain thread, and the asynchronous UART API

Forced by decision 2 — **with the tracing core compiled out there is nothing to reuse** — and independently right: **Zephyr's stock UART tracing backend writes one byte at a time in a polling loop, and additionally depends on the console UART.** Spinning per byte inside the drain path **burns exactly the CPU time the trace is trying to measure.** The outpost's UART is a dedicated devicetree node, **distinct from the DUT's console.**

The ring is a bounded multi-producer queue: **a producer reserves a slot with a compare-and-swap on a monotonic head, writes it, then publishes by storing the reservation number into the slot's own sequence, and the consumer advances only over slots whose sequence matches the index it is reading.** So **a producer preempted mid-write stalls the drain at that slot rather than letting a later record overtake an earlier one.**

*Rejected: a spinlock.* On a uniprocessor Cortex-M that is an interrupt lock around about ten instructions — **cheap and obviously correct.** Not used **for a reason specific to what the emit path *is*: it runs inside interrupt context at arbitrary priority, and an interrupt lock there raises the interrupt latency of every other ISR in the system by the length of the trace write. A trace whose cost is a latency floor on unrelated interrupts distorts exactly the thing it measures.** The compare-and-swap **charges the producer, not the system.**

**One implementation detail is load-bearing and not obvious: a slot holding reservation *n* publishes *n+1*, never *n*.** That offset is what makes the ring correct **straight out of zeroed memory with no initialiser to run — and there is no moment at which running one would be safe, because the first hooks fire during kernel startup, long before any init hook the module could register.** Zero-initialised memory **would otherwise read as "reservation 0 is published" to a consumer sitting at tail 0, in exactly the window that matters.**

**A polling fallback exists** for a port whose driver has no async support — **present so such a port still produces a stream, not because it is fine.**

### 5 — Overflow policy: drop, count, and emit an explicit gap record. Never block, never overwrite

When the ring is full the record is dropped and a counter increments; **the next frame opens with a gap record naming how many were lost.** **A host renders the gap as a gap** — a labelled band — **rather than drawing a continuous, plausible, wrong picture across it.**

**Drop-the-newest rather than overwrite-oldest:** overwriting **discards the beginning of a busy burst and keeps the aftermath, which is backwards for a continuous timeline.** Zephyr's own tracing increments a drop counter **that never reaches the wire; closing that is this module's job, because the losses correlate with load, which is exactly when the trace matters.**

**A gap record is always the first record of its frame** — emitted directly into the frame, never through the ring, **the ring being full being the reason it exists.** That position is a **bound**: a host places the losses between the previous frame's arrival and that frame's. **The DUT's own clock narrows it further, stating the interval outright.**

**Two honest consequences.** On the host's clock the band is **wider than one frame whenever a header frame arrived in between**, because a rendered trace carries only frames that held records **and cannot see the header's arrival — too wide is still a bound, too narrow would be a claim.** And **a gap's own stamp legitimately runs ahead of the records printed after it**, because the ring is FIFO and records reserved before the overflow are still draining — **which is why the band's end comes from the firmware's own figure and never from "the next row."**

### 20 — The drain thread waits for a batch to fill, and that is only free because the DUT kept its clock

If the ring holds less than a batch's worth, **sleep once, then send whatever is there.**

**The loop was a fixed point at the link rate, and nothing about record volume could escape it.** The drain thread sends, blocks on the transmit, then drains exactly the records that arrived while it was blocked — **so frame size settles at whatever the record rate produces during one frame's own wire time, and duty sits near 100% however few records there are. Removing records makes frames smaller, which makes them transmit faster, which makes the loop spin faster.**

**The trade is latency, and only latency — which is exactly what the per-record clock bought back.** A record can sit in the ring for the wait before transmission, **and that costs nothing because it carries its own DUT stamp, so when it left the ring has no bearing on when a host says it happened. Under layout 2 this change would have been unavailable**: a frame's arrival was the only clock, **so delaying a frame would have moved every event in it.** Same for resolution — **bigger frames used to mean a coarser trace and now mean nothing of the kind.**

**One sleep and not a loop**, because a second wait **would double the latency bound to buy a second-order saving.** The target is computed against the **maximum** record size rather than an average, **so it is reached before a batch could overflow and a frame is never cut short by having waited for one record too many.**

**The pending count is a hint, not a fact:** it can be stale, and it can count a slot a preempted producer has reserved but not published. **Both errors make the drain thread wait *less* than it meant to, which costs a slightly smaller frame and nothing else.** It is clamped to the ring size, **because a producer that reserved past a full ring increments head and then drops its record, so head can run ahead of anything a consumer will ever see.**

**The wait does not affect burst tolerance; the ring does.** During a burst the pending count is far above the target, **so the drain thread never sleeps and its throughput is identical to no wait at all.** What bounds a burst is the drain thread's **peak** throughput against the ring's depth — **and average capacity is never the constraint: a link averaging a quarter busy still lost thousands of records to bursts, and quadrupling the ring absorbed nearly all of them.** So: **the ring is the burst knob, the wait is the latency knob, and the record's size is the throughput knob.**

*Rejected: a smaller batch size to get finer frames.* **A live idea while the frame was the instrument's resolution, and the per-record clock inverted it: frame size no longer affects resolution at all, so smaller frames buy nothing and cost framing overhead. Bigger is strictly better on this wire**, up to the latency the wait already bounds.
