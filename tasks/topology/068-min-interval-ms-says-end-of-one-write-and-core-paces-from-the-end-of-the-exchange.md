# 068 — `min_interval_ms` says "end of one write"; Core paces from the end of the whole exchange

**State:** claimed by agent/topology/068-min-interval-measurement-point, 2026-10-28 17:25
**Reserve at dispatch (2026-10-28):** nothing in `embarch-topology` is in reserve.
**Source:** `suite/049`'s fold (supervisor log, 2026-10-28 16:27, "Least sure about"), the reviewer's note: "pacing is measured from the end of a command's read, so it never undershoots, but topology's `min_interval_ms` doc comment says 'end of one write' (a one-line comment fix nobody has filed)".
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`Instrument::min_interval_ms` (`src/hardware/instrument.rs`, decision 49) documents the interval as running "from the end of one write to the start of the next". `embarch-core`'s `instrument::talk` calls `mark_sent` *after* `exchange_with` returns, so for a query or an acknowledging set the clock starts when the reply has been read, and for an unacknowledged set when the write was flushed. The interval Core enforces is therefore never shorter than the documented one, and usually longer by the instrument's reply time.

When this is done, the field's doc comment (and decision 49's text, if it states the measurement point) says what Core does: from the end of the previous exchange with that instrument (its reply read, or its write when nothing is read) to the start of the next write, process-wide. The contract lives here because every caller reads it here; Core's own `pace_left` comment ("since the last write") is Core's and is not this task's to change — name it in the changelog fragment so the next `core` unit can align it.

## Why now

A field whose doc misstates its measurement point is how a caller tunes `min_interval_ms` down to a value it believes is safe. The first instrument (an ET5410A+) wants 200 ms between commands and poisons its parser on a violation (decision 49).

## Done when

- [ ] `min_interval_ms`'s doc comment states the measurement point Core uses.
- [ ] Decision 49 corrected in place if it states the old point.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), every CI cell (default, hardware, bin, software+wire).
- [ ] `changelog.d/` fragment dropped, naming Core's comment as the remaining mismatch.
