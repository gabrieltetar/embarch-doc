# embarch-api: host-study tools

**Status:** active, 2026-10-28. A study Core runs itself, and its operator prompts ([decisions](../decisions/host-study.md) 99; Core's [decision 105](../../embarch-core/decisions/host-prompt.md)); see [tools.md](tools.md) for the one-table premise. Each tool is also a kebab-case subcommand.

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `run_host_study` / `run-host-study --study-file` | `study_file` | Reads a `HostStudy` JSON file, checks it, Core `POST /host-studies`. Returns `study_id`; the study runs on. Refused `409` while any study holds the bench |
| `answer_prompt` / `answer-prompt <study_id> <prompt_id> <answer>` | `study_id`, `prompt_id`, `answer` (`confirmed`/`cancelled`) | Core `POST /study/{id}/prompt`, `answered_by` `mcp` or `cli`. **Relays a person's answer only.** `409` names the prompt now waiting when this one already ended |

`study_watch` returns early with `prompt_pending {prompt_id, list, step_index, step_name, text, opened_utc_ms, deadline_utc_ms}` when a prompt waits; `study_status` shows it as `pending_prompt`, and a finished host study's record as `host_result`. `study-status --follow` prints prompts and follows on.

**Nothing here has met a real Core.**
