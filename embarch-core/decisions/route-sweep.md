# embarch-core decisions: The route sweep

**Status:** active, 2026-09-28.

Three mechanisms that all read `build_router`'s own source in `api.rs` to keep something else
in step with it: the bearer-token coverage, the documented route count, and the reach from
each route to its intended handler. Split out of [decisions/auth.md](auth.md) (`tasks/core/046`)
verbatim, along the file's own seam — that mission is auth, binding and configuration; this one
has never been about authentication, only about `api.rs` staying honest about itself.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## The route sweep

### 42 — The bearer-token sweep derives its route list from `build_router`'s own source
Decision 5's invariant is "every route, no exceptions", and it was checked by one hand-written `*_requires_the_bearer_token` test per route. Two lists that must agree, with nothing asserting they do: by 2026-09-06 the router registered 26 paths and 12 had a test — the 14 without included **every** `/study*` route, the newest and largest surface added since the tests were written. Nothing was actually unauthenticated; the *evidence* for the invariant had quietly become half of it.

So the list is no longer written twice. `registered_route_paths()` scans `include_str!("api.rs")` for `.route("` literals, and `every_registered_route_has_an_auth_case` asserts set equality in both directions against a table of `(method, path, concrete URI)` — a registered path with no row fails, and a row for a path no longer registered fails too. Two table-driven sweeps then drive every row through the real router with no `Authorization` header and with a wrong token, expecting `401`. The old individual tests are folded into the table rather than left beside it, since two lists is the shape that drifted in the first place.

Reading the source text rather than the `Router` is not a shortcut: axum exposes no route iterator, so a built `Router` cannot be asked what it serves. The scan asserts it found a plausible number of registrations, so a broken scan fails loudly instead of vacuously passing. **A lexical scan is not a Rust parse, and the residual is one-sided:** a route registered in a form the scan does not match — split across lines by rustfmt, or a router assembled in another file — is invisible to *both* directions of the set-equality check and passes silently, while the `> 20` guard catches only a wholly broken scan. A *reformatted existing* route still fails loudly, through the stale-row direction; **only a newly added one is at risk.** All 22 `.route(` registrations are one contiguous block in `api.rs` today — 23 auth cases, since `/signals` is one line chaining `.get()`/`.post()` (`GET /logs/stream` retired, `tasks/core/021`; the three fixed-channel study-data aliases retired, `tasks/suite/015`) — with no `nest`/`merge`/`fallback` anywhere in the crate, which is what keeps this cheap. **The number in this sentence is prose and nothing checks it**; `DOCUMENTED_ROUTE_COUNT` in `api.rs` is the pinned literal a drift actually fails on. Nothing here touches hardware — `auth_middleware` is a `.layer` on the whole router and rejects before axum routes the request, so no handler runs. `embarch-api` reached the same conclusion for its own machine-readable surface (its decision 54); this is the `embarch-core` half, and neither repo depends on the other for it.

### 46 — `interfaces.md`'s route count is pinned as a literal in `api.rs`, not read across repos
`tasks/core/018` found the router at 27 routes with `interfaces.md` documenting 22 — three rows behind, alongside a missing CLI subcommand in `spec.md` — despite decision 42's own auth sweep deriving its list mechanically from the same source. That mechanism was pointed at auth only; nothing compared the documented surface to the registered one.

The auth sweep's own trick — reading `include_str!("api.rs")` — cannot be pointed at `interfaces.md` the same way: that file lives in a different repo, and under the fleet's one-branch-two-worktrees model (`embarch-fleet/protocol.md` §5) the two repos' worktrees for the same unit of work do not share a parent directory, so any relative path that resolves for a human at a normal two-sibling-checkout desk breaks for a worker with no signal beyond an `include_str!` compile error naming a path nobody touched. Reading the file at runtime rather than compile time has the identical problem, plus a new one: whether the doc repo is even checked out next to this one at test time was never a promised property.

So `api.rs`'s test module carries `DOCUMENTED_ROUTE_COUNT: usize`, a literal hand-counted against `interfaces.md`'s tables, and a test asserting it equals `registered_route_paths().len()` with a message naming both files. It runs one behind `AUTH_CASES.len()` on purpose: `/signals` is one `.route()` call chaining `.get()`/`.post()`, so the scan sees one line where the auth table (and `interfaces.md`) carries two rows. **This is convention backed by a forcing function, not full mechanical enforcement**: the count catches a route added or removed without a matching doc edit, but not a route documented under the *wrong* row, or a doc-only edit that drifts the count back into accidental agreement. Full enforcement would need a doc build step reading both repos in the same process — no such step exists in either repo today, and building one is out of scope for closing three missing rows.

*Rejected:* a relative `include_str!("../../embarch-doc/embarch-core/interfaces.md")` or an equivalent runtime read — works from a normal checkout, breaks silently-until-CI under a worker's worktree pair, and this suite has already paid once for a doc mechanism that only worked in one layout (decision 42's own history, for the router side).

### 60 — The route sweep's other half: each handler declares its own route, and `build_router` is checked against it
Decision 42's sweep measures exactly one property — every route refuses an absent or wrong token — and says nothing about whether a route reaches the handler it is *meant* to reach. A `.route(path, verb(handler))` line with the wrong `handler` identifier (a copy-paste in the router, a path that shadows another) was green under that sweep and stayed invisible; `embarch-core/open.md` carried this as a known gap.

Closing it without hand-writing a second "route → intended handler" table: that table is exactly the thing a copy-paste bug would also get wrong, so agreeing with itself would prove nothing (`embarch-api` decision 54 hit the identical shape and derived from source rather than re-list). Instead, every handler now carries a `// route: METHOD path` comment directly above its own `[pub] async fn` definition — authored once, at the handler, with no view of `build_router`'s line for the same handler. `registered_route_bindings()` derives `(method, path, handler)` from `build_router`'s own `.route(...)` lines (the same scan `AUTH_CASES` draws on, extended to also capture the handler identifier per chained verb); `handler_declared_route()` derives `(method, path)` from the handler's own comment, reading `api.rs` or `study.rs` depending on whether the identifier carries a `study::` prefix. `every_registered_route_reaches_its_intended_handler` requires the two to agree for all 23 verb/handler bindings and names both sides on a mismatch.

**Mutation-verified to decision 46's standard:** swapping two handler identifiers between two `.route()` lines (`resolve_chip_handler` and `enroll_probe_handler`, tried and reverted) turns the new test red, naming the handler, the route it was wired to, and the route its own comment says it answers.

**Not covered:** a route registered in a form the scan does not match (split across lines, assembled outside this one contiguous block) is invisible to this check the same way decision 42 already documents for its own scan; a handler whose `// route:` comment is simply wrong — never checked against a live request — is not caught either, since this is a wiring cross-check between two texts, not a functional test of the handler behind either one. Both handlers stayed hardware-free to check: no probe, serial port or study handler runs, because the comment/registration comparison never invokes the router.

`embarch-core/open.md`'s "route sweep proves rejection, not reach" bullet is struck; this is the reach half.

---
