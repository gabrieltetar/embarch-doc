# embarch-study-designer decisions: Serialization, framing, and the link

**Status:** active, 2026-09-02.

Two formats, COBS framing, an append-only enum, and the link budget.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 3 — Format-agnostic at the type level; two formats chosen per hop

`embarch-api` ↔ `embarch-core` stays JSON, matching every existing Core endpoint (`embarch-core/decisions.md` §4) — no reason to break that convention for a hop that isn't resource-constrained. `embarch-core` ↔ `embarch-dev-bench` uses **`postcard`** (pairs naturally with `serde` + `no_std`, no allocator required). Locked without real dev-bench hardware to spike against; a stand-in `no_std`/no-alloc round-trip check is treated as sufficient, flagged for re-confirmation once real nRF54 hardware exists — the same posture as decision 7's firmware-language call. Framing is layered on top: decision 10.

### 4 — Transport for the Core↔dev-bench hop is serial (UART or USB CDC)

Chosen over HTTP because dev-bench is a resource-constrained MCU wired directly to whatever machine runs `embarch-core`. Mirrors Core's existing DUT serial-log pattern (`serialport`, `embarch-core/decisions.md` §5) rather than requiring dev-bench to carry a network stack.

### 10 — COBS-framed postcard, versioned by an append-only top-level enum — not a length prefix or a version byte

postcard has no framing and no self-describing schema. COBS (Consistent Overhead Byte Stuffing) wraps each encoded message in a self-terminating frame that resyncs after a dropped or corrupted byte — chosen over a fixed length-prefix header, which desyncs the reader on any single corrupted length field until a resync heuristic kicks in, a real risk on a physical UART. The `cobs` crate is `no_std` with no allocator, matching decision 5.

Versioning rides on making every message a variant of one top-level `serde` enum (`DevBenchMessage`): postcard's varint enum discriminant gives wire compatibility across additions for free **provided variants are only ever appended, never reordered or removed** — the discipline this decision commits to instead of a hand-rolled version byte. Every later variant follows it (decisions 20, 24, 36, 39), and every `Action` discriminant is likewise append-only: `GattMonitorStart`/`GattMonitorStop` at 5 and 6 (decision 36), `BleSecurity` at 7 (decision 44), `BleUnbond` at 8 (decision 50), `GattMonitorSelected`/`GattMonitorSelectedStart` at 9 and 10 (decision 53).

The one exception, and why it was safe: decision 39 **reuses** discriminants 2, 3 and 4 from the stream triple it retired, because postcard encodes by declaration index and leaving holes would need placeholder variants existing only to be un-constructible. The `Hello`/`HelloAck` handshake refusing a version mismatch outright is what makes reuse safe — and no dev-bench firmware carrying the old shapes had ever been flashed.

### 24 — `Study` crosses in one message; per-step results stream back

Closed the largest gap the 2026-08-15 design review found: `embarch-core/decisions.md` §4 said Core "begins relaying `Study.steps`", but no wire message carried a `Study` at all, and whether steps crossed one at a time or as a vector was unspecified — a real gap, since decision 17's `steps_crc` is computed over the whole vector at once.

`StudyStart { steps, steps_crc }` (Core→dev-bench, once, immediately after the `Hello`/`HelloAck` handshake) carries the whole vector in one postcard message. Whole-vector rather than per-step because it keeps decision 17's CRC check atomic: a per-step transfer needs either a running CRC accumulated message-by-message or per-message CRCs plus a final reconciliation, for a payload already small and bounded (`MAX_STEPS_PER_STUDY = 64`, each `Step` itself bounded by decision 15) and therefore cheap to send in one frame. `StudyDone { completed: bool }` comes back once, after the last step dev-bench actually ran.

Per-step *results* stream incrementally instead, mirroring `StreamChunk`'s reasoning (decision 20): `StepResult { step_index, result }` is sent as each step completes, so Core writes `events.json`'s per-step entries progressively and decision 16's host-side watchdog can key off individual arrivals rather than one final blob.

`StudyStart` has grown by appending only, never inserting, so dev-bench's hand-written C decoder sees one unconsumed trailing field instead of a re-shuffled sequence: `streams` and `streams_crc` after `steps_crc` (decision 39), `dev_bench_log_level` after those (decision 51), `protocols` and `protocols_crc` after that (decision 58).

### 25 — The UART link budget is stated, and stream chunks batch

Closed review item 3: a COBS+postcard single-`Sample` `StreamChunk` (decision 20) is [measured] roughly 10–14 bytes on the wire, and the power-profiling rate this crate serves (10–100 kHz per §1) needs far more throughput than one frame per sample delivers at any reasonable baud.

- **The Core↔dev-bench UART runs at 1 Mbaud** — [assumed] the practical ceiling for both the nRF54L15's UART peripheral and the on-board J-Link VCOM bridge it crosses ([embarch-dev-bench/decisions.md](../../embarch-dev-bench/decisions.md) decision 6) without exotic clocking. Stated here because nothing in either doc previously named a rate.
- **Batching:** one base timestamp plus a fixed sample interval (both known at `StreamStart` time, from `PowerSampleWindow.sample_rate_hz`) means every sample after the first carries only its value. `unit`/`channel_id` (decision 27) ride once per batch, not once per sample, since a capture window doesn't change units mid-stream. Core reconstructs each `rx_utc_ms` as `base_utc_ms + i * sample_interval_ms`.

Superseded in shape by decision 39, which collapsed `StreamChunk` and `StreamChunkBatch` — both of which were still live and still handled by Core in separate match arms, a duplication *this* decision was believed to have removed — into one `StreamChunkBatch` carrying `{ rx_utc_ms, bytes }` records rather than `Sample`s. The link budget and the batching rationale above are unchanged by that.

---

