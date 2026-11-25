# embarch-study-designer: Analog capture

**Status:** active, 2026-11-24. Code: `src/analog.rs`, `src/session.rs`, always compiled, `no_std`. Why: [../decisions/analog-capture.md](../decisions/analog-capture.md), decisions 104 to 106. `DEV_BENCH_WIRE_SCHEMA_VERSION` 16, `HOST_TYPE_SCHEMA_VERSION` 23.

All integers little-endian. The fields are the owner's (EMB-469 decisions 7 and 8); the byte values are this crate's, and `embarch-dev-bench` emits them.

**Start header**, once per session, 75 bytes: `EAH1` (4), `sample_rate_hz` u32, `resolution_bits` u8, `gain_numerator` u8, `gain_denominator` u8, `reference` u8 (0 internal, 1 VDD/4, others carried), `channel_count` u8, `vdd_mv` u16 (measured once at start), `input_name` 16, `board` 24, `image_version` 16 (UTF-8, NUL-padded), CRC-32/ISO-HDLC over the 71 bytes before it (4). Refused: wrong length, magic or CRC, text with a non-NUL after a NUL, a zero rate, resolution, gain part or channel count.

**Sample block**, `16 + 2 * channels * samples_per_block` bytes (528 for one channel of 256): `EAB1` (4), `index` u32 (per-channel sample index of the first frame), event word u32, the `i16` raw ADC codes **frame-interleaved**, CRC-32/ISO-HDLC over every preceding byte (4). Channels and frames come from the study's `AnalogBlocks` layout; a block carries neither. **Event word:** bits 0 to 7 first-edge frame offset, bit 8 level after it, bits 16 to 23 edge count (0 means the rest is meaningless); other bits are kept in `raw()`, not refused.

| Function | Returns |
|---|---|
| `decode_block(bytes, channels, samples_per_block)` | `AnalogBlock { index, events, .. }` with `sample(frame, channel)` and `codes()`, or `BlockError` (`BadLayout`, `WrongLength`, `BadMagic`, `CrcMismatch { stored, computed }`) |
| `decode_start_header(bytes)` | `StartHeader`, or `HeaderError` |
| `IndexTracker::observe(index, frames)` | `InOrder`, `Gap { expected, got, missing_samples }` or `Backwards` |
| `verify_blocks(bytes, channels, samples_per_block)` | `BlockReport`: a `RecordReport`, `header_ok`, up to `MAX_GAPS_REPORTED` (32) `IndexGap`s, `gap_count`, `missing_samples`, `backwards_count`, `marker_edges` |
| `encode_block`, `encode_start_header` | the bytes, for fixtures and the firmware's own tests |
| `Study::validate_analog_capture()` | the cross-checks of decision 105 and the session's rules; run after `validate_taps` and `validate_record_checks` |

**Study declarations.** `StreamSource::AnalogInput { sample_hz, channel }` ([taps.md](taps.md)); `record_checks[].framing = AnalogBlocks { channels, samples_per_block }`; `Study.session = SessionSpec { start_text, run_fields: [RunField { name, label, required }], done_text, max_duration_ms, export_dir }`, `None` when absent. Limits: `MAX_ANALOG_SAMPLE_HZ` 200000, `MAX_ANALOG_CHANNELS` 8, `MAX_ANALOG_SAMPLES_PER_BLOCK` 4096, `MAX_SESSION_MS` 300000, `MAX_RUN_FIELDS` 8, name 32, label 64, answer 128, prompt text 192, `export_dir` 128 bytes (all **assumed**).

`validate_session` and `validate_run_answers` return `SessionError`; every error's `Display` names the field.
