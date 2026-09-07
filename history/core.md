# core: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- `GET /status` now serves `core_version`, compiled in from `CARGO_PKG_VERSION`; no `contract_version` beside it (decision 13).

### Changed
- Core's study decisions split by mission: the version gate and handshake identity (31, 35) move verbatim to [decisions/handshake.md](../embarch-core/decisions/handshake.md).
- `embarch-core/open.md` is out of reserve: two bullets restating spec.md and decision 31 are gone, two shortened.
- The bearer-token test sweep now derives its route list from `build_router`'s own source: all 26 routes, not 12 ([decision 42](../embarch-core/decisions/platform.md)).
- Core's spec.md and open.md compacted out of reserve (DOC-COMPACTION §9); no open question dropped.
- embarch-core/open.md compacted off its cap; all 26 questions kept, none answered by the pass.
- `embarch-core`'s 233 KB `design.md` became spec.md (9K), decisions.md (30K), interfaces.md (9K) and open.md (5K) — 53 KB, all 40 decision numbers intact.
- `embarch-core`'s decisions split by mission into seven `decisions/<topic>.md` files (largest 7.7 KB) with `decisions.md` as a 1.6 KB index; all 40 numbers still resolve.

### Fixed
- A study stopped by a timed-out step now names that step; "did not arrive" means no step outcome was recorded at all ([decision 45](../embarch-core/decisions/studies.md)).
- `/logs/stream` no longer splits a log line across two SSE frames; its offset advances past a `\n` or not at all (embarch-core decision 44).
- `hw_lock` contention queues silently — decision 14's `503` naming the holder was never built; three docs said it was. See [decisions/platform.md](../embarch-core/decisions/platform.md).
- `chip-list --help` and the `/resolve-chip` 404 now say to edit Core's compiled-in `SOC_TO_CHIP`, not a retired `embarch-api` config key.
- `/study/{id}/events` docs now list `GattTranscript` and note it has no `Last-Event-ID`/replay.

### Decided
- A study's public `current_step` is the index of the last step that *finished* — stated in [interfaces.md](../embarch-core/interfaces.md), decision 43.
- The `{code, message, cause}` error body is deferred as cross-repo work with a named trigger, not left as pending (decision 12).
