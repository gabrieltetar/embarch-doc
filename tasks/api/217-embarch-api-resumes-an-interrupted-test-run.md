# 217 — embarch-api resumes an interrupted Test run

**State:** open
**Source:** EMB-587 — embarch-api cannot resume an interrupted Test run
**Issue:** EMB-587
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Core decision 153 (`core/178`) added `POST /test-runs/{id}/resume {run_id}`:
either token, `201` with `{run_id, run_hash, resumes, lease_holder,
duration_bound_ms, pending, kept}`, which prepares a new run of the
interrupted run's pending tests, cut from the interrupted run's own record.
The new run has its own card, nonce and go, like any run. Refusals: `404`;
`409` for never started, in flight, ended otherwise, already resumed, nothing
pending, or the id in use; `400`. embarch-api cannot reach the route:
`embarch-core-client` has no method for it, and no CLI subcommand or MCP tool
calls it.

When this is done:

- `embarch-core-client` has a method for the route, beside `test_run_status`,
  `test_run_card` and `test_run_go` in `crates/embarch-core-client/src/client.rs`.
- A CLI subcommand and an MCP tool prepare the resume and then hand off to the
  **same** card-and-go path a fresh Test run uses (`run_test`'s): the tool
  prepares, never starts; the go stays the engineer's on Core's card. Name the
  new run and the run it resumes (`resumes`) in what the caller sees.
- A refusal from Core reaches the caller as Core said it, never reworded into
  a different reason and never retried.

**The MCP tool's permission class.** `suite/agent-guide.md` §1.1 places every
registered tool in allow or ask (`suite/064` placed all 64). A new tool must be
placed there too, and that file is the supervisor's, not yours: say in your
report which list it belongs in and why (`run_test`, which also only prepares,
is in allow), and write a `status.d/` fragment naming the target doc and the
line, per `status.d/README.md`.

**This is a shared crate.** The supervisor reads the client diff before
landing, and `tasks/suite/065` (the client reads `prompt_kind` on the
`PromptPending` event, a field in `study_events.rs`) lands just after you in
the same crate. Keep the client change additive and away from
`study_events.rs`.

## Where to look

- `crates/embarch-core-client/src/client.rs` (the Test run calls), `src/tools.rs`
  (the Test run tools), `src/cli.rs`
- `embarch-doc/embarch-core/interfaces/test-runs.md` (the route),
  `embarch-doc/embarch-core/decisions/test-run-resume.md` (153)
- `embarch-doc/embarch-api/decisions/` (the Test run tool decisions, and the
  client-crate decision for the new method); `interfaces/tools-test-*.md`

## Where the doc goes

A new api decision for the resume tool and verb, beside the Test run tool
decisions; the interface doc that lists the Test run tools gains the tool. **Over
or near their limit, do not grow:** `lease#90`, `test-plans#134`, `ledger#98`,
`bench-exchange#89`, `failure-reporting#67`, `publish-test-run#144`. Check
`scripts/check-doc-size.py --pressure` before you write; `spec.md` was 20 B under
its reserve line on 2026-11-26. If your work puts a file into reserve, file
`tasks/api/<NNN>-compact-api.md` in the same commit (`tasks/README.md` has the
shape; number from `scripts/check-task-numbers.py --next api`).

**Decision numbers:** the next api decision is the next free number in
`decisions.md`'s index when you write it; cite that one, and only that one, in
code comments.

## Done when

- [ ] An interrupted Test run can be resumed from the CLI and from the MCP
      tool against a mock Core, the new run naming the first in `resumes`, and
      neither starts it.
- [ ] Core's `409` (not interrupted, already resumed, nothing pending) and
      `404` reach the caller as Core said them.
- [ ] Gate green (`cargo build --workspace`, `cargo test --workspace`,
      `cargo clippy --workspace --all-targets -- -D warnings`).
- [ ] Decision written; interface doc names the tool; `status.d/` fragment for
      `suite/agent-guide.md` §1.1; `changelog.d/` fragment; feature row if the
      Test run feature row lists what api can do with a run.
