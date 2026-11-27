# embarch-api decisions: resuming an interrupted Test run

**Status:** active, 2026-11-26 (EMB-587, `tasks/api/217`).

Decision 148. Index: [../decisions.md](../decisions.md). Builds on [test-run.md](test-run.md) (135: `run_test` prepares and never starts). Core's route and why the new run is cut from the interrupted run's own record: [core 153](../../embarch-core/decisions/test-run-resume.md), [test-runs](../../embarch-core/interfaces/test-runs.md). Interface: [../interfaces/tools-tests.md](../interfaces/tools-tests.md).

### 148 - `resume_test` prepares the rest and shows the card; it never starts it, and a refusal is Core's words

**One tool, one verb, one client method.** `resume_test` (CLI `resume-test <run_id> [--new-run-id <id>]`) calls `CoreClient::resume_test_run`, `POST /test-runs/{run_id}/resume {run_id: <new>}`, and answers with the new run's card. The client method is new and additive beside `test_run_card`; nothing existing changed. Either token may call the route, so the tool needs no person's token.

**The card path is `run_test`'s.** Both read the card through one function (`hil_run::shown`): the nonce and its expiry are dropped, `started` is `false`, and the message says the go is the engineer's on the card, with the session holding the lease (a restart restored none, core 153). The tool names the new run and the run it resumes: `run_id`, `resumes`, `pending` (the tests the new run will run), `kept` (the tests the interrupted run finished, whose verdicts stay in its record). `test_run_go` is still named by no agent path; `tests/run_test_cli.rs` still fails if `src/hil_run.rs` does.

**The new id is optional.** Core wants an id the caller picks, used once. `new_run_id` names it; omitted, the crate makes a fresh one as `run_test` does. A caller never has to invent one.

**A refusal is Core's, once.** `404`, `409` (never started, in flight, ended other than `interrupted`, already resumed, nothing pending, id in use) and `400` come back as `resume_test: embarch-core returned <status>: <Core's text>`, never reworded into another reason and never retried: no retry changes a run's history, and the tool description says so. No card read follows a refusal.

**Permission class: allow.** Like `run_test`, it only prepares; the go is the person's and stays off every agent path. Placed in `suite/agent-guide.md` 1.1 by the supervisor (status fragment).

**Not built.** Publishing a resumed pair as one zip (core 153 does not either), and choosing which pending tests to resume: Core resumes all of them.

**Measured:** against a mock Core, from the CLI (the tool calls the same function): a `201` shows `resumes`, `pending`, `kept`, no nonce and no request to a go route; the body sent is `{run_id}`; `409` three ways and `404` reach the caller with Core's text and one request each; the client's bearer sweep covers the route. **Not run:** a real interrupted run on a bench, and the MCP transport itself.
