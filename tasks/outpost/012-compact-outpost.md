# 012 — `embarch-outpost/open.md` and `decisions/module.md` are in reserve

**State:** open
**Source:** `scripts/check-doc-size.py`, spent by `tasks/outpost/011`'s commit adding the "no CI"
note to `open.md`'s "Deferred with a named trigger" section — and, in the same unit's landing, by
the supervisor's amendment to `decisions/module.md` decision 22.
**Scope:** outpost
**Hardware:** none
**Owner:** no

## What

**Compacts:** `embarch-outpost/open.md`, `embarch-outpost/decisions/module.md`, embarch-outpost/spec.md, embarch-outpost/decisions/transport.md

`open.md` is 4,891 / 5,120 B, 229 B left (95.5%); `decisions/module.md` is 7,730 / 8,192 B, 462 B
left (94.4%).

`open.md` is in reserve, per `DOC-COMPACTION.md` §2. It is writable and the gate passes; this task
exists so the next unit to write there does not hit the cap mid-flight with no warning.

**In flux: no.** The edit that spent the reserve (naming the CI gap under "Deferred with a named
trigger") is a one-time addition, not a half-finished thread — nothing about `tasks/outpost/011`
leaves this file expecting a follow-up edit soon. This task is not blocked.

A compaction pass should look at whether any of `open.md`'s five sections holds more than one
mission that could split into its own file (`DOC-COMPACTION.md` §3's per-mission split), or whether
any entry states more than a reader needs — the file's own entries are dense and each already earns
its length, so this may turn out to be a case for splitting rather than cutting prose.

## Why now

`DOC-COMPACTION.md` §2: a file in reserve must be named on a `Compacts:` line in an open task in
the scope directory of the doc being compacted, filed by whoever spends it, in the same commit.

## Done when

- [ ] `open.md` is back under `check-doc-size.py`'s reserve threshold (below 90% of its cap), by
      either compacting an existing section or splitting by mission.
- [ ] `decisions/module.md` likewise back under 90%. **`In flux: no` for it too**, with one
      exception a compactor must respect: decision 22's third paragraph now carries the two
      verification runs taken on 2026-09-07 (cross-decoder `PASS` on 831 rows of 41 frames with the
      siblings present; `SKIP:` plus the trap's note with them absent). Those are the only written
      evidence that the reordering and the trap actually work, and the file is the only place they
      exist.
- [ ] **Must not delete:** in `decisions/module.md`, decision 22's *"Rejected: fail the leg when the
      fixtures are missing"* paragraph and the reason — a repo cannot assert its own tests red over
      a fact only a sibling checkout controls — because a later reader meeting a silent skip will
      propose exactly that, and the two verification runs named above. In `open.md`: the "one
      binding number" entry (the 40 KB ring ceiling and the
      19.7%/36% burst-loss figures), the two clock-backwards facts under "Structural, and priced",
      and the CI gap just added under "Deferred with a named trigger" — all load-bearing, measured
      facts with no other home.
- [ ] Gate green.

**Widened 2026-09-07 by the reserve floor.** `check-doc-size.py`'s reserve was 90% of a limit; a percentage of a small cap is not runway, and the corpus reached `suite/features.md` with 36 bytes left and `embarch-api/decisions/core-link.md` with 22. Reserve is now `max(1200 B, 10%)` from the top, so the paths added to the `**Compacts:**` line above crossed on the rule change, not on an edit. **Prefer a SPLIT** — [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split restates nothing, so it costs no argument, and a file warned 1.2 KB out still has a seam to cut. Squeeze only where there is none.
