# embarch-study-designer decisions: Integrity seals and pre-flight validation

**Status:** active, 2026-09-02.

Three sibling CRCs, and what is deliberately outside all of them.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 17 — CRC-sealed integrity checks, verified independently at both hops

Neither existing safeguard covers payload corruption: COBS (decision 10) provides frame resync after a dropped byte, not corruption *detection*; postcard has no checksum; and the api↔Core hop is plain JSON over HTTP with no equivalent check at all.

`Study` carries a `steps_crc: u32` over `steps` specifically — not `name`. Computed via a crate-exported `steps_crc()` (CRC-32/ISO-HDLC, the `crc` crate, one element streamed through the digest at a time), checked **twice**: Core recomputes over what it deserialized from the HTTP body and rejects with `400` before generating a `study_id` (alongside decision 18's structural checks), then dev-bench recomputes over what it decoded before running any step and rejects the study outright on mismatch rather than running with possibly-corrupted step data.

**Three sibling seals, not one widened seal.** `streams_crc` joined it in `crc.rs` beside `steps_crc` — same algorithm, same one-element-at-a-time digest, its own `StreamTapTooLargeError` (decision 39) — and `protocols_crc` after that (decision 58), each carried on the wire **immediately after the one contiguous span it covers**, so dev-bench's hand-written C digests one run of bytes per seal and a mismatch names which of the three is corrupt.

Widening `steps_crc` instead was considered and rejected on a corrected fact. The recorded objection had been that widening would "silently invalidate every saved study's sealed value" — it would not, because `embarch-api` recomputes and overwrites on every submit (decision 26), so no stored value is ever trusted. The real cost is structural: `steps_crc` sits *between* `steps` and `streams` on the wire, so the C side would have to digest two non-contiguous spans, or `StudyStart`'s field order would have to be reshuffled — a reshape where an append will do.

**What is deliberately outside every seal:** `Study.decoders` (decision 52) and `Study.dev_bench_log_level` (decision 51), because how the host renders a captured byte and how loud the bench is change neither what dev-bench executes nor what it captures. Re-rendering a capture with a corrected layout, or re-running at a louder log level, **must leave it the same study by every check that matters** — otherwise debugging a failure would require altering the artifact under investigation. `requires` (decision 40) and `gatt` (decision 45) are outside because they are host-side only and never cross that wire at all.

Two implementation findings:

- **dev-bench's decoder did *not* already walk the `streams` span, so adding `streams_crc` was net-positive firmware, not net-negative.** The expectation was "one varint read and one CRC call over a span the decoder already walks". It walked no such span — decision 39's Phase A appended `streams` *after* `steps_crc` precisely so C could stop there and see one unconsumed trailing byte, which is what it did. Checking the seal at that hop therefore required teaching C to walk a `StreamTap`: a ~120-line `pc_skip_stream_tap` covering every `StreamSource`/`StreamEncoding`/`StreamScope` variant, since postcard carries no per-variant length. [Measured on `native_sim`: 25,660 → 26,314 bytes of text, +654.] The decision stands as written — a seal computed at one hop and taken on trust at the other is not "checked independently at both hops" — and the walker is not wasted, since taps have to be decoded to be opened anyway. What was wrong is only the estimate.
- **`Study.streams_crc` is `#[serde(default)]`, and the default is *correct* rather than merely permissive.** Saved studies (decision 38) are JSON deserialized straight back into `Study`, so a mandatory field would make every one unloadable. A study authored before taps existed has no taps, and `0` is the genuine CRC-32/ISO-HDLC of zero bytes (init and xorout are both `0xFFFF_FFFF` and cancel), not a sentinel. The sharp edge: an empty tap list validates against a decoder that never computed the CRC at all — which is why the both-languages pin deliberately carries three real taps.
- **The FFI decode surface still checks `steps_crc` only.** `essd_study_decode_and_verify`'s single `out_crc_matches` bool and `essd_study_decode_full`'s single `CrcMismatch` status cannot say which of three seals failed; folding them in would quietly destroy the property the sibling seals exist to provide, and widening the C ABI would extend a surface §7 records as having no caller anywhere. Left as-is with the reason written at the call site. The real Core↔dev-bench check is dev-bench's own C decoder, which computes all of them.
- **dev-bench aborts the study on a seal mismatch**, naming which seal failed in its own log line, even for seals covering things that firmware version could not yet act on. Computing a seal and ignoring it would leave a study whose declarations arrived corrupt running to completion and reporting captures that are silently missing or wrong.

### 18 — Core validates a submitted `Study` structurally, before generating a `study_id` or touching the serial link

Every `limits` capacity (decision 15) within bounds, every referenced index in-bounds, `Requirements` present and non-blank (decision 40), and every named tap actually declared (`embarch-core`'s `validate_study`/`validate_taps`, decision 19's implementation note). Each failure produces a `400` naming the offending field and limit rather than a raw `serde` deserialize error — which matters because §6's `--study-file` path means a human is often hand-writing the JSON.

### 26 — `steps_crc` is filled in by whoever *submits* a study, not required of whoever *authors* one

Review item 4: decision 17 requires a correct CRC on submission, which makes a hand-authored `Study` JSON file unusable without a human computing a CRC by hand — squarely against decision 6's symmetric-access principle. Resolved without touching the check: `embarch-api`'s `run_study` tool / `run-study` CLI computes `steps_crc` via this crate's exported function and overwrites whatever value (including a missing or zero one) was in the submitted JSON, immediately before `POST /study`. A caller that already computed a correct value — a fuzzing driver generating studies programmatically — is unaffected, since the recomputation is idempotent.

The crate also ships a generated `study.schema.json` for `Study` (via `schemars`), so a human hand-authoring a `--study-file` gets editor/CI validation before ever submitting, independent of the CRC question.

---

