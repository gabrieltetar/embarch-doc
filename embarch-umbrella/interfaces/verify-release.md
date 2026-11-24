# embarch-umbrella: `embarch verify-release`

**Status:** active, 2026-11-17. Built on a branch for EMB-192 (`tasks/umbrella/097`). Step 3 of
[the release-signing proposal](../../embarch-release-signing-proposal.md), whose design this
implements without reopening. Index: [../decisions.md](../decisions.md); the verb in
[../spec.md](../spec.md).

`embarch verify-release [DIR] [--trusted-root FILE | --refresh-trust-root]`. `DIR` holds
`embarch-manifest.json`, `embarch-manifest.json.sigstore.json` and the files the manifest
lists; it defaults to the running `embarch`'s own folder, as `setup` does.

**Checks, in order; the first failure ends the run and names what failed.**

1. The manifest's bytes against its bundle (`sigstore-verify`), under
   `VerificationPolicy::new(identity, issuer)`: issuer
   `https://token.actions.githubusercontent.com`, identity
   `https://github.com/gabrieltetar/embarch-umbrella/.github/workflows/assemble-suite.yml@refs/tags/suite-v<suite_version>`
   with the manifest's own `suite_version`. Exact string, never a pattern, never
   `any_identity()`.
2. The signing certificate's own extensions, read after the signature passes, each an exact
   string and never a pattern: Source Repository URI (`1.3.6.1.4.1.57264.1.12`) is
   `https://github.com/gabrieltetar/embarch-umbrella`; Source Repository Ref (`.1.14`) is
   `refs/tags/suite-v<suite_version>`; Build Config URI (`.1.18`) equals the identity of
   check 1. A missing extension fails and names it; a differing one names the extension, the
   expected value and the found one. A bundle whose identity matches but whose extensions
   name another repository or ref fails.
3. Every entry of the manifest's `files` object (relative path to SHA-256): present, same
   hash. A path that is absolute or climbs out of the folder is refused.
4. Trust root: the public-good root compiled into `sigstore-trust-root` by default, so
   **verification fetches nothing**. `--trusted-root` reads one file. `--refresh-trust-root`
   fetches through TUF for that run with the TUF cache disabled, so nothing is kept. A
   transparency-log rejection (unknown key, no key valid at the entry's time, a checkpoint or
   proof the root cannot vouch for) says so and names `--refresh-trust-root`. The output
   says which root was used.

**Output** (stdout; failure on stderr, exit `1`): suite version, each component's tag and
commit, the verified certificate identity, the issuer, the log entry's time, the file count.
The manifest's `components` object maps each name to its tag (the shape `doctor` reads) and a
sibling `commits` object maps it to the commit; a component missing from `commits` prints
"commit not recorded". The shape is fixed by `assemble-suite.yml` (EMB-190) and read unchanged by
`manifest.rs` and `verify_release.rs`:

```json
{"suite_version": "0.2.0", "target": "x86_64-unknown-linux-gnu",
 "components": {"embarch": "v0.2.0", "embarch-core": "v0.1.4", "embarch-api": "v0.1.0"},
 "commits": {"embarch": "<sha>", "embarch-core": "<sha>", "embarch-api": "<sha>"},
 "files": {"embarch": "<sha256>", "embarch-core": "<sha256>", "embarch-api": "<sha256>"}}
```

`files` covers every file of the archive but the manifest. The release carries the manifest and
bundle per target as `embarch-manifest-<target>.json` and `.json.sigstore.json`; rename them to
`embarch-manifest.json` and `embarch-manifest.json.sigstore.json` beside the unpacked archive (the
archive holds the same manifest, and a bundle signs bytes, not a name).

**For the checked install (step 4):** `verify_release::verify_release(dir, &TrustRootSource)
-> Result<Verified, VerifyError>` (async) and the synchronous, offline
`verify_release_with_root(dir, &TrustedRoot, label)`. They print nothing.

**Pins.** `sigstore-verify`, `sigstore-types` and `sigstore-trust-root` are `=0.16.0`; the
crate is pre-1.0, so the pin moves only with the fixture tests passing. They add
`aws-lc-sys` (a C and `cmake` build), checked on the aarch64 cross leg by
`.github/workflows/build-check.yml`.

**Tests**, offline: two public bundles committed under `tests/fixtures/` and verified by
digest (cosign v3.1.4's `cosign-linux-amd64`, uv 0.13.8's x86_64 Linux build attestation,
the latter issued by `sigstore-intermediate`), each failing on a wrong identity, issuer and
digest; the uv bundle's three extensions read and asserted, a differing expected value failing
naming the extension, and the cosign bundle (a human identity, no CI claims) failing naming the
missing one; a root with its log keys removed; and the file check on a synthetic manifest (missing
file, one changed byte, unsafe paths). **No signed suite manifest has been verified end to
end** until the owner tags the first signed suite release.
