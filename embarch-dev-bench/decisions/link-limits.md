# embarch-dev-bench decisions: Frame and step ceilings

**Status:** active, 2026-09-02. Split verbatim out of [link.md](link.md) on 2026-09-28
(`tasks/dev-bench/014`) when that file went into reserve — this file's own topic seam,
named in that task, is the two ceilings found on hardware rather than the link's
transport/detection/identity concerns `link.md` keeps.

The two ceilings the inbound path and the step decoder hit on real hardware, and what closed each.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The link itself: [link.md](link.md).

### 30 — The inbound path is interrupt-driven, closing a silent 128-byte ceiling
The dispatch loop read the link UART itself, polling and sleeping 1 ms whenever the FIFO happened to be empty. At 1 Mbaud one millisecond is ~100 bytes of arrivals against a 128-byte hardware FIFO — so **any inbound frame larger than the FIFO lost whatever landed while the reader was asleep.** Decode then failed on the truncated result and the loop simply continued, which is the worst possible presentation: Core saw no reply of any kind and reported a step timeout, indistinguishable from a dead link or a wedged board.

**Why it went unnoticed:** every study ever authored fit in the FIFO. The first stimulate-and-capture study is 132 payload bytes — the first one large enough to cross the line, which is why that whole feature had never once worked on hardware despite every unit test passing. The boundary was then confirmed directly rather than inferred, by sweeping a single step's payload length: ~128 bytes completed, ~134 timed out, repeatably. After the fix, ~450-byte frames complete.

An ISR now drains the FIFO into a ring buffer sized to **scheduling latency, not a whole frame**. Overruns are counted and reported as a log line rather than dropped silently — the entire point is that a lost inbound byte must never again look like a dead link. A poll-mode fallback stays behind an `#ifdef` for a platform with no interrupt-driven UART; it carries the original ceiling and is not what hardware uses.

**A test-methodology change this forced.** Every `StudyStart` test round-tripped through this file's own encoder, so a decoder bug the encoder mirrored exactly would pass all of them while failing against Core. The suite now also decodes **the real bytes Core puts on the wire**, COBS-framed by an independent encoder written in the test itself.

### 35 — One step decoded at a time from the retained span, and the local step cap goes away — **not implemented as of 2026-09-08**
Decision 21 shrank a static `StudyStart` step array from the crate's 64 to a local **16**, costing ~9.2 KB of permanently-resident RAM for a worst-case step that almost no step is, and creating a divergence: **the host accepts a 20-step study and the wire silently refuses it.** The plan recorded here was to decode step N into a single struct at dispatch time from the retained raw span instead of a fixed array, dropping RAM to roughly one frame plus one step and letting the crate's constant become the one authority again, `steps_crc` still verified before step 0 (reusing the `streams_crc` span walker).

**Amendment, `tasks/dev-bench/002`, 2026-09-08: never built.** `serial_protocol.h:55` still defines `DBM_MAX_STEPS_PER_STUDY 16` against the fixed `steps[]` array this decision describes replacing (`:714`); `serial_protocol.c` still refuses `steps_len > 16` outright; the ztest pinning that refusal is unchanged. The paragraph above is the plan, not the record. **The divergence is still live** (crate 64, bench 16; 17–64-step studies the host accepts are silently unrunnable here). Trigger to revisit: a real study needing >16 steps on real hardware, per the constant's own comment.

*Declined: streaming steps from Core one at a time* — the smallest possible RAM, and the repo owner's own first instinct. It loses two things deliberately bought: `steps_crc` could no longer be checked before execution begins, becoming a running digest verified at the end, which **inverts the guarantee the seal exists for**; and a serial round-trip would land between every step, folding link latency into exactly the timing `delay_before_ms` was added to make authorable. Recorded rather than discarded — if a study ever gets long enough that even the raw frame is a problem, this is the next move, and the trigger is that specific.
