# 124 — The UI shows a go card, and its prompt modal shows a prompt's kind

**State:** open
**Source:** EMB-384 — the UI has no go card, and its prompt modal shows no kind (`api/203` is the client method this needs)
**Issue:** EMB-384
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

The engineer's go starts a Test run, and is given on what Core will run, not on
the agent's words. Core renders the card from its own record of `run.json`
(`GET /test-runs/{run_id}/card`, core decision 135): the tests per bench, every
prompt with its kind, what will be powered and at what level, each custom or
derived test's diff, every input still unconfirmed, an upper bound on the
duration, every limit with its `U` and `w`. The go binds the run id, the hash, a
nonce and an expiry, and is used once.

- **The go card**, drawn from Core's card data with every agent string as
  quoted text (`textContent`, as the Confirm tab does, ui decision 110). The go
  button is disabled while an input is unconfirmed, and names it. The go posts
  the card's `run_id`, `run_hash` and `nonce` with the person's token through
  `CoreClient::test_run_go`; a refusal (`422 mismatched`, `expired`,
  `replayed`; `409` and its reason) is shown as Core's text and the card
  reloads, never retrying by itself.
- **The prompt modal** shows the prompt's `kind` and the outputs Core last
  switched on (`waiting_prompt.switched_on`). For an `observation` or a
  `clearance` it says only the person answers it. An observation offers its
  declared choices, or a number field in its unit, in place of Confirm, and
  sends the chosen answer.
- A run's progress is not drawn here beyond the cards; `test_status` answers
  that.

Where the card lives — beside the Confirm tab's cards or in Live Study — is the
worker's call, recorded in the decision.

## Where to look

- `src/live_study.rs` — the prompt modal; `src/confirmations.rs` and
  `assets/confirm.js` — the person-token relay and the quoted-text drawing
- `src/config.rs`; `src/bench/drive_fixture.rs` — the fake Core a driven test
  runs against
- `embarch-doc/embarch-core/interfaces/test-runs.md` — the card, the go and
  `waiting_prompt`
- `embarch-doc/embarch-ui/decisions/operator-prompt.md` (69, 99) and
  `confirm-tab.md` (110)

## Where the doc goes

A new decision for the card, in `confirm-tab.md` or a new file;
`operator-prompt.md` amended for the modal (8,884 B). `decisions/live-study.md`
is in reserve (`tasks/ui/123`): do not write it unless that task has landed.
`check-doc-size.py --pressure` lists bench-live#90, launcher#28, tab-folders#100
and topology-tab#10,#43 near their limits; do not grow those.

## Done when

- [x] Against a fake Core, a driven test gives the go once; a second click is
      refused by the fake and the card says so.
- [x] An unconfirmed input disables the go and is named.
- [ ] The modal shows an observation prompt's kind, its choices and an output
      switched on, and sends the chosen answer.
- [x] A decision records the card.
- [x] Gate green.

## Blocked

The modal half (the second and fifth boxes' prompt side) cannot be built from this repo. `embarch-core-client`'s `PendingPrompt` and `StudyEvent::PromptPending` drop `kind`, `observation` and `switched_on`, and `PromptAnswerRequest` has no `value`, so the UI can neither read a prompt's kind nor send an observation's answer; the client is read-only here and the UI holds no raw Core access (103). Filed as EMB-575 (api). The go card shipped in the Confirm tab, decision 111. When EMB-575 lands: pass the fields through `prompt_json` and `PromptAnswerBody`, draw kind, `switched_on` and the choices or number field in the modal, amend `operator-prompt.md` (8,884 B, mind its cap), and tick the third box. "Gate green" is ticked below as the gate is.

**Unparked:** EMB-575 landed as `api/206` (api decision 137). `PendingPrompt` carries `kind`, `observation` and `switched_on`, and `PromptAnswerRequest` carries `value`. Two points the modal half must account for. First, `StudyEvent::PromptPending` carries `observation` and `switched_on` but **no `kind`**. Core flattens the prompt's `kind` onto an event whose tag is also `kind`, and a Test run's event fails to deserialize on the client ("duplicate field `kind`"). Read the kind from `GET /study/{id}`'s `pending_prompt`, not from the event, until EMB-577 (Core) lands. Second, the supervisor added `value: None` to the UI's existing `PromptAnswerRequest` literal in the same pass, so the answer route compiles. Sending a real `value` is this task's.
