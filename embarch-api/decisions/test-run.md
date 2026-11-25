# embarch-api decisions: preparing and watching a Test run

**Status:** active, 2026-11-25 (EMB-377, `tasks/api/200`).

Decision 135. Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Interface: [../interfaces/tools-tests.md](../interfaces/tools-tests.md). Design: [HIL 03](../../notes/hil/03-test.md), "A run" item 6 and "Selecting and rerunning". Core's routes: [test-runs](../../embarch-core/interfaces/test-runs.md). The expansion: [hil-run](../../embarch-study-designer/interfaces/hil-run.md).

### 135 - `run_test` prepares and never starts; `test_status` is one read; the benches that exist are the ones saved in the repo

**No agent path calls the go.** `run_test` expands, sends and shows the card; the go takes the person's token on every Core ([core 135](../../embarch-core/decisions/test-run-go.md)). The client crate carries `CoreClient::test_run_go` for the UI, the person's surface (`ui/124`), and `tests/run_test_cli.rs` fails if `src/tools.rs`, `src/cli.rs` or `src/hil_run.rs` name a `/go` route or `test_run_go`. The answer says `started: false` and that the engineer gives the go on the card or in the terminal, with the session still holding the lease. **The card's `nonce` and `expires_utc_ms` are dropped from the answer**, null for the agent's token anyway.

**The order.** (1) A saved `plan`, or a `suite` with `tests`, `tags` or `all` that builds one (its pin's commit is `commit`, else `unpinned`, since this crate cannot tell what a tree is). A suite with none of those lists its applicable tests, as `test_plan` does, prepares nothing and asks. (2) `hil_expand::expand` over the suite's tests and studies; a refusal is the crate's and **Core is not called**. (3) `POST /definitions` for each test and the manifest of a repo suite, and the plan; a premade suite's are Core's. (4) `POST /test-runs` with `run`, the plan's hash, the suite's hash (repo suites only) and every study by `study.file`, the expanded ones included. (5) `GET /test-runs/{id}/card` for the preview.

**Inputs the agent cannot know are asked for, never defaulted:** the standard and its revision, the unit's serial and board revision; `hardware_id` is optional. **Confirmations are sent empty**: Core's own record fills `confirmed`, and its comparison blanks it on both sides, so an unconfirmed input shows on the card and blocks the go there.

**"The benches the project has" is `embarch/topologies/<slug>.toml` existing for a suite bench's name**, the file `test_plan` copies in when it selects a suite. A test on another bench is `bench_missing`, listed in `not_run` with its reason, and a run left with no test is refused before Core. *Assumed, not measured:* a saved bench is the project's evidence that the bench exists; it does not prove the bench is wired.

**`test_status` returns Core's body whole** and beside a waiting prompt adds `prompt_relay`: a `setup` or `action` prompt is relayable with `answer_prompt` (a setup prompt's study id is the run id), an `observation` or a `clearance` is not. `studies: true` adds each verdict's studies' own status. `answer_prompt`'s `403` gains the same rule as text ([core 138](../../embarch-core/decisions/host-prompt.md)).

**Not verified:** a mock Core only. Whether Core accepts the extra base-study keys a template needs, serves a premade suite's studies at `GET /definitions/<study hash>` (the premade path tries it), or reproduces this crate's `run.json` byte for byte has never been run. See [open/bench-verification.md](../open/bench-verification.md).
