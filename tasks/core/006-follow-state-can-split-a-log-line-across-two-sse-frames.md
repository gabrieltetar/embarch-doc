# `FollowState::poll_in` can split one log line across two SSE frames, and its doc comment says it cannot

**State:** open
**Source:** owner's repo survey, 2026-09-06 — a comment asserting an invariant the code does not hold
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`src/logs.rs:113-119` claims "Offsets always land exactly after a `\n` … so a read from `offset` is
always UTF-8-boundary-clean, not liable to split a line in half." `logs.rs:141-146` then does
`read_to_string` to EOF and `self.offset += read`, so if the tick lands mid-write the offset stops
mid-line, `buf.lines()` publishes the partial as a complete line, and the remainder arrives as a
second "line" next tick. `src/api.rs:1051-1055` forwards whatever comes back as a `lines` SSE event.
The three follow tests (`logs.rs:206-269`) only ever append whole lines.

`poll_in` should advance the offset only to the last `\n` it read and hold the trailing partial for
the next tick. **The doc comment must end up describing what the code does**, whichever way this is
resolved.

The race is narrow — a poll landing inside a `tracing-appender` write — so the strongest half of
this task is the comment. If the retained-remainder change turns out to cost more than it buys, say
so in `decisions.md` and fix the comment; do not leave the claim standing either way.

## Why now

`spec.md` §4 makes `logs.rs` "one implementation behind the CLI and both HTTP routes". A comment
asserting an invariant the code does not have is a claim a later reader builds on.

## Done when

- [ ] A partial write emits nothing on the tick that sees it, and exactly one complete line on the
      tick after the write finishes — or `decisions.md` records why not.
- [ ] The `poll_in` doc comment describes the rule the code actually implements.
- [ ] The existing three follow tests pass unchanged.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
