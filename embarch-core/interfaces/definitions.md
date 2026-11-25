# embarch-core: the definitions and confirmation routes

**Status:** active, 2026-11-25 (`tasks/core/157`, [decision 133](../decisions/definitions.md)). Index: [../interfaces.md](../interfaces.md).

All six take a token and are lease-open (files and the run log, never a port). Errors are plain text. Hashes are 64 lowercase hex characters, the `definition_hash` of `embarch-study-designer`'s `hil_test`.

| Method | Path | Token | Body | Response |
|---|---|---|---|---|
| `POST` | `/definitions` | either | `{kind, definition, study?, bench?, measured?}`; `kind` is `test`, `suite`, `plan`, `bench`, `capability` or `hook`. `study` (a host study) and `bench` (a suite bench) go together and run `hil_check::check_test` on a test, with `measured` `{<measurement>: {by: bench\|dut\|person, source, range_min, range_max, resolution, u}}`; without them a test gets the shape check | `201` new, `200` already kept: `{hash, kind, kept, checked: "shape"\|"definition", confirmation}`; `422` the crate's reason, one refusal per line (nothing kept), or a body that is not a definition; `400` `study` without `bench` |
| `GET` | `/definitions/{hash}` | either | none | `200 {hash, kind, definition, confirmation}`; `404` |
| `GET` | `/suites` | either | none | `200 {configured, suites: [{id, version, manifest_sha256, tests: [{test_id, sha256}], problems}], problems}` from `EMBARCH_SUITES_DIR`, read now |
| `GET` | `/confirmations/pending` | either | none | `200 {pending: [{hash, kind, name}]}`: kept definitions that are neither premade, held nor confirmed; no card data, no nonce |
| `GET` | `/confirmations/{hash}/card` | **person, on every Core** | none | `200 {card: {hash, kind, definition, diff?}, confirmation, nonce, expires_utc_ms}`; `nonce` is null unless the definition waits; `diff` is a copy's `derived_diff` against the premade test its `derived_from` names; `403` the agent's token; `404` |
| `POST` | `/confirmations` | **person, on every Core** | `{hash, nonce, surface?}` | `201` the `confirmed` `{entry, hash}`; `403` the agent's token, or a nonce that is unknown, used, expired or for another card (the attempt spends it); `409` the definition needs none; `404`; `400` malformed hash |

`confirmation` is `premade` (identical to a test of a suite Core reads; needs none), `held` (a suite manifest Core reads), `not_required` (a bench or a plan: the go's), `confirmed`, `confirmed_with_suite` (listed by a confirmed suite manifest Core does not hold) or `unconfirmed`. A nonce is 32 random bytes in hex, single use, ten minutes, in memory. The agent's `403` names embarch-ui and the CLI under `EMBARCH_PERSON_TOKEN`; it is refused by `person_middleware` before any handler, as `token_store::CONFIRMATION_ROUTES`, whatever the Core's mode (decision 133, against decision 132's service-only `PERSON_ROUTES`).

A kept definition is `definitions/<hash>.json` in the store: `{"kind": ..., "definition": ...}`. The suites checkout is any folder holding `suite.json` files up to three folders down (a test's `file` is relative to its `suite.json`, a path inside it); a test counts only when its file hashes to the manifest's line.

The run log's `confirmed` entry is in [run-log.md](run-log.md).
