# embarch-study-designer: declared payload layouts

**Status:** active, 2026-09-02.

How a captured byte payload becomes CSV columns, and the line this crate does not cross. Why: [../decisions/payload-meaning.md](../decisions/payload-meaning.md). Taps: [taps.md](taps.md).

## Struct layouts

`StreamEncoding::Struct { decoder }` indexes `Study.decoders`, which is **host-only and never crosses the dev-bench hop** — the same posture as `requires`, and for a stronger reason: what a payload means is exactly the knowledge the generic pipeline took away from that node. Only the index rides on the tap, because a tap's encoding *does* cross and dev-bench walks past it.

- **`ScalarType`** — `u8`/`i8` plus the 16/32/64-bit integer and IEEE-754 float widths in both byte orders, 18 in all. **Width, signedness and byte order only** — no scale, no offset, no unit.
- **`StructField { name, ty }`** — one named scalar. Fields are packed in declaration order with **no padding**: a layout needing padding declares a field for it, rather than having an alignment rule guessed on the DUT compiler's behalf.
- **`StructLayout { name, header, repeat }`** — `header` is read once at offset 0; `repeat`, when non-empty, is read as many times as fits in what remains, producing **one row per repetition** with the header's values denormalized onto each.

Authored in the firmware repo's `embarch/study-structs.toml` and resolved into the study at build time, so the submitted study is self-contained — **Core cannot read that repo**.

**Row shape:** `rx_utc_ms, step_index, step_name, rep_index, <header fields…>, <repeat fields…>, payload_hex, decode_note, core_rx_utc_ms`. The last two are **always present, not only on a failed row**, so a reader can tell a payload that fitted the layout from one that didn't **without the columns shifting mid-file**.

**A payload that doesn't fit still gets a row**, decoded columns empty and the raw bytes plus a reason filled. The raw file is written before any decode is attempted, so a wrong layout costs a rendering rather than a capture. **An empty repetition list is zero rows and no error** — a DUT sending a header with nothing after it is real, and a row invented for it would be invented data. The rendered error text carries no comma and no quote, asserted in its own tests, because **this crate refuses to produce a CSV value that would break the column shape rather than quoting it.**

## Sample layouts

**`SampleLayout`** — `F32Le`/`F32Be`/`I16Le`/`I16Be`/`U16Le`/`U16Be`. **Element width, type and byte order only: no scaling, no offset, no unit conversion.** Those would be a claim about what a particular DUT's bytes *mean*, which is its engineers' knowledge and not this crate's; `unit` names the quantity, and nothing here transforms the number. Append-only.

**`Sample { rx_utc_ms, value, unit, channel_id }`** is **no longer a wire type**: the wire carries arrival-stamped bytes, and a `Sample` is what the crate-side decode produces from those against a tap's declared layout. Every `Samples`-encoded tap shares this identical row shape rather than each inventing its own columns, and **that row shape is untouched by the reshape** — only the path the numbers take to reach it changed.

`rx_utc_ms` is stamped **by dev-bench at capture time** off its own clock, seeded and resynced from the host on every handshake — not assigned by Core on arrival, so the timestamp reflects when the sample was taken rather than when it reached Core over a variable-latency link. `unit` and `channel_id` are declared **once per tap** rather than repeated per message, since neither changes mid-capture.

**Row shape:** `rx_utc_ms, step_name, value, unit, channel_id`, with `core_rx_utc_ms` appended by Core itself rather than by this crate — **it is Core's own receipt time, not part of the wire type.** A row whose step name will not fit returns nothing, and Core logs and skips that one row, because **a truncated CSV row is a worse failure than a dropped one.**

**The decode's timestamp rule:** with a declared rate, element *i* is stamped `rx_utc_ms + i * 1000 / sample_hz`; **with no declared rate, every sample carries the record's own arrival stamp unchanged**, rather than an interpolation nobody stated the basis for. A trailing partial element is dropped, **never zero-padded into a plausible wrong value.**
