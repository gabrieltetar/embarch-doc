# 140 — Compact api's decisions/client-crate.md

**State:** open
**Source:** tasks/api/139 added the "Applied `api/139`" paragraph to decision 58, which pushed the file to 11581/12288 B (94.2%), inside `check-doc-size.py`'s reserve.
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/client-crate.md

## What

`embarch-api/decisions/client-crate.md` is in the size reserve (707 B left). Run a compaction pass per `DOC-COMPACTION-PASS.md`, quoting every hunk in the commit message per its quoting rule.

## In flux

No. The crate's response-field rule (decision 58) is settled and `api/139` closed the last known violations; the file only grows when a decision is added.

## Must not delete

- Decision 58's rule sentence ("every response field ... is `Option<T>` with `#[serde(default)]`"), its attribute-anchored check, and the `api/139` paragraph's `erased` ruling.
- Decision 66's stated cost and its reversal condition.

## Done when

- [ ] `embarch-api/decisions/client-crate.md` back under the reserve threshold in `scripts/check-doc-size.py`.
- [ ] Every hunk quoted in the commit message per `DOC-COMPACTION-PASS.md`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
