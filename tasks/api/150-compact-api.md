# 150 — Split api's open.md by mission

**State:** claimed by agent/api/150-compact-api, 2026-11-13 13:47
**Reserve at filing (2026-11-10):** `embarch-api/open.md` 4,227/5,120 B, 893 B left; `api/127` then took it to 4,502 B with the `build --each` bullet. `api/126` spent it first on the build-verdict verification bullet; the file had been 14 B under the reserve line.
**Source:** `tasks/api/126` (build verdict and named variants), per `DOC-BUDGET.md`'s reserve rule: the actor that spends the reserve files the debt.
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/open.md
**Size debt due:** 2026-11-24
**In flux:** no — the split moves bullets verbatim; the build-verdict bullet changes when the field variant pair is replayed (`tasks/api/126`), so move it as written
**Must not delete:** every hardware- or toolchain-verification debt bullet with its decision pointer; the "Settled-deferred" reasons

## What

`embarch-api/open.md` is in the size reserve. Every bullet in it is a live limitation, so the default remedy is a split by mission into `embarch-api/open/<topic>.md`, verbatim, per `DOC-BUDGET.md` and `DOC-COMPACTION-PASS.md`, not a squeeze. One seam to check first: the bench-verification items (bootload, bench_exchange, study_watch, ledger, lease, build verdict) against the rest.

## Done when

- [ ] `embarch-api/open.md` out of the reserve in `scripts/check-doc-size.py`, by a split.
- [ ] `collect-open-questions.py` still prints every bullet.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.
