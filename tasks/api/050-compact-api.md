# 050 — `embarch-api/decisions/build.md` is in reserve after amending decision 18

**State:** done
**Source:** `api/030`'s fix (the drain treating a UTF-8 decode error as EOF)
amended decision 18 and crossed the 11,059 B reserve line the same commit;
`DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:**
**Size debt due:** 2026-09-22
**Must not delete:** decision 18's provenance note that the 1:3 head/tail split
is `[assumed]` and the exact condition that would move it (a real over-cap
Zephyr failure showing its first error past 16 KB) — that sentence is the only
thing standing between "reasoned" and "measured". The amendment's own point,
that a drain reading a decode error as EOF is the defect this closes, not a
polish. Decision 19's full three-call reasoning for `target.json` (why it's
written after the build, why absence means "unattributable" not "orphaned",
and the FNV-1a-not-`DefaultHasher` migration story) — it is the entry a reader
most needs explained per its own text. Decision 42's rejected per-call
`base_address` override and why it differs from `--firmware-path`.

## What

`decisions/build.md` is now **11,134 B against its 12,288 B cap** — 1,154 B of
headroom, inside the 11,059 B reserve line. The next `api` unit that adds to
this file may find little room, and per `DOC-COMPACTION.md` §2 a split is the
default remedy: this file already carries four distinct missions (decision 5's
generic-command call, decision 18's log capture/truncation/drain, decision 19's
`target.json` provenance, decision 42's `base_address`) that a verbatim split
by mission could separate without shortening any of them.

## Why now

`check-doc-size.py --pressure` fails on a file in reserve with no task naming
it, and the commit that spends the reserve is the one that files it
(`DOC-COMPACTION.md` §2). This task is that filing.

**Paid by `api/051`:** `decisions/build.md`'s four missions (decision 5's
generic-command call, decision 18's log capture/truncation/drain, decision 19's
`target.json` provenance, decision 42's `base_address`) were split verbatim
into `decisions/build.md` (5), `decisions/log-capture.md` (18, plus the new
decision 65 for the drain-decoding policy the amendment left unnumbered),
`decisions/target-json.md` (19) and `decisions/flash-address.md` (42). Every
`Must not delete:` item above is carried through intact into whichever file it
now lives in. `decisions/build.md` is struck off `Compacts:` above because the
split cleared its reserve; nothing else in this task is unblocked by it.

## Done when

- [x] `decisions/build.md` is clear of the 11,059 B reserve line, or a
      successor confirms `In flux: no` and re-blocks/re-files with a concrete
      compaction plan — most likely the four-way mission split named above.
- [x] Every `Must not delete:` item above is still readable, wherever it ends up.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
