# 097 — `embarch verify-release`: check a suite release offline before installing it

**State:** done on agent/umbrella/097-embarch-verify-release, 2026-11-17 (awaiting landing)
**Source:** EMB-192, filed by the owner: step 3 of `embarch-doc/embarch-release-signing-proposal.md`, whose spike passed on 2026-11-16
**Issue:** EMB-192
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

One command answers "is this unpacked suite release exactly what EmbArch's
release workflow signed?", with no network. Today `embarch setup` copies the
binaries from the running `embarch`'s own directory with no check at all
(`src/setup.rs`), and the suite manifest holds tags only.

**Read first:** the proposal's "The design in one screen", "Order" step 3 and
"Checked (2026-11-16)", then EMB-192 if you can reach it. The design is the
owner's; this unit implements it and does not reopen it.

**The verb.** `embarch verify-release [DIR]`, `DIR` defaulting to the running
`embarch` binary's own directory as `setup` does, holding
`embarch-manifest.json`, `embarch-manifest.json.sigstore.json` and the files the
manifest lists. A `VerifyRelease { dir, trusted_root, refresh_trust_root }`
variant in `src/main.rs`'s `Command`, the code in a new
`src/verify_release.rs`, the check exposed as a crate-public function that
returns a result type rather than printing, so step 4 (the checked elevated
install) can call it.

**The checks, in order:**

1. Verify `embarch-manifest.json` against its bundle with the
   `sigstore-verify` crate (`Verifier::new(&root)`, `Verifier::verify`), under
   `VerificationPolicy::new(identity, issuer)`: issuer
   `https://token.actions.githubusercontent.com`; identity built from the
   manifest's own `suite_version`, exactly
   `https://github.com/gabrieltetar/embarch-umbrella/.github/workflows/assemble-suite.yml@refs/tags/suite-v<suite_version>`.
   Never a regular expression, never `VerificationPolicy::any_identity()`.
2. Every file in the manifest's `files` object (relative path to SHA-256)
   exists in the folder with that hash. A listed file missing, or one whose hash
   differs, fails. `sha2` is already a dependency.
3. The trust root is `TrustedRoot::from_embedded(SigstoreInstance::PublicGood)`
   by default, and **verification never fetches anything**. A bundle whose log
   key is not in the embedded root fails with an error that says so and names
   `--refresh-trust-root`, which fetches the root through TUF
   (`TrustedRoot::from_tuf(TufConfig::production())`) for that one run and
   **never caches it**. `--trusted-root <file>` takes an explicit root. The
   output says which root was used.

**Output:** the suite version, each component's tag and commit, the verified
certificate identity and the log entry's time; exit 0 only when everything
checked, and any failure names what failed.

**Dependencies, pinned exactly:** `sigstore-verify = "=0.16.0"`,
`sigstore-types = "=0.16.0"`, `sigstore-trust-root = { version = "=0.16.0",
default-features = false, features = ["aws-lc-rs"] }`, plus its `tuf` and
`rustls` features for the refresh path. They add `aws-lc-sys`, a C and `cmake`
build (`cmake` is installed here). Only `--refresh-trust-root` code may reach
the network.

**Tests**, with public fixtures verified by digest so no large binary is
committed (`Verifier::verify` takes a `Sha256Hash`):

- cosign v3.1.4's `cosign-linux-amd64.sigstore.json`
  (`gh release download v3.1.4 -R sigstore/cosign -p cosign-linux-amd64.sigstore.json`),
  artifact SHA-256 `424e2c97d0b45fd7a6b608a87f090f35633f4c23ece5f092d48bba11aaf4bbfa`,
  identity `keyless@projectsigstore.iam.gserviceaccount.com`, issuer
  `https://accounts.google.com`;
- uv 0.13.8's build attestation for `uv-x86_64-unknown-linux-gnu.tar.gz`
  (`gh attestation download <file> -R astral-sh/uv`, the bundle whose
  certificate is issued by `sigstore-intermediate`), artifact SHA-256
  `5acfd9177cfecf0bf87578f059728215ccc884388988f55f7a65041b57387d91`, identity
  `https://github.com/astral-sh/uv/.github/workflows/release.yml@refs/heads/main`,
  issuer `https://token.actions.githubusercontent.com`;
- each fixture also fails with a wrong identity, a wrong issuer and a wrong
  digest;
- the file-hash check on a synthetic manifest through the internal function,
  since no signed suite manifest exists until EMB-190 ships and the owner tags a
  release.

