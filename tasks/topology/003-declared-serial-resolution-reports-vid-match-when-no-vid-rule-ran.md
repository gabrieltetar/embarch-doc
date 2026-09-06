# Give a declared-serial port resolution an honest provenance instead of `vid-match`

**State:** open
**Source:** owner's repo survey, 2026-09-06 — a comment that is provably stale, and a documented value set that is incomplete
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`src/hardware/port.rs:110-117` returns `"vid-match"` for any VID outside the three constants, with
the comment "unreachable given how candidates are filtered". That has been untrue since
`Filter::no_vid_gate` landed (`:172-183`), which `signal::resolve_link_port` uses for every
`Route::Direct` resolution (`src/hardware/signal.rs:227`) — so an outpost signal landing on an
FTDI/CH340 bridge reports a rule name for a path where **no VID rule ran**. `DetectedPort::detected_by`'s
own doc at `:79-82` enumerates only three possible values.

A port selected by a declared serial with the VID gate off should report a provenance naming what
actually decided it; the doc should enumerate every value the field can hold, including `ENUMERATED`;
and the stale "unreachable" comment should go.

Nothing has misled an operator here yet — this is filed as the staleness it is.

## Why now

Decision 18 already set the precedent for the unfiltered listing: its provenance is "a fourth answer
… rather than one of the three that name a *rule*, because an unfiltered listing applied no rule".
The declared-serial path is the same argument, unapplied.

## Measured on the bench, 2026-09-06 (leg 020, `tasks/topology/006`)

This was filed from source reading; it has now been observed live, and the ambiguity is wider
than the filing assumed. With both probes attached, `GET /dev-bench/port` returned:

    {"port_name":"COM17","detected_by":"segger-vid-match","interface":2,
     "serial_number":"001057729826","product_id":4201}

and the host had **three** SEGGER CDC UART ports at that moment [measured, `Win32_PnPEntity`]:
`COM16` (`VID_1366&PID_1069&MI_00`), `COM17` (`…&MI_02`) — one device instance, one serial —
and `COM5` (`VID_1366&PID_1024&MI_00`) on the other J-Link. **So the rule the answer is
credited to matched all three.** The declared serial eliminated `COM5` and the declared
interface eliminated `COM16`; `segger-vid-match` eliminated nothing.

**Why this is worse than a label error:** `detected_by` is the field an operator reads to
judge how much to trust a port, and it currently names the *weakest* rule consulted rather
than the one that chose — so the most-declared, most-trustworthy resolution on this bench is
reported with the provenance of the least-discriminating rule available.

## Done when

- [ ] A named constant for the declared-serial provenance exists beside `ENUMERATED`, and `select`
      sets it when `no_vid_gate` is on.
- [ ] `DetectedPort::detected_by`'s doc lists every value the field can hold.
- [ ] The existing declared-serial tests in `signal.rs` assert the provenance as well as the port name.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features hardware`.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
