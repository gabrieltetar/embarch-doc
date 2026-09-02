# embarch-study-designer decisions: Integrity seals and pre-flight validation

**Status:** active, 2026-09-02.

Three sibling CRCs, and what is deliberately outside all of them.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 17 — CRC-sealed integrity checks, verified independently at both hops

**Neither existing safeguard covers payload corruption:** COBS provides frame *resync* after a dropped byte, not *detection*; postcard has no checksum; **and the API↔Core hop is plain JSON with no equivalent check at all.**

The seal covers the steps specifically — not the name — and is **checked twice, independently**: Core recomputes over what it deserialized and rejects before generating an id, then **dev-bench recomputes over what it decoded before running any step and rejects the study outright rather than running with possibly-corrupted step data.**

**Three sibling seals, not one widened seal.** `streams_crc` joined it in `crc.rs` beside `steps_crc` — same algorithm, same one-element-at-a-time digest, its own `StreamTapTooLargeError` (decision 39) — and `protocols_crc` after that (decision 58), each carried on the wire **immediately after the one contiguous span it covers**, so dev-bench's hand-written C digests one run of bytes per seal and a mismatch names which of the three is corrupt.

**Widening one seal instead was rejected on a corrected fact.** The recorded objection was that it would *"silently invalidate every saved study's sealed value"* — **it would not, because the API recomputes and overwrites on every submit, so no stored value is ever trusted.** The real cost is structural: **the first seal sits *between* the two spans on the wire, so the C side would have to digest two non-contiguous spans, or the field order would have to be reshuffled — a reshape where an append will do.**

**What is deliberately outside every seal:** `Study.decoders` (decision 52) and `Study.dev_bench_log_level` (decision 51), because how the host renders a captured byte and how loud the bench is change neither what dev-bench executes nor what it captures. Re-rendering a capture with a corrected layout, or re-running at a louder log level, **must leave it the same study by every check that matters** — otherwise debugging a failure would require altering the artifact under investigation. `requires` (decision 40) and `gatt` (decision 45) are outside because they are host-side only and never cross that wire at all.

Two implementation findings:

- **The C decoder did *not* already walk the second span, so adding its seal was net-positive firmware, not net-negative.** The expectation was *"one varint read and one CRC call over a span the decoder already walks"* — **it walked no such span, because the field had been appended *after* the first seal precisely so C could stop there and see one unconsumed trailing byte.** Sealing it needed a full variant walker, **since postcard carries no per-variant length: +654 bytes.** The decision stands — **a seal computed at one hop and taken on trust at the other is not "checked independently at both hops"** — and the walker is not wasted, since taps must be decoded to be opened. **What was wrong is only the estimate.**
- **The second seal defaults, and the default is *correct* rather than merely permissive.** Saved studies deserialize straight back, **so a mandatory field would make every one unloadable.** A study authored before taps existed has no taps, and **zero is the genuine CRC of zero bytes, not a sentinel.** The sharp edge: **an empty tap list validates against a decoder that never computed the CRC at all — which is why the both-languages pin deliberately carries three real taps.**
- **The FFI decode surface still checks the first seal only.** Its single boolean and single status **cannot say which of three failed; folding them in would quietly destroy the property the sibling seals exist to provide**, and widening the C ABI would extend a surface with **no caller anywhere.** Left as-is with the reason written at the call site.
- **dev-bench aborts on a seal mismatch**, naming which one failed, **even for seals covering things that firmware version could not yet act on.** Computing a seal and ignoring it **would leave a study whose declarations arrived corrupt running to completion and reporting captures that are silently missing or wrong.**

### 18 — Core validates a submitted `Study` structurally, before generating a `study_id` or touching the serial link

Every capacity within bounds, every referenced index in-bounds, requirements present and non-blank, and **every named tap actually declared.** Each failure **names the offending field and limit rather than producing a raw deserialize error — which matters because the study-file path means a human is often hand-writing the JSON.**

### 26 — `steps_crc` is filled in by whoever *submits* a study, not required of whoever *authors* one

Decision 17 requires a correct seal on submission, **which makes a hand-authored study file unusable without a human computing a CRC by hand — squarely against decision 6's symmetric-access principle.** Resolved **without touching the check**: the API recomputes and overwrites whatever value was in the submitted JSON immediately before posting. **A caller that already computed a correct value is unaffected, since the recomputation is idempotent.**

The crate also ships a generated JSON schema, **so a human hand-authoring a study file gets editor and CI validation before ever submitting, independent of the seal question.**

---

