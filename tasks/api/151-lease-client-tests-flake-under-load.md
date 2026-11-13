# 151 — Two `lease_client` tests fail once under load, then pass

**State:** claimed by agent/api/151-lease-client-tests-flake-under-load, 2026-11-12 19:33
**Source:** EMB-155, filed while landing `api/108` on 2026-11-10: the first gate run on the merge result was red on two tests the change could not reach
**Issue:** EMB-155
**Scope:** api
**Hardware:** none
**Owner:** no

## What

One full `cargo test` in `embarch-api` at `15cef80` failed 2 of 19 tests in
`tests/lease_client.rs`, both on request-count asserts against the mock Core,
and every run after passed:

- `a_second_process_sends_the_token_from_the_environment_with_no_argument`,
  line 151, `assert_eq!(reqs.len(), 2)`: left 3, right 2.
- `a_required_lease_leaves_open_routes_alone_so_a_session_can_take_one`,
  line 341, `assert_eq!(asked(&mock, "/status"), 1)`: left 0, right 1.

The change under test touched only a `#![cfg(windows)]` file, so the cause is
already on `main`. The failing run was a worktree's first build, with other
cargo and doc-gate processes running at once. `cli_in_session()` strips
`EMBARCH_LEASE_TOKEN` and `EMBARCH_REQUIRE_LEASE` from the child, so the
session's own variables are not it.

Two hypotheses:

- **A child from an earlier test outlives it.** A CLI child (the keepalive
  test's, say) still sends requests after its test ends, and they reach a later
  test's mock that took the same ephemeral port: one extra request in the first
  test, a missing `/status` in the second.
- **A request is counted before the mock records it**, under load.

**Next check.** Run `cargo test --test lease_client` repeatedly under CPU load
and log each mock's port and every request it receives, with its test name. An
extra request from an earlier test's port confirms the first hypothesis. Make
the load from your own worktree (for example a `cargo build --release` into a
scratch `--target-dir` beside it), never from another repo. A shell `for` loop
cannot be allowlisted, so write the repeat loop as a Python script with the
Write tool, outside the repo tree (beside your worktree), and run it with
`python3`.

**What you may change.** Only `embarch-api` and `embarch-doc/embarch-api/`.

**Doc reserve.** `embarch-api/open.md` is 4,502 of 5,120 B, in reserve, and
filed as `tasks/api/150-compact-api.md`. Add nothing to it unless a bullet goes
out in the same edit. Decisions near their own limit: `ledger` (98) 15 B,
`bench-exchange` (89) 122 B, `failure-reporting` (67) 192 B. A fix of the test
harness should need no new decision; if the lease client itself changes,
decision 101 is in `decisions/lease.md`.

## Why now

A gate test that fails one run in some is a red every lander has to judge by
hand, and the judgement on 2026-11-10 ("a flake") rests on one red and one green.

## Done when

- [ ] The cause of the two failures is named in this file.
- [ ] It is fixed, with the test or harness change that shows it, or filed as a
      `bug` naming the fix's location.
- [ ] `cargo test --test lease_client` passes 50 runs in a row under CPU load,
      and this file says how the load was made.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
