# 129 — Core signs each study run's record with an Ed25519 key, as a DSSE envelope over an in-toto Statement

**State:** done on agent/core/129-sign-study-run-records, 2026-11-21
**Source:** Fleet Ready issue: Core does not sign study run records, so a published zip cannot be checked without trusting the agent. `notes/hil/14-implementation-plan.md`, unit M1.5 (after M1.1, landed as `tasks/study-designer/084`); `notes/hil/12-prevention.md`, "What Core then guarantees, in code", item 1, and "The root of trust: Core, under its own account" for the key and the challenge.
**Issue:** EMB-220
**Scope:** core
**Hardware:** none
**Owner:** no

## What

- **An Ed25519 signing key in Core's store**, generated at first start, under the engineer's account in milestone 1 (an unattested Core: no elevated install, no service account), kept beside the token files with its path per OS as `embarch-token.md` gives the token's.
- **A DSSE envelope over an in-toto Statement per study run**, written when the study ends. Its subjects are the SHA-256 of each capture, `events.json`, `measurements.json` and the study file as Core kept it by hash. Its predicate **keeps what Core observed apart from what it was told**: the build's commit, dirty state and toolchain come from embarch-api and are carried as claims; Core's own observations (identities, image status, the scopes that made each declaration, the shared crate's behaviour versions) are not.
- **The challenge route signs only a fixed frame**: the text `embarch-core-auth-v1`, a nonce of Core's own and the caller's nonce. No route signs bytes a caller supplies.

## Why now

M1.6 (the hash-chained run log, which holds each Statement's hash) follows this, and publish and `verify` rest on it.

## Dispatch notes

- **`measurements.json` does not exist yet**: Core starts writing it in M1.7. Sign whatever files a study run has when it ends, and make the subject list come from the files present, so M1.7 adds a subject without changing this unit's code; a test can supply a fixture `measurements.json`.
- **Write against `embarch-study-designer/interfaces/hil-shapes.md`'s conventions** (SHA-256 as 64 lowercase hex, JCS-canonical JSON Core writes, `*_utc_ms` times) and Core decision 109 (`core/128`: the two token scopes and the `Scope` request extension, which is where a predicate's scopes come from).
- Library choice (`ed25519-dalek` is the notes' unverified suggestion) and the predicate type URI are this unit's decision; record both. Use a standard DSSE envelope (`payloadType`, `payload`, `signatures[{keyid, sig}]`) so a third-party DSSE verifier checks it.
- **Decisions near their size limit**: `lease` #93 (182 B left). A new signing topic file is the expected home.
- **Native Windows build**: a worktree cannot build it; leave a hardware-free debt note saying how to check the key file's path and ACL on Windows from the main checkout, as `core/128` did.
- Out of scope: the run log (M1.6), `measurements.json` itself (M1.7), signing the publish manifest (M1.8), an attested install and the fingerprint file.

## Done when

- [x] A study run's record verifies with a standard DSSE check in a test, and fails it when a subject's bytes change.
- [x] The challenge route signs only its frame, and a test shows a caller-chosen payload cannot be signed through it.
- [x] `spec.md`, `decisions/`, `interfaces/` updated; `changelog.d/` fragment dropped; a `status.d/` fragment for `embarch-token.md` if the key file sits beside the tokens.
- [x] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope core` on both branches).

## Done

Decision 110 (`embarch-core/decisions/signing.md`), `interfaces/signing.md`, `src/signing.rs`. Library `ed25519-dalek` 2; predicate type the URN `urn:embarch:predicate:study-run:v1`.

- **Decided beyond the task text:** the challenge route is `POST /auth/challenge` and takes **no token** (the notes' check happens before any token is sent), so it sits in `signing.rs` outside the swept `build_router` lines and the sweep's "every route requires the token" claim now has one stated exception. A device study now keeps its `Study` as `study.json` (the name host studies use) so it can be a subject. Build claims arrive as query parameters on both study routes (`build_commit`, `build_dirty`, `build_toolchain`); embarch-api does not send them yet (a follow-up in `embarch-api`).
- **Declaration scopes** are an in-memory ledger stamped by the five declaration routes; the predicate says from when it has been watching (`witnessed_since_utc_ms`). Persisting it is M1.6's.

## Debts

- **Windows (native build, not run; a worktree cannot build it):** from the main checkout in a Windows session, start Core, then `icacls %ProgramData%\embarch\signing-key` should list only the running account, `SYSTEM` and `Administrators`; a second start reuses the key (same `keyid` in `core.log`). Also `cargo build` there for the `windows`-only `pub(crate) restrict_token_file_permissions` call from `signing.rs`.
- No third-party DSSE tool (e.g. a Go or Python verifier) was run against an envelope; the tests' independent check follows the DSSE v1 text.
- Follow-ups for others: `embarch-api` sending the `build_*` parameters and calling the challenge before sending a token; `embarch-core-client` for both.
