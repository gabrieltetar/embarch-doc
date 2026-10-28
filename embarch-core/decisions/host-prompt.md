# embarch-core decisions: Operator prompts in a host study

**Status:** active, 2026-10-28.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). HTTP surface: [../interfaces/host-studies.md](../interfaces/host-studies.md). Siblings: [host-study.md](host-study.md) (decisions 95, 98, 99, the executor this extends). Design of record: [the proposal](../../embarch-host-study-proposal.md), owner's choice 4.

### 105 — A `Prompt` step waits for a person's answer, relayed by any surface and checked by prompt id, until its own deadline

Field use on a USB PD charger board (2026-10-09 to 10-14): the operator typed 25 confirmations into a chat during one bench session, 13 of them in one hour ("out", "in", "on", "done"), and nothing recorded who confirmed what or when. Decision 95 refused `Prompt` by name until this unit.

**What runs.** A `Prompt { text }` publishes a pending prompt and waits. Core sends `PromptPending {prompt_id, list, step_index, step_name, text, opened_utc_ms, deadline_utc_ms}` and shows the same fields as `pending_prompt` on `GET /study/{id}`, because the event stream keeps no replay (decision 41): a watcher that connects after the event finds the prompt there. `POST /study/{id}/prompt {prompt_id, answer, answered_by}` answers it. The step ends on the first of three things. **`confirmed`** passes (`detail: confirmed`). **`cancelled`** fails it (`prompt_cancelled`), so the study stops unless `continue_on_fail` and the teardown runs. **The deadline** times it out (`prompt_timed_out`, `TimedOut`). A cancel of the study under a prompt ends it as any other step (`cancelled`). `PromptResolved {prompt_id, answer, answered_by, resolved_utc_ms}` follows each; `answer` there is also `timed_out` or `study_cancelled`. The record keeps `prompt_id`, `prompt_deadline_utc_ms` and `answered_by`.

**The two open points of the proposal, answered.**

- **Who may answer: anyone holding Core's token, from any surface, and the prompt id is the check.** `answered_by` is `ui`, `mcp` or `cli` and is recorded, never trusted for anything else, because every surface relays the same person. The route is **not lease-gated**: the agent that started the study holds the lease, and the person at the bench answers from the UI in front of them. An answer names the prompt it is for, so one meant for a prompt that timed out is refused `409` naming the prompt that is waiting, rather than confirming the next one. An answer is taken once; a second is `409`. Whether an agent may answer is the `embarch-api` tool's rule: it relays a person's answer and never answers on its own judgement.
- **The default timeout: none.** The designer already requires every step to state a nonzero `timeout_ms`, and a prompt's is its deadline. Core caps it at **one hour**, refused `400` by step above that. Reasoned, not measured: the field's longest gap between two confirmations was minutes, and a waiting prompt holds `study_lock`, so a forgotten one has to end on its own.

**Where a prompt may stand.** In the steps, inside a `Repeat` (its text is not substituted; decision 86 names `Exchange` and `Instrument` lines only), and in the teardown, where it waits out its deadline and a cancel of the study does not end it, like every teardown step. A prompt takes no `hw_lock`: it touches no hardware, and a lock held while a person walks to the bench would refuse every flash for that long.

**Why one slot polled, not a channel.** The pending prompt and its answer live in one mutex slot that the executor looks at every 20 ms, the cancel poll's period. The executor clears the slot under the same lock as its last look, so an answer either lands before the clear and counts, or finds no prompt and is refused. None is accepted and then lost.

**Measured vs assumed.** Every exit path is proven over the scripted backend, and the wait and the answer route over the real slot across two threads. **Not run:** a prompt answered on a real bench, by any surface. The UI's modal is `tasks/ui/100`.
