# embarch-outpost decisions: Two clocks

**Status:** active, 2026-09-02.

Which clock measures, which places, and the join that refuses rather than guesses.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 17 — Two clocks, and each one has exactly one job: the DUT's `cycles` measures, the host's `rx_utc_ms` places. Reworked 2026-08-27.

    Written 2026-08-26, when decision 4 had removed every DUT timestamp and host receipt time was the trace's *only* clock. Layout 3 restored `cycles` the next day at no lock cost, and the sentence that has to change is "only": both clocks are on the wire, they answer different questions, and **neither substitutes for the other.**

    - **`cycles`, read per record by `outpost_time.h`, is what measures.** A span's duration is the difference between its two ends' own stamps. On this target that is microsecond-exact.
    - **`rx_utc_ms`, stamped per frame by `embarch-core` (`embarch-core/decisions.md` §3 decision 30), is what places.** It is the same wall clock `core_rx_utc_ms` carries on a power sample and on a GATT transcript entry, so laying a trace beside a power capture is an alignment rather than a guess. Layout 1 had no sync point between DUT cycles and host wall time at all, and nothing in the suite ever bridged them; that gap closed on 2026-08-26 and stays closed.

    **The rules that follow, in the order a host applies them:**

    - **A host measures on the finest clock every row carries, and says which one it used.** `embarch-ui` has three tiers — DUT microseconds, host milliseconds, frame index — and reports the axis clock by name (`embarch-ui/design.md` §3 decision 10). One row missing the stamp its tier needs drops the whole view to the next tier down: half a timeline in microseconds and half in milliseconds is one axis pretending to be another, and so is half in milliseconds and half in frame indices.
    - **Nothing interpolates, on any clock.** Even spacing inside a frame would look better and be fabricated.
    - **A frame is the resolution only when the host's clock is the one drawing the axis.** With `cycles` present, which frame delivered a record is a fact about the transport and has no bearing on how long anything took.
    - **What is below the resolution is a property of the clock, not of the wire.** On the host's clock a span whose two ends arrive in one frame has no measurable duration, is counted, and contributes zero — and an ISR is below the resolution *by construction* there, because enter and exit land in one frame essentially always. On the DUT's clock nothing is below the resolution, and an ISR is timed like anything else.

    **Measured, and the numbers are why this decision was reworked rather than annotated.** The same reference capture (`bbd4818b`, 9205 rows, 4.08 s of a quiet reference-dut), summarised on each clock:

    | | host clock | DUT clock |
    |---|---|---|
    | resolution | 4.0 ms | 1 µs |
    | spans below it | **4286 of 4955** | **0** |
    | `drain_thread` share | **78.1%** | **1.6%** (66.3 ms over 778 runs, 85 µs each) |
    | idle thread | 7.9% | **95.6%** |
    | every ISR in the system | 147 ms, almost all excluded | **24.8 ms = 0.6%**, all measured |
    | `uarte_nrfx_isr_async` | 2 spans measurable of 1540 | 1540 of 1540, **9.9 µs each** |
    | window unaccounted for | 430 ms (10.6%) | 4.3 ms (0.1%) |

    The 78% is the mechanism of the host clock, stated plainly: the drain thread switches in on one frame and out on the next, so it is charged the whole frame interval — 3.9 ms for 85 µs of work, 46× over. A load table built on that clock does not report the instrument's cost, it reports the instrument's *framing*.

    *Rejected: interpolating records evenly across a frame's interval.* One line of code, a visibly smoother chart, and a lie in exactly the register this suite exists to refuse — it manufactures a resolution the wire does not have, and nothing downstream could tell the manufactured part from the measured part. Still rejected, and now unnecessary: the resolution it would have manufactured is one the wire actually has.

    *Rejected: reconstructing intra-frame timing from the record count and the baud rate.* "N records took N×12 bytes at 1 Mbaud, so they were 96 µs apart" describes when the bytes *left*, not when the events *happened*: the ring decouples them, which is the whole point of having a ring.

    *Rejected: dropping `rx_utc_ms` from the rendered row now that `cycles` measures better.* It is the only thing that places this trace against another stream in the same study, which is a job the DUT's counter cannot do at all — there is no sync point between them. `embarch-ui` keeps reporting the frame interval as the *placement* resolution while measuring in microseconds, which is the pair of facts a reader needs.

    **The DUT's clock is the only one of the three that can go backwards, and it does so for two unrelated reasons — added 2026-08-27, from a real capture.**

    - **Microseconds, inherently.** A hook reads the counter and *then* reserves its ring slot, so an interrupt that preempts a thread between those two operations reserves after it and is stamped before it. The ring publishes in reservation order, so the pair emerges inverted by the width of that window. A real study's capture showed one such step, of **13 µs**. This is not a defect and a host must tolerate it — refusing the clock over it would refuse every real capture. It also means the earliest instant in a capture is not reliably in its first row, so a window must be taken from the minimum.
    - **Seconds, meaning the counter restarted.** A capture spanning a DUT reset holds two epochs and timing anything across the boundary is meaningless. The same study showed a step of **195 seconds**, and its effect was not subtle: an 1.2-second capture's window read as 11 ms and two lanes came out with a **9159% share**.

    **What separates them is the other clock, not a threshold.** A backwards step longer than the whole capture took is two independent clocks contradicting each other, and the host's is monotonic — so that is the test, and with no host stamps the DUT's own total forward span stands in. When it fires, `embarch-ui` refuses the DUT clock, falls to the host's, and says so; `dut_backsteps` and `dut_backstep_max_us` are reported either way so the harmless inversions stay visible.

    **The cause of the 195-second step was Core, and it is fixed at the source.** A TX-only DUT transmits whether or not anyone is listening, so the OS driver's receive buffer can already hold minutes-old bytes when a study opens the port. Core now discards them on open (`embarch-core/decisions.md` §3 decision 30's settlement 3). Worth recording *why nobody had seen it*: on a monotonic host clock a stale prefix is invisible — it just looks like a capture that started earlier. **Making the DUT's clock the axis is what made a pre-existing defect observable**, which is the second time in two days that decision 17's rework has surfaced something that was always wrong.

    *Rejected: letting a host pick its clock per span.* Measure the long spans on the DUT's clock and the short ones on the host's, or vice versa — a mixed axis, arrived at one span at a time, and unauditable. The tier is chosen once for a whole view and named.

