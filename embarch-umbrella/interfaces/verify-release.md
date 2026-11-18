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
2. Every entry of the manifest's `files` object (relative path to SHA-256): present, same
   hash. A path that is absolute or climbs out of the folder is refused.
3. Trust root: the public-good root compiled into `sigstore-trust-root` by default, so
   **verification fetches nothing**. `--trusted-root` reads one file. `--refresh-trust-root`
   fetches through TUF for that run with the TUF cache disabled, so nothing is kept. A
   transparency-log rejection (unknown key, no key valid at the entry's time, a checkpoint or
   proof the root cannot vouch for) says so and names `--refresh-trust-root`. The output
   says which root was used.

**Output** (stdout; failure on stderr, exit `1`): suite version, each component's tag and
commit, the verified certificate identity, the issuer, the log entry's time, the file count.
A component the manifest records as a bare tag prints "commit not recorded"; the manifest
`doctor` reads today names tags only, and the object form `{"tag", "commit"}` is accepted
for the signed manifest EMB-190 writes. **That shape is an assumption until EMB-190 ships.**

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
digest; a root with its log keys removed; and the file check on a synthetic manifest (missing
file, one changed byte, unsafe paths). **No signed suite manifest has been verified end to
end** until EMB-190 ships and a release is tagged.
