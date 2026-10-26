# 144 — Compact api's open.md

**State:** open
**Source:** tasks/api/131 added the `bench_exchange` item to `embarch-api/open.md`, which took it to 4034/5120 B, inside `check-doc-size.py`'s reserve.
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/open.md

## What

`embarch-api/open.md` is in the size reserve (1,086 B left). Run a compaction pass per `DOC-COMPACTION-PASS.md`, quoting every hunk in the commit message per its quoting rule.

## In flux

No. The file is a list of known-wrong, structural and settled-deferred items; an item changes only when the work it names lands, and none is being reworked now.

## Must not delete

- Every hardware-verification debt item (`bootload`, `study_watch`, `bench_exchange`) with its decision pointer and the task it came from.
- The "Settled-deferred" reasons (a reason is the point of an item there).

## Done when

- [ ] `embarch-api/open.md` back under the reserve threshold in `scripts/check-doc-size.py`.
- [ ] Every hunk quoted in the commit message per `DOC-COMPACTION-PASS.md`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
