# 110 — `embarch install-core` verifies a signed release before it installs

**State:** open
**Source:** EMB-338 — no install verifies a signed release before installing Core
**Issue:** EMB-338
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`src/verify_release.rs` is built (EMB-192) and its comment says the checked
elevated install can call `verify_release`. `setup` copies the binaries per
user and installs the service by running that copy's `install` (`install.rs`,
decision 28; `setup.rs`). There is no staging folder, no downgrade rule and no
record of what was installed. The release proposal
(`embarch-doc/embarch-release-signing-proposal.md`, "The design in one
screen" and "Order" step 4) copies the archive into a staging folder only the
elevated step can write, checks it there, records the manifest hash and the
verified identity, and refuses an older suite version unless
`--allow-downgrade`, which is recorded. When this is done:

- `embarch install-core <release dir or archive> [--allow-downgrade]
  [--dry-run]` builds a plan, then runs an elevated half.
- The elevated half copies the release into
  `<data dir>/release-staging/<n>/`, a folder it creates for Administrators or
  root alone (apart from the engineer-writable firmware `staging/`), runs
  `verify_release` there, compares the suite version with
  `installed-release.json`, refuses an older one unless `--allow-downgrade`,
  and writes `installed-release.json`: suite version, manifest SHA-256,
  identity, issuer, log time, each binary's SHA-256, whether a downgrade was
  allowed, and the time.
- A failed check writes nothing and installs nothing.
- The elevated half is a function taking its folders, so tests run it as an
  ordinary user in temp dirs; the verifier is a seam (a trait or a function
  parameter), so tests need no real signature.
- The OS steps after the record (registering the service under its own
  account) are later units, not this one. Name them in the decision.

Where: `src/verify_release.rs` (`verify_release`, `Verified`), `src/setup.rs`,
`src/install.rs`, `src/main.rs`.

## Why now

EMB-338, unit A.19 of the HIL attested phase
(`embarch-doc/notes/hil/14-implementation-plan.md`, "The Test and attested
phases"). The Windows and Linux elevated steps and Core's
`install --service` run after it. The command's name is the plan's
recommendation; the owner may strike it later.

**A new numbered decision is yours to write**, in `decisions/install.md`
(10,468 B, decisions 14 and 28 there) or a new topic file if that one would
cross its cap. Add `interfaces/install-core.md` with the record's shape, and
update `spec.md` (its command table now lives in `spec/commands.md`).
Decision files within 200 B of their limit: `prune-policy` (26), `deploy`
(32), `mirrors` (20), `budgets` (44); leave them alone.

No file is in reserve on the size ledger at dispatch.

## Done when

- [ ] With a fake verifier, a passing release writes the record with every
      field; a failing one writes nothing.
- [ ] An older suite version is refused; with `--allow-downgrade` it is
      written and the record says so.
- [ ] `--dry-run` prints the plan and touches nothing.
- [ ] Windows-gated code, if any, type-checks with
      `cargo check --target x86_64-pc-windows-msvc`
      (`embarch-dev-workflow.md` §4).
- [ ] A new decision; `interfaces/install-core.md` gives the record's shape.
- [ ] Gate green; `changelog.d/` fragment dropped; `status.d/` fragment for
      anything suite-level it made false.