### 18 — The arrival stamps are persisted beside the capture, keyed by frame index, and a join that cannot be verified stamps nothing. 2026-08-26. Decision 10 renders post-hoc, from the complete raw file, long after the read that saw the bytes — so the stamps have to survive that gap on disk. `streams/<tap>.arrival.csv` does it: `frame_index,rx_utc_ms,frame_bytes`, one row per frame, written incrementally as the bytes arrive.

    **The key is a frame index both sides count the same way, and neither side decodes for the other.** Core's capture path counts non-empty runs between `0x00` delimiters; the decoder counts exactly the same thing (`outpost::chunks`'s enumeration order). A frame that later fails its CRC still consumed an index on both sides, which is what keeps them in step — the alternative, indexing by *successfully decoded* frame, silently shifts every stamp after the first corrupt frame.

    **`frame_bytes` is in the row so the join is checkable.** The raw capture rotates under retention (`embarch-core/decisions.md` §3 decision 30's segment rotation) and this file deliberately does not, so their "frame 0" can stop being the same frame. Each row carrying its frame's length means the renderer can try the two alignments that can actually occur — the log starting where the capture starts, and the log running ahead of a capture that lost its beginning — and **verify** the one it picks. When neither fits, nothing is stamped and `streams/index.json` says why. A whole trace shifted by three frames is readable, wrong, and indistinguishable from a correct one; refusing is the same posture decision 9 takes toward a manifest from another build.

    **`named` and `timed` are two facts in the index, not one note.** A trace can be named and untimed, timed and unnamed, or neither, and `note` is prose for a person. Before this, `embarch-api`'s client derived "is this trace fully resolved?" from `rendered && note.is_none()` — correct while a note could only ever mean "unnamed", and wrong the moment an untimed-but-named trace could carry one. Both booleans now come from Core's own finding, over `GET /study/{id}/streams`, and no caller pattern-matches on the prose.

