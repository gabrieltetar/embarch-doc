# 058 — Remove Core's deprecated halted field after its date

**State:** blocked
**Unparks when:** 2026-12-01 — `embarch-core` decision 97 and `embarch-api` decision 83 mark the field "deprecated, removed after 2026-11-30"
**Source:** suite review audit, 2026-11-23: the removal is decided and dated in three docs, and nothing was queued to do it
**Issue:** EMB-312
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`halted` on `/live/mem-read` is deprecated and due out after 2026-11-30
(`embarch-core` decision 97, `embarch-api` decision 83). It still exists in
three places: `embarch-core/src/live.rs` (the field, where it is set, and a
test), `embarch-api/crates/embarch-core-client/src/client.rs` (the field) and
a branch in `embarch-api/src/tools.rs` that renders it.

When this is done the field and its renderer branch are gone, and no doc says
"deprecated, removed after". The doc rows to drop:
`embarch-core/interfaces/hardware.md`,
`embarch-api/decisions/failure-reporting.md` and
`embarch-api/interfaces/tools-build-flash.md` (each carries one line on it).

**Keep `found`, `left` and `halt_count` optional.** `embarch-api` decision
58's allowance for parsing an older Core stands; making them required would be
a new decision, and this task needs none.

## Why now

It is dated, and a date nothing fires on is missed. This file is the firing:
it unparks on 2026-12-01.

## Notes for whoever runs it

A cross-repo pass (`../../embarch-fleet/protocol.md` §8), and a wire change,
so it is announced and parked for its 30-minute window before it runs
(`../../embarch-fleet/ops.md` §4). Order: `embarch-core` first (Core stops
sending the field; an api that still reads it as optional keeps parsing),
then `embarch-api` (core-client and the renderer), then `embarch-doc`. Each
repo's `main` compiles on its own at every step.

## Done when

- [ ] The `halted` field is gone from Core's response, from core-client, and
      the renderer branch in `tools.rs` is gone.
- [ ] No doc says "deprecated, removed after" about it; decisions 97 and 83
      amended to say it was removed.
- [ ] `changelog.d/` fragments dropped for `core` and `api`.
- [ ] Gate green in both code repos and `embarch-doc`
      (`../../embarch-fleet/protocol.md` §10).
