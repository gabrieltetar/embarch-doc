# 009 — `embarch-ui/decisions/trace-view.md` crossed into reserve

**State:** done, closed as a ride-along by `ui/003` (`DOC-COMPACTION.md` §2), 2026-09-07
**Source:** `ui/008` spent 461 B of this file's headroom recording that the decoder now counts the rows it refuses; `DOC-COMPACTION.md` §2
**Scope:** ui
**Hardware:** none
**Owner:** no

**Compacts:** embarch-ui/decisions/trace-view.md
**In flux:** **yes, in two named places, and that is why this is blocked.**
Decision 19's closing sentence — "Unverified against the real 18-record prefix"
— is what `ui/007` exists to make false, and it rewrites the paragraph above it
as well as itself. Decision 10's paragraph on the load repartition is settled;
so are its axis tiers, its five rules and the gap-band material, none of which
any open `ui` task touches.
**No for the rest of the file.** The three-tier axis table and the 46× error it
records are the most-cited content here and are finished.
**Must not delete:** the 46× figure and the two numbers behind it — 78% of
measured extent against the DUT clock's 1.6%, and 4286-of-4955 spans read as
below-resolution — because they are the only written evidence that reading the
coarser of two clocks is a silent error rather than a rounding one. Decision
19's four conditions, each named as "a way this would otherwise eat real data",
and specifically **"Sign is not the signal"** with its 38-second-read-as-563
consequence: a backwards-only check is the obvious implementation and this is
the only note saying why it is wrong. The statement that the shares deliberately
do not total 100%, and why (idle counted twice by construction, ISR time running
inside what it interrupted) — it was found by building it and is claimed by no
other doc.

## What

`decisions/trace-view.md` is **11,080 B against a 12,288 B cap**; the reserve
line is 11,059. It is 21 bytes over, with 1,208 B still free, so this is a
runway note rather than a wall: nothing is blocked on it today, and the next two
edits to this file are.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it, and the
commit that spends the reserve is the one that files it (`DOC-COMPACTION.md`
§2). This task is that filing. It is filed by the worker that spent the bytes,
while it still knows which paragraphs are about to be rewritten — which is the
question a later compactor cannot answer.

## Blocked

Was blocked on **`ui/007`** (the stale-prefix drop has never met a real stale
prefix), because rewriting decision 19's last two sentences and compacting them
first would have been work done twice. **That risk did not apply to `ui/003`'s
pass**: it added its own decision 21 and compacted only the settled repartition
and three-tier-axis material this task already named as fair game — decision
19 was not read for meaning, not trimmed, and not touched at all, so `ui/007`
still has exactly the same two sentences to rewrite whenever it lands. Filing
this done does not stand in for `ui/007`; that task is unaffected and still
open.

## Done when

- [x] `decisions/trace-view.md` is clear of its 11,059 B reserve line. 10,989 B
      after `ui/003`'s pass (was 11,080; adding decision 21 and compacting the
      repartition/three-tier-axis material netted -91 B).
- [x] Every `Must not delete:` item above is still readable. Verified by grep
      against the post-compaction file: the 46× figure, 78%/1.6%/4286-of-4955,
      "Sign is not the signal" and its 38-second-read-as-563 consequence, and
      the shares-do-not-total-100% statement with its idle/ISR reasoning are
      all present, worded slightly tighter but unchanged in claim.
- [x] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words: *what does someone starting on `embarch-ui`
      tomorrow lose if this paragraph is gone?* — nothing: the repartition and
      axis paragraphs lost scene-setting and repeated phrasing, not a claim,
      a number, or a caveat; every fact this task's `Must not delete:` list
      names is still stated, just not stated twice.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — verified by `ui/003`.
