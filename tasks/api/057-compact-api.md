# 057 — `embarch-api/decisions/zephyr.md` is in reserve after decision 63

**State:** blocked
**Source:** `api/056`'s fix (decision 63, the `app/`/`apps/` scan) landed the
same commit that had already put this file 1,232 B into its reserve band;
`DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/zephyr.md
**Size debt due:** 2026-10-09
**In flux:** yes — this is the file every Zephyr-discovery-shaped change lands
a decision in (decisions 12, 13, 20, 21, 22, 51, and now 63, all here), and
`api/056`'s dispatch notes independently flagged it as "just outside the 10%
reserve band" before this unit even landed. A shortening pass now risks
compacting prose a near-term Zephyr-discovery unit will need to revise or add
to again. Unparked once a unit lands here without adding a new decision or
materially editing an existing one, or once a mission split is judged safe to
do verbatim — the file's own natural seam is "what a call may name and how it
resolves" (12, 20, 21, 51) vs "what board.yml/app scanning trusts and how it's
kept honest" (13, 22, 63).
**Must not delete:** decision 12's "never cached" framing and its scoped
exception to decision 5's "no toolchain-specific logic" — every later entry in
this file leans on both. Decision 51's "reject, not splice" distinction for a
`static` project. Decision 63's three concrete outcomes: both `app/` and
`apps/` are scanned unconditionally and merged (not a config field, not
first-hit-wins), a same-name collision resolves to `apps/` deterministically,
and neither directory present is `ScanError::NoAppDir`, distinct from one
directory present but empty (`Ok(vec![])`) — reverting any of the three
reintroduces `api/056`'s source defect (`chargerito-fw`'s `apps/` repo
scanning to zero targets with nothing saying why).

## What

`decisions/zephyr.md` is now **14,238 B against its 12,288 B cap** — 1,950 B
past the cap itself, well into the reserve band `DOC-COMPACTION.md` §2 defines
at 11,059 B (90% of cap).

## Why now

`check-doc-size.py --pressure` fails on a file in reserve with no task naming
it, and the commit that spends the reserve is the one that files it
(`DOC-COMPACTION.md` §2). This task is that filing.

## Done when

- [ ] `decisions/zephyr.md` is clear of the 11,059 B reserve line, or a
      successor confirms `In flux: no` and re-blocks/re-files with a concrete
      compaction plan — most likely the two-seam split named above.
- [ ] Every `Must not delete:` item above is still readable, wherever it ends up.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
