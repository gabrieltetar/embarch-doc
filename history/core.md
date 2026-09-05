# core: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Changed
- embarch-core/open.md compacted off its cap; all 26 questions kept, none answered by the pass.
## 2026-09

### Added
- `GET /status` now serves `core_version`, compiled in from `CARGO_PKG_VERSION`; no `contract_version` beside it (decision 13).

### Decided
- The `{code, message, cause}` error body is deferred as cross-repo work with a named trigger, not left as pending (decision 12).
## 2026-09

### Fixed
- `/study/{id}/events` docs now list `GattTranscript` and note it has no `Last-Event-ID`/replay.
## 2026-09

### Changed
- `embarch-core`'s 233 KB `design.md` became spec.md (9K), decisions.md (30K), interfaces.md (9K) and open.md (5K) — 53 KB, all 40 decision numbers intact.
- `embarch-core`'s decisions split by mission into seven `decisions/<topic>.md` files (largest 7.7 KB) with `decisions.md` as a 1.6 KB index; all 40 numbers still resolve.
