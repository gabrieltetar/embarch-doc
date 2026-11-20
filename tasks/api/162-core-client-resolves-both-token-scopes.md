# 162 — `embarch-core-client` resolves the agent and the person token, and embarch-api's MCP server sends only the agent's

**State:** open
**Source:** Fleet Ready issue: Core has one full-authority token, and HIL needs an agent scope and a person scope ("embarch-api and embarch-ui read the pair"). `notes/hil/14-implementation-plan.md`, unit M1.4; `notes/hil/12-prevention.md` ("the agent ... holding the repo, embarch-api and an agent-scoped Core token only").
**Issue:** EMB-219
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-core-client`'s token discovery (`crates/embarch-core-client/src/token_discovery.rs`) resolves a token **by scope**: the agent's as it does today, and the person's from its own explicit config, environment variable or file, as `tasks/core/128` defined them, including the WSL2-to-Windows path mapping. `embarch-api`'s MCP server always sends the agent's token. Whether any `embarch-api` CLI verb sends the person's, and how a caller asks for it, is this unit's decision; the MCP surface never does.

## Why now

Core accepts both tokens once `core/128` lands, and `tasks/ui/111` (the UI calling with the person token) waits on this crate resolving it.

## Dispatch notes

- **`embarch-core-client` is a shared crate**: `embarch-ui` and `embarch-umbrella` path-depend on it. Keep today's resolution of the agent token byte-for-byte compatible, so neither consumer changes until it asks for the person's.
- Read `core/128`'s decision and `embarch-token.md` as that unit's fold left them; do not re-decide the file name or the variable.
- Out of scope: the UI's use of the person token (`ui/111`), and any route refusing a scope (none does on an unattested Core).

## Done when

- [ ] A unit test resolves each scope from each source (explicit, environment, file), and the agent's resolution is unchanged.
- [ ] The MCP server's client is built with the agent's token, and a test or a type says so.
- [ ] `spec.md`, `decisions.md` and `interfaces/` updated; `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope api` on both branches; `embarch-ui` and `embarch-umbrella` still build against the crate).
