# 047 — `embarch-api/decisions/tool-wrapping.md` is in reserve after decision 60

**State:** blocked
**Source:** `api/036`'s rework added decision 60 (the settled `dev_bench_hello`
rendering call) to the file `api/036` itself created by splitting
`decisions/surface.md`, and crossed the 11,059 B reserve line the same commit;
`DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/tool-wrapping.md
**Size debt due:** 2026-10-05
**In flux:** yes — this is the file every per-tool wrapping decision now lands
in (`api/036`'s split moved 23, 29, 34, 35, 41, 47, 52 here verbatim and added
59 and 60), which is to say it is the tool surface's own growth point: the next
tool this crate wraps, or the next design correction to one already wrapped,
writes here. A shortening pass now would be compacting a file mid-motion,
exactly `DOC-COMPACTION.md` §2's own reason to prefer letting it settle first.
**Must not delete:** decision 41's distinction between a routine knob and
`erase` being the one tool argument that can leave a board unrecoverable — the
whole reason its description is worded the way it is. Decision 52's three
rejected alternatives and the `host_type_schema_version` vs `schema_version`
name-collision they're rejected to avoid. Decision 59/60's full reasoning for
`dev_bench_hello` — in particular the `None`-is-not-`"not-reported"` contract
and the two-rendering-states rule — since that is the exact judgement this
whole unit was refused once for losing.

## What

`decisions/tool-wrapping.md` is now **12,222 B against its 12,288 B cap** — 66 B
of headroom left, inside the 11,059 B reserve line. The next `api` unit that
adds or changes a per-tool wrapping decision may find none.

## Why now

`check-doc-size.py --pressure` fails on a file in reserve with no task naming
it, and the commit that spends the reserve is the one that files it
(`DOC-COMPACTION.md` §2). This task is that filing.

## Done when

- [ ] `decisions/tool-wrapping.md` is clear of the 11,059 B reserve line, or a
      successor confirms `In flux: no` and re-blocks/re-files with a concrete
      compaction plan (a further mission split, most likely, since this file
      already holds every per-tool decision as one mission).
- [ ] Every `Must not delete:` item above is still readable, wherever it ends up.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
