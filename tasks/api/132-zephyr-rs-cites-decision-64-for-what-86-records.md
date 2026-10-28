# 132 — `zephyr.rs` cites a retired-config decision for the single-SoC rules decision 86 records

**State:** done — landed 2026-10-28 (embarch-api `744b94b`, embarch-doc `25f394d4`); the worker left the claim line, set at the fold
**Dispatch note (2026-10-28 13:47 leg):** api reserve — `decisions/client-crate.md` 11,581/12,288 (707 B left, filed `api/140`), `open.md` 4,494/5,120 (626 B, filed `api/144`). Neither should need a write here; if one does and it crosses its line, file per `tasks/README.md`. `suite/047` runs after you in `embarch-api` (`--version`, `versions --json`, MCP `status`) — stay out of those.
**Source:** `api/122`'s reviewer, 2026-10-25 (below its bar, filed by the supervisor so it is not lost when the log folds).
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`api/122` (embarch-api `2f3749b`) wrote decision **86** in `embarch-api/decisions/zephyr-scan.md`,
but ten doc comments and test docs it added to `crates/embarch-firmware-build/src/zephyr.rs` cite
**decision 64** for those rules (lines 252, 340, 432, 464, 562 and 1309–1364 at `2f3749b`). Decision
64 exists, and is about something else: it lives in `decisions/config-retirement.md` (retired
config keys and target selection). So every one of those citations sends a reader to a real,
unrelated decision with nothing failing. When done, each cites 86, and no other comment in the
crate cites 64 for a scan rule.

## Why now

A wrong citation to an existing decision is the worst kind: `check-decision-refs.py` resolves it
and passes. It is a comment-only change in one file.

## Done when

- [x] Every `decision 64` in `zephyr.rs` that means the single-SoC rules reads `decision 86`.
- [x] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green (comments only, but run them).
- [x] Gate green (`../../../embarch-fleet/gate.md`). No changelog fragment: nothing reader-facing changes.
