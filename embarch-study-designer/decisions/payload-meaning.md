# embarch-study-designer decisions: Declared payload meaning

**Status:** active, 2026-09-02.

Where a byte payload acquires a meaning, and why that place is never firmware.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 52 — An engineer-declared payload layout: `StreamEncoding::Struct` and a per-repo `study-structs.toml`
Opened authoring the first study that captures **one specific characteristic rather than everything**: a notify tap could only be raw bytes, **producing a binary file and no CSV at all**, or the sample encoding, which can say "packed integers, one column" and nothing else. **A real notification is a small header followed by a packed sample array, and neither describes it.**

A layout is a header read once plus an optional repeat read as many times as fits, producing **one row per repetition** with the header denormalized onto each. **That repetition is the whole reason the type exists** rather than a flat field list: **a notification carrying a sequence number and twenty samples is one record and twenty rows, and rendering it as one row with twenty columns makes it unanalysable by every tool that reads a CSV.** Field-level shape: [../interfaces/decoders.md](../interfaces/decoders.md).

**The layout lives in the firmware repo and resolves into the study at build time**, for decision 35's reason: **it is engineer-authored knowledge about *this* DUT.** The study carries the layout rather than a name, because **Core cannot read that repo** — a study naming one **would render nothing on any machine but the author's, and *differently* after an unrelated edit.** The on-disk registry mirrors the wire type with plain strings on purpose, **so a hand-edited file's mistakes become a named error rather than one pointing at a capacity constant.**

**What crosses the wire is an index, not the layout** — the list is **host-only.** A tap's encoding *does* cross, because the bench walks past it to reach the scope; **a variable-length definition there would cost a nested walker in hand-written C for a value dev-bench must never act on**, and would put what a payload *means* **back inside the node decision 39 took it away from.** Sealed by neither CRC: **re-rendering a capture with a corrected layout must leave it the same study.**

**A payload that doesn't fit still gets a row** — decoded columns empty, the raw bytes and the reason filled. Never a dropped record and never a forced decode: the raw file is on disk first, so a wrong layout costs a rendering that can be redone rather than a capture that cannot, and **a record that arrived must be visibly present-and-undecoded rather than absent and indistinguishable from a notification that never came.**

**Integers render as integers.** The sample layout can only produce `f32`, and a `u64` counter round-tripped through one loses its low bits — a plausible, wrong number, which is the failure this crate keeps refusing to produce.

### 55 — A `StreamSource::GattNotify` tap actually produces records, and dev-bench keeps what it needs to route them
The variant had existed since decision 39 and was **decoded but dead**: dev-bench opened and closed the tap and never sent a record on it, which the firmware's own comment said out loud. So "give this characteristic its own file" was expressible in the type model and impossible in practice.

**Routing, not subscribing.** A notify tap does not arm its own subscription; it routes what a monitor step already subscribed. dev-bench's transcript sink is the one place every captured notification passes through, so one entry now fans out to the transcript tap *and* to every open notify tap whose characteristic matches — the tap getting **the raw ATT value and nothing around it**, because Core decodes those bytes against a layout describing the DUT's packet rather than a dev-bench record wrapping it. One notification landing in two files is not duplication: the transcript is the complete story of the connection, the tap is one characteristic's data with a declared layout, and neither is optional given the other.

*Rejected: a tap arming its own subscription.* It needs lazy-subscribe machinery in firmware — a whole-study tap opens before the connect step, so there is no connection yet — and it would give one characteristic two independent subscribers to reconcile. Routing costs a UUID comparison in a callback that already runs.

**The cost is addressing rather than meaning:** dev-bench now keeps a notify tap's characteristic UUID, having skipped those bytes outright. The encoding stays deliberately unkept — what a payload means is exactly what decision 39 took away from that node — but *which characteristic's notifications go to which tap id* is routing, precisely like the source tag, and this node has to know it because this node sends the record. The service UUID stays skipped: a notification identifies itself by characteristic.

**The failure this leaves reachable, and where it is caught.** A tap naming a characteristic no step subscribes to captures nothing, passes, and looks fine. Refused at authoring time by `embarch-ui`, which has both the steps and the taps in hand — not at run time, where it is an empty file after a run that cost hardware time.


### 70 — A tap declares its records' framing, and the host checks the checksum the data already carries
Opened by a capture that was short and reported itself complete. A 10 h PPG drain (`embarch-core` study `872aef3c466dd465c66e671412a97760`, 2026-09-08) lost three `StreamChunkBatch` frames on the Core↔dev-bench UART — 976 bytes, four 244-byte notifications — damaging 3 of its 598 records, and `list-study-streams` reported `truncated: false`. **Every layer's own accounting was honest.** The DUT advanced its BDS offset only on notifies that returned 0 and declared 9538149 bytes in its `PROGRESS` frames; dev-bench's queues dropped nothing; Core wrote the 9537173 bytes it received and logged the three frames it could not decode. Nothing was wrong except that no one compared the ends.

**So this adds no integrity mechanism — it declares where the one already in the data lives.** Every `GWF1` record ends in a CRC-32 the DUT computed over its own contents, and that cost was already paid, on flash, in the record format. `Study.record_checks` names a tap by its `id` and says its records begin with a magic and end with a little-endian CRC-32/ISO-HDLC over the preceding bytes; Core walks the capture after the run and reports totals, which records failed, and any bytes belonging to no record.

**Checked end to end, which is the whole reason it is here and not on a link.** A record that verifies was read correctly off the DUT's flash and survived an unacknowledged BLE notification stream, dev-bench's queues, the UART, Core's deframer and the write to disk. *Rejected: a per-frame sequence number on the Core↔dev-bench link.* It would have caught this one fault and none of the others — a bad flash read, a lost notification, a frame corrupted but still decodable — and it costs a `DEV_BENCH_WIRE_SCHEMA_VERSION` bump, so a firmware reflash, to check one hop of six.

**Record length is deliberately not declared.** Boundaries come from scanning for the next magic and the trailing CRC confirms the guess, so **a record that verifies was split correctly by construction**; a stray magic inside a payload is retried against later boundaries before the record is called damaged. That is what lets one declaration cover `GWF1` and the WDS flash spill, which share the shape, with no per-format arithmetic anywhere and no way to be confidently wrong about a boundary.

**Host-only, and the addressing is what keeps it that way.** It rides beside `requires` and `decoders`: sealed by neither `steps_crc` nor `streams_crc`, never transmitted. Unlike a `StructLayout`, which `StreamEncoding::Struct` indexes into, this names its tap directly — an encoding crosses the wire inside `StudyStart`, so referencing a host-side check from there would have made it cost a firmware reflash for a check no firmware runs. `HOST_TYPE_SCHEMA_VERSION` 17 → 18; `DEV_BENCH_WIRE_SCHEMA_VERSION` stays 15.

**`records` is not redundant with `truncated`, and the two answer different questions.** `truncated` is what some *link* reported about itself; `records` is whether the bytes on disk match what the DUT checksummed. A capture with no declared framing reports `records` absent rather than clean — "nobody could check" and "it checked out" are different facts, and conflating them is how the short capture read as complete to begin with.
