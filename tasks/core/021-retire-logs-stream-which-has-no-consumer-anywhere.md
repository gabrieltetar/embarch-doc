# 021 — `GET /logs/stream` has no consumer anywhere, and the UI decision that was going to be its consumer decided against it

**State:** open
**Source:** suite review pass 2026-09-06, dimension 6 (deletion candidates). Code-confirmed, with a whole-suite caller grep.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-core/src/api.rs:87` registers `GET /logs/stream`; `:1317` is its handler.
`embarch-core/open.md:12` already says *"`GET /logs/stream` has no consumer, and its torn-write
path has never met a real tear."* What that bullet does not say is that the route's only intended
consumer has since decided against the shape.

`embarch-ui/decisions/debug-tab.md` decision **7** built it: *"Core gains a live-tail SSE route
*and* a recent-lines route, so the tab has backlog on first open rather than starting blank."*
Decision **13**, in the same file, orphaned it: `embarch-api`'s logs must be read from a rolling
file because *"the record outlives the process, which no endpoint-based design can offer here"*,
and therefore *"**The poll/diff loop is shared; only the fetch differs.**"* A shared poll/diff loop
across both sources structurally excludes an SSE source. Nothing has replaced it.

Grepped all nine repos plus the doc corpus for `logs/stream` and `logs_stream`: every hit is
inside `embarch-core`, its own docs, or the fleet's supervisor log. `embarch-core-client` has **no
method** for it — enumerating its 27 `pub fn`s and route-format strings, `/logs/stream` is one of
only two registered Core routes with no client method. `embarch-ui` calls `core.logs_recent(`
only. No MCP tool, no CLI subcommand, no `EventSource` in `app.js`.

Retiring it removes, counted: the route registration; `logs_stream_handler` and its SSE plumbing;
`logs.rs`'s poll-follow `FollowState`/`poll_in` machinery (`/logs/recent` uses
`read_recent`/`tail_lines`, which are separate and stay); one row of the route auth sweep; **an
entire numbered decision** — `embarch-core/decisions/logging.md` decision 44, whose whole subject
is a hold-past-`\n` rule on this surface plus a first-tick/rotation anchor exception; and
`open.md`'s bullet. **Seven moving parts.**

Note what decision 44 actually says, because it is the closest thing to a keep: it opens *"Why
hold rather than publish, when `/logs/stream` has no consumer today"* and then deliberately argues
from *"what a consumer could hold rather than from who is watching."* That is a decision about the
**rule**, explicitly declining to reason from consumer absence — not a decision to keep the route.

Candidate direction: retire the route and decision 44 with it, or give the Debug tab a reason to
subscribe — but **record which**, because the current state is a documented invariant with no
reader. Retiring is the smaller suite: `/logs/recent`'s 2 s poll is already the live path, nobody
has asked for it faster, and `embarch-topology` decision 19 used exactly this argument to retire
live push in favour of a 5 s poll.

## Why now

Whoever next touches Core's log rotation or tailing must reason about a torn-write anchor and a
hold-past-newline rule for a subscriber that does not exist. Nothing catches it: `check-docs.py`
reads shapes, and the one review that surveyed the consumers was scoped by its supervisor to
"retain the partial vs just fix the comment" — retirement was never on the table
(`embarch-fleet/supervisor-log.md:735-745`).

## Done when

- [ ] `GET /logs/stream` is gone, or `embarch-core/decisions/logging.md` records what will consume
      it and by when.
- [ ] Decision 44 either goes with it or states which surface its rule now governs.
- [ ] The route auth sweep's row count matches the router's, and `embarch-core/interfaces.md`
      matches both.
- [ ] `embarch-core/open.md`'s bullet is closed.
- [ ] `status.d/core-*` fragment for `embarch-ui/decisions/debug-tab.md` decision 7's mention.
- [ ] Gate green; `changelog.d/core-*` fragment.
