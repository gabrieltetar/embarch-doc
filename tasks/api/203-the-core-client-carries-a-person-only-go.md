# 203 — The core client carries a person-only go, and the go ban narrows to the agent's surfaces

**State:** done — test_run_go on the client, mock test and sweep entry, ban narrowed to the agent surfaces, decision 135 amended
**Source:** EMB-384 — the UI has no go card (the `embarch-api` half: the UI's go has to leave through `embarch-core-client`; `ui/124` is the card)
**Issue:** EMB-384
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Core's `POST /test-runs/{run_id}/go` takes `{run_id, run_hash, nonce}` from the
card and the person's token only, on every Core (core decision 135). `api/200`
made the agent unable to give the go, and did it by keeping the go out of
`embarch-core-client` entirely: `tests/run_test_cli.rs` fails if `src/tools.rs`,
`src/cli.rs`, `src/hil_run.rs` **or the client crate** name a `/go` route. That
is right for the agent and wrong for the UI, which reaches Core only through
that crate and is where the person gives the go (`ui/124`).

So the ban moves from the crate to the agent's surfaces:

- `CoreClient::test_run_go(run_id, run_hash, nonce)` posts the body Core
  documents, through the same `send` funnel as every other method (the bearer
  is whichever token the client was built with), and returns Core's answer.
  Additive only: the crate is shared with `embarch-ui` and `embarch-umbrella`.
  Its doc comment says it is the person's, that Core answers `403` to the
  agent's token, and that no MCP tool or CLI verb may call it.
- `tests/run_test_cli.rs` keeps failing on a `/go` route in `src/tools.rs`,
  `src/cli.rs` and `src/hil_run.rs`, and adds that none of those three names
  `test_run_go`. The client crate leaves the ban.
- The mock test for the method asserts the path, the body and the bearer
  header, and the method is in the one-funnel sweep as `api/199`'s were.

## Where to look

- `crates/embarch-core-client/src/client.rs` — `test_run_card`,
  `prepare_test_run` and `confirm` for the shape
- `tests/run_test_cli.rs` — the two `/go` assertions (lines near 169 and 238)
- `embarch-doc/embarch-core/interfaces/test-runs.md` — the go row and its
  refusals
- `embarch-doc/embarch-api/decisions/test-run.md` — decision 135's
  "No code path calls the go" paragraph

## Where the doc goes

Decision 135 amended in place: no *agent* path calls the go, and the client
carries a person-only method for the UI (`test-run.md` is 3,484 B, room
enough). `embarch-api/spec.md` is in reserve (`tasks/api/201`, blocked,
`In flux: yes`): do not write it in this unit. `check-doc-size.py --pressure`
lists lease#90, test-plans#134, ledger#98, bench-exchange#89 and
failure-reporting#67 over or near their limits; do not grow those.

## Done when

- [x] `CoreClient::test_run_go` exists, is mocked with path, body and bearer
      asserted, and goes through the one funnel.
- [x] The test still fails if `src/tools.rs`, `src/cli.rs` or `src/hil_run.rs`
      names a `/go` route or `test_run_go`, and no longer covers the client
      crate.
- [x] Decision 135 says the agent cannot give the go and the UI can.
- [x] Gate green, the client crate included.
