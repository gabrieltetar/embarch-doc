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

## Done when

- [ ] A named constant for the declared-serial provenance exists beside `ENUMERATED`, and `select`
      sets it when `no_vid_gate` is on.
- [ ] `DetectedPort::detected_by`'s doc lists every value the field can hold.
- [ ] The existing declared-serial tests in `signal.rs` assert the provenance as well as the port name.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features hardware`.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
