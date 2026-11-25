# embarch-core decisions: Operator prompts in a host study

**Status:** active, 2026-10-28.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). HTTP surface: [../interfaces/host-studies.md](../interfaces/host-studies.md). Siblings: [host-study.md](host-study.md) (decisions 95, 98, 99, the executor this extends). Design of record: [the proposal](../../embarch-host-study-proposal.md), owner's choice 4. Who resolves 107's name: `embarch-ui` decision 99.

### 105 — A `Prompt` step waits for a person's answer, relayed by any surface and checked by prompt id, until its own deadline

Field use on a USB PD charger board (2026-10-09 to 10-14): the operator typed 25 confirmations into a chat during one bench session, 13 of them in one hour ("out", "in", "on", "done"), and nothing recorded who confirmed what or when. Decision 95 refused `Prompt` by name until this unit.

**What runs.** A `Prompt { text }` publishes a pending prompt and waits. Core sends `PromptPending {prompt_id, list, step_index, step_name, text, opened_utc_ms, deadline_utc_ms}` and shows the same fields as `pending_prompt` on `GET /study/{id}`, because the event stream keeps no replay (decision 41): a watcher that connects after the event finds the prompt there. `POST /study/{id}/prompt {prompt_id, answer, answered_by}` answers it. The step ends on the first of three things. **`confirmed`** passes (`detail: confirmed`). **`cancelled`** fails it (`prompt_cancelled`), so the study stops unless `continue_on_fail` and the teardown runs. **The deadline** times it out (`prompt_timed_out`, `TimedOut`). A cancel of the study under a prompt ends it as any other step (`cancelled`). `PromptResolved {prompt_id, answer, answered_by, resolved_utc_ms}` follows each; `answer` there is also `timed_out` or `study_cancelled`. The record keeps `prompt_id`, `prompt_deadline_utc_ms` and `answered_by`.

**The two open points of the proposal, answered.**

- **Who may answer: either token, from any surface, and the prompt id is the check; the kind and the token's scope say whose answer it is ([138](#138--a-prompts-kind-comes-from-the-run-and-the-tokens-scope-decides-who-may-answer-it)).** `answered_by` is `ui`, `mcp` or `cli`, the surface, and decides nothing; each answer also records the token's `scope`. The route is **not lease-gated**: the agent that started the study holds the lease, and the person at the bench answers from the UI in front of them. An answer names the prompt it is for, so one meant for a prompt that timed out is refused `409` naming the prompt that is waiting, rather than confirming the next one. An answer is taken once; a second is `409`.
- **The default timeout: none.** The designer already requires every step to state a nonzero `timeout_ms`, and a prompt's is its deadline. Core caps it at **one hour**, refused `400` by step above that. Reasoned, not measured: the field's longest gap between two confirmations was minutes, and a waiting prompt holds `study_lock`, so a forgotten one has to end on its own.

**Where a prompt may stand.** In the steps, inside a `Repeat` (its text is not substituted; decision 86 names `Exchange` and `Instrument` lines only), and in the teardown, where it waits out its deadline and a cancel of the study does not end it, like every teardown step. A prompt takes no `hw_lock`: it touches no hardware, and a lock held while a person walks to the bench would refuse every flash for that long.

**Why one slot polled, not a channel.** The pending prompt and its answer live in one mutex slot that the executor looks at every 20 ms, the cancel poll's period. The executor clears the slot under the same lock as its last look, so an answer either lands before the clear and counts, or finds no prompt and is refused. None is accepted and then lost.

**Measured vs assumed.** Every exit path is proven over the scripted backend, and the wait and the answer route over the real slot across two threads. **Not run:** a prompt answered on a real bench, by any surface. The UI's modal is `tasks/ui/100`.

### 107 — A prompt's `bench_config` is forwarded as the study wrote it, and Core resolves nothing

`embarch-study-designer` decision 88 lets a `Prompt` name a bench configuration. **Core knows no bench**: configs are the UI's record of the live bench. It checks the name against nothing and refuses none; a name the live bench lacks is the showing surface's case, where a person picks a config or goes on with the text (owner, 2026-11-01).

- **Where it goes.** `PendingPrompt.bench_config`, so `PromptPending` (flat) and `pending_prompt` carry it, and the step's record beside `prompt_id`, `prompt_deadline_utc_ms` and `answered_by`: `events.json` and the steps rows (which until now dropped all four) say which config was confirmed, by which surface and when. Absent when `None`, so a prompt naming none publishes the bytes it did.
- **Not on `PromptResolved`**, which the prompt id ties to it, **or `HostStepCompleted`**, which carries no prompt id but follows the prompt in order at the same `(list, step_index)`.
- *Rejected:* resolving it here, which needs the UI's bench file and would fail a study that only needed a person to re-cable.

**Measured vs assumed.** Proven over the scripted backend, the real backend's slot and event, and the steps route. **Not run:** on a real bench.

### 138 — A prompt's kind comes from the run, and the token's scope decides who may answer it

`notes/hil/12-prevention.md`: an observation's answer is a measurement and a clearance's is a person's safety, so the agent relays neither, and "relayed" is the token's scope, never `answered_by`.

- **The kind is `run.json`'s `prompt_kinds`, by step name** (the engineer confirmed it with the test), taken at the executor ([136](test-run-executor.md)) and given to the study's backend. A study cannot relabel its own prompt: its `kind` field is not read, here or by the verdict. **A study run outside a Test run has no `run.json`**, so its prompts carry no kind and answer as under 105: either token, `confirmed` or `cancelled`.
- **`403`** for the agent's token on an `observation` or a `clearance`, whatever it answers, naming the kind and the person's surfaces (the UI, the CLI where there is no UI); the prompt stays pending. Checked after the `409`s, under the slot's one lock.
- **Every answer records the token's scope** (`person`/`agent`) in the step's `answered_scope` beside `answered_by`.
- **An observation's answer is its value** (the owner may strike this shape, plan choice 27): `answer: confirmed` with `value`, one of the prompt's declared `answers` or a number when it declares one in a unit, with the person's token only. A value outside the choices, or not a number, is `400` naming what it declares; a value on any other prompt, or a missing one, is `400`. It is recorded in the step (`observed`) and written to `measurements.json` as `by: person`, `method {kind: "prompt", prompt_kind: "observation"}`, `declared_by` scope `person`. `cancelled` carries none.
- **Unanswered:** an observation's timeout or cancel is `inconclusive`, `observation_unanswered`; any other kind's is `error`, `prompt_not_confirmed`, both from the crate's `step_verdict` with the kind from `run.json`.
- **`switched_on`:** a prompt lists the outputs the energising steps (the crate's `energises`, worked out at the prepare and kept in the run's record as `energising_steps`) last switched on: per target, the last line sent. Core cannot tell an off line from an on one, so it lists the last energising line and does not subtract. A record kept before this has none.

**Measured vs assumed.** Proven over the scripted backend and the real slot; the real backend's kind and `switched_on` through the slot and the run card. **Not run:** a bench, a person's answer from a surface, a real energising step. Session prompts ([127](analog-capture.md)) record no scope in their own record, and a number's declared resolution is not checked.
