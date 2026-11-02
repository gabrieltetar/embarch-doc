# embarch-api decisions: Host-run studies and operator prompts

**Status:** active, 2026-10-28.

Index: [../decisions.md](../decisions.md). Tools: [../interfaces/tools-host-study.md](../interfaces/tools-host-study.md). Core's side: [`embarch-core` decisions 95, 105 and 107](../../embarch-core/decisions.md). Design of record: [the proposal](../../embarch-host-study-proposal.md).

### 99 — `run_host_study` and `answer_prompt`, and a watch that stops for a waiting person

**The tools.** `run_host_study {study_file}` reads a `HostStudy` as JSON, runs its own `validate()` so a malformed study is refused with the designer's words, and posts it to `POST /host-studies` behind the same schema-version gate as `run_study`. `answer_prompt {study_id, prompt_id, answer}` relays `confirmed` or `cancelled` to `POST /study/{id}/prompt` with `answered_by: "mcp"`. The subcommands `run-host-study --study-file` and `answer-prompt <study_id> <prompt_id> <answer>` are the same calls, answering as `cli`.

**`answer_prompt` relays a person's answer and nothing else, and its description says so in capitals.** A prompt asks for a physical act — plug a cable, switch a supply — that only a person at the bench can confirm happened, so an agent that answered from its own reading of the study would be asserting a hardware fact it inferred (the suite's [no-inference invariant](../spec.md)). The description tells the agent to show the person the text, ask, and pass on exactly what they said; a `409` for a prompt that already ended means ask again, not retry with the new id.

**`study_watch` returns early when a prompt waits** (`FollowOptions::stop_on_prompt`), with `prompt_pending {prompt_id, text, deadline_utc_ms, …}`. An MCP call is bounded at 60 s by default and a prompt's deadline can be an hour; a watch that sat out its budget while the person never saw the prompt would spend the deadline for nothing. `study-status --follow` does not stop: it prints the prompt as a line and follows on, because a person is already reading it.

**In `embarch-core-client`.** The event mirror decodes `HostStepCompleted`, `PromptPending` and `PromptResolved`. `follow_study` reports a prompt already waiting from its opening poll and from polling, never twice, because the stream keeps no replay and a prompt published before the subscription would otherwise never be seen. `GET /study/{id}` gains `pending_prompt`, and a host study's record (`kind: "host"`) moves to `host_result` before the typed parse: it is not a bench `StudyResult`, and before this every follow of a finished host study failed parsing it. The crate enables study-designer's `alloc` itself for the host types, which every consumer already enabled by unification.

**Measured vs assumed.** Tested against a mock Core: the bearer token on both routes, a live prompt stopping a follow, a prompt already waiting found by the opening poll, the host record parsed. **Not run:** against a real Core, by a real agent relaying a real person.

### 100 — A prompt's `bench_config` reaches the person as Core sent it; the agent neither authors a parameter for it nor resolves it

A `Prompt` may name a bench configuration (`embarch-study-designer` decision 88), which Core forwards unresolved (`embarch-core` decision 107). **No tool parameter**: `run_host_study`'s `study_file` is already a `HostStudy`, so an agent writes `bench_config` in the file. `embarch-core-client` carries it on `PendingPrompt` and `PromptPending` (`#[serde(default)]` for an older Core, skipped when `None`), so `study_watch`'s `prompt_pending` and `--json` lines hold it, and `study-status --follow` prints `[bench config 'x']`.

**The agent shows it and resolves nothing.** The description tells it to show the person the text and any `bench_config`; whether the bench is in that config is a physical fact only the person confirms, decision 99's rule. *Rejected:* checking the name against Core's topology, which holds no configs.

**Measured vs assumed.** Mock Core only: the event and the opening poll carry it, an event without it re-emits no key.
