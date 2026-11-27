# embarch-api: test tools

**Status:** active, 2026-11-25 ([decisions 134](../decisions/test-plans.md), [135](../decisions/test-run.md)); see [tools.md](tools.md) for the one-table premise. Each tool is also a kebab-case subcommand (`test-propose`, `test-plan`, `run-test`, `test-status`; `run-test`'s `capabilities` and `hooks` are `--capabilities-file` and `--hooks-file`, its picks repeated `--test` and `--tag`), `--project` defaulting to the session's desk's. On the CLI a JSON parameter is a file: `--definition-file`, `--study-file`, `--bench-file`, `--measured-file`, `--capabilities-file`. Code: `src/hil_repo.rs`, `src/hil_run.rs`. The crate's shapes: [hil-tests](../../embarch-study-designer/interfaces/hil-tests.md); Core's route: [definitions](../../embarch-core/interfaces/definitions.md).

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `test_propose` | `kind` (`test`, `capability`, `hook`), `definition`, `study?`, `bench?`, `measured?`, `suite?`, `project?` | The crate checks it (shape; with `study` and `bench`, `hil_check::check_test` over `measured`); a refusal is the crate's reason, one line each, `refused_before_core: true`, and Core is not called. Else `POST /definitions`; the answer has `hash`, `kept`, `checked` (`shape` or `definition`), `confirmation`, `waits_for_confirmation` and `message`. Only the engineer confirms. With `suite`, a test is then written under `embarch/tests/suites/<suite>/`, and `written` lists the paths |
| `test_plan` | `plan?`, `suite?`, `definition?`, `capabilities?`, `project?` | `plan` + `definition`: write or update the plan (`replaced` says which) and select its suite. `plan` alone: read it. `suite` alone (or with `plan`, whose capabilities it uses): `applicable_by_bench` and `not_applicable` with reasons |

| `run_test` | `plan?`, or `suite?` with `tests?`, `tags?`, `all?`, `capabilities?`, `hooks?`, `stop_on_fail?`, `commit?`; `standard_name`, `standard_revision`, `declared_serial`, `board_revision`, `hardware_id?`; `project?` | Expands the selection, sends `run.json`, its definitions and its studies to `POST /test-runs`, and returns `run_id`, `run_hash`, `duration_bound_ms`, `started: false`, `card` (Core's card data: tests per bench, prompts with kinds, what is powered, `unconfirmed`, no nonce), `not_run` (tests out of the run, with the reason, such as a bench not saved) and a `message` saying the engineer gives the go. **It never starts a run; no code path calls the go.** A suite with no selection returns `applicable_by_bench`, `prepared: false` and `ask`. A refusal by the crate is before Core |
| `resume_test` | `run_id`, `new_run_id?` | `POST /test-runs/{run_id}/resume {run_id: new}` (core 153), then the card as `run_test` shows it: `run_id`, `resumes` (the interrupted run), `pending`, `kept`, `run_hash`, `duration_bound_ms`, `started: false`, `card` (no nonce). CLI `resume-test <run_id> [--new-run-id]`. A refusal (`404`; `409` not interrupted, in flight, already resumed, nothing pending, id in use; `400`) is Core's text, sent once |
| `test_status` | `run_id`, `studies?` | `GET /test-runs/{id}` as `run`: `state`, `bench`, `test`, `verdicts`, `waiting_prompt`, and with a prompt `prompt_relay {kind, relayable, study_id, say}`; `studies: true` adds each study's own status |

**`measured`** is `{<measurement>: {by: bench\|dut\|person, source, range_min, range_max, resolution, u}}`, Core's own shape. **`study.hash`** may be left out of a test's `definition`: it is the hash of the study as the tool writes it, and is filled.

**Selecting a suite** copies each bench of its manifest to `embarch/topologies/<slug>.toml`; the answer's `selection` lists `copied`, `unchanged` and `left_alone` (each with a `diff`, `-` the saved bench's line, `+` the suite's). A saved bench is never overwritten.

**The layout**, under the project's `source_path`:

- `embarch/tests/suites/<suite>/suite.json`, and per test `<test id>/test.json` with its study file beside it; a manifest line's `file` is `<test id>/test.json`.
- `embarch/tests/plans/<plan>.json`.
- `embarch/tests/results.jsonl`: the run log's mirror, written by [the test ledger tools](tools-test-ledger.md).

Every name is `[a-z0-9][a-z0-9._-]*`. **Not verified on a bench or against a real Core** ([open.md](../open.md)).
