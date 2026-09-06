# 022 — 9 of `CoreClient`'s 25 routes set the bearer token by hand, and a comment says none do

**State:** open
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

## Unparked 2026-09-06 by `api/023` — and where your decision goes

This was `blocked` because `decisions/shape.md` was 7 bytes under its cap and there was nowhere
in `embarch-api/decisions/` to put a new entry. **`api/023` split it**: `shape.md` is now
7,654 B and the new `decisions/tests.md` 5,434 B, both far clear.

**Your decision goes in `decisions/core-link.md`** — the shared-client file, decisions 11, 14,
15, 17, 26, 36, 37, 38, 43, 48, 49 — **and that file is at 10,879 B against a reserve line of
11,059, so you have 180 bytes before you owe a compaction task.** Plan for owing one and file it
at `tasks/api/<NNN>-compact-api.md`; **not** `tasks/doc/`, which `check-ownership.py` refuses to
you. `decisions/tests.md` is the roomy file and it is the wrong home — this is a change to the
client, not to how far the tests reach.

The rest of `embarch-api`'s decision corpus is still narrow (`zephyr.md` 11,056 against 11,059;
`interfaces/config.md` 11,008; `build.md` 10,934; `surface.md` 10,928) and is recorded as a
standing hazard in [open.md](../../embarch-api/open.md). **Do not solve your own headroom by
putting the entry in whichever file has room** — leg 015 did that with 96 bytes left and it is
the reason that bullet exists.

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
