# 022 — 9 of `CoreClient`'s 25 routes set the bearer token by hand, and a comment says none do

**State:** blocked
**Source:** `api/020`'s reviewer, 2026-09-06, which found this while verifying decision 54 and
explicitly left the filing to the supervisor.
**Scope:** api
**Hardware:** none. `crates/embarch-core-client` and its tests; no board, no live Core.
**Owner:** no

## What

`.bearer_auth(…)` appears at **11 sites** in `crates/embarch-core-client`: 2 inside the
`send` / `send_no_content` funnels, and **9 hand-written** — `client.rs` lines 1030, 1109, 1226,
1267, 1310, 1456, 1512, 1549, and `study_events.rs:419`. Those nine bypass the funnels because
they need typed `404`/`409` handling, or because they stream.

**`client.rs:786`'s own comment says the opposite**: *"every other route gets it applied for it
by `send`/`send_no_content`, and that stays the rule."* That is untrue of 9 of 25 methods, and
it is the kind of sentence a later reader takes as an invariant.

**Fold those nine into the funnels** — a `send` variant that returns the response for typed
status handling rather than consuming it, and whatever `open_study_events` needs to stream —
so the token is applied by construction on every route. Then the comment becomes true, and
`api/020`'s sweep becomes a guard on a funnel rather than a sweep over 25 hand-written sites.

**This is the move `embarch-api/decisions/surface.md` decision 24 already made elsewhere** —
`json_out` as a single funnel, "unconditional by construction, not by convention", with a guard
test that fires if a second serializer appears. Same shape, applied to auth.

## Why blocked

**`embarch-api/decisions/shape.md` is at 12,281 / 12,288 B — 7 bytes.** This task ships a
decision and there is nowhere in `embarch-api/decisions/` to put one:
`zephyr.md` 11,056 (3 B from its reserve line), `interfaces/config.md` 11,008 (51 B),
`build.md` 10,934 (125 B), `surface.md` 10,928 (131 B), `core-link.md` 10,879 (180 B).

**Unparks when `tasks/api/021-compact-api.md` lands** — its mission split of `shape.md`
(scope-and-boundaries vs test reach) is what buys the room. Do not dispatch this before then;
a worker sent at it now meets the cap mid-flight, which is exactly how an `embarch-api` decision
ended up in the wrong topic file on 2026-09-05.

## Not a security bug today, and say so wherever this is cited

All 25 routes **do** send the token — `api/020`'s sweep proves it by observation on every one.
This is about the mechanism being convention rather than construction, and about a comment that
misdescribes it. Nothing is currently unauthenticated.

## Do not take the tempting shortcut

**`default_headers` on the `reqwest::ClientBuilder` is not this task**, and `api/020` rejected
it for a reason that still stands: `base_url = "auto"` probes a candidate list, so a header
attached to *every* request this client makes turns "no auth, refused, loudly" into "token sent
somewhere it should not be, silently". The funnel keeps the token attached per-route.

## Done when

- [ ] No `.bearer_auth(…)` call site outside the funnels, or each survivor is named with why it
      cannot be folded.
- [ ] `client.rs:786`'s comment is true as written, or rewritten to be.
- [ ] A guard test that fires if a new route builds a request outside the funnels — the
      decision-24 shape, not a second hand list.
- [ ] `api/020`'s `the_sweep_calls_every_networked_method` still passes, and the red
      demonstration is re-run against the new structure.
- [ ] A decision entry, and `embarch-api/open.md` updated if this changes what that file claims.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
