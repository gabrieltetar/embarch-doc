# 121 — The UI shows a card on which the engineer confirms a test input

**State:** open — unparked by `api/199`'s fold: `CoreClient` now has `pending_confirmations`, `confirmation_card` and `confirm`, each returning `serde_json::Value`
**Source:** EMB-383 — the UI has no card on which the engineer confirms a test input
**Issue:** EMB-383
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

A confirmation is the engineer's act, made where the agent cannot reach and on
exactly what Core recorded. The UI has the prompt modal and no card for any
other act (`src/live_study.rs`; decision 69). The design: "a confirmation is
made in the UI only, or the CLI where there is no UI"; what is confirmed is a
custom or derived test whole, with its diff against the premade test, and each
DUT input field by field (`notes/hil/03-test.md`, "The DUT's inputs"); the card
"renders the act from Core's own record", "treats every string the agent wrote
as data", and submits "with a nonce Core issued for that card's rendering"
(`notes/hil/12-prevention.md`, item 4). Core already serves the three routes
(`embarch-core/src/confirmations.rs`): `GET /confirmations/pending`,
`GET /confirmations/{hash}/card` (the card's data and a nonce for a definition
still waiting) and `POST /confirmations`. When this is done:

- **A card lists what waits**, from `GET /confirmations/pending` and each
  item's card data: each custom or derived test with its `derived_from` diff
  and its prompt kinds, each capability with its provenance, each hook mapping,
  each limit with its `U` and `w`, as Core rendered them.
- **Every string the agent wrote is shown as text**, quoted, never as markup.
- **Confirm one item, or all shown**, with the person token the UI already
  holds (decision 111) and the card's nonce; a refused confirmation shows
  Core's reason. The surface recorded is `ui`.

## Where to look

- `src/live_study.rs` — the prompt modal, the pattern to follow
- `src/config.rs` — the person-token client
- `src/bench/drive_fixture.rs` — driven tests against a fake Core
- `embarch-core/src/confirmations.rs` and
  `embarch-doc/embarch-core/interfaces/` for the routes' shapes
- `embarch-doc/embarch-ui/decisions/operator-prompt.md` (69, 99),
  `core-token.md` (103, 111)

## Where the doc goes

A new decision recording the card, in `decisions/operator-prompt.md` (8,884 B at
filing) or a new topic file beside it; `spec.md` for the card. If your work
pushes any file into reserve, file `tasks/ui/<NNN>-compact-ui.md` in the same
commit per `tasks/README.md`.

## Done when

- [ ] Against a fake Core, a driven test confirms one input and the fake
      receives the person token and the nonce.
- [ ] A test name holding markup is shown as text.
- [ ] A refused confirmation shows Core's reason.
- [ ] A decision records the card.
- [ ] Gate green.

## Blocked

The card needs `GET /confirmations/pending`, `GET /confirmations/{hash}/card` and `POST /confirmations` from the UI, with the person token. `embarch-core-client` (embarch-api) has no method for any of them: it has `post_definition`, `definition` and `suites` only. `CoreClient::base_url` and `dispatch` are `pub(crate)`, and the client's own test `every_outbound_request_is_sent_through_the_one_funnel` forbids a second send site, so the UI cannot make the calls itself without bypassing Core's attestation of the token. The client is a second repo, which this task may not touch, and no embarch-api branch holds the methods (checked 2026-11-25).

Filed for embarch-api as a gap (title "core client has no methods for the confirmation routes"); the desk was down (Linear's free issue limit), so `fleet-linear.py` spooled it at `.fleet/linear-spool/20261125-094432-2081508-core-client-has-no-methods-for-the-confirmation-ro.json` for the next leg. Nothing was written in embarch-ui.

Design left for whoever builds this once the methods exist: `/api/confirmations` (list, each item joined with its card) and `POST /api/confirmations` relaying `{hash, nonce, surface: "ui"}` with Core's `403/409` text passed on as `api_live_prompt` does; a card in `assets/` that renders every agent string with `textContent`.
