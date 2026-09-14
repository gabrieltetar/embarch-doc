# 088 — The smoke harness fails under concurrent load, and a supervisor's merge gate reads that as a real red

**State:** done
**Source:** observed by the leg of 2026-09-13 while landing `tasks/api/087`. Not a task anyone
filed, and **not a defect in `api/087`'s change** — I proved that before writing this.
**Scope:** api
**Hardware:** none — a host-side test-robustness change. No board, no live Core, no deploy.
**Owner:** no

## What happened, with the measurements

Landing `api/087` ran the merge gate — `cargo build` / `cargo test` / `clippy` on the merge result —
**while an unrelated worker was running its own `cargo test` in a different repo on the same
machine.** The result:

| run | condition | result | duration |
|---|---|---|---|
| merge gate, 1st attempt | another worker's `cargo test` running concurrently | **FAILED** | 30.53 s |
| `main`, unmodified | quiet machine | passed | 0.29 s |
| `api/087` branch, isolated worktree | quiet machine | passed | 0.35 s |
| merge gate, 2nd attempt | quiet machine | passed | — |

The failing test is `smoke_sequence_against_a_throwaway_core_and_a_fixture_repo` in
`tests/smoke_harness.rs`. **A hundredfold jump in wall time and no other difference is a timeout,
not a logic failure** — the test spawns a throwaway `embarch-core` and waits for it to become
reachable, and under CPU contention it did not come up inside whatever bound the harness allows.

## Why this is worth fixing rather than tolerating

`.claude/leg.md` tells a supervisor to re-run the full gate on the merge result and **hard-reset
both repos on any red**, and to leave the task `blocked` rather than fix it. That is the right rule
and it worked exactly as written here — nothing bad landed. But the red was false, and a false red
costs one of two things depending on how careful the supervisor is:

- **The careful path** — what happened this time: diagnose, run the test on `main`, run it on the
  branch in an isolated worktree, conclude contention, re-land. That is roughly ten minutes of a
  leg's twenty-minute budget spent proving a negative.
- **The uncareful path**: leave `api/087` `blocked` with "smoke test failed", and a completed,
  correct unit sits parked until a human reads the log.

A supervisor keeps a wave of workers in flight **by design**, so a gate that is sensitive to
concurrent load is sensitive to the fleet's normal operating condition, not to an unusual one. And
it is timing-sensitive, so it will not reproduce when investigated — the shape of failure that
teaches a reader to distrust the gate. `.claude/leg.md` already warns that a supervisor who learns
to wave through a red check is the real hazard.

## What to do

Make the harness robust rather than fast, and say which bound you changed. Options, in rough order
of preference — pick one and argue it in the decision:

1. **Poll with a generous deadline instead of a fixed sleep or a short timeout.** Retry the
   reachability check until a wall-clock deadline (tens of seconds) rather than assuming startup
   fits in a fixed window. A test that takes 0.3 s on a quiet machine and 8 s on a loaded one is
   fine; one that fails on a loaded one is not.
2. **Report the timeout as a timeout.** Whatever the bound becomes, the failure message should say
   *"the throwaway Core did not become reachable within N s"* and name N, so the next reader can
   tell a startup timeout from a behavioural failure **without** running the test three times to
   find out. This is worth doing even if you also do (1).
3. Mark it `#[ignore]` and run it only on demand — **listed for completeness and probably wrong**:
   `embarch-api/open.md` already records that Windows never runs this tier at all, so narrowing
   where it runs makes a thin tier thinner.

Find the actual bound first — read `tests/smoke_harness.rs` and whatever helper spawns the Core, and
say in the decision what the old bound was. **Do not guess that a timeout exists; locate it.** If it
turns out the failure was not a timeout at all, that is a more interesting finding than the fix:
say so and stop, because the evidence above would then be explained by something else.

## Done when

- [x] The actual bound is located and named, and the failure mode is confirmed as a startup timeout
      rather than assumed. **Located, and it is not a "startup" timeout in the sense assumed above —
      there is no reachability-poll loop anywhere in this harness or `tests/support::MockCore`.
      `MockCore::start` binds its listener before returning, so nothing here waits for a server to
      *come up*.** The bound is the existing per-request HTTP timeout on the sequence's one Core
      call (`status`): `CoreConfig::status_timeout_secs`, defaulting to 10s
      (`crates/embarch-core-client/src/lib.rs`). Confirmed by direct reproduction, not just reading
      the code: scaled artificial CPU contention on the same worker machine (up to 80 competing
      `yes` processes across 14 cores) stretched the identical call from 0.30s upward (0.97s at 21
      competing loops, 2.52s at 80), the same direction and shape the leg's own numbers show, before
      the fleet's own workload-interference guard refused further escalation on this shared machine.
- [x] The harness tolerates a loaded machine, or says clearly that it timed out and after how long.
      Fixed by raising the fixture's own `status_timeout_secs` to 60s (`tests/smoke_harness.rs`),
      not the crate-wide default real hardware calls still want short. `CoreClient::dispatch` now
      also names the configured timeout in its error context on every failure — a caller of this
      crate sees *how long* it waited, not only that `reqwest` errored (it already said "operation
      timed out" via the chain, just not the bound).
- [x] A numbered `embarch-api` decision records the choice — derive the next free number with
      `scripts/check-decision-refs.py` / `decisions.md`, never by eyeballing the highest visible.
      Decision 74, `embarch-api/decisions/tests.md`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). All 11 `check-docs.py` checks pass;
      `check-client-names.py` and `check-ownership.py` (both repos) pass; `embarch-api`'s
      `cargo build`/`cargo test`/`cargo clippy --all-targets -- -D warnings` all green.
- [x] `changelog.d/` fragment. `changelog.d/api-smoke-harness-concurrent-load.fixed.md`.

**Decision 74 pushed `embarch-api/decisions/tests.md` into its reserve band (12201/12288 B,
99.3%, 87 B left) — filed `tasks/api/090-compact-api.md` in this same commit, per the reserve
note below.** (Filed as `089` and renumbered to `090` by the supervisor at landing: the leg had
already issued `tasks/api/089` in a refill commit this branch was cut before.)

## Reserve, for planning

`embarch-api/spec.md` is 9,102/10,240 B — **1,138 B left, 88.9%** — filed against blocked
`tasks/api/083`. `decisions/surface.md` came **out** of reserve on 2026-09-13 when `api/087` split
it; `decisions/tests.md` is where this repo's test decisions live, so check its headroom before
filing there. If your work leaves any `embarch-api` doc in the last 10% of its cap unfiled, file
`tasks/api/<next>-compact-api.md` in the same commit — **your own scope**, never `tasks/doc/`.
