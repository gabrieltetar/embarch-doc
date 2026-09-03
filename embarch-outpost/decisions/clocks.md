# embarch-outpost decisions: The two clocks

**Status:** active, 2026-09-02.

Which clock measures, which places, and what a host may claim from each.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 17 — Two clocks, each with exactly one job: the DUT's `cycles` measures, the host's `rx_utc_ms` places

- **`cycles`, read per record, is what measures.** A span's duration is the difference between its two ends' own stamps; microsecond-exact on this target.
- **`rx_utc_ms`, stamped per frame by [embarch-core](../../embarch-core/decisions.md) decision 30, is what places.** It is the same wall clock every other stream in a study carries, so laying a trace beside a power capture is an alignment rather than a guess. **The DUT's counter cannot do this at all — there is no sync point between them.**

**Neither substitutes for the other**, and the rules a host applies, in order:

- **Measure on the finest clock every row carries, and say which one it used.** One row missing the stamp its tier needs **drops the whole view to the next tier down** — half a timeline in microseconds and half in milliseconds is one axis pretending to be another.
- **Nothing interpolates, on any clock.** Even spacing inside a frame would look better and be fabricated.
- **A frame is the resolution only when the host's clock draws the axis.** With `cycles` present, which frame delivered a record is a fact about the transport with no bearing on how long anything took.
- **What is below the resolution is a property of the clock, not of the wire.** On the host's clock an ISR is below it *by construction* — counted, contributing zero — because enter and exit land in one frame essentially always. On the DUT's clock nothing is below it.
- **The tier is chosen once for a whole view and named**, never per span.

**The DUT's clock is the only one that can go backwards, for two unrelated reasons.**

- **Microseconds, inherently.** A hook reads the counter and *then* reserves its ring slot, so an interrupt preempting a thread between those two operations reserves after it and is stamped before it. **A host must tolerate this — refusing the clock over it would refuse every real capture** — and the earliest instant in a capture is therefore not reliably in its first row, so a window is taken from the minimum.
- **Seconds, meaning the counter restarted.** A capture spanning a DUT reset holds two epochs, and timing anything across the boundary is meaningless.

**What separates them is the other clock, not a threshold.** A backwards step longer than the whole capture took is two independent clocks contradicting each other, and the host's is monotonic — so that is the test, with the DUT's own total forward span standing in when there are no host stamps. When it fires, a host **refuses the DUT clock, falls to the host's, and says so**; the harmless inversions stay reported either way.

**A TX-only DUT transmits whether or not anyone is listening**, so the OS driver's receive buffer can already hold minutes-old bytes when a study opens the port. Core discards them on open.

*Rejected: interpolating records evenly across a frame's interval* — one line of code, a visibly smoother chart, and **a lie in exactly the register this suite exists to refuse: it manufactures a resolution the wire does not have, and nothing downstream could tell the manufactured part from the measured part.**

*Rejected: reconstructing intra-frame timing from the record count and the baud rate* — that describes when the bytes *left*, not when the events *happened*. **The ring decouples them, which is the whole point of having a ring.**

*Rejected: dropping `rx_utc_ms` now that `cycles` measures better* — it is **the only thing that places this trace against another stream in the same study**, a job the DUT's counter cannot do at all.

*Rejected: a host picking its clock per span* — measure the long spans on one clock and the short ones on the other and you have **a mixed axis, arrived at one span at a time, and unauditable.**

### 18 — The arrival stamps are persisted beside the capture, keyed by frame index, and a join that cannot be verified stamps nothing

Decision 10 renders post-hoc, from the complete raw file, **long after the read that saw the bytes — so the stamps have to survive that gap on disk.** A sidecar CSV does it: frame index, arrival stamp and frame length, one row per frame, written incrementally as the bytes arrive.

**The key is a frame index both sides count the same way, and neither side decodes for the other.** Core's capture path counts non-empty runs between delimiters; the decoder counts exactly the same thing. **A frame that later fails its CRC still consumed an index on both sides, which is what keeps them in step** — the alternative, indexing by *successfully decoded* frame, **silently shifts every stamp after the first corrupt frame.**

**The frame length is in the row so the join is checkable.** The raw capture rotates under retention and this file deliberately does not, **so their "frame 0" can stop being the same frame.** Each row carrying its length lets the renderer try the two alignments that can actually occur — the log starting where the capture starts, and the log running ahead of a capture that lost its beginning — and **verify** the one it picks. **When neither fits, nothing is stamped and the stream index says why: a whole trace shifted by three frames is readable, wrong, and indistinguishable from a correct one.** Refusing is the same posture decision 9 takes toward a manifest from another build.

**`named` and `timed` are two facts in the index, not one note.** A trace can be named and untimed, timed and unnamed, or neither, **and the note is prose for a person.** A caller deriving "is this trace fully resolved?" from *rendered and no note* was correct while a note could only mean "unnamed", **and wrong the moment an untimed-but-named trace could carry one.** Both booleans come from Core's own finding, and **no caller pattern-matches on the prose.**
