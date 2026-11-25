# 124 — The UI shows a go card, and its prompt modal shows a prompt's kind

**State:** blocked — needs `CoreClient::test_run_go`, which is `api/203`
**Unparks when:** `api/203` lands
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

- [ ] Against a fake Core, a driven test gives the go once; a second click is
      refused by the fake and the card says so.
- [ ] An unconfirmed input disables the go and is named.
- [ ] The modal shows an observation prompt's kind, its choices and an output
      switched on, and sends the chosen answer.
- [ ] A decision records the card.
- [ ] Gate green.
