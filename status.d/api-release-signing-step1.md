**Target:** embarch-release-signing-proposal.md — "Order", step 1 (sign every release in CI), `embarch-api`'s half
**Was:** step 1 proposed; nothing signed
**Now:** `embarch-api`'s `release.yml` is written to sign every archive (cosign 3.0.4+, `sign-blob --bundle`, `.sigstore.json` beside each asset) in one `sign-and-publish` job with `environment: release` and `id-token: write`, in the file itself; unrun (no tag cut, `actionlint` absent). Check: [embarch-api/spec/implementation.md](embarch-api/spec/implementation.md) §8.
