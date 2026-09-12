# 071 — Compact `embarch-api/interfaces/config.md` out of size reserve

**State:** blocked
**Source:** `check-doc-size.py`, raised by task `api/070` spending the file's last bytes
(11193/12288 B, 91.1%, 1095 B left) fixing the `[dev_bench]` `env` row.
**Scope:** api
**Hardware:** none.
**Owner:** no
**Size debt due:** 2026-09-25

## What

`embarch-api/interfaces/config.md` is in the last 10% of its size cap. Compact it per
`DOC-COMPACTION-PASS.md`, honouring the **Must not delete:** list below.

**In flux:** yes — this file describes `[dev_bench]`/`[[projects]]` config, and task
`api/070` just touched two of its rows (the `env` semantics and the `:81` tool count) in this
same window; a compaction pass should re-check for drift against `src/config.rs`,
`src/tools.rs` and `src/dev_bench.rs` rather than assume the prose is settled.

**Must not delete:**
- Every field's Type/Req/Default/Notes row for `[core]`, `[[projects]]`, and `[dev_bench]` —
  the schema reference is this file's whole purpose.
- The `env` additive-semantics note on both the `[[projects]]` and `[dev_bench]` rows
  (just corrected by `api/070` — do not let a compaction pass silently re-diverge them).
- Every numbered `../decisions/*.md` citation.
- The retirement notices for `soc_chip_overrides` and `[[projects.targets]]` (both
  config-load-time failures a reader needs to recognize).

**Compacts:** `embarch-api/interfaces/config.md`

## Why now

`check-doc-size.py` requires a filed debt for any file in its last 10% of cap; this file
crossed that line under `api/070`'s edit and the gate fails without a task recording it.

## Done when

- [ ] `embarch-api/interfaces/config.md` compacted, back under its size reserve threshold.
- [ ] `Must not delete:` list above still present and accurate after the pass.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
