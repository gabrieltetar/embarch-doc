# 020 — A new `CoreClient` endpoint escapes the bearer sweep, because the sweep is a hand-written list

**State:** claimed by agent/api/020-bearer-sweep-exhaustive, 2026-09-06 02:23
**Source:** [embarch-api/open.md](../../embarch-api/open.md) — "The smoke harness
([decisions](../../embarch-api/decisions/shape.md) 30) is named and unwritten. The six mocked
criteria beside it live in `tests/` ([decisions](../../embarch-api/decisions/shape.md) 46), with
two gaps: the end-to-end half is `#[cfg(unix)]`, and **a new endpoint escapes the bearer sweep
unless its route list grows.**"
**Scope:** api
**Hardware:** none. Everything here runs against `MockCore` in `tests/support/`.
**Owner:** no

## What

`tests/core_client_http.rs`'s `every_outbound_call_carries_the_bearer_token` calls **24
`CoreClient` methods by hand** and asserts each request carried `Authorization: Bearer …`. Its
own doc comment states the problem outright: *"A new endpoint added to `CoreClient` without
`.bearer_auth(…)` is only caught here if the sweep calls it, so this list is meant to stay
exhaustive over the client's networked surface."*

**"Meant to stay exhaustive" is not a mechanism.** This is
`embarch-decision-reversals.md`'s recurring shape — a comment describing a gap is not something
that closes one — and it is a security-relevant one: the failure mode is a route that reaches
Core unauthenticated and no test that fails.

**Make the sweep's exhaustiveness enforced rather than intended**, so that adding a networked
method to `CoreClient` without adding it to the sweep fails a test. **Two shapes, and choosing
between them is part of the task** — record the rejected one in the decision:

- **Structural.** Derive the set of networked methods from the code (a macro that both defines
  the method and registers it; or a test that parses `crates/embarch-core-client/src/**.rs` for
  the request-building call sites and diffs that set against the swept set). Real enforcement;
  a parser is its own maintenance surface.
- **Coverage-by-observation.** Assert the sweep's recorded requests cover every route the client
  can emit, by comparing `mock.requests()`'s `(METHOD, path)` pairs — `tests/support/mod.rs:69`
  says that is already the pair the sweep matches on — against a route inventory the client
  itself exposes. Cheaper, and only as exhaustive as the inventory.

**Whichever you pick, the acceptance test is the same and you must actually run it:** add a
networked method to `CoreClient` that does *not* set the bearer token, confirm the suite goes
red naming it, then revert. A mechanism that has not been watched fail is a mechanism nobody has
tested — that is this suite's own repeated finding, and `umbrella/019` is the most recent one.

**Out of scope, deliberately:** the `#[cfg(unix)]` half of the same open-question bullet. It is
a Windows-build problem and `tasks/doc/012` records that no Linux leg can run a native Windows
build at all. Leave that clause in `open.md`, narrowed to say the sweep half is closed.

## Why now

`decisions/shape.md` 46 put these six criteria in `tests/` precisely so they would be checked by
something rather than asserted; this is the one of the six whose check does not hold itself
together. It is a pure test-side change in one repo with no wire, no schema and no hardware.

## Reserve, at dispatch — read this before you plan

**Nothing in `embarch-api` is in reserve, and everything you would write to is close to it.**
The reserve line for a `decisions/*.md` is **11,059 B** (90% of the 12,288 cap):

- `decisions/zephyr.md` — **11,056 B. 3 bytes.** Do not write here; nothing in this task belongs
  here anyway. Noted because leg 015 put an `embarch-api` decision in the wrong topic file with
  96 bytes of headroom left, and this is the file it happened to.
- `decisions/shape.md` — 10,305 B, **754 bytes of headroom.** This is where your decision
  belongs (30 and 46 are here). It probably fits; if it does not, **file
  `tasks/api/021-compact-api.md`** in the same commit, per `tasks/README.md`. Note the path is
  `tasks/api/`, **not** `tasks/doc/` — `check-ownership.py` refuses `tasks/doc/**` to you.
- `decisions/surface.md` 10,928 (131 B), `decisions/build.md` 10,934 (125 B),
  `interfaces/config.md` 11,008 (51 B), `decisions/core-link.md` 10,879 (180 B). All one
  paragraph from reserve. **Do not spread a decision across them to stay under the line** — that
  is the exact failure `DOC-COMPACTION.md` §2 names.
- `embarch-api/open.md` is 3,957 / 5,120 with room, and your edit there **shrinks** it.

## Done when

- [ ] Adding a networked `CoreClient` method that omits `.bearer_auth(…)` makes the test suite
      fail and names it — **demonstrated by actually doing it and reverting**, and the report
      says what the red output looked like.
- [ ] The existing 24-call sweep still passes and still asserts the token is not leaked into the
      request target.
- [ ] A decision entry in `embarch-api/decisions/shape.md` naming the mechanism, the rejected
      alternative, and what it still does not cover.
- [ ] `embarch-api/open.md`'s bullet narrowed: the bearer-sweep clause closed, the
      `#[cfg(unix)]` clause and the unwritten smoke harness left standing.
- [ ] `changelog.d/` fragment.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
