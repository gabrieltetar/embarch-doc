# 045 — The route sweep proves rejection, not reach: a route wired to the wrong handler passes it

**State:** open
**Source:** `embarch-core/open.md` — "**The route sweep proves rejection, not reach.** Decision 42
asserts all 26 registered routes answer `401` without a token and with a wrong one; only `/status`
asserts a *correct* token reaches its handler. A route wired to the wrong handler is not caught".
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Decision 42's sweep is a real mechanism and it measures exactly one property: **every route
refuses an absent or wrong token.** It says nothing about whether a route reaches the handler it
is supposed to reach. A route registered against the wrong handler — a copy-paste in the router, a
path that shadows another — is green under the sweep today, and green is what anyone reads.

Add the other half: for each of the 26 registered routes, an **authorized** request reaches its
**intended** handler. The cheapest honest shape is likely a wiring-level assertion rather than 26
live calls — a table derived from the router's own registration, the way `embarch-api` decision 54
derives its bearer sweep from the source rather than from a hand-kept list. **Derive it; do not
hand-write a second list of 26 routes**, because a hand-kept list is the failure decision 54 spent
a whole mechanism escaping and this is the same shape.

## Why now

`embarch-core/open.md` has carried this as a known gap, and it is the one blind spot behind a check
that currently reads as full route coverage. No hardware is involved: a wrong-handler wiring bug is
visible entirely on the host.

## Done when

- [ ] Each of the 26 registered routes has an assertion that an authorized request reaches the
      handler that route is meant to reach, and the route set is **derived from the router's own
      registration**, not re-typed.
- [ ] Mutation-verified to decision 46's standard: swapping two routes' handlers turns the new
      check red and names them.
- [ ] `embarch-core/open.md`'s bullet is struck, or narrowed to whatever genuinely remains.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green; gate green;
      `changelog.d/` fragment.
