# 199 — The core client calls the confirmation routes

**State:** done — three CoreClient methods, mocked and in the funnel sweep; gate green
**Source:** `ui/121`'s worker, blocked: the UI's confirmation card (EMB-383) needs client methods for Core's confirmation routes
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`crates/embarch-core-client/src/client.rs` has `post_definition`, `definition`
and `suites`, and nothing for Core's other three confirmation routes
(`embarch-core/src/confirmations.rs`): `GET /confirmations/pending`,
`GET /confirmations/{hash}/card` and `POST /confirmations`. `CoreClient::base_url`
and `dispatch` are `pub(crate)`, and the test
`every_outbound_request_is_sent_through_the_one_funnel` forbids a second send
site, so `embarch-ui` cannot make the calls itself, and `ui/121` (the
engineer's confirmation card) stopped on it. When this is done, three methods
sit beside `post_definition`, reusing `status_timeout` and `dispatch`:

- `pending_confirmations()` for `GET /confirmations/pending`, answering
  `{pending: [{hash, kind, name}]}`;
- `confirmation_card(hash)` for `GET /confirmations/{hash}/card`, answering
  `{card, confirmation, nonce, expires_utc_ms}`; Core refuses the agent's token
  `403`;
- `confirm(hash, nonce, surface)` for `POST /confirmations` with body
  `{hash, nonce, surface}`; a refusal (`403` for a nonce unknown, spent, expired
  or for another card; `409` for a definition needing no confirmation; `404`)
  comes back as `embarch-core returned {status}: {body}`, as `post_definition`
  does.

Typed answers or `serde_json::Value` are the worker's choice; say which in the
interface doc. No MCP tool or CLI subcommand: a confirmation is the person's
act, made in the UI or the person's own terminal, never relayed by the agent
(`notes/hil/12-prevention.md`, item 4).

## Where to look

- `crates/embarch-core-client/src/client.rs` — `post_definition`, the pattern
- `tests/core_client_http.rs` — the every-call-carries-the-bearer-token sweep
- `embarch-core/src/confirmations.rs` and
  `embarch-doc/embarch-core/interfaces/` for the routes' shapes

## Where the doc goes

The client crate's interface doc. **Do not grow decisions 90 (`lease.md`), 98
(`ledger.md`) or 134 (`test-plans.md`)**, each at or over its per-decision
limit. If your work pushes any file into reserve, file
`tasks/api/<NNN>-compact-api.md` in the same commit per `tasks/README.md`.

## Done when

- [x] The three methods exist on `CoreClient`, each with a mocked test that
      asserts the bearer header, and each in the funnel sweep.
- [x] A refused `confirm` returns Core's text.
- [x] Gate green, the client crate included.
