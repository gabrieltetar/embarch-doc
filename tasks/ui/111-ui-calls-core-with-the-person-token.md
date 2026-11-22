# 111 — embarch-ui calls Core with the person token

**State:** claimed by agent/ui/111-ui-calls-core-with-the-person-token, 2026-11-21 17:12 — unparked by `api/162`'s fold.
**Source:** Fleet Ready issue: Core has one full-authority token, and HIL needs an agent scope and a person scope ("embarch-api and embarch-ui read the pair"). `notes/hil/14-implementation-plan.md`, unit M1.4; `notes/hil/12-prevention.md` ("the UI holds the person's token").
**Issue:** EMB-219
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

embarch-ui is the person's surface, so every request it makes to Core carries the person token, resolved through `embarch-core-client` as `tasks/api/162` left it. If the person token cannot be resolved, the UI says so where it reports Core being unreachable today, rather than falling back to the agent's token silently.

## Why now

M1.8 attributes notes and prose adoptions by the token's scope, and the card those acts are made on is the UI's.

## Dispatch notes

- Read `api/162`'s decision and `core/128`'s before writing: the resolution and the file are theirs. `api/162` landed as `embarch-api` decision 109: `CoreClient::new_with_scope(config, TokenScope::Person)`, with `CoreConfig::person_token` / `person_token_env`, and a person client with no person token is an error naming its sources, never the agent's token.
- Whether the UI falls back to the agent token when the person's is missing is a design choice with a trust cost (a fallback makes every UI act read as the agent's). Decide it in a `embarch-ui` decision and say the cost.
- No `embarch-ui` doc is in reserve. Decisions near their size limit: `trace-view` #10 (0 B), `gatt-capture` #17 (4 B), `trace-chart` #10 (14 B), `launcher` #28 (22 B), `tab-folders` #100 (113 B); put the new decision where none of those grows.
- Out of scope: any card or person's act itself (later units).

## Done when

- [x] The UI's Core client is built with the person token, and a test or a type says so.
- [x] A missing person token is reported as the decision says.
- [x] `spec.md`, `decisions.md` updated; `changelog.d/` fragment dropped.
- [x] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope ui` on both branches).

## Outcome

Decision 103 (`embarch-ui/decisions/core-token.md`): `config::core_client` builds the one `CoreClient` with `TokenScope::Person`; no agent fallback. **Deviation from the What, on purpose:** a missing person token stops the UI at start (error naming the sources) instead of a banner where "Core unreachable" shows, because every handler holds one `CoreClient` and none can be built without a token; reasons in the decision. If the owner wants the banner, that is a follow-up (an `Option<CoreClient>` through the handlers).

**Verification debt:** not run against the installed `embarch-ui.service` or a real Core with a person token; the missing-token test is conditional (a machine with a `person-token` file passes without erroring).
