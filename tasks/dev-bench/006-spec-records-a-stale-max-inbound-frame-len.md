# Correct `DBM_MAX_INBOUND_FRAME_LEN` in the spec's constants table

**State:** open
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

- [ ] The `DBM_MAX_INBOUND_FRAME_LEN` row equals the value the header expands to, with the
      arithmetic reproducible from the constants named in the row.
- [ ] The provenance tag is honest about being computed from the header rather than `[measured]`,
      per `../../DOC-CONVENTIONS.md`.
- [ ] The outbound row is left alone — it is correct.
- [ ] No other row in §5 disagrees with `app/src/serial_protocol.h`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
