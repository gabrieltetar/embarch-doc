# 012 — `embarch-outpost/open.md` is in reserve

**State:** open
**Source:** `scripts/check-doc-size.py`, spent by `tasks/outpost/011`'s commit adding the "no CI"
note to `open.md`'s "Deferred with a named trigger" section.
**Scope:** outpost
**Hardware:** none
**Owner:** no

## What

**Compacts:** `embarch-outpost/open.md`, 4,891 / 5,120 B, 229 B left (95.5%).

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
- [ ] **Must not delete:** the "one binding number" entry (the 40 KB ring ceiling and the
      19.7%/36% burst-loss figures), the two clock-backwards facts under "Structural, and priced",
      and the CI gap just added under "Deferred with a named trigger" — all load-bearing, measured
      facts with no other home.
- [ ] Gate green.
