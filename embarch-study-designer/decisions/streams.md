# embarch-study-designer decisions: Streams: one generic capture pipeline

**Status:** active, 2026-09-02.

One declared tap model replacing four near-identical capture paths.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 11 — Result storage splits by data shape: a JSON events file plus CSV data files, not one file and not a database

Per-step pass/fail and captured BLE data go in a small, human-readable `events.json`; time-series samples — potentially large and high-rate — go in separate CSV files referenced from it rather than embedded. So the common case (did this study pass) never requires parsing a large series, while the small side still follows the suite's no-database principle (`embarch-api/decisions.md` §3.6). Full layout in §5.2. Decision 39 replaced the fixed `data.csv`/`waveform.csv`/`gatt.csv` set with `streams/<tap name>`; the split itself is unchanged, and is the same reasoning that keeps decision 36's inline summary separate from its streamed transcript.

### 20 — A streaming sub-protocol from dev-bench to Core, replacing discrete end-of-window sampling
A capture can run for the length of a step, producing far more data than fits in one bounded message. Open/chunk/close variants (append-only per decision 10) carry records; chunks carry no channel tag of their own, since Core tracks which channel is open from the last matching open — keeping per-chunk overhead minimal on a UART link. More than one channel can be open concurrently, so open and close both carry the tag.

Originally each chunk carried a `Sample` directly rather than raw sensor bytes, so a chunk was self-contained and hardware-agnostic at the wire level, with translating a raw reading into a `Sample` being dev-bench's job before the value reached the wire. **That is what kept Core's CSV writing free of hardware-specific decoding** — the same property decision 39 preserves by moving *meaning* into a declared encoding rather than back into the node.

**Core writes each record to disk incrementally** rather than buffering the whole capture until the study finishes, so raw capture data survives even a Core crash that writes off the study itself.

### 21 — Sensor-waveform capture is a `GattOperation` variant, not a step-level field

`StreamCapture` joined `Read`/`Write`/`Notify`/`Indicate`/`Subscribe` (§4.3) — a continuous capture of whatever the characteristic streams (a PPG waveform, say). No separate duration field, matching `PowerSampleWindow`'s reasoning: it runs for exactly as long as the step's own `timeout_ms`/completion allows, so a capture can't silently outlive or fall short of the step characterizing it. Folded into decision 39's tap model as `StreamSource::GattNotify`.

### 27 — `Sample` carries `unit` and `channel_id`

Resolving an ambiguity `StreamChannel`'s two variants already implied but never settled: `Sample { rx_utc_ms, value }` was one shape shared by power and arbitrary waveform data, with nothing on the wire saying what `value` meant or which of several concurrent channels on the same step it came from — a real gap the moment a capture needs more than one bare scalar (current *and* voltage sampled together, a multi-lead sensor). Added ahead of real hardware forcing the question, to avoid stacking a second breaking wire change on the one hardware validation will likely already require.

`unit: Unit` is a small append-only enum (`Milliamps`, `Volts`, `Milliwatts`, `Raw`); `channel_id: u8` disambiguates concurrent streams on the same channel (`0` for the common single-channel case). Both thread through `Sample::to_csv_row`/`csv_header` as trailing columns, and both ride once per batch rather than once per sample (decision 25).

### 39 — One generic inbound stream pipeline; the write direction explicitly not accepted
Opened by [embarch-outpost](../../embarch-outpost/design.md), whose DUT-side debug UART needs its bytes captured for a study's duration and which would otherwise have become **the fourth** near-identical capture pipeline here, after power, sensor waveform, and (as of the day before) the GATT transcript. **Four pipelines differing only in what the bytes mean is the point at which the pattern has to be named rather than repeated again.**

`Study` gains one field beside `steps`: a list of `StreamTap`s. A tap declares four things and nothing else — **where the bytes come from, how long the tap lives, how to render what arrives, and what to call the output.** Every bespoke channel becomes a declared source; every bespoke row shape becomes a declared encoding. Shapes: [../interfaces/types.md](../interfaces/types.md) §4.8.

| Was | Becomes |
|---|---|
| the power channel plus its sample-carrying chunks (decisions 20/25) | `StreamSource::PowerFrontEnd { sample_hz }` + `StreamEncoding::Samples` |
| `GattOperation::StreamCapture` (decision 21) | `StreamSource::GattNotify { … }` + `StreamEncoding::Samples` |
| a dedicated transcript message (decision 36) | `StreamSource::GattTranscript` + the matching encoding |
| `LogLine`, which reached only Core's rolling log and never a study's results | `StreamSource::DevBenchLog`, a reserved tap — closing a real asymmetry rather than inventing a feature |
| *(did not exist)* | **`StreamSource::Signal { name }`** — a signal Core reads itself, its carrier resolved by topology. The outpost's tap |
| *(did not exist)* | **`StreamEncoding::OutpostTrace`** — decoded against a build-time manifest |

**`StreamSource::Signal { name }` is the one genuinely new idea, and it is what makes the outpost expressible at all.** Every other source is dev-bench-mediated: dev-bench receives the bytes and forwards them. The outpost's bytes reach Core over a wire that **bypasses dev-bench entirely** today and are intended to go through it later — so the tap names the *signal* and topology's declared route decides the carrier. The identical saved study (decision 38) then runs unchanged across that migration, across a differently-enumerating USB bridge, and against a Core on another machine. **A source variant naming the concrete port or pin would have re-authored every saved study the day the bench was rewired.**

**The write direction is explicitly not accepted.** A send action, an expect action and the shell-interaction case stay in the proposal, unadopted: the outpost is TX-only and needs nothing from them, and adopting a step type nothing yet sends would build a capability nothing needs. (Decision 58 later closed that direction by a different route — an authored state machine, not a generic write step.)

**`Step.power_sample` is retired; a `PowerFrontEnd` tap is the only way to author power capture.** Settled against what the code did rather than what the types allowed: `power_sample` was already **fully vestigial** — Core never read it, dev-bench's encoder wrote its `Option` byte as `None` unconditionally and its decoder read-and-discarded it, and the one authoring path always emitted `None`. Retiring it deleted a second way of saying something only one way had ever said.

**The cost of doing this when it was done, stated plainly.** It reversed a decision one day old (36), re-bumped a just-bumped schema, and edited firmware that was code-complete and deployed. The offsetting fact is the one the proposal argued for itself: **no real byte had ever crossed the streaming path**, verified rather than assumed at the time. Nothing was load-bearing on a real bench yet, and that stops being true the moment either runs. **This was the last cheap moment and it was taken deliberately.**

**A leftover found on the same wire**, walking the C encoder against the Rust type: dev-bench was still writing two `Option` bytes for two `StepResult` fields retired a version earlier — on the message it sends most. Both suites stayed green because each agreed with itself, since that message predated decision 36's both-languages rule, which applied to *new* records. **That pairing has now found a real discrepancy the first time it ran for a given record, twice.**

