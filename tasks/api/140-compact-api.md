# 140 — Compact api's decisions/client-crate.md

**State:** claimed by agent/api/140-compact-api-client-crate, 2026-10-28 14:58
**Reserve (supervisor, 2026-10-28):** `embarch-api/decisions/client-crate.md` 707 B left (this task's file); `embarch-api/open.md` 446 B left, filed under `api/144` (open, not yours). The supervisor is running `suite/046` in parallel and will add api decisions for it; it will not edit `client-crate.md`, so take what room you need there.
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
