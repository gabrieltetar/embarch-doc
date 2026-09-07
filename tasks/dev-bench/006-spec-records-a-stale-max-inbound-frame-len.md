# Correct `DBM_MAX_INBOUND_FRAME_LEN` in the spec's constants table

**State:** done by agent/dev-bench/006-stale-inbound-frame-len, 2026-09-07
**Source:** owner's repo survey, 2026-09-06 — one row of a table that was correct once and went stale at schema v15
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-dev-bench/spec.md:80` records `DBM_MAX_INBOUND_FRAME_LEN` as **9,415 B
[measured]**. Expanding the macros in `app/src/serial_protocol.h:162-164` and `:236-238` gives
**12,507 B** (`STUDY_START_LEN` = 12,312 since decision 41 added `DBM_MAX_PROTOCOLS_WIRE_LEN` =
3,072). The sibling row at `:81`, 3,082 B outbound, is exactly right — so the table was correct once
and one row went stale.

The row should carry the value the header actually computes, and say what changed it (the
`protocols` span joining `StudyStart`'s bound at schema v15). Same pass, check the neighbouring
`link_rx_ring` row: its "deliberately not `DBM_MAX_FRAME_LEN`" rationale is unaffected but reads
against the wrong magnitude.

Doc-only — this is arithmetic over a committed header, and needs no build.

## Why now

`app/src/main.c:888` sizes a static RX buffer from this constant and `spec.md` §4 argues the ring
size against it. A stale figure understates resident SRAM by ~3 KB on a board `spec.md` describes as
87.04% full.

## Done when

- [x] The `DBM_MAX_INBOUND_FRAME_LEN` row equals the value the header expands to, with the
      arithmetic reproducible from the constants named in the row.
- [x] The provenance tag is honest about being computed from the header rather than `[measured]`,
      per `../../DOC-CONVENTIONS.md`.
- [x] The outbound row is left alone — it is correct.
- [x] No other row in §5 disagrees with `app/src/serial_protocol.h`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Notes

Arithmetic, from `app/src/serial_protocol.h`:

- `DBM_MAX_STUDY_START_LEN` = 8 + (16 × (512 + 64)) + 8 + 3072 + 8 = 12,312 B
  (`DBM_MAX_STEPS_PER_STUDY`=16, `DBM_MAX_PAYLOAD_LEN`=512,
  `DBM_MAX_PROTOCOLS_WIRE_LEN`=3,072).
- `DBM_MAX_INBOUND_RAW_LEN` = 12,312 + (8 × 16) + 16 = 12,456 B
  (`DBM_MAX_STREAMS_PER_STUDY`=8).
- `DBM_MAX_INBOUND_FRAME_LEN` = 12,456 + ⌊12,456 / 254⌋ + 2 = **12,507 B**.

`link_rx_ring`'s neighbouring row (spec.md §5) states no numeric value for
`DBM_MAX_FRAME_LEN` and its "deliberately not `DBM_MAX_FRAME_LEN`" rationale
does not depend on the stale figure — left unchanged; checked against
`serial_protocol.h` and still accurate.

`decisions/logging.md`'s citation of "9,415 bytes" (decision 38) is a dated
historical snapshot of the constant's value *before* schema v15 added
`DBM_MAX_PROTOCOLS_WIRE_LEN` to `StudyStart` — correct as history, left alone
per `DOC-CONVENTIONS.md`'s decision-entry semantics (a decision entry is what
was true on the day it was written).

No `decisions.md`/`open.md` change and no `status.d/` fragment: this is an
arithmetic correction, not a design decision, and touches no suite-level fact.
`decisions/ble.md` has 6 B of reserve left regardless, so no new entry was an
option worth avoiding anyway. Doc-only — no build, no board.
