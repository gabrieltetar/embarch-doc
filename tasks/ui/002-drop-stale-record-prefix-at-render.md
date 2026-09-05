# 002 — A capture still opens with stale records; drop the discontinuous prefix at render time

**State:** claimed by agent/ui/002-drop-stale-record-prefix-at-render, 2026-09-05 00:32

**Doc-size reserve at dispatch (supervisor, leg 009):** **no `embarch-ui` file is in
reserve** — the five files in reserve suite-wide are all `api` and `umbrella`, and all
filed. Normal headroom. If any `embarch-ui` file enters reserve on your commit, file a
compaction task in the same commit; note that `tasks/README.md` says
`tasks/doc/<NNN>-compact-ui.md` but `check-ownership.py --scope ui` **refuses
`tasks/doc/**`** — that contradiction is `tasks/doc/004`, and the precedent set by
`api/009` is to file at `tasks/ui/<NNN>-compact-ui.md` instead, which
`check-doc-size.py` still finds because it matches the `**Compacts:**` field.

**Two gate quirks already known, so you do not rediscover them:**
1. If you add or edit a `features.d/` row, `build_features.py --check` goes red and
   `check-ownership.py` refuses `suite/features.md`. **Do not commit that file** —
   leave it stale, say so in your report, the supervisor assembles it in the fold
   (`tasks/doc/002`).
2. `check-ownership.py --scope ui` run bare against `origin/main...HEAD` may name paths
   from this leg's other units that are in your base. Check your own diff instead:
   `git diff --name-only <your branch point>...HEAD | scripts/check-ownership.py --scope ui --stdin`.

**Context from `ui/001`, which landed an hour ago and touched the same view:** the Trace
view no longer serializes `Lane.spans` at all — it fetches windowed, server-binned runs
from `GET /api/trace/{study}/{tap}/bins?from&to&width`, and one decoded capture is
cached server-side in `AppState.trace_cache`. **The prefix drop almost certainly belongs
at decode time, before the cache and before binning**, not in `app.js`. Read
`embarch-ui/decisions/trace-transfer.md` (decision 18) before you design it.
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
