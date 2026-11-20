# Proposal: signed EmbArch releases — Sigstore keyless signing in CI, one manifest per suite release, checked by the elevated install

**Status:** proposal, 2026-11-16.

Spans `embarch-core`, `embarch-api`, `embarch-topology`, `embarch-umbrella`, `embarch-dev-bench` and this repo, which is why it sits at the root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). **It is what [the HIL evidence proposal](embarch-hil-evidence-proposal.md) rests on** when it says an attested Core is installed only from a signed release ([12](notes/hil/12-prevention.md#the-root-of-trust-core-under-its-own-account)).

## Why

**Releases exist; nothing in them is signed.** Each of `embarch-core`, `embarch-api`, `embarch-topology` and `embarch-umbrella` has a tag-triggered `release.yml` that builds four targets and uploads archives to a GitHub release. `embarch-umbrella`'s `assemble-suite.yml`, started by hand, downloads one tagged release of each, repackages the three binaries per target with an `embarch-manifest.json` naming the component tags, and publishes `suite-v<version>` ([decision 14](embarch-umbrella/decisions/install.md)). **There is no signature, no checksum, and the manifest names tags, not hashes**; a release asset can be replaced by anyone holding the account; no build carries an OS signature. The last releases are from 2026-08 (`embarch-core` v0.1.4, `suite-v0.1.0`); the owner's own Core runs from source.

**The HIL design needs more than binaries from a release**: Core's protected store takes from it the hashes of the released bench firmware, which every bench board's image is compared with ([03](notes/hil/03-test.md#a-run), item 3), and its own copy of the premade suites ([03](notes/hil/03-test.md#the-duts-inputs)).

## Decided (owner, 2026-11-16)

- **Sigstore keyless signing from CI.** GitHub Actions signs through its OIDC token; there is no key to hold. Trust rests on the GitHub account and the workflow file, and every signature is entered in Sigstore's public transparency log.
- **One signed manifest per suite release, covering everything**: the binaries, the bench firmware images and the premade suites, each by SHA-256.
- **OS code signing is deferred** until engineers outside EmbArch install it.
- **A release is cut when a deliverable needs an attested run.** Daily work stays on the development Core ([12](notes/hil/12-prevention.md#the-root-of-trust-core-under-its-own-account)).

## The design in one screen

Recommended, not yet answered one by one. Facts about the tools were checked on 2026-11-16 against Sigstore's and GitHub's own pages ([Checked](#checked-2026-11-16)).

- **Signing in CI is written (step 1, 2026-11-17, EMB-190) and not yet run on a tag**, and lives in the owning repos' docs: each component's `release.yml` signs its archives ([core](embarch-core/spec.md#release-assets), [api](embarch-api/spec/implementation.md#8-release), [topology](embarch-topology/spec.md#what-a-release-carries)), and the suite assembly, on `suite-v*` tags, verifies each component's bundle by its exact identity, writes and signs a manifest per target with every file's SHA-256 and each component's tag and commit, and attests each archive ([umbrella spec](embarch-umbrella/spec.md), [decision 14](embarch-umbrella/decisions/install.md)). Each target's manifest and bundle are published as `embarch-manifest-<target>.json` and `embarch-manifest-<target>.json.sigstore.json`, since four would collide on one release. The reason the signing stays in each workflow file: the certificate's identity is `https://github.com/` plus the job's `job_workflow_ref`, which names a reusable workflow rather than its caller.
- **`embarch verify-release` is built (step 3, 2026-11-17)** and lives in `embarch-umbrella`'s [spec](embarch-umbrella/spec.md) and [interfaces/verify-release.md](embarch-umbrella/interfaces/verify-release.md): the issuer and an exact identity built from the manifest's version, never a pattern; Sigstore's trust root embedded, so a check fetches nothing and an unknown log key names `--refresh-trust-root`, which fetches through TUF for that run and **never caches the root**, since a cached root in a folder the engineer's account can write could be swapped; the pinned `sigstore-verify` crate, not the "experimental" `sigstore` crate and not `cosign`, a runtime dependency against [umbrella decision 1](embarch-umbrella/decisions/release.md). **Still proposed:** checking the certificate's source-repository and ref extensions against that identity too (the identity already names both), and a test against a real suite release bundle, which needs step 1 first.
- **The elevated install verifies before it installs**: it copies the archive into a staging folder only the elevated step can write, checks it there, so nothing can swap a file between the check and the install, and only then installs Core under its service account, **fills Core's protected store from the manifest** (bench firmware hashes, premade suites), records the manifest hash and the verified identity, and on a first install generates Core's key, shows its fingerprint and writes `core-fingerprint` ([12](notes/hil/12-prevention.md#the-root-of-trust-core-under-its-own-account)). **A failed check installs nothing.** An older suite version than the installed one is refused unless the person passes `--allow-downgrade`, which is recorded.
- **Two signatures, two questions.** The release signature says which build is EmbArch's; Core's own key, made at install, signs its records, and a client still checks that key's fingerprint, got from the engineer. **`verify` can join the two**: the Core binary hash a signed record carries ([umbrella decision 56](embarch-umbrella/decisions/schema-skew.md)'s `binary_sha256`) looked up in a verified release manifest, so a report reads "Core: suite-v0.2.0, release verified".
- **The GitHub account becomes the root of trust, so it is hardened**: a passkey or security key as second factor; tag rulesets so `v*` and `suite-v*` tags are never moved or deleted; **the signing jobs in a GitHub environment with the owner as required reviewer**, one click per release; workflow files changed only through `main`.
- **Bench firmware**: `embarch-dev-bench`, which has no CI today, gets a release workflow building the dev bench and `pd-bench` images in the Zephyr SDK container from its pinned manifest and patches, and signing them; assembly takes them like the binaries. **Premade suites** get their slot in the manifest, empty until the first suite exists.
- **One script cuts a release** (`embarch-umbrella/scripts/`): checks the versions, tags each component that changed, waits for its CI, tags the suite, waits, downloads and verifies the result, and prints the elevated install command. The install stays the owner's step.

## What it costs, and the risks

- **Trust moves to the GitHub account and Sigstore's public instance.** A stolen account that also passes the environment's approval can sign a release; the hardening above is what stands in the way. A Sigstore outage stops releases being signed, not installed ones being verified.
- **The log is public**: each release's hashes and workflow identity appear in it, as the repos already are.
- **The embedded trust root ages**, by a new log shard about every six months, so an older `embarch` needs `--refresh-trust-root`, and network, for a release logged to a newer shard; with neither, the guide's `cosign verify-blob` command.
- **Verifiers have bugs in exactly this path.** A 2026 cosign advisory let a bundle verify although its log entry did not match the artifact, for users passing `--trusted-root` (fixed in 2.6.2 and 3.0.4); a later one, rated high, concerns legacy bundles. **CI and the guide pin cosign 3.0.4 or later**; `sigstore-verify` is pre-1.0, 23 releases in a year, so its pin moves only with the CI test passing.
- **Installers keep warning** on Windows and macOS until OS signing is taken up.
- **Firmware builds in CI** need the Zephyr SDK image (minutes per release, unmeasured).

## The work, by sub-project

| Sub-project | Work |
|---|---|
| `embarch-umbrella` | `embarch verify-release`'s extension check (the rest of it is built). The elevated install verifying in a protected staging folder, then filling Core's store; a `doctor` check naming the verified release Core came from. The release script |
| `embarch-dev-bench` | A release workflow for the bench firmware images |
| `embarch-doc` | [The user guide](suite/user-guide.md)'s install section, with the first download checked by `cosign`; [the dev workflow](embarch-dev-workflow.md)'s cutting a release; the HIL notes' release wording pointed here |
| GitHub, by hand | Done: step 2 below |

## Order

1. **Sign in CI**: written 2026-11-17 (EMB-190), in the five workflows the first bullet above names, and not yet run on a tag. `actionlint` has not run on any of them. The first signed suite release needs new signed component tags in `embarch-umbrella/suite.toml`, and cutting them is the owner's.
2. **Harden the account**: done 2026-11-16. A passkey; on the five release repos, the tag ruleset and the `release` environment (the owner reviews, tag runs only).
3. **`embarch verify-release`**: built 2026-11-17 (EMB-192), now in `embarch-umbrella`'s docs. Its `aws-lc-sys` build passed `build-check.yml`'s first run on the aarch64 Linux cross leg; the macOS leg was cancelled, unverified.
4. **The elevated install checking before installing**, landing with the evidence proposal's step 3 (Core's own account and store, the attested phase).
5. **The bench firmware release**, then the premade suites once the first exists.

## The first download

**No `embarch` exists yet to check the first `embarch`**, so the guide gives one command, with cosign 3.0.4 or later, and `gh attestation verify` as an alternative; from then on every update is checked by the installed `embarch`, and an attested install only ever by the elevated step:

```
cosign verify-blob embarch-manifest-<target>.json \
  --bundle embarch-manifest-<target>.json.sigstore.json \
  --certificate-identity https://github.com/gabrieltetar/embarch-umbrella/.github/workflows/assemble-suite.yml@refs/tags/suite-v<version> \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

then each unpacked file's SHA-256 against the manifest's `files`.

## Checked (2026-11-16)

- **The certificate**: identity `https://github.com/{job_workflow_ref}`; repository, commit, ref and trigger in the provider-generic extensions from OID `1.3.6.1.4.1.57264.1.8` on, the GitHub-specific ones before it deprecated ([Fulcio's OIDC page](https://github.com/sigstore/fulcio/blob/main/docs/oidc.md), [its OID list](https://github.com/sigstore/fulcio/blob/main/docs/oid-info.md)). The issuer, `job_workflow_ref` naming the reusable workflow, and a tag's ref as `refs/tags/<tag>` (the last inferred from the subject format): [GitHub's OIDC reference](https://docs.github.com/en/actions/reference/security/oidc).
- **cosign**: `--bundle` required, exact identity and issuer flags, `--trusted-root` for a supplied root (else fetched through TUF), no `--offline` flag ([`verify-blob`'s reference](https://github.com/sigstore/cosign/blob/main/doc/cosign_verify-blob.md)). The advisory: [GHSA-whqx-f9j3-ch6m](https://github.com/sigstore/cosign/security/advisories/GHSA-whqx-f9j3-ch6m), CVE-2026-22703.
- **Rust**: `sigstore-verify` 0.16.0 (2026-11-09, Apache-2.0, `sigstore/sigstore-rust`, [docs.rs](https://docs.rs/crate/sigstore-verify/latest)).
- **The log and the trust root**: shards about every six months, the current shard from TUF's signing config, old and new shard keys from the trust root ([rekor-tiles](https://github.com/sigstore/rekor-tiles)); TUF metadata re-signed at least every three days, no published key-rotation schedule ([root-signing](https://github.com/sigstore/root-signing)).

## Open questions

- **The new log's entries**: the crate parses them and its embedded root holds the 2025 shard's key, but no public bundle with one was found to test; both spike bundles carry the old log's entries.
- **How long old shards' keys stay in the trust root**, which decides how old a release can be and still verify: not documented.
- **Reproducible builds**, for a client to rebuild and compare: later.
- **`verify` joining Core's binary hash to the release manifest**: recommended above, not answered.
- **OS code signing**: deferred by the owner; costs to check when it is taken up.

**Fold:** each step moves its part into the owning sub-project's docs as it is accepted and deletes it here. This file is deleted once nothing in it is still proposed.
