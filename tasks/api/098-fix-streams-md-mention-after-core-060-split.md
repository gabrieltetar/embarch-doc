# 098 — Fix `embarch-api/interfaces/studies.md`'s stale `decisions/streams.md` mention after core/060's split

**State:** done — 2026-09-16 — `embarch-api/interfaces/studies.md` line 16 now cites `` (`embarch-core` decision
62; suite decision 4) `` with no file-path mention, per `DOC-CONVENTIONS.md`'s bare-number preference.
Verified no other `decisions/streams.md` mentions in `embarch-api/`. Gate green.
**Source:** `tasks/core/060-compact-core.md` (leg 116, 2026-09-16) — found while compacting
`embarch-core/decisions/streams.md` out of reserve.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-core/decisions/streams.md` was split (`tasks/core/060`): decisions 62 and 63 moved verbatim to
a new file, `embarch-core/decisions/stream-index.md`. `embarch-core/decisions.md`'s index table was
updated in that commit, and the one in-scope stale mention (`embarch-core/interfaces/studies.md`) was
fixed to link the index rather than the topic file.

One mention is out of `core`'s ownership row and could not be touched from that task:
`embarch-api/interfaces/studies.md` line 16 reads `` (`embarch-core` decision 62, `decisions/streams.md`;
suite decision 4) `` — plain inline code, not a markdown link, so `check-decision-refs.py` and
`check-links.py` both pass it either way (neither checks inline-code file mentions), but the filename is
now wrong: decision 62 lives in `decisions/stream-index.md`, not `decisions/streams.md`.

Fix: drop the file-path mention entirely and cite the bare number, per `DOC-CONVENTIONS.md`'s own
preference ("prefer the bare number" over naming a file, since a mission split moves entries between
topic files without renumbering) — e.g. `` (`embarch-core` decision 62; suite decision 4) ``.

## Why now

Not urgent — nothing fails today, since neither gate script checks an inline-code file mention. It is a
correctness debt: a reader following the current text to `embarch-core/decisions/streams.md` for
decision 62 will not find it there.

## Done when

- [x] `embarch-api/interfaces/studies.md` line 16 no longer names `decisions/streams.md`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
