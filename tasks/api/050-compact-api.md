# 050 — `embarch-api/decisions/build.md` is in reserve after amending decision 18

**State:** blocked
**Source:** `api/030`'s fix (the drain treating a UTF-8 decode error as EOF)
amended decision 18 and crossed the 11,059 B reserve line the same commit;
`DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/build.md
**Size debt due:** 2026-09-22
**In flux:** yes — this file has taken a live edit in each of the last two
units to touch it (`api/030` just amended decision 18; open.md already flagged
it as a paragraph short of the line before that). Build orchestration is an
active surface — the capture path alone has now been revisited twice for
correctness bugs — so a shortening pass now risks compacting reasoning a third
visit will need verbatim. Unparked once a unit lands here without adding to
decision 18/19/42's argument, or once a mission split (this file already mixes
the generic-command call, log capture/truncation, `target.json` provenance,
and `base_address` — four missions in one file) is judged safe to do verbatim.
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

## Done when

- [ ] `decisions/build.md` is clear of the 11,059 B reserve line, or a
      successor confirms `In flux: no` and re-blocks/re-files with a concrete
      compaction plan — most likely the four-way mission split named above.
- [ ] Every `Must not delete:` item above is still readable, wherever it ends up.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
