# embarch-api: host-study tools

**Status:** active, 2026-10-28. A study Core runs itself, and its operator prompts ([decisions](../decisions/host-study.md) 99, 100; Core's decisions [105 and 107](../../embarch-core/decisions/host-prompt.md)); see [tools.md](tools.md) for the one-table premise. Each tool is also a kebab-case subcommand.

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `run_host_study` / `run-host-study --study-file` | `study_file` | Reads a `HostStudy` JSON file (a `Prompt` may carry `bench_config`), checks it, Core `POST /host-studies`. Returns `study_id`; the study runs on. Refused `409` while any study holds the bench |
| `answer_prompt` / `answer-prompt <study_id> <prompt_id> <answer>` | `study_id`, `prompt_id`, `answer` (`confirmed`/`cancelled`) | Core `POST /study/{id}/prompt`, `answered_by` `mcp` or `cli`. **Relays a person's answer only.** `409` names the prompt now waiting when this one already ended For a Test run's prompt ([135](../decisions/test-run.md)) a setup prompt's `study_id` is the run id and an action prompt is relayed too; a `403` (an observation or a clearance, core 138) is explained in the error: the person answers on the card or in their terminal, and a retry changes nothing. |
| `cancel_study` / `cancel-study <study_id>` | `study_id` | Core `POST /study/{id}/cancel` (Core decision 128): any host or device study, `202 {status: "cancelling"}` at once; the study ends after its teardown or the bench's stop, so watch it with `study_status`. Takes the lease token as a gated call. `404` unknown, `409` not running: Core's text, reported |

`study_watch` returns early with `prompt_pending {prompt_id, list, step_index, step_name, text, bench_config?, opened_utc_ms, deadline_utc_ms}` when a prompt waits (`bench_config` as Core sent it, absent when the step names none); `study_status` shows it as `pending_prompt`, and a finished host study's record as `host_result`. `study-status --follow` prints prompts and follows on.

**Nothing here has met a real Core**; `cancel_study` has met a mock one only.
