# Measure the 250,000-row view cap at the next number up, so raising it stops being an extrapolation

**State:** open
**Source:** `embarch-ui/open.md` — "it should be made against a measurement at the new number rather than by extrapolating this one"
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`embarch-ui/open.md` says the 250,000-row cap "is now the only term left, and the reason it was set
is gone". The cap is `src/trace.rs:120`. The instrument already exists at `src/trace.rs:3748`
(`summarise_a_capture_from_disk`, `EMBARCH_VIEW_CSV`) but needs a real file on disk.

Add a synthesiser plus an `#[ignore]`d measurement test that builds captures of the committed
fixture's shape at 250k / 500k / 1M rows and prints decode time, resident view size and `/bins`
payload size at a reference grid width. Put the numbers in `open.md` (or a decision), then either
raise the cap with the measurement beside it or leave it where it is **with the measurement as the
reason**. Both outcomes close this; an unstated one does not.

## Why now

`open.md` states the decision is blocked only on a measurement at the new number, and
`decisions/trace-transfer.md` 18 already removed the transfer half of the original justification.
Nothing else about it is open.

## Done when

- [ ] A synthesiser and an `#[ignore]`d measurement test exist and run from a documented one-line
      invocation, needing no file on disk.
- [ ] Decode time and both payload sizes are recorded at three row counts, marked
      `[measured <date>, <build>]` per `../../DOC-CONVENTIONS.md`.
- [ ] The cap is either changed or explicitly kept, with the number cited.
- [ ] `open.md`'s bullet is rewritten to what is now unknown.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
