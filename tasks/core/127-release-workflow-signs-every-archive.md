# 127 — The release workflow signs every archive it uploads

**State:** claimed by agent/core/127-release-workflow-signs-every-archive, 2026-11-17 22:36
**Source:** EMB-190, the owner's issue: step 1 of `embarch-release-signing-proposal.md` ("Order"), sign every release in CI
**Issue:** EMB-190
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Step 1 of the release-signing proposal, `embarch-core`'s half. Read
`embarch-doc/embarch-release-signing-proposal.md` first: "The design in one
screen" (first bullet) and "Checked (2026-11-16)". The owner's account
hardening (step 2) is done: this repo has a GitHub environment named
`release`, reviewed by the owner, tag runs only. `embarch-umbrella`'s suite
assembly will verify this repo's bundles against the exact identity
`https://github.com/gabrieltetar/embarch-core/.github/workflows/release.yml@refs/tags/<tag>`
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
`decisions/platform.md` already cites `release.yml`; amend an existing
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

**What you may change.** Only `embarch-core` and `embarch-doc/embarch-core/`.
No core file is in doc-size reserve.

## Why now

The owner moved EMB-190 to Fleet Ready. Step 3 (`embarch verify-release`) is
built and has nothing signed to check.

## Outcome

`release.yml`: build matrix now `contents: read` and uploads `archive-<target>` workflow artifacts; new `sign-and-publish` job (`needs: build`, `environment: release`, `contents: write` + `id-token: write`, in this file) installs cosign v3.0.4 via `sigstore/cosign-installer@v4`, runs `cosign sign-blob --yes --bundle <asset>.sigstore.json <asset>` on all four archives (fails if not exactly 4) and publishes assets and bundles with `softprops/action-gh-release@v2`. Docs: `embarch-core/spec.md` §3 "Release assets" (exact `verify-blob` command), `decisions/platform.md` decision 1/2/7/17 note. No new decision.

**Debt (owner-side):** `actionlint` is not installed and did not run; the workflow only loaded as YAML under PyYAML. Nothing ran on a real tag: the first release shows whether `cosign-installer@v4` accepts `cosign-release: v3.0.4`, and whether `download-artifact` merge-multiple lays files flat in `dist/`. `workflow_dispatch` runs would also now wait on the `release` environment (tag-only, so the environment may refuse them).

## Done when

- [x] `release.yml` signs every uploaded asset with cosign 3.0.4 or later and uploads a `.sigstore.json` bundle beside it.
- [x] The signing job has `id-token: write` and `environment: release`, and sits in `release.yml` itself, not a reusable workflow.
- [x] `actionlint` passes on the changed workflow, or, where it is not installed, it parses as YAML and the debt is recorded here.
- [x] The core docs say what a release carries and give the exact `cosign verify-blob` check.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment; the `status.d/` fragment for the proposal.
