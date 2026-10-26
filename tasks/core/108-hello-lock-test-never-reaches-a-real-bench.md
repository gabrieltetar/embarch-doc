# 108 — `core/104`'s hello lock test never reaches a real bench

**State:** claimed by agent/core/108-hello-lock-test-no-bench, 2026-10-26 01:45
**Source:** the `core/104` reviewer's below-bar notes, 2026-10-26 (code `8e29f06`), filed by the supervisor because the first one is a host test that can touch hardware.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`hello_is_refused_409_while_the_link_is_held_and_releases_its_own_hold` (`embarch-core/src/study.rs`, tests module) ends by calling `hello_handler` with a free link and ignoring the result, on the reasoning that it "fails later (no bench here)". On a machine with a dev-bench plugged in, that call runs `resolve_dev_bench_port` against the real USB enumeration, then `enforce_dev_bench_gate`, which attaches the real probe through `validate_role`, and, if that passes, `open_and_handshake` opens the real port and sends `Hello`. A `cargo test` on a bench machine (the owner's Windows checkout is one) would therefore drive hardware from a unit test, which nothing in the suite allows a host test to do.

When this is done the test proves the same property — hello's `study_lock` hold is released on every return path — without any path that can reach a port or a probe: an injected failure, a seam that stops before port resolution, or a test-only resolver that returns "no dev-bench". Also fix the `AppState` doc comment in `src/api.rs` (around lines 22-26), which still says `study_lock` is "explicitly separate from `hw_lock`"; since `core/104` the two are taken in a fixed order (`study_lock`, then `hw_lock`), as `decisions/platform.md` now says.

## Why now

The test landed an hour ago and runs in every `cargo test`; it is harmless only on machines with no bench attached, which is exactly the condition nobody checks before running tests.

## Done when

- [ ] No test in `embarch-core` calls `hello_handler` (or anything that resolves the dev-bench port or attaches a probe) on a path that can reach real hardware; the release-on-return property is still tested.
- [ ] The `AppState` comment states the lock order.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped only if reader-facing.
