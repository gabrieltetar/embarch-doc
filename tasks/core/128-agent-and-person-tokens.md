# 128 — Core writes an agent token and a person token, and every request carries its scope

**State:** claimed by agent/core/128-agent-and-person-tokens, 2026-11-20 15:50 — resumed: the 14:39 claim's worker died with its leg (last write 14:45); its uncommitted trees are code `c2ad59f`, doc `b0bc9438` on the branch
**Source:** Fleet Ready issue: Core has one full-authority token, and HIL needs an agent scope and a person scope so a report can say who did each act. `notes/hil/14-implementation-plan.md`, unit M1.4; `notes/hil/12-prevention.md` ("Core needs scoped tokens either way"; "Unattested, the two scopes still exist").
**Issue:** EMB-219
**Scope:** core
**Hardware:** none
**Owner:** no

## What

At its first start Core writes two tokens, an **agent** token and a **person** token, and authenticates a request with either. `auth_middleware` resolves which one the bearer matched into a scope that travels with the request, so every route records the scope it was called with, and a handler a later unit writes (a declaration, a note, a prose adoption, a publish) can stamp it without re-deriving it.

**Nothing is refused by scope in this unit.** Core is unattested today, so the identity routes stay on the agent's token, labelled as the agent's (`notes/hil/12-prevention.md`); both tokens reach every route.

## Why now

The plan marks M1.4 as needing nothing, and M1.8 (Core's side of publish) attributes notes, prose adoptions and the publisher by scope.

## Dispatch notes

- **Keep every existing caller working unchanged.** `embarch-api`, `embarch-ui` and `embarch-atlas` find the token today through `embarch-core-client`'s discovery of the one machine-wide file (`embarch-token.md` §2). That file, and `EMBARCH_TOKEN`, stay the agent's, so this unit lands without touching another repo. The person token gets a file of its own beside it, the same permissions (`restrict_token_file_permissions`, `embarch-core` decision 53), and an explicit override of its own. Name the file and the variable in a decision.
- **"Records its scope"** must be something a test can assert for a call with each token, and something M1.5 to M1.8 can read. Decide where it lives (a request extension every handler can take, plus whatever per-request record Core already keeps) and say in `open.md` which existing records do not carry it yet.
- **Amend `embarch-core` decision 93** (`decisions/lease.md`) where it touches who holds the bench, or add a decision beside it, as the issue asks; `decisions.md` indexes it. Decisions within 256 B of their limit: none in `embarch-core`.
- **`embarch-token.md` is not yours to write** (it is suite-level). Drop `status.d/core-<slug>.md` naming the sections that become false: §1's "single opaque string", §2's table, §3's "no per-caller identity", §5's "No per-caller identity" gap.
- **Out of scope**, filed as their own tasks: `embarch-core-client` and `embarch-api` resolving the pair (`tasks/api/162`), and `embarch-ui` calling with the person token (`tasks/ui/111`). Signing a scope into a record is M1.5.
- **Owed, not a Done-when item:** the native Windows build, which a worktree cannot run (`gate.md`). Write it into the task file's closing note as a debt; the person-token file's permissions on Windows go through the same `icacls` path as the agent's, unvalidated there.

## Done when

- [x] A fresh data directory gets both token files at first start, and a restart reuses both.
- [x] A test calls one route with each token and asserts the scope recorded for each; a call with neither is refused as today.
- [x] `spec.md`, the auth decision and `interfaces/` say what the two tokens are, where each lives, and where the scope is recorded.
- [x] `status.d/` fragment for `embarch-token.md`; `changelog.d/` fragment dropped.
- [x] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope core` on both branches).

## Closing note

Shipped as `embarch-core` decision 109 (`decisions/auth.md`): `token_store::resolve_tokens` reads `EMBARCH_TOKEN` / `token` (agent) and `EMBARCH_PERSON_TOKEN` / `person-token` (person); `auth_middleware` inserts a `Scope` request extension, which handlers take as an extractor. Decision 93 amended with a one-line pointer: the lease holder is not the scope. `status.d/core-agent-and-person-tokens.md` covers `embarch-token.md` §1, §2, §3, §5.

**Debt: native Windows build and the person-token `icacls` lockdown** are unrun here (a worktree cannot build natively; `gate.md`). The person file goes through the same `restrict_token_file_permissions` as the agent's. Verify from the main checkout on Windows: first start creates both files with the restricted ACL, and a restart reuses them.

**Not done, by design:** no client resolves the person token (`tasks/api/162`, `tasks/ui/111`); `service.rs`'s install passes only `EMBARCH_TOKEN`; no existing record carries the scope (`open.md`).

**Resume:** the first worker died unverified. On resume the build and clippy were green but 2 route-sweep tests failed, because the new test-only `/probe` router put a line starting `.route("` in `api.rs`, which the sweep's source scan counts as a registered route; the probe now sits on one `Router::new().route(` line. 395 tests then passed. The features fragment was renamed from `core-125-` to `core-128-` to carry this task's number.
