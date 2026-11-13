# 150 — Split api's open.md by mission

**State:** done
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

- [x] `embarch-api/open.md` out of the reserve in `scripts/check-doc-size.py`, by a split.
- [x] `collect-open-questions.py` still prints every bullet.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment dropped.

## Result

Split by mission: seven verification-debt bullets (bootload, bench_exchange, study_watch, ledger, lease, build verdict, `build --each`) moved verbatim to `embarch-api/open/bench-verification.md`, with a pointer bullet left in `open.md` (4,502 to ~3,100 B). `stack` and `patches` stay in `open.md`: they are real-repo debts, not bench or toolchain-build ones, and the Settled-deferred reasons are untouched.

**DOC-COMPACTION-PASS human question:** can `spec.md` alone answer what someone needs to work on this component today? Mostly yes for what the surface is and what it guarantees; what it cannot answer is what has never met real hardware, which is exactly what `open.md` and `open/bench-verification.md` carry, so a worker about to touch bootload, bench_exchange, ledger or lease must read the split file too. The pointer in `open.md` keeps that route visible.
