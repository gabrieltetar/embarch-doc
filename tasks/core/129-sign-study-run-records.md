# 129 — Core signs each study run's record with an Ed25519 key, as a DSSE envelope over an in-toto Statement

**State:** open
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

- [ ] A study run's record verifies with a standard DSSE check in a test, and fails it when a subject's bytes change.
- [ ] The challenge route signs only its frame, and a test shows a caller-chosen payload cannot be signed through it.
- [ ] `spec.md`, `decisions/`, `interfaces/` updated; `changelog.d/` fragment dropped; a `status.d/` fragment for `embarch-token.md` if the key file sits beside the tokens.
- [ ] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope core` on both branches).
