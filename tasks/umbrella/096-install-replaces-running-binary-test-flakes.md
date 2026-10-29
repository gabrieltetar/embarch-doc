# 096 — `install::tests::install_binaries_replaces_a_binary_that_is_running` failed once under a parallel `cargo test`

**State:** claimed by agent/umbrella/096-install-replaces-running-binary-test-flakes, 2026-10-29 15:27
**Source:** `umbrella/095`'s worker, leg started 2026-10-29 15:03 (log entry `2026-10-29 15:13 — umbrella/095`): the test failed once in a parallel `cargo test` run in its worktree, then passed on the next two runs (258/258); the supervisor's own gate run passed. One observation, not a measured rate. Filed from `inbox/umbrella-install-replaces-running-binary-test-flakes.md`.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`embarch-umbrella/src/install.rs:676` `install_binaries_replaces_a_binary_that_is_running` is suspected of being order- or timing-dependent under `cargo test`'s default parallelism. Find out whether it shares state with another test (a fixed temp path, a process it spawns and does not reap, an environment variable) or races the "running binary" it starts, and make it deterministic. If it cannot be made to fail in a loop of parallel runs, record that and close.

## Why now

A flaky test in a gate the fleet re-runs on every umbrella unit will eventually block a correct unit as red, and the protocol reads two identical reds as a systemic fault.

## Done when

- [ ] The test's failure mode is identified and fixed, or a loop of parallel runs (say 50) shows no failure and that is recorded.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment if code changed.
