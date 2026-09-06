# 022 — 9 of `CoreClient`'s 25 routes set the bearer token by hand, and a comment says none do

**State:** done — agent/api/022-bearer-auth-funnels, 2026-09-06
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

- [x] No `.bearer_auth(…)` call site outside the funnels, or each survivor is named with why it
      cannot be folded. **Zero survivors.** All eleven sites collapse to one, inside a new
      `CoreClient::dispatch(request, timeout: Option<Duration>)` that applies the token, applies
      the timeout and sends. `send`/`send_no_content` are now readers over it; the nine typed
      routes and `open_study_events` pass it a `RequestBuilder` and read the status themselves.
      `timeout: None` is the streaming case, which is what the SSE route actually needed.
- [x] `client.rs:786`'s comment is true as written, or rewritten to be. **The method it sat on is
      gone**: `bearer_token()` is retired, so nothing outside `dispatch` can reach the token at
      all. `http()` survives — `study_events` still builds its own request — with its doc saying
      it carries no credential.
- [x] A guard test that fires if a new route builds a request outside the funnels — the
      decision-24 shape, not a second hand list. `every_outbound_request_is_sent_through_the_one_funnel`
      in `tests/core_client_http.rs`, over the same lexical scan `api/020` built: exactly one
      `.bearer_auth(…)` in the crate, and no `.send()`/`.execute(` outside `dispatch`.
- [x] `api/020`'s `the_sweep_calls_every_networked_method` still passes, and the red
      demonstration is re-run against the new structure. It passes untouched — every route still
      builds its own `self.client.<verb>(…)`, so the scan sees the same 25 methods. Three
      mutations, each reverted: **drop `.bearer_auth` from `dispatch`** → the new guard red on
      `found 0`, the sweep red on `GET /status went out without the bearer token`;
      **add a route that sends its own request** → the new guard red naming
      `client.rs:833 (in mutation_probe)`, the sweep's exhaustiveness test red naming
      `mutation_probe`; **re-introduce a hand-written `.bearer_auth` on `remove_signal`** → the
      new guard red naming that line. The second is the one that matters: the old sweep could
      only say "you forgot to call it", the guard says which line is wrong.
- [x] A decision entry, and `embarch-api/open.md` updated if this changes what that file claims.
      Decision 55 in `decisions/core-link.md`, as directed. `open.md`'s bearer bullet and its
      headroom bullet both moved; `spec.md` §6 gained the funnel; decision 54 in
      `decisions/tests.md` gained an amendment saying the sweep now measures a mechanism.
- [x] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

## What this cost, and what it did not

**The entry took 1,387 B of `core-link.md`'s 1,409.** The file is now 12,266 B against a 12,288 B
cap — in reserve, with `tasks/api/026-compact-api.md` filed in this commit. `In flux: yes` there,
blocked on `api/001`: decisions 48/49's event stream has still never met a real Core, and
shortening them now would state as settled the thing that run exists to test. The task names the
verbatim split as the move that is *not* blocked.

**Nothing outside this repo sees a change.** `dispatch`, `http()` and the retired `bearer_token()`
are all `pub(crate)`; no `pub` signature moved, no wire byte moved, no error string a caller
renders with `{}` moved. `embarch-ui`, which path-deps this crate, recompiles unchanged.

**No hardware-verification debt.** The property under test is which header goes out, and
`MockCore` observes that on a loopback socket.
