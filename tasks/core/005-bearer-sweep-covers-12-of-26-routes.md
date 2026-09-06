# Make the bearer-token route sweep derive itself — 14 of 26 routes have no test

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `embarch-core/spec.md:25`'s "no exceptions" is tested for less than half the surface
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`src/api.rs:69-98` registers 26 route paths. The hand-written `*_requires_the_bearer_token` tests
(`src/api.rs:1267-1464`) cover 12 of them. `/flash`, `/reset`, `/serial-log`, `/probes/enroll`,
`/resolve-chip`, `/dev-bench/port`, `/dev-bench/hello` and **all seven `/study*` routes** have none
— the list has already drifted, and the studies surface is the newest and least covered.

One test extracts every `.route("<path>"` literal from `include_str!("api.rs")` and asserts each is
exercised by a table-driven unauthenticated case expecting `401`. Adding a route without adding it
to that table fails the test rather than shipping a silently open path. The middleware rejects
before any handler runs, so nothing touches a probe or a port.

**Fold the existing individual tests into the table rather than leaving them beside it** — two
lists is the shape that drifted in the first place.

This is the `embarch-core` half. `embarch-api` did the same work for its own sweep in `api/020`
(decision 54); this task does not touch that repo.

## Why now

`embarch-doc/embarch-core/spec.md:25` states "**Every route requires `Authorization: Bearer <token>`**,
no exceptions," and `src/api.rs:64-68` records that the one historical exception was retired. An
invariant asserted in prose and tested for less than half the surface is the shape
`../../embarch-fleet/risks.md` calls a discipline rather than a mechanism.

## Done when

- [ ] One test derives the route list from `api.rs`'s own source and fails when a registered path
      has no auth case.
- [ ] All 26 paths return `401` with no `Authorization` header, and with a wrong token.
- [ ] The old individual `*_requires_the_bearer_token` tests are folded in, not left as a second
      drifting copy.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
