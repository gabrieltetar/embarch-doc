# 098 — The suite release verifies its components and signs a hashed manifest

**State:** open
**Source:** EMB-190, the owner's issue: step 1 of `embarch-release-signing-proposal.md` ("Order"), sign every release in CI
**Issue:** EMB-190
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

Step 1 of the release-signing proposal, `embarch-umbrella`'s half. Read
`embarch-doc/embarch-release-signing-proposal.md` first: "The design in one
screen" (first two bullets), "The first download" and "Checked (2026-11-16)".
The owner's account hardening (step 2) is done: the five release repos have a
GitHub environment named `release`, reviewed by the owner, tag runs only.
`embarch-core`, `embarch-api` and `embarch-topology` get the same signing in
their own `release.yml` as sibling tasks (`core/127`, `api/160`,
`topology/069`); this task does not touch those repos.

1. **`release.yml` signs every asset it uploads.** Pin cosign 3.0.4 or later
   through `sigstore/cosign-installer` (version pinned). After packaging, run
   `cosign sign-blob --yes --bundle <asset>.sigstore.json <asset>` and upload
   the bundle beside the asset. The signing job carries `id-token: write` and
   `environment: release`. The shape that gives one approval per release and
   keeps `id-token` off the build jobs: the build matrix uploads its archives
   as workflow artifacts, and one signing job (`needs:` the matrix) downloads
   them, signs each and publishes asset and bundle together. Use that shape or
   say why not. **No signing step goes in a reusable workflow**: the
   certificate identity would then name the called workflow, not this one.
2. **`assemble-suite.yml` runs on tags `suite-v*.*.*`**, not
   `workflow_dispatch`. The component tags it pulls move into a new committed
   file, `embarch-umbrella/suite.toml` (`core`, `api`, `umbrella`), read by
   the job; the suite version is taken from the tag. Commit `suite.toml` with
   the current newest tags of the three repos; the first signed suite release
   needs new signed component tags, and cutting them is the owner's.
3. **It verifies each downloaded component archive before repackaging**:
   `cosign verify-blob <asset> --bundle <asset>.sigstore.json
   --certificate-identity https://github.com/gabrieltetar/<repo>/.github/workflows/release.yml@refs/tags/<tag>
   --certificate-oidc-issuer https://token.actions.githubusercontent.com`.
   Exact identity, never a regexp; a failure fails the job.
4. **`embarch-manifest.json` gains `files`** (every file of the target's
   archive by relative path, to its SHA-256) **and each component's commit
   beside its tag.** `src/manifest.rs` must keep reading it unchanged, so its
   `doctor` check 1 still works and its tests still pass. `embarch
   verify-release` (umbrella/097) assumed a shape until this task fixed it:
   pick one shape that both `manifest.rs` (unchanged) and `verify-release`
   read, and make `verify-release`, its tests and
   `embarch-doc/embarch-umbrella/interfaces/verify-release.md` agree with
   exactly that shape.
5. **The manifest is signed**: `cosign sign-blob --bundle
   embarch-manifest.json.sigstore.json`, both uploaded to the suite release
   beside the archives, under the same `environment: release` and
   `id-token: write` rule. `actions/attest-build-provenance` attests each
   suite archive as a second record.

**Decision 14 is amended in place, not replaced.** It says assembly is
deliberately manual; the human act is now committing `suite.toml` and pushing
a `suite-v` tag, and the manifest gains hashes, commits and a signature. Edit
its body and keep its reason. **No new numbered decision** (burndown): if the
work needs a design call the umbrella decisions do not cover, file it with
`scripts/fleet-linear.py file --from decision` and say so in this file.

**Nothing is released.** The fleet pushes no tag and cuts no release; the
first signed release is the owner's.

**Ask for the proposal's fold.** Write a `status.d/` fragment targeting
`embarch-release-signing-proposal.md` that names what this task built, so the
fold can move step 1's umbrella part out of the proposal per its own Fold rule.
You do not edit that file.

**`actionlint` is not installed on this machine** (checked 2026-11-17) and
you may not install it. Run it if it is there. If it is not, load every
changed workflow with `python3` and PyYAML to catch a syntax error, say in this
file that `actionlint` did not run, and leave it as an owner-side debt.

**What you may change.** Only `embarch-umbrella` and
`embarch-doc/embarch-umbrella/`. Decisions within 256 B of their limit in this
sub-project, should you edit any: `prune-policy#26` (19 B), `deploy#32`
(29 B), `mirrors#20` (32 B), `probe-vendors#49` (140 B), `sticky-host#48`
(186 B), `budgets#44` (200 B). No umbrella file is in doc-size reserve.

## Why now

The owner moved EMB-190 to Fleet Ready. Step 3 (`embarch verify-release`)
landed on 2026-11-17 against an assumed manifest shape, and nothing it checks
exists until this ships.

## Done when

- [ ] `release.yml` signs every uploaded asset with cosign 3.0.4 or later and uploads a `.sigstore.json` bundle beside it; the signing job has `id-token: write` and `environment: release`.
- [ ] `assemble-suite.yml` triggers on `suite-v*.*.*` tags, reads the component tags from `suite.toml`, and fails when any component bundle does not verify against its exact workflow identity.
- [ ] `embarch-manifest.json` carries a `files` object of per-file SHA-256 and each component's commit; `manifest.rs` is unchanged and its tests pass; `verify-release`, its tests and `interfaces/verify-release.md` read that exact shape.
- [ ] The suite release carries `embarch-manifest.json.sigstore.json` and a build-provenance attestation per archive.
- [ ] `actionlint` passes on every changed workflow, or, where it is not installed, each parses as YAML and the debt is recorded here.
- [ ] Decision 14 amended in place; `spec.md` and the release docs say what a release now carries.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment; the `status.d/` fragment for the proposal.
