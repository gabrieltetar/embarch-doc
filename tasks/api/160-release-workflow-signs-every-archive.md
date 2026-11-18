# 160 — The release workflow signs every archive it uploads

**State:** open
**Source:** EMB-190, the owner's issue: step 1 of `embarch-release-signing-proposal.md` ("Order"), sign every release in CI
**Issue:** EMB-190
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Step 1 of the release-signing proposal, `embarch-api`'s half. Read
`embarch-doc/embarch-release-signing-proposal.md` first: "The design in one
screen" (first bullet) and "Checked (2026-11-16)". The owner's account
hardening (step 2) is done: this repo has a GitHub environment named
`release`, reviewed by the owner, tag runs only. `embarch-umbrella`'s suite
assembly will verify this repo's bundles against the exact identity
`https://github.com/gabrieltetar/embarch-api/.github/workflows/release.yml@refs/tags/<tag>`
(sibling task `umbrella/098`), so the signing must run in this file, at the
tag.

`.github/workflows/release.yml` builds four targets on a `v*.*.*` tag and
uploads bare archives with `softprops/action-gh-release@v2`, under
`permissions: contents: write`, with no signature. Make it:

- **Pin cosign 3.0.4 or later** through `sigstore/cosign-installer` (version
  pinned).
- **Sign every uploaded asset**: `cosign sign-blob --yes --bundle
  <asset>.sigstore.json <asset>` after packaging, and upload the bundle beside
  the asset.
- **The signing job carries `id-token: write` and `environment: release`.**
  The shape that gives one approval per release and keeps `id-token` off the
  build jobs: the build matrix uploads its archives as workflow artifacts, and
  one signing job (`needs:` the matrix) downloads them, signs each and
  publishes asset and bundle together. Use that shape or say why not.
- **No signing step goes in a reusable workflow**: the certificate identity
  would then name the called workflow, not this one.

Record in this sub-project's docs what a release now carries and how to check
an asset (`cosign verify-blob` with the exact identity and issuer above).
`decisions/build.md` already cites `release.yml`; amend an existing
decision's body where one describes the release, rather than adding one.
**No new numbered decision** (burndown): if the work needs a design call,
file it with `scripts/fleet-linear.py file --from decision` and say so in
this file.

**Nothing is released.** The fleet pushes no tag and cuts no release.

**Ask for the proposal's fold.** Write a `status.d/` fragment targeting
`embarch-release-signing-proposal.md` that names what this task built. You do
not edit that file.

**`actionlint` is not installed on this machine** (checked 2026-11-17) and
you may not install it. Run it if it is there. If it is not, load the changed
workflow with `python3` and PyYAML to catch a syntax error, say in this file
that `actionlint` did not run, and leave it as an owner-side debt.

**What you may change.** Only `embarch-api` and `embarch-doc/embarch-api/`.
Decisions within 256 B of their limit, should you edit any: `ledger#98`
(15 B), `bench-exchange#89` (122 B), `failure-reporting#67` (192 B). No api
file is in doc-size reserve.

## Why now

The owner moved EMB-190 to Fleet Ready. Step 3 (`embarch verify-release`) is
built and has nothing signed to check.

## Done when

- [ ] `release.yml` signs every uploaded asset with cosign 3.0.4 or later and uploads a `.sigstore.json` bundle beside it.
- [ ] The signing job has `id-token: write` and `environment: release`, and sits in `release.yml` itself, not a reusable workflow.
- [ ] `actionlint` passes on the changed workflow, or, where it is not installed, it parses as YAML and the debt is recorded here.
- [ ] The api docs say what a release carries and give the exact `cosign verify-blob` check.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment; the `status.d/` fragment for the proposal.
