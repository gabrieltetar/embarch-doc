# embarch-study-designer decisions: Analog capture

**Status:** active, 2026-11-24.

What a study declares to record an analog input at audio rate: the source, the framed bytes, and the session around them. The owner's thirteen decisions are EMB-469's; these are how this crate carries them. Reference: [../interfaces/analog.md](../interfaces/analog.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 104 — `StreamSource::AnalogInput { sample_hz, channel }`: the rate and the input are the study's, and the source is a wire change

A tap of this source starts the dev bench's analog input at `sample_hz` on `channel` (an index; which pin it is lives in the board's devicetree overlay, EMB-469 decision 3). The tap is `Raw`, open for the whole study, and at most one per study (one samples link). `validate_taps` refuses a rate of 0 or over `MAX_ANALOG_SAMPLE_HZ` (200000, **assumed**: a backend that cannot reach a declared rate still refuses it at run time), a channel at or past `MAX_ANALOG_CHANNELS` (8), another encoding, a step-range scope, and a second input, each with the index and the reason.

- **Whole study, because the start header comes once.** A tap opened later would hold blocks with no header to read them against.
- **A wire bump.** `StreamSource` rides `StudyStart` and `streams_crc`, and dev-bench must read the rate to start the input: `DEV_BENCH_WIRE_SCHEMA_VERSION` 15 to 16, `HOST_TYPE_SCHEMA_VERSION` 22 to 23 (decision 12). The new variant is appended at discriminant 5; `[05 80 FA 01 00]` is `{32000, 0}`, pinned by a test. **dev-bench's firmware has no arm for tag 5 until its own work item adds one**, and its build reads the new constant from this source.
- **Counted as dev-bench-mediated**, though its bytes reach Core on the samples link and not as `StreamChunkBatch`: the node that produces them is the bench.
- *Rejected: a host-only tap description.* dev-bench needs the rate, and a second declaration beside the tap could disagree with it.

### 105 — `RecordFraming::AnalogBlocks`, and one crate-side decoder for the block and the start header

`Study.record_checks` gains a second framing, `AnalogBlocks { channels, samples_per_block }`, naming the analog tap. **Unlike `MagicPrefixedCrc32Le` the length is declared**, because a block's size is fixed by the layout: a block is cut by length and a damaged one is skipped to the next `EAB1`. `validate_record_checks` refuses 0 or over-cap values; `Study::validate_analog_capture` refuses an analog tap with no such check, a check naming a missing or non-`Raw` tap, and a tap with no session.

**The bytes are this crate's choice inside the owner's fields** (EMB-469 decisions 7 and 8), pinned in [analog.md](../interfaces/analog.md): little-endian, magics `EAB1` and `EAH1`, frame-interleaved `i16`, a CRC-32/ISO-HDLC on the header as well as on each block, and an event word of edge count, first-edge offset and level. **`embarch-dev-bench` has to emit exactly these**; the byte tests in `src/analog.rs` are the vectors.

`decode_block`, `decode_start_header` and `verify_blocks` are `no_std`, allocation-free and panic-free, so Core's samples decoder, the WAV export and tests share them. **A skipped block is found by the index sequence, not counted**: `verify_blocks` reports each gap's expected and received index, the total missing samples, backward steps and marker edges, beside the usual `RecordReport`. A damaged block costs one block; its own index is unknown, so it shows as a gap in its neighbours.

- *Rejected: widening `RecordReport` with the gaps.* Core builds that type by literal; a new field would break it for a fact only this framing has. `verify_records` returns the report half.
- *Rejected: a marker-edge offset per sample.* The word carries the first edge and a count; a block with several edges names the first and counts the rest.

### 106 — A session is a host-only declaration on `Study`, because a dev-bench study cannot hold a prompt

Checked 2026-11-24: `Action` has no prompt variant and the dev-bench wire has no message for one; `HostAction::Prompt` is only in `HostStudy`, whose taps are `Signal` only. So `Study.session: Option<SessionSpec>` (host-only, never on the wire, sealed by neither CRC, appended last and never skipped, since `Study` also travels as postcard):

- `start_text`, `done_text`, up to 8 `run_fields { name, label, required }`, `max_duration_ms` (1 to 300000: the owner's 5 minutes, about 19 MB at 32 ksps) and `export_dir`.
- **Run fields are free text.** The study declares which are asked and so saves them with it; Core records the answers as `RunFieldValue`s, and `validate_run_answers` checks only that each names a declared field once and that required ones are not blank. Nothing types or ranges an answer.
- **`export_dir` is named by the study and resolved by Core**: blank, a control character or a `..` component is refused; absolute is allowed.
- **No prompt kind.** The HIL run file's `prompt_kinds` has no type in this crate yet, and neither session prompt asks anyone to observe.
- **An analog tap needs a session**, because without a cap a recording runs at about 64 kB/s until something stops it.
- *Rejected: a `Prompt` action in `Action`.* A wire change to the step list and a firmware prompt path for something only Core shows.
