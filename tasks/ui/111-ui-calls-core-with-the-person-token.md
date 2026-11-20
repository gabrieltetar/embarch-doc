# 111 — embarch-ui calls Core with the person token

**State:** blocked — waits on `embarch-core-client` resolving the person token.
**Unparks when:** tasks/api/162 lands.
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

- Read `api/162`'s decision and `core/128`'s before writing: the resolution and the file are theirs.
- Whether the UI falls back to the agent token when the person's is missing is a design choice with a trust cost (a fallback makes every UI act read as the agent's). Decide it in a `embarch-ui` decision and say the cost.
- Out of scope: any card or person's act itself (later units).

## Done when

- [ ] The UI's Core client is built with the person token, and a test or a type says so.
- [ ] A missing person token is reported as the decision says.
- [ ] `spec.md`, `decisions.md` updated; `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope ui` on both branches).
