# 161 — Core enforces a prompt's kind by the token's scope

**State:** claimed by agent/core/161-core-enforces-a-prompts-kind-by-the-tokens-scope, 2026-11-25 09:42
**Source:** EMB-367 — Core does not know a prompt's kind and lets the agent answer any prompt (first half; the setup window is `core/162`)
**Issue:** EMB-367
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`POST /study/{id}/prompt` takes `answered_by` from the request body and checks
no scope (`src/host_study.rs`, `answer_prompt_handler`), and a prompt has no
kind. An observation's answer is a measurement and a clearance's is a person's
safety, so the agent must not relay either (`notes/hil/12-prevention.md`:
"Core refuses a relayed answer to an observation or a clearance"; "Relayed is
decided by the token's scope, never by `answered_by`"). When this is done:

- **Each prompt's kind comes from the run's `run.json`** (`prompt_kinds`, which
  the engineer confirmed with the test; the shared crate's `RunPromptKind`),
  looked up by step name. A study cannot relabel it. A study run outside a Test
  run has no `run.json`: its prompts carry no kind and keep today's answers;
  say so in the decision.
- **An answer to an `observation` or `clearance` prompt with the agent's token
  is refused `403`**, naming the kind and the person's surfaces (the UI, or the
  CLI where there is no UI).
- **Every answer records the token's scope** (`person` or `agent`);
  `answered_by` stays the surface and decides nothing. Amend decision 105.
- **An observation's answer is its value**: one of the prompt's declared
  `answers`, or a number in its declared unit (the crate's observation-answer
  shape beside `PromptKind`), taken only with the person's token and written to
  `measurements.json` as `by: person`, `method {kind: "prompt", prompt_kind:
  "observation"}`. An answer outside the declared choices is refused `400`,
  naming them. `confirmed` and `cancelled` stay the answers of every other
  kind. The owner may strike this shape (plan choice 27): say so in the
  decision.
- **An unanswered observation** (timeout or cancel) is `inconclusive`,
  `observation_unanswered`; any other kind's timeout or cancel is `error`,
  through the crate's `step_verdict` as `core/160`'s executor already calls it.
- **Each prompt records the outputs Core last switched on**, from the
  energising steps it ran (the crate's `hil_check::energises`), so a surface
  can show them.

Not this unit: the setup prompt between benches and the setup-call window in
`lease_middleware` (`core/162`).

## Where to look

- `src/host_study.rs` — `answer_prompt_handler`, `PromptSlot`, `PendingPrompt`
- `src/test_executor.rs` (decisions 136, 137) — where a run's study runs, and
  where `run.json` is in hand
- `src/token_store.rs` — the token's scope; `src/measurements.rs`
- `embarch-study-designer/src/host_study.rs` (`PromptKind`, the observation
  answer), `src/hil_expand.rs` (`RunPromptKind`), `src/hil_check.rs`
  (`energises`), `src/verdicts.rs` (`step_verdict`)

## Where the doc goes

`decisions/host-prompt.md` (5,372 B) holds 105 and 107: amend 105 there, and
add a new decision for the kinds. **Do not grow decisions 93 (`lease.md`, 144 B
over its per-decision limit), 95 (`host-study.md`, 799 B over) or 133
(`definitions.md`, 233 B over)**; point to the new decision from your own text
instead. `interfaces/` for the `403` and `400` refusals and the prompt record's
new fields. If your work pushes any file into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md`.

## Done when

- [ ] An observation answered with the agent's token is refused `403`; with the
      person's, its choice is recorded with scope `person` and written as a
      `by: person` measurement.
- [ ] An answer outside the declared choices is refused `400`, naming them.
- [ ] An unanswered observation is judged `inconclusive`,
      `observation_unanswered`; an unanswered `action` prompt is `error`.
- [ ] A prompt after an instrument set lists that output as switched on.
- [ ] A study outside a Test run answers as it did before.
- [ ] Decision 105 amended; a new decision records the kinds.
- [ ] Gate green.
