# `FollowState::poll_in` can split one log line across two SSE frames, and its doc comment says it cannot

**State:** done by agent/core/006-follow-partial-line, 2026-09-06
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

- [x] A partial write emits nothing on the tick that sees it, and exactly one complete line on the
      tick after the write finishes — or `decisions.md` records why not.
- [x] The `poll_in` doc comment describes the rule the code actually implements.
- [x] The existing three follow tests pass unchanged.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Outcome

**Resolved by implementing the retention**, not by narrowing the comment —
`embarch-core/decisions/logging.md` decision 44 has the reasoning. `poll_in`
now reads bytes, advances `self.offset` only past the last `\n` it read, and
leaves the trailing partial in the file to be re-read next tick; no buffer and
no new field, so there is no retained state to drift. The byte read also makes
the UTF-8 half of the old comment true by construction rather than asserted,
since `0x0A` cannot occur inside a multi-byte sequence.

**One case is knowingly left open and now stated in the comment instead of
claimed away:** the offset anchor taken at rotation-detection time is the
file's length, which a rotation tick landing inside a torn write would leave
mid-line. Closing it needs a flag carried across ticks; the cost of not
closing it is one short line.

New test `follow_state_holds_a_trailing_partial_line_until_its_newline_arrives`
was proved able to fail: with the old `read_to_string`/advance-to-EOF body
restored it panicked at "a line with no newline yet is not a line — it must not
be published", the other three follow tests passing alongside it. Fix restored,
`cargo test` 162 passed / 0 failed / 2 ignored, clippy `--all-targets -D
warnings` clean.

`status.d/`: none — no suite-level fact changed. `features.d/`: none — the live
tail was already `Shipped` and its maturity did not move. Dropped
`inbox/ui-spec-claims-logs-stream.md`: `embarch-ui/spec.md:32` claims the UI
reaches Core over `GET /logs/stream`, and it does not.
