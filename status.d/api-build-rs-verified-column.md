**Target:** suite/features.md — the `embarch-api` table, `Verified` column on the "Artifact freshness check (mtime before and after)" and "Per-project build concurrency lock" rows
**Was:** both rows read `Verified: unit`
**Now:** artifact freshness is genuinely unit-verified as of 2026-09-03; the concurrency lock still is not — `embarch-api/src/build.rs` had no `#[cfg(test)]` module at all from the initial commit until now, so both rows were claiming a verification that did not exist.

Freshness is covered end-to-end and directly by `embarch-api/tests/build_capture.rs`, along with the two-pipe drain invariant and UTF-8-boundary truncation ([embarch-api decision 46](../embarch-api/decisions/shape.md)). `BuildLocks` is still untested, so its row wants an honest value rather than `unit` — `n/a`, or whatever the supervisor uses for "asserted, not verified".
