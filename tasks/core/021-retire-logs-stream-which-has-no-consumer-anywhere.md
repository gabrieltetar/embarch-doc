# 021 — `GET /logs/stream` has no consumer anywhere, and the UI decision that was going to be its consumer decided against it

**State:** claimed — leg 068, `agent/core/021-retire-logs-stream`

**Dispatch note, leg 068 — retire it. The direction is decided; do not re-open it.**

The task left two ends open ("retire, or give the Debug tab a reason to subscribe"). I am closing it
as **retire**, on the argument already written in the task and not on my own new reasoning:
`embarch-ui` decision 13 structurally excludes an SSE source by sharing one poll/diff loop across
both log sources, nothing has replaced it, the whole-suite grep found no caller in any of the nine
repos, `embarch-core-client` has no method for it, and `embarch-topology` decision 19 already set
the precedent of retiring live push in favour of a poll. `/logs/recent`'s 2 s poll is the live path
and nobody has asked for it faster.

**What to remove**, per the task's own count of seven moving parts: the `GET /logs/stream` route
registration (`src/api.rs:87`), `logs_stream_handler` and its SSE plumbing (`:1317`), `logs.rs`'s
poll-follow `FollowState`/`poll_in` machinery, the route auth sweep's row for it, and `open.md`'s
bullet. **Keep `read_recent`/`tail_lines`** — `/logs/recent` uses them and stays.

**Decision 44 gets a tombstone, not a deletion.** Its subject is the hold-past-`\n` rule and the
first-tick/rotation anchor exception on this surface. With the surface gone the rule governs
nothing, so retire it to `embarch-core/decisions/removed.md` (this repo's convention for a retired
decision) carrying its own reasoning verbatim plus one sentence saying which unit retired it and
why. Do not renumber anything. If `decisions/removed.md` does not exist in this sub-project, say so
in your report and put the tombstone at the end of `decisions/logging.md` marked retired rather than
inventing a file layout.

**Read decision 44 before you delete anything.** It opens by explicitly declining to reason from
consumer absence — *"what a consumer could hold rather than ... who is watching"* — so it is not
itself an argument to keep the route, but that distinction belongs in the tombstone.

**Two things I know and you should not have to rediscover.** First, `embarch-core` is the one repo
whose native Windows build this environment cannot run; `tasks/core/015` is that debt and it is the
owner's. Run `cargo build`, `cargo test` and `clippy --all-targets -- -D warnings` on Linux and say
plainly in your report that the Windows build was not attempted. Second, the third `Done when` box
asks that the route auth sweep's row count match the router's — check that number after your
deletion rather than assuming the sweep is generated.

**Doc-size reserve in your scope:** `embarch-core/open.md` is 4,813/5,120 B (**307 B left**, filed
against `tasks/core/022-compact-core.md`, which is `open`, not blocked). You are *removing* a bullet
from that file, so you should be paying this debt down rather than spending it — if you leave it in
reserve anyway, note that in your report; if you push any other file into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit.
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
