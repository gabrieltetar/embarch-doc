# 195 — The client sends Core's token only after a challenge

**State:** done — decision 133: token sent only after a verified challenge, picked by core-fingerprint
**Source:** EMB-333 — embarch-api sends Core's token to whatever answers on the port
**Issue:** EMB-333
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-core-client` resolves a token from config, the environment or the
machine-wide file (`token_discovery.rs`) and sends it on every request.
`embarch-api core-key` checks a challenge's signature and prints the
fingerprint (`src/core_key.rs`), but nothing compares it with a recorded one
and no code reads a `core-fingerprint` file. When this is done:

- On first use per process, and after a reconnect, the client sends a fresh
  nonce to `POST /auth/challenge` and checks the frame and signature
  (`core_key::check` moves into the crate).
- **`core-fingerprint` present** beside the token file (the same discovery, the
  WSL2 path included): a match gets the machine-wide token; no match gets the
  development token from the development store (`%LOCALAPPDATA%\embarch\dev\`
  through WSL2, `~/.local/state/embarch/dev` on Linux) if present, else nothing,
  with an error naming both fingerprints. The owner may strike these paths:
  they match Core's development store.
- **`core-fingerprint` absent**: today's behaviour, since no Core on the machine
  is attested.
- An explicit token in config still wins, but is sent only after the challenge.
- `status` (tool and CLI) prints the mode, the fingerprint and whether it
  matches the installed one.

**`embarch-ui` links this crate and is not yours.** Keep every public item it
uses source-compatible: add, do not change a signature. If the design cannot be
done without breaking a public item, stop and say so in this file; that would
make it a cross-repo pass. The supervisor builds `embarch-ui` against your
branch before landing.

## Why now

The attested Core's first rule: a development Core left running, or one the
agent started, must not receive the service's tokens. `deploy-core`'s
development Core (EMB-341) and the UI's display of which Core answers (EMB-336)
wait on it. Design: `embarch-doc/notes/hil/12-prevention.md`, "The root of
trust"; `notes/hil/14-implementation-plan.md`.

## Where the doc goes

Amend decision 109 (`decisions/client-crate.md`) or add a new decision beside
it; `interfaces/` for the `status` fields. `embarch-token.md` is suite-level and
not yours: drop a `status.d/` fragment naming what it now gets wrong.
**Decisions near their per-decision limit (`check-doc-size.py --pressure`):**
`lease.md` 90 (over), `ledger.md` 98 (15 B left), `bench-exchange.md` 89
(122 B), `failure-reporting.md` 67 (192 B); do not grow them. If your work
pushes a file into reserve, file `tasks/api/<NNN>-compact-api.md` in the same
commit per `tasks/README.md`.

## Done when

- [x] Against a fake Core: a match sends the machine-wide token; a mismatch
      sends the development token from a temp store; a mismatch with no
      development store sends no `Authorization` header at all and errors.
- [x] No `core-fingerprint` file: the same token as today.
- [x] A challenge answer with a bad signature or a foreign frame sends nothing.
- [x] `status` shows mode, fingerprint and match.
- [x] Decision 109 amended or a new decision; a `status.d/` fragment for
      `embarch-token.md`.

## Outcome

Decision 133 (`embarch-api/decisions/client-crate-funnel.md`). `dispatch_with` takes its token from `CoreClient::attested()`: with a `core-fingerprint` beside the token file, one challenge per connection (cached, cleared on a connect failure), then machine-wide token on a match, development token (or no header and an error naming both fingerprints) on a mismatch, nothing on a bad challenge. No fingerprint file: today's behaviour with no challenge, an explicit config token included (chosen so the suite's fake Cores need no signing route); with the file, an explicit token still wins but waits for a good challenge. `core_key::check` moved to `embarch_core_client::attest`; `status` (tool and CLI) carries `attestation`. Added public items only: `attest::*`, `CoreClient::{attestation, new_with_stores}`, `CoreConfig::token_is_explicit`. **Hardware/live-Core debt:** the development-store paths and the WSL2 `%LOCALAPPDATA%` shell-out were never run against a real Core; tests use temp stores and a signing mock. Existing integration tests that use real discovery would start challenging if a `core-fingerprint` is installed on the test machine.
