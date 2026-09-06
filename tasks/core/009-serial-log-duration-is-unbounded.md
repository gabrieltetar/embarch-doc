# Bound `GET /serial-log`'s `duration_ms`, which holds `hw_lock` past every client's timeout

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `embarch-core/interfaces.md:21` calls this route bounded; only the caller bounds it
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`src/api.rs:510-529` takes `hw_lock` for the whole handler and passes the caller's `duration_ms`
straight through with no ceiling (`SerialLogQuery`, `api.rs:488-502`, default 2000). `src/serial.rs:17-28`
then loops to that deadline appending into an unbounded `Vec`. The shared client's serial timeout
defaults to 15 s (`embarch-api/crates/embarch-core-client/src/lib.rs:41-43`), so any
`duration_ms >= 15000` means the caller gives up while Core keeps the hardware locked for the full
duration — then discards the result. **Corrected 2026-09-06 by `core/007`: it does not `503`
everything else, it *queues* everything else, silently and with no deadline** — measured, and the
`>` was wrong too, since `duration_ms=15000` meets the client's 15 s deadline exactly and fails.

`duration_ms` is validated against a named cap and rejected with `400` naming the cap and the value
given. The capture buffer gets a byte cap in the spirit of `EMBARCH_STREAM_MAX_BYTES`. An `Ok(0)`
read no longer spins a blocking-pool thread with no yield. `serial.rs` gets its first tests by
splitting the read loop over a `Read`, so it is exercisable **without opening a port**.

## Why now

`embarch-doc/embarch-core/interfaces.md:21` calls this route "a bounded snapshot, not a stream", and
it is bounded only by a number the caller chooses. And because contention **queues rather than
refusing** (`core/007`, 2026-09-06), one long `duration_ms` stalls every other hardware caller for
its whole span with no message — a self-inflicted outage indistinguishable from Core being hung,
which is the exact failure decision 14's unbuilt `503` was meant to make legible.

## Done when

- [ ] A `duration_ms` over the cap returns `400` naming the cap and the value; at or under it is
      unchanged.
- [ ] The capture is byte-bounded, and hitting that bound is reported rather than silent.
- [ ] `serial.rs` has tests covering the deadline, the byte cap and the `Ok(0)` path, with no port
      opened.
- [ ] The cap appears in `embarch-doc/embarch-core/spec.md` §5's constants table and
      `interfaces.md`'s `/serial-log` row.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