Fetching the two fixtures once with `gh` is part of this task. `cargo test`
itself must pass with no network.

**CI:** a `build-check.yml` workflow in this repo, on pushes to any branch,
building the four release targets the way `release.yml` does without uploading
anything, so the `aws-lc-sys` build is checked on the aarch64 cross leg.
Pushing your branch triggers it; report its result if it has finished when you
are done, and say so if it has not. **Cut no release and push no tag.**

**Docs.** Record the verb in `embarch-umbrella`'s `spec.md` and its
interfaces, citing the proposal and EMB-192. Drop a `status.d/` fragment naming
`embarch-release-signing-proposal.md` and saying step 3 now lives in
`embarch-umbrella`'s docs, so the supervisor can fold that step out of the
proposal (its own "Fold" rule). You do not edit the proposal.

**No new numbered decision, and no edit to an existing one** (burndown). If
you find one owed — decision 28's "copies with no check" is the likely
candidate — file it with `scripts/fleet-linear.py file --from decision` and
name it in this file. Several of `embarch-umbrella`'s decision topic files are
within 256 B of their limit (`prune-policy` 19 B, `deploy` 29 B, `mirrors`
32 B), which is a second reason to leave them alone.

**What you may change.** Only `embarch-umbrella` and `embarch-doc/embarch-umbrella/`.

**Doc reserve.** Nothing of `embarch-umbrella`'s is in reserve.

## Why now

The owner filed EMB-192 with the design settled and moved it to Fleet Ready;
it does not wait on EMB-190, since its tests use public bundles and a synthetic
manifest.

## Done when

- [x] `embarch verify-release [DIR]` exists, verifies the manifest's bundle under the exact identity and issuer above, then every listed file's SHA-256, and prints the suite version, component tags and commits, identity and log time.
- [x] The cosign and uv fixture tests pass under `cargo test`, and each also fails with a wrong identity, a wrong issuer and a wrong digest.
- [x] A synthetic-manifest test fails on a missing file and on a changed byte.
- [x] `cargo test` passes with the network unavailable, and only `--refresh-trust-root` code reaches it.
- [x] `cargo clippy --all-targets -- -D warnings` is clean.
- [x] `build-check.yml` exists and builds all four targets on a branch push, aarch64 included; its first run's result is recorded here.
- [x] The verification function is public to the crate and returns a result type.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment and the `status.d/` fragment above dropped.

## Result

- Code: `src/verify_release.rs`, the `VerifyRelease` variant in `src/main.rs`, pinned deps in `Cargo.toml`, fixtures in `tests/fixtures/` (the cosign bundle and uv's `sigstore-intermediate` bundle, 7 KB and 14 KB; the other uv attestation, issued by GitHub's own instance, was not kept). Public API: `verify_release::verify_release(dir, &TrustRootSource) -> Result<Verified, VerifyError>` and the sync `verify_release_with_root`.
- Gate: `cargo build`, `cargo test` (272 pass, offline), `cargo clippy --all-targets -- -D warnings` clean; `check-docs.py`, client-name and both ownership checks green.
- **`build-check.yml` first run** (branch push, run 44217599100): `aarch64-unknown-linux-gnu` success (the `aws-lc-sys` cross leg), `x86_64-unknown-linux-gnu` success, `x86_64-pc-windows-msvc` success, `aarch64-apple-darwin` **cancelled** with no log and no failed step. The worker could not re-run it (admin rights needed). Treat macOS as unverified until a re-run or the next push.
- **Found, not fixed:** a log key missing from the root usually surfaces from `sigstore-verify` as `InclusionPromise("No log key valid at integrated time ...")`, not `UnknownLog`, so `VerifyError::LogNotTrusted` (which names `--refresh-trust-root`) covers `UnknownLog`, `InclusionPromise`, `InclusionProof` and `Checkpoint`. The hint also shows on a genuinely bad proof.
- **Assumption:** the signed manifest's component commits (EMB-190 not shipped). Components parse as a bare tag or `{"tag","commit"}`; `files` is `{path: sha256}`. Reconcile when EMB-190 fixes the shape.
- **Decision 28's "copies with no check"** is now stale in part (`verify-release` exists; `setup` still copies unchecked until step 4). No decision filed or edited, per the burndown rule; step 4 is the natural place to amend it.
- **Hardware debt:** none. **Windows-native build:** not applicable (no `embarch-core` change).
