# 115 — Stamp each line of a signal capture with its receive time

**State:** done (agent/core/115-capture-lines-carry-receive-times), 2026-10-26
**Source:** api/131 (decision 89 in `embarch-api/decisions/bench-exchange.md`): `bench_exchange` merges two consoles into one timeline, but `GET /signals/{name}/capture` carries a byte range with `offset`, `next_offset`, `elapsed_ms` and `gaps`, nothing per line, so the client can only stamp a line with the poll that first saw it (a ceiling, within its poll interval, default 100 ms). `tasks/core/101` stamps lines only inside a host-study tap, so it does not cover this. Filed from `inbox/core-capture-line-receive-times.md` by the 2026-10-26 leg.
**Scope:** core
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 06:42 leg

**Doc reserve in your scope, all parked under `tasks/core/112` (blocked, `In flux: yes`):** `embarch-core/open.md` 5,070 / 5,120 B (**50 B left**), `embarch-core/spec.md` 9,638 / 10,240 B (602 B left), `embarch-core/decisions/probes.md` 11,263 / 12,288 B (1,025 B left). Decision 92 lives in `decisions/signal-capture.md` (4.3 KB, not in reserve): amend it there or add a new topic file. A blocked compaction task parks the pass, not the reserve, so **if you add bytes to `open.md` or `spec.md`, compact that file in this unit**: remove or shrink only what is closed or restated elsewhere, carry `core/112`'s `Must not delete:` list (decision 89's "assumed, not measured" spelling paragraph and the `409 chip-mismatch` wording; decision 80's ARMv6 RCC reasoning; decision 22's identity-gate relation), leave the decision-89 bullet alone, and say what you cut in your report. Prefer recording any open point inside the decision instead of `open.md`. The capture `GET` route's response is a wire shape `embarch-api`'s client decodes (`SignalCaptureResponse`, api decision 88): keep the change additive.

## What

A capture (`embarch-core` decision 92) records, for each line it completes, the time that line's first byte was received, on one Core clock shared by every capture and by exchange replies. `GET /signals/{name}/capture` returns, beside `text`, a `lines` list (or a parallel array) of `{offset, rx_ms}` for the lines in the returned range, `rx_ms` relative to the capture's start with the capture's start time given in UTC ms, so two captures and an exchange can be merged exactly. A client that does not read the new field is unaffected (additive).

## Why now

`bench_exchange` shows a timeline whose order across consoles is only as good as its poll interval: a DUT log line and the command that caused it can land in one poll window and be ordered by arrival at the client, not by the wire. Core sees the bytes arrive; it is the only place the real time exists.

## Done when

- [x] A capture read returns per-line receive times on a clock the exchange reply (`elapsed_ms` start) can also be placed on.
- [x] Offsets in `lines` match `text` byte for byte, including across a `gaps` entry.
- [x] Test with a scripted port: two lines written 200 ms apart carry receive times 200 ms apart (within a stated tolerance).
- [x] `embarch-core` spec/decisions updated; gate green.

## Shipped

Decision 94 (`embarch-core/decisions/signal-capture.md`). Capture `GET`/`DELETE` gain `started_utc_ms` and `lines: [{offset, rx_ms}]` (line first-byte times); exchange reply gains `started_utc_ms`. Test `lines_carry_receive_times_and_offsets_match_text_across_a_gap` (scripted port, 200 ms apart, tolerance 150..600 ms). No reserve file touched, nothing cut.

**Debt:** no real port has produced these times; the read-latency and cross-capture wall-clock error are assumed. Native Windows build not run.
