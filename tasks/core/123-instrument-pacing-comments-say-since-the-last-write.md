# 123 — Core's instrument pacing comments say "since the last write"; pacing runs from the end of the exchange

**State:** claimed by agent/core/123-pacing-comments-end-of-exchange, 2026-10-28 22:17
**Reserve (dispatch note, 2026-10-28):** `embarch-core/open.md` (316 B left), `spec.md` (462 B) and `decisions/probes.md` (1,025 B) are in reserve, parked under `tasks/core/112` (blocked, in flux). This task should need none of them; if it must touch one, it spends no bytes there (a net-zero or shrinking edit), and it never compacts what `core/112`'s `Must not delete:` names.
**Source:** `tasks/topology/068` (landed 2026-10-28): its changelog fragment names Core's `pace_left` comment as the remaining mismatch with `Instrument::min_interval_ms`'s now-corrected doc comment (`embarch-topology` decision 49).
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`src/instrument.rs` documents `last_sent` as "when each instrument was last written" and `pace_left` as "since the last write to `name`", and the function that stamps it is `mark_sent`. `talk` calls `mark_sent` after `exchange_with` returns, so the stamp is the end of the whole exchange (the reply read for a query or an acknowledging set, the write flushed when nothing is read), which is what topology's field doc now says. When this is done, those comments say the same thing as `min_interval_ms`'s doc, and `mark_sent`'s name either matches (for example `mark_exchanged`) or carries a one-line comment saying what instant it records. If decision 104 states the measurement point as "the last write", correct it in place.

## Why now

Two descriptions of one interval, in the two crates a reader checks, disagree; the next person tuning the ET5410A+'s 200 ms reads whichever they open first.

## Done when

- [ ] `last_sent`, `pace_left` (and `mark_sent`) describe the end of the previous exchange, matching topology's field doc.
- [ ] Decision 104 corrected in place if it states the old point; no behaviour change.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.
