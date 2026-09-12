# 072 — `spec.md` states the outbound token precedence backwards

**State:** open
**Source:** refill sweep for scope spread, leg 091, 2026-09-11. **Line numbers are as the sweep
reported them — re-check each against the source before you act on it.**
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api/spec.md:56` says:

> **Outbound** is `EMBARCH_TOKEN`: config `token`, then `token_env`, then machine-wide token-file
> discovery.

`crates/embarch-core-client/src/token_discovery.rs:12-30` — `resolve_token` checks
`explicit_token_env` **first**, returning its env value if present, and only then falls through to
the inline `token` and then the token file. The crate's own doc comment agrees
(`crates/embarch-core-client/src/lib.rs:94`: "`token_env` wins if set, then inline `token`"), and so
do two sibling docs: `interfaces/config.md:24` ("**Wins if both are set.**") and
`embarch-doc/embarch-token.md:23`. `spec.md` is the lone outlier.

## Why it costs something

`spec.md` is the "what is true now" entry point. An engineer debugging a `401` with both `token` and
`token_env` set chases the inline value, which never wins — and the doc set contradicts itself on
the one fact that decides which secret goes on the wire.

## What to do

Read `resolve_token` and confirm the real order, then correct `spec.md`'s sentence to match. This is
a **doc fix, not a behaviour change**: do not reorder the resolution to match the prose — three
other places already document the code's order, so the code is the settled side. No new numbered
decision.

## A second, separable thing in the same sub-project

`decisions/client-crate.md:43` (decision 58) offers a grep as the check that its rule is still
universal: *"`client.rs` had already made this choice **thirteen** times… `grep -c 'serde(default)'`
returns 14 on that file because one hit is a doc comment"*, and :45 calls `validated_at_utc_ms` the
fourteenth. The sweep reports `grep -c 'serde(default)'` on
`crates/embarch-core-client/src/client.rs` now returns **21** — 18 attribute lines and 3 doc-comment
mentions. Neither 13/14 nor the "one hit is a doc comment" parenthetical holds.

Re-count it yourself. Then decide, and say which you did and why: update the numbers, or replace the
frozen count with a check that does not rot (the decision's *point* is that every optional field
takes `serde(default)`, and a count is a poor way to assert a universal). **Do not delete the check
outright** — it is the only thing in that decision a reader can run.

## Done when

- [ ] `spec.md:56`'s precedence matches `resolve_token`, verified by reading it.
- [ ] Decision 58's count is either correct today or replaced by something that stays correct, with
      the reasoning written in the decision body.
- [ ] No behaviour change in token resolution and no new numbered decision.
- [ ] Watch the doc-size reserve: `embarch-api` has six open or blocked compaction tasks and
      `interfaces/config.md` is at 91.1% of cap. If your edit spends reserve in a file, file
      `tasks/api/<NNN>-compact-api.md` in the same commit.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
