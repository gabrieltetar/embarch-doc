**Target:** embarch-token.md §1, §2, §3 and §5
**Was:** §1 "A single opaque string, shared across every caller."; §3 "Single shared secret, no per-caller identity."; §5 "No per-caller identity."; §2's table, which lists one token file
**Now:** Core holds two tokens (decision 109): the agent's (`EMBARCH_TOKEN`, else `token`) and the person's (`EMBARCH_PERSON_TOKEN`, else `person-token` beside it), either authenticating, each request carrying its scope. §2's table gains the person file for Core only; clients still resolve the agent's alone. Scope is recorded, not enforced.

See [embarch-core/decisions/auth.md](../embarch-core/decisions/auth.md) decision 109.
