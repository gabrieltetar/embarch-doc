# 049 — `CoreConfig`/`ProjectConfig` still hand-mirror `embarch-api`, with no check that would notice drift

**State:** open
**Source:** `embarch-umbrella/open.md` — "Both mirrors closed, `CoreConfig` still hand-kept … no CI diff job exists. Depend on `embarch-core-client` for `CoreConfig` too, or build the diff job."
**Scope:** umbrella
**Hardware:** none — a type/dependency change and a test, entirely host-side.
**Owner:** no

## What

Two of this repo's three mirrors of `embarch-api`-internal logic are closed — the token
mirror by depending on `embarch-core-client` directly ([decisions/mirrors.md](../../embarch-umbrella/decisions/mirrors.md) decision 20's
amendment), and check 6's config drift by sourcing its verdict from the located `embarch-api`
(decision 16's amendment, `umbrella/036`). What remains is that `CoreConfig` and `ProjectConfig`
are still **hand-written copies** of `embarch-api`'s own types, kept in step by someone
remembering. Nothing fails when they drift.

Close it the same way the token mirror was closed if that is available — depend on the shared
crate for the type rather than restating it — and if it is not (the type may live inside
`embarch-api`'s own binary rather than in `embarch-core-client`), **say so in a numbered decision
and build the cheaper half instead**: a test that parses a real `embarch-api` config fixture
through this repo's type and fails on an unknown or missing field.

Whichever half lands, the outcome to aim for is that **a field added to `embarch-api`'s config
cannot silently go unseen here**. Do not widen the ownership map: `embarch-api` is not this
worker's to edit. If the only correct fix is on `embarch-api`'s side, that is an `inbox/` drop
(absolute path `/home/gabriel/Github/embarch/embarch-doc/inbox/`), not a change to make.

## Why now

`embarch-umbrella`'s two other mirrors both produced real, shipped defects before they were
closed, and both were found by a human reading a call site rather than by a check. This is the
last one standing, and it is the one a config-format change would hit first — `setup` and
`doctor` both read it.

## Done when

- [ ] Either `CoreConfig`/`ProjectConfig` come from the shared crate, or a numbered decision
      records why they cannot and a fixture-parse test covers the drift instead.
- [ ] `embarch-umbrella/open.md`'s "Both mirrors closed, `CoreConfig` still hand-kept" bullet is
      updated to say what is now true; if a third answer was found, name it.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped; `status.d/` fragment for anything suite-level made false.
