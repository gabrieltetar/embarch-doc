# 114 — Put the three /signals/{name}/capture routes under the auth sweep and the route-count pin

**State:** open
**Source:** reviewer finding on core/100 (code 845f3ea, doc c43051a8): decisions 42 and 46 (embarch-core/decisions/route-sweep.md) contradicted by the new route registration; filed from `inbox/core-capture-routes-outside-auth-sweep.md` by the 2026-10-26 05:14 leg
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`core/100` registered `/signals/{name}/capture` as a multi-line `.route(` call (`src/api.rs` ~line 162, `.route(` then the path on the next line). Decision 42's `registered_route_paths()` matches only lines that start with `.route("`, so the new registration is invisible to both directions of `every_registered_route_has_an_auth_case`. The diff adds no `AUTH_CASES` rows for POST/GET/DELETE `/signals/{name}/capture`, and `DOCUMENTED_ROUTE_COUNT` (decision 46) stays 32 while `interfaces/topology.md` now documents three more rows. Decision 42 names this exact residual ("a route registered in a form the scan does not match ... only a newly added one is at risk"), so the gate stayed green with the invariant unproven for three routes and the count pin stale.

Fix forward: put the registration on one line (or add a row-by-row case), add the three `AUTH_CASES` rows, move `DOCUMENTED_ROUTE_COUNT` to match, and make the scan fail loudly on a bare `.route(` line.

## Why now

Decision 5's "every route, no exceptions" is the invariant; the sweep is its evidence, and it silently covers fewer routes than the router serves. Auth is a whole-router layer, so no actual hole is known; this is lost evidence, not a vulnerability. The supervisor confirmed the finding against `embarch-core@845f3ea` (`src/api.rs:162-165`, `DOCUMENTED_ROUTE_COUNT` at `:2501`).

## Done when

- [ ] `AUTH_CASES` has the three capture rows and the sweep fails if they are removed.
- [ ] `DOCUMENTED_ROUTE_COUNT` equals the documented rows.
- [ ] A `.route(` line the scan cannot parse fails the test.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `decisions/route-sweep.md` amended if the scan's rule changes; `changelog.d/` fragment only if reader-facing. `embarch-core/spec.md` and `open.md` are in reserve under `tasks/core/112`: do not grow them.
