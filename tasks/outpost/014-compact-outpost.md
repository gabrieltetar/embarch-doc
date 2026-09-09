# 014 — Compact embarch-outpost/spec.md

**State:** open
**Source:** `scripts/check-doc-size.py`, run from `agent/outpost/005-verify-the-arrival-join`
**Scope:** outpost
**Hardware:** none
**Owner:** no
**Compacts:** embarch-outpost/spec.md
**In flux:** no
**Must not delete:** the `--allow-unverified-join` / `--allow-build-id-mismatch`
posture pairing in the invariant-61 paragraph — it is the reader's only pointer
from the invariant to the escape hatch and the decision it mirrors; and the
missing/short `frame_bytes` column's degrade-not-refuse behaviour, which is the
one case a reader could otherwise assume is a third refusal alongside the
manifest and build-ID ones.

## What

`agent/outpost/005-verify-the-arrival-join` implemented `spec.md:61`'s
invariant in the reference decoder and added one paragraph recording it,
which put `embarch-outpost/spec.md` at 9,515/10,240 B — inside the last 10%
of its cap (`RESERVE_PCT`), 725 B left. The file is still writable and the
gate still passes; this task exists only to name the debt per
`DOC-COMPACTION.md` §2, since the commit that spent the reserve owes the task
that files it.

## Why now

`check-doc-size.py` failed the doc gate for `embarch-outpost` with this file
named and no open task covering it (`embarch-outpost/decisions/tracing.md`'s
reserve is already covered by `tasks/outpost/008`, which is a different file).

## Done when

- [ ] `embarch-outpost/spec.md` reduced below its reserve threshold without
      losing any fact the `Must not delete:` list names — a paragraph
      tightened or a repeated fact folded into a cross-reference, not a
      judgement removed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `check-doc-size.py`
      no longer names this file.
- [ ] `changelog.d/` fragment dropped for the compaction itself.
