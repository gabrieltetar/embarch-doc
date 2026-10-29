# embarch-core decisions: Host-run studies

**Status:** active, 2026-10-26.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). HTTP surface: [../interfaces/host-studies.md](../interfaces/host-studies.md). Siblings: [signal-exchange.md](signal-exchange.md) (decisions 79, 85, whose code path a step runs), [studies.md](studies.md) (decision 19's `study_lock`). Design of record: [the proposal](../../embarch-host-study-proposal.md), [`embarch-study-designer`](../../embarch-study-designer/decisions.md) decisions 80, 86.

### 95 — `POST /host-studies`: Core runs `Exchange` and `Wait` steps itself, and the teardown on every way out

Field use on a USB PD charger board (2026-09-09 to 2026-10-20) ran the PD source sequence as a bash script: 441 shell exchanges in 16 e-load runs. Each script reimplemented abort and safe state, so a run that died part-way left the load sinking and the partner at 20 V, and two runs were lost to an empty reply the script could not tell from a dropped command.

**The route.** `POST /host-studies` takes a `HostStudy` (`embarch-study-designer`), checks it, takes `study_lock` (one lock for bench and host studies and `/dev-bench/hello`: `409` while any holds it), checks every `Exchange` signal against topology (declared, direct, `host-to-dut` or `bidirectional`: `400` by step), and runs the steps on one blocking thread. `202 {study_id}`; the record is the usual `events.json`, read unchanged by the Studies routes. Lease-gated (decision 93).

**`Exchange` shares the exchange route's code** (`api::run_signal_exchange`), with `hw_lock` per step, not per run: a flash can interleave between steps, and gets `503` naming the holder if a step holds it. The line goes out with `\n` appended, since a `HostStep.line` carries no terminator and the signal declares none (assumed, as the field scripts sent it; a per-signal terminator is a topology change, not made here).

**Outcomes decide on markers only.** `refused_on` in the reply is `Fail` (the one marker `embarch-study-designer` decision 80 allows); else `until` seen is `Pass`; else a lost port is `Fail`; else **zero bytes back is `Fail` with `detail: empty_reply`**, and bytes without `until` is `TimedOut` with `detail: until_not_seen`. No step reads a number out of a reply. `HostStepResult.outcome`'s `Fail` reason is 64 bytes, so a longer account (port names seen, error text) is the record's `note`. Rows also carry Core's start and end times; the reply is raw, escape codes kept, capped at `MAX_HOST_REPLY_LEN` (4,096) with `reply_truncated` set (fields: [interfaces](../interfaces/host-studies.md)).

**Teardown always runs**: after the last step, a failed or timed-out step, a cancel, a caught panic in a step. It ignores the cancel flag, runs every step even when one fails, and records each; `continue_on_fail` has no effect in it. A study stops at the first non-`Pass` step without `continue_on_fail`; the job is still `completed`, with `completed: false` and a `stopped_reason` in `events.json`.

**`POST /study/{id}/cancel`** sets a flag (`202`). The step in flight finishes (an exchange cannot be interrupted, so within its `timeout_ms`, at most 10 s; a `Wait` or `delay_before_ms` within 20 ms), the rest are skipped, the teardown runs. `409` unless it is a running host study (a bench study has no cancel), `404` for an unknown id.

**Events.** Not the proposal's reused `StepCompleted`: a bench `StepResult` has no reply field, so a host step is its own `HostStepCompleted {study_id, list, step_index, result, detail, started_utc_ms, ended_utc_ms, delay_before_ms}` on the same SSE channel.

**Every action runs:** `Instrument` since [104](instruments.md), `Prompt` (also inside a `Repeat`) since [105](host-prompt.md). `Repeat` and `line_counts` run ([99](#99--repeat-runs-and-line-counts-are-rendered-from-the-raw-tap-files)). `streams` taps run on [98](#98--a-host-studys-signal-taps-are-captures-opened-once-for-the-whole-study)'s terms. No dev-bench wire change.

**Measured vs assumed.** Every exit path is proven over a scripted fake port only. **Assumed:** the `\n` terminator against the PD bench, and teardown reaching a real partner after a forced failure (hardware debts, task `core/102`). **Open:** whether waiting out an exchange in flight is too slow for a load that must stop is unknown until a bench run.

### 98 — A host study's signal taps are captures, opened once for the whole study

Field use (2026-09-09 to 2026-10-20): every exchange dropped what the console printed since the last one (`discard_pending`), and a listen lasted at most 10 s, so the field scripts listened in 42 windows of 1.5 to 6 s and an event between windows was lost. The 8-Hard-Reset count (56 s, two consoles) went around Core with two PowerShell readers.

**A tap is a [decision 92](signal-capture.md) capture, started at submission and stopped after the teardown.** `POST /host-studies` starts one per `Signal` tap before the job is accepted, so a port that cannot be opened, is held by another tap or has a capture running is a `409` and nothing was written. No new port owner: an `Exchange` on a tapped signal already finds the capture in the registry (`api::run_signal_exchange`) and writes through its open handle, so the port opens once (Windows allows one open per COM port) and the reply is read from the same byte stream, from the write, with the echo rule applied. On a tapped signal `discard_pending` is moot: nothing is discarded, what came before the write is in the tap. Two consoles tapped in one study give both sides of a PD exchange.

**Storage.** A capture takes an optional sink, called with every run of bytes it reads (an exchange's reply included), in order. The sink writes `streams/<name>.txt` verbatim (ANSI kept; stripping is for views) and a row per line into `<name>.arrival.csv` (`byte_offset,core_rx_utc_ms,bytes`), through `StreamStore`, so `GET /study/{id}/stream/{name}` and `/arrivals` read it unchanged. A chunk is split at newlines before it is stored, so a read holding three lines yields three rows; a line split across reads is two rows, the first being when its first byte arrived. The bench-study tap (`read_signal_tap`) splits the same way. **One clock:** every stamp is one anchor taken at the study's start plus the monotonic time since, shared by all taps, so two consoles' lines order against each other without a wall-clock step. The markers a capture inserts for a lost port are not written to the file; `events.json`'s `streams` carries each tap's `state`, `bytes_written`, `truncated` and `gaps` instead.

**Limits.** A tap ends at `TAP_MAX_S` (6 h) or the capture's 16 MiB buffer cap, whichever first; `streams[].state` then says `expired` or `byte_cap`, `truncated` is set, and later exchanges open the port themselves. **Reasoned, not measured:** the field's longest run was minutes. `Text` and `WholeStudy` only; `Steps` scopes wait for `Repeat`'s semantics.

**Measured vs assumed.** Proven over in-process fake serial pairs only (two consoles, exchanges on both, nothing lost between steps, opened once, stamps on one clock). **Assumed:** the same on COM ports at the PD bench's rates, and that a tapped CDC ACM console survives a Hard Reset without a gap (hardware debt, task `core/101`).

**The CY4500 analyzer (open, not decided here).** Whether a `Prompt` asks the operator to save the analyzer's capture and Core attaches it, or the analyzer is out of scope, needs the capture format confirmed on the analyzer. Not inferred; filed as an inbox drop.

### 99 — `Repeat` runs, and `line_counts` are rendered from the raw tap files

Field use: 34 of 96 bench tests ended in a `grep -c` over a console dump, one-off and not rerunnable with a corrected pattern.

**`Repeat`.** A marker `IterationMarker` is recorded as each pass starts; `{value}` in an inner `Exchange.line` is the `values` entry or the 1-based pass number; each inner record carries `iteration` and `inner_index` (its `index` is the `Repeat`'s). An inner step's own `continue_on_fail` governs; a cancel is seen before each pass and inner step; `delay_before_ms` applies once. Teardown may hold a `Repeat` and never stops. A `Prompt` or `Instrument` inside one runs as at top level (104, 105). **One clock:** `StudyClock` (anchor plus monotonic time) stamps the markers, step times and every tap line, so a marker compares with a line directly. `events.json` gains `iterations` (the markers) and `repeats` (each `Repeat`'s span, which says where the last pass ends).

**The view.** `GET /study/{id}/line-counts` counts each `LineCount` over `streams/<tap>.txt` split at newlines **after** the run, so a line that arrived in two records is one line, placed by the row holding its first byte. Per `Repeat`: a count per pass; plus the whole-run total, the tap's line count, and `outside_passes` (before pass 1, after the last pass, between repeats). A count is **shown, never compared**. The submitted study is kept as `study.json` so the view can be rendered later; `POST` of the same path takes `{line_counts: [...]}` to count a corrected pattern over the same finished run (nothing stored; `400` for an undeclared tap or a pattern that does not compile; `409` before the run ends). Both routes are lease-open: they read files and open no port.

**Measured vs assumed.** The fixture study's eight counts are proven over a canned two-tap capture written through the real stream store. **Assumed:** a real console's lines land in the pass that caused them (a reply delayed past the pass's end counts in the next pass), which only the PD bench shows (hardware debt, task `core/116`).
