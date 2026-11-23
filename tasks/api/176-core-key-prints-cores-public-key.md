# 176 — `core-key` prints the public key of the Core it reaches, checked against the challenge

**State:** claimed by agent/api/176-core-key-prints-cores-public-key, 2026-11-23 15:41
**Source:** Fleet Ready issue, found while writing the HIL guide's Study section
**Issue:** EMB-247
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Verifying a published zip takes Core's public key
(`embarch-api verify <zip> --public-key <hex>`), and nothing in EmbArch prints
it. Core serves the key only inside `POST /auth/challenge`'s answer (Core
decision 110, `embarch-doc/embarch-core/interfaces/signing.md`), which needs a
caller-chosen nonce, so `suite/hil-guide.md`'s Study step 6 tells the reader to
`curl` that route with a fixed nonce and read `public_key` out of the JSON.

When this is done, `embarch-api core-key [--json]` runs the challenge against
the Core that `status` reaches, with a **fresh random nonce**, **checks Core's
signature over the challenge's fixed frame** before it trusts anything in the
answer, and prints the raw public key (64 hex characters, the form `verify
--public-key` takes) and its SHA-256 fingerprint. A signature that does not
check, or an unreachable Core, prints why and exits non-zero. `--json` prints
the same two values as fields.

## Why now

The HIL guide (EMB-228, landed 2026-11-23) routes every Study's verify step
through a hand-written `curl` with a fixed nonce, which checks nothing about the
answer. A command is shorter and actually proves the key signed a nonce it chose.

## Constraints

- **The key stays out of band.** `core-key` prints; it does not write the key
  into any config, and `verify` does not learn to read it from one. `verify`
  stays a command that needs no config and no Core.
- Read the frame from `embarch-core/interfaces/signing.md` and Core decision
  110; do not derive it from Core's source alone. `src/verify.rs` already holds
  Ed25519 verification and the key-fingerprint convention: reuse them, do not
  add a second definition of the fingerprint.
- CLI only. An MCP tool for this is out of scope.
- **The guide.** Change Study step 6 in the pinned copy,
  `embarch-api/guide/hil-guide.md`, to name `embarch-api core-key` in place of
  the `curl`, and change nothing else in the file. You may not write
  `embarch-doc/suite/hil-guide.md`: drop a `status.d/` fragment targeting it that
  says "copy `embarch-api`'s `guide/hil-guide.md` over it", and the supervisor
  folds it so the two match again.
- **The drift guard is red in your tree by construction.** Run `cargo test` with
  `EMBARCH_DOC_DIR=<your embarch-doc worktree>`, so
  `the_pinned_copy_matches_the_suite_guide_where_one_is_reachable` reads the
  suite guide at your branch's base rather than the owner's checkout. After your
  guide edit that one test fails, because you cannot write the suite copy. Report
  it as the one expected red, with its message; every other test must be green.
  `tests/ble_gatt_rate_fixture.rs` also reads the guide: it must stay green.
- If you add the challenge call to `crates/embarch-core-client`, that is a shared
  crate: say so in your report, and keep the change to that one call.

## Where

- `src/main.rs` (the `Commands` enum, beside `Verify`), `src/cli.rs`.
- `src/verify.rs` for the key and fingerprint helpers.
- `embarch-doc/embarch-core/interfaces/signing.md` for the challenge's request,
  answer and signed frame.
- `guide/hil-guide.md`, Study, "6. Verify it in a clean folder".

## Dispatch note

No `embarch-api` doc file is in size reserve. Per-decision caps close to their
limit in this scope: `ledger` #98 (15 B), `bench-exchange` #89 (122 B),
`failure-reporting` #67 (192 B). If `core-key` needs a decision, file a new one
rather than growing any of those.

## Done when

- [ ] `embarch-api core-key` prints Core's public key and its SHA-256
      fingerprint after checking the challenge's signature over a fresh nonce,
      and exits non-zero, saying why, when the signature does not check.
- [ ] A test covers a good answer and a bad signature without a live Core.
- [ ] The pinned guide's Study step 6 names `core-key` instead of the `curl`;
      `status.d/` fragment for `suite/hil-guide.md`.
- [ ] Gate green (`../../embarch-fleet/gate.md`), bar the drift guard above.
- [ ] `spec.md`/`decisions.md`/`interfaces/` updated where they list the CLI,
      `changelog.d/` fragment dropped.
