**Target:** embarch-token.md — "The auto-generated token file" (where files beside the token live)
**Was:** the token and `person-token` are the only files Core keeps beside each other in the machine-wide data directory
**Now:** Core also keeps `signing-key` there (its Ed25519 key for study run records: 64 hex characters, `0600` on Linux, the same `icacls` lockdown on Windows, unrun), created on first start and reused. Unlike the tokens it has no env override, and rotating it makes every earlier record's `keyid` differ. See [embarch-core decision 110](../embarch-core/decisions/signing.md).
