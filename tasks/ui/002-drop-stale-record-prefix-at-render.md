# 002 — A capture still opens with stale records; drop the discontinuous prefix at render time

**State:** open
**Source:** [embarch-core/open.md](../../embarch-core/open.md) — "Discarding a signal port's buffered input on open is not sufficient (decision 30) … **Candidate fix:** drop a leading run of records whose cycles are discontinuous with the bulk, at render time, where the whole file is in hand."
**Scope:** ui
**Hardware:** verify-only

## What

With Core's open-time purge in place, a real capture **still began with 18 stale
records** carrying a cycle count seconds away from the rest, and the purge reported
no error — the bytes are presumably inside the USB-UART bridge or in flight, beyond
an OS-level purge. The clear stays (it is correct and free). The current defence is
`embarch-ui` refusing the DUT clock whenever a capture's two clocks contradict,
**which costs the microsecond axis for the whole capture** over a handful of leading
records.

Build the candidate fix `embarch-core/open.md` names, on the side that can do it:
at render time the whole file is in hand, so a **leading run** of records whose
cycle counts are discontinuous with the bulk can be identified and dropped, and the
DUT clock kept for everything after it.

Two things to get right rather than approximate:

- **A discontinuity inside the bulk is not this.** `embarch-outpost/open.md` records
  that the DUT's clock legitimately goes backwards by small amounts — a real capture
  showed a **13 µs** step from a hook that reads the counter and then reserves its
  ring slot — and "a host must tolerate it, since refusing the clock over it would
  refuse every real capture." Only a *leading* run, and only one discontinuous with
  the bulk, is in scope.
- **Say so in the view.** A reader must be able to tell that N leading records were
  dropped, not silently see a shorter capture — `embarch-outpost/open.md`'s own
  standard for the self-exclusion hole is that a gap is reported rather than hidden.

## Why now

The existing defence throws away the microsecond axis for a whole capture to defend
against a prefix, and the better fix has been written down and unbuilt since. The
logic is testable against a crafted fixture with a synthetic discontinuous prefix;
confirming it fires on a real bridge-buffered capture is the hardware debt.

## Hardware-verification debt

Reproducing the real 18-record prefix needs the bench and a real capture. Ship the
host-side half and **write the debt into this file** for the owner's own session.

## Scope warning

If the leading records are dropped better on Core's side than at render — or if the
renderer cannot see cycle counts without a Core change — **stop and report that
here** rather than reaching into `embarch-core`
(`../../embarch-fleet/protocol.md` §5 rule 2).

## Done when

- [ ] A leading run of cycle-discontinuous records is dropped at render, and the
      DUT clock is kept for the remainder.
- [ ] A small in-bulk backwards step (the 13 µs case) is **not** treated as this and
      is covered by a test.
- [ ] The view states how many leading records were dropped.
- [ ] Hardware-verification debt written into this file.
- [ ] `spec.md`/`decisions.md`/`open.md` updated; `changelog.d/` fragment dropped;
      `status.d/` fragment for anything suite-level made false.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
