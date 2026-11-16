# Proposal: signed EmbArch releases — Sigstore keyless signing in CI, one manifest per suite release, checked by the elevated install

**Status:** proposal, 2026-11-16.

Spans `embarch-core`, `embarch-api`, `embarch-topology`, `embarch-umbrella`, `embarch-dev-bench` and this repo, which is why it sits at the root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). **It is what [the HIL evidence proposal](embarch-hil-evidence-proposal.md) rests on** when it says an attested Core is installed only from a signed release ([12](notes/hil/12-prevention.md#the-root-of-trust-core-under-its-own-account)).

## Why

**Releases exist; nothing in them is signed.** Each of `embarch-core`, `embarch-api`, `embarch-topology` and `embarch-umbrella` has a tag-triggered `release.yml` that builds four targets and uploads archives to a GitHub release, after a job that refuses a tag whose `Cargo.toml` version disagrees ([umbrella decisions 27, 29](embarch-umbrella/decisions/release.md)). `embarch-umbrella`'s `assemble-suite.yml`, started by hand, downloads one tagged release of each, repackages the three binaries per target with an `embarch-manifest.json` naming the component tags, and publishes `suite-v<version>` ([decision 14](embarch-umbrella/decisions/install.md)). **There is no signature, no checksum, and the manifest names tags, not hashes**; a release asset can be replaced by anyone holding the account; macOS builds are unsigned and Windows ones carry no Authenticode. The last releases are from 2026-08 (`embarch-core` v0.1.4, `suite-v0.1.0`); the owner's own Core runs from source.

**The HIL design needs more than binaries from a release**: Core's protected store takes from it the hashes of the released bench firmware, which every bench board's image is compared with ([03](notes/hil/03-test.md#a-run), item 3), and its own copy of the premade suites ([03](notes/hil/03-test.md#the-duts-inputs)).

## Decided (owner, 2026-11-16)

- **Sigstore keyless signing from CI.** GitHub Actions signs through its OIDC token; there is no key to hold. Trust rests on the GitHub account and the workflow file, and every signature is entered in Sigstore's public transparency log.
- **One signed manifest per suite release, covering everything**: the binaries, the bench firmware images and the premade suites, each by SHA-256.
- **OS code signing is deferred** until engineers outside EmbArch install it.
- **A release is cut when a deliverable needs an attested run.** Daily work stays on the development Core ([12](notes/hil/12-prevention.md#the-root-of-trust-core-under-its-own-account)).

## The design in one screen

Recommended, not yet answered one by one; tools and behaviour marked "from memory" are to check before building.

- **Each component's `release.yml` signs its archives**: `cosign sign-blob --bundle` per asset, with `id-token: write`, and the bundle (`.sigstore.json`: the signature, the short-lived certificate and the log's inclusion proof) uploaded beside the asset. **The certificate names the repo, the workflow file and the tag** it ran on (from memory).
- **Suite assembly becomes tag-triggered** on `suite-v*`, rather than started by hand, so its certificate names a tag rather than `main`. It **verifies each component's bundle against that component's own workflow identity** before repackaging, since a replaced asset would otherwise be signed again; writes `embarch-manifest.json` with **the SHA-256 of every file of every target**, the component tags and commits; signs the manifest; and adds GitHub's build provenance (`actions/attest-build-provenance`) as a second, non-deciding record.
- **The identity policy is compiled into `embarch`**: the issuer GitHub Actions' token service, and a certificate identity of `embarch-umbrella`'s `assemble-suite.yml` on a `suite-v*` tag. **Sigstore's trust root is embedded beside it at build time**, so a check needs no network: the bundle carries its own inclusion proof (from memory).
- **`embarch verify-release <archive>`** checks the manifest's bundle against that policy, then every file's hash, and prints the suite version, the commits and the log entry. **In Rust, through the `sigstore` crate**, not by shelling out to `cosign`, which would add a runtime dependency against [umbrella decision 1](embarch-umbrella/decisions/release.md).
- **The elevated install verifies before it installs**: it copies the archive into a staging folder only the elevated step can write, checks it there, so nothing can swap a file between the check and the install, and only then installs Core under its service account, **fills Core's protected store from the manifest** (bench firmware hashes, premade suites), records the manifest hash and the verified identity, and on a first install generates Core's key, shows its fingerprint and writes `core-fingerprint` ([12](notes/hil/12-prevention.md#the-root-of-trust-core-under-its-own-account)). **A failed check installs nothing.** An older suite version than the installed one is refused unless the person passes `--allow-downgrade`, which is recorded.
- **Two signatures, two questions.** The release signature says which build is EmbArch's; Core's own key, made at install, signs its records, and a client still checks that key's fingerprint, got from the engineer. **`verify` can join the two**: the Core binary hash a signed record carries ([umbrella decision 56](embarch-umbrella/decisions/schema-skew.md)'s `binary_sha256`) looked up in a verified release manifest, so a report reads "Core: suite-v0.2.0, release verified".
- **The GitHub account becomes the root of trust, so it is hardened**: a hardware-key second factor on the account; tag rulesets so `v*` and `suite-v*` tags are created only by the owner and never moved or deleted; **the signing jobs in a GitHub environment with the owner as required reviewer**, one click per release; workflow files changed only through `main`.
- **Bench firmware**: `embarch-dev-bench`, which has no CI today, gets a release workflow building the dev bench and `pd-bench` images in the Zephyr SDK container from its pinned manifest and patches, and signing them; assembly takes them like the binaries. **Premade suites** get their slot in the manifest, empty until the first suite exists.
- **One script cuts a release** (`embarch-umbrella/scripts/`): checks the versions, tags each component that changed, waits for its CI, tags the suite, waits, downloads and verifies the result, and prints the elevated install command. The install stays the owner's step.

## What it costs, and the risks

- **Trust moves to the GitHub account and Sigstore's public instance.** A stolen account that also passes the environment's approval can sign a release; the hardening above is what stands in the way. A Sigstore outage stops releases being signed, not installed ones being verified.
- **The log is public**: each release's hashes and workflow identity appear in it. The repos are public already.
- **The embedded trust root ages.** After Sigstore rotates a key, an older `embarch` may fail to verify a newer release; the guide then gives the out-of-band `cosign verify-blob` command for installing the newer `embarch` by hand. How often that happens is to check.
- **Installers keep warning** on Windows and macOS until OS code signing is taken up.
- **Firmware builds in CI** need the Zephyr SDK image and add minutes per release (unmeasured).

## The work, by sub-project

| Sub-project | Work |
|---|---|
| `embarch-core`, `embarch-api`, `embarch-topology` | `release.yml`: `id-token: write`, a bundle signed and uploaded per asset, the signing job in the protected environment |
| `embarch-umbrella` | `assemble-suite.yml` on `suite-v*` tags: component bundles verified, a per-file SHA-256 manifest signed, build provenance. `embarch verify-release`, with the identity policy and trust root embedded. The elevated install verifying in a protected staging folder, then filling Core's store; a `doctor` check naming the verified release Core came from. The release script. [Decision 14](embarch-umbrella/decisions/install.md) amended: the manifest gains hashes and a signature |
| `embarch-dev-bench` | A release workflow for the bench firmware images |
| `embarch-doc` | [The user guide](suite/user-guide.md)'s install section, with the first download checked by `cosign`; [the dev workflow](embarch-dev-workflow.md)'s cutting a release; the HIL notes' release wording pointed here |
| GitHub, by hand | The second factor, the tag rulesets, the environment and its reviewer |

## Order

1. **Sign in CI**: the component archives and the suite manifest. Useful at once, since anyone can check a release with `cosign`. About half a day.
2. **Harden the account**: about 30 minutes, the owner's.
3. **`embarch verify-release`**: about a day if the `sigstore` crate verifies a bundle offline as expected, two to three if it does not.
4. **The elevated install checking before installing**, landing with the evidence proposal's step 1 (Core's own account and store).
5. **The bench firmware release**, then the premade suites once the first exists.

## The first download

**No `embarch` exists yet to check the first `embarch`**, so the guide gives one `cosign verify-blob` command with the identity flags, and `gh attestation verify` as an alternative; from then on every update is checked by the installed `embarch`, and an attested install only ever by the elevated step.

## Open questions

- **The `sigstore` crate**: whether it verifies a bundle fully offline against an embedded trust root, its maturity and its licence (Apache-2.0, from memory).
- **Reproducible builds**, so a client can rebuild a release and compare: later.
- **`verify` joining Core's binary hash to the release manifest**: recommended above, not answered.
- **OS code signing**: deferred by the owner; costs to check when it is taken up.

**Fold:** each step moves its part into the owning sub-project's docs as it is accepted and deletes it here. This file is deleted once nothing in it is still proposed.
