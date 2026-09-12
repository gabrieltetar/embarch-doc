# 073 — Compact `embarch-api/decisions/client-crate.md` out of size reserve

**State:** blocked
**Source:** `check-doc-size.py`, raised by task `api/072`'s decision-58 correction
(11639/12288 B, 94.7%, 649 B left).
**Scope:** api
**Hardware:** none
**Owner:** no
**Size debt due:** 2026-09-25

## What

`embarch-api/decisions/client-crate.md` is in the last 10% of its size cap (reserve floor
11,059 B). `api/072` added a correction paragraph to decision 58 (the stale `serde(default)`
grep count) and could not avoid crossing the floor without cutting into decision content the
task's own `Must not delete:` forbade touching. Compact it per `DOC-COMPACTION-PASS.md`.

**In flux:** yes — decision 58's check was just re-derived (`api/072`, 2026-09-11) from a stale
13/14 count to an attribute-anchored grep; a compaction pass should re-verify the count against
`crates/embarch-core-client/src/client.rs` rather than assume either number is still current.

**Must not delete:**
- Every decision's number and core claim: 36 (512 MiB thread-stack fix, rejected
  `Builder::thread_stack_size`), 37/38 (crate extraction, two wrappers), 55 (one bearer-token
  funnel, rejected `default_headers`), 58 (per-field `#[serde(default)]` rule and its check), 62
  (WSL2 predicate delegation), 66 (crate stays in this repo, not a tenth repo, plus its stated
  reversal condition).
- Decision 58's corrected check line: `grep -c '^\s*#\[serde(default)\]'
  crates/embarch-core-client/src/client.rs` — the attribute-anchored form, not the old bare
  `grep -c 'serde(default)'`.
- Decision 66's reversal condition (a fourth Cargo consumer with independent release cadence, or
  an `api`-only change here silently breaking `embarch-ui`/`embarch-umbrella`) and its
  "**Corrected at its own fold**" note about the consumer count (three: `embarch-api`,
  `embarch-ui`, `embarch-umbrella`).

**Compacts:** `embarch-api/decisions/client-crate.md`

## Why now

`check-doc-size.py` requires a filed debt for any file in its last 10% of cap; this file crossed
that line under `api/072`'s edit and the gate fails without a task recording it.

## Done when

- [ ] `embarch-api/decisions/client-crate.md` compacted, back under its size reserve threshold.
- [ ] `Must not delete:` list above still present and accurate after the pass.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
