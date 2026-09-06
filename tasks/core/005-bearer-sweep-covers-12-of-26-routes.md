# Make the bearer-token route sweep derive itself — 14 of 26 routes have no test

**State:** done
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

- [x] One test derives the route list from `api.rs`'s own source and fails when a registered path
      has no auth case.
- [x] All 26 paths return `401` with no `Authorization` header, and with a wrong token.
- [x] The old individual `*_requires_the_bearer_token` tests are folded in, not left as a second
      drifting copy.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Shipped

`src/api.rs`: the twelve hand-written `*_requires_the_bearer_token` tests and
`stream_data_requires_the_bearer_token` are gone, replaced by `AUTH_CASES` (27
rows — 26 registered paths, `/signals` twice for its two methods) plus three
tests: `every_registered_route_has_an_auth_case` (set equality in **both**
directions against the `.route("` literals scanned out of `include_str!("api.rs")`),
and `every_registered_route_rejects_a_{missing,wrong}_bearer_token`, which drive
each row through the real router. Verified the guard actually fires by adding a
throwaway `.route("/brand-new", …)` and watching it fail with the intended
message, then reverting it.

`status_succeeds_with_the_correct_bearer_token`,
`stream_data_is_routed_to_the_handler_rather_than_the_fallback` and
`the_signal_link_wire_shape_is_what_clients_send` were **kept** — they assert
things the sweep does not.

Docs: decision 42 (`embarch-core/decisions/platform.md`, indexed in
`decisions.md`), the `spec.md` invariant now says the "no exceptions" is asserted
mechanically, a new `open.md` structural limit (the sweep proves rejection, not
reach), `changelog.d/core-bearer-route-sweep.changed.md`, and
`features.d/core-080-…` re-stated with the verification depth. **No `status.d/`
fragment**: nothing suite-level said anything this made false — `embarch.md`'s
Core row and `embarch-token.md` are unchanged and still true.

## Hardware-verification debt

**None from this change** — `auth_middleware` is a `.layer` on the whole router,
so every case rejects before axum routes the request and no handler, probe or
port is reached. The sweep runs entirely in `tower`'s `oneshot`.

**`embarch-core`'s native Windows build was not run** (`protocol.md` §10): no
worktree can, since Windows cannot follow the Linux symlinks a worktree reaches
its path-dep siblings through. The change is test-module-only and platform
independent, but it is unbuilt on Windows until someone runs `cargo build` from
the main checkout (~52 s).
