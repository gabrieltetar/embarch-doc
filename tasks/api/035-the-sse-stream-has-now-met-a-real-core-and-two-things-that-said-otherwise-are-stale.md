# 035 — The study event stream has now met a real `embarch-core`, and three things still say it has not

**State:** done — leg 072
**Source:** observed by the supervisor on leg 021 while running `tasks/api/029` on the bench, 2026-09-06
**Scope:** api
**Hardware:** none to write this up; **one live study to re-observe**, and the boards were attached when it happened
**Owner:** no

## What was observed

Running `study_watch` against a real, installed `embarch-core` on study
`4d7bcc93cb38f7d01fae509a790d22bd`, the call returned:

```json
{ "transport": "live",
  "events": [ { "type": "transport", "mode": "live",
                "detail": "subscribed to GET /study/{id}/events" },
              { "type": "event", "event": { "kind": "StepCompleted",  "step_index": 0, … } },
              { "type": "event", "event": { "kind": "StatusChanged", "status": "completed" } } ],
  "lagged": null, "timed_out": false }
```

**Those are pushed frames from a live Core, not a mock and not a poll.** The
contrast is visible in the same session: an earlier, faster study on the same
Core returned its status as `{"type": "polled"}` because it finished before any
frame arrived, and `transport` still read `live`. So both the subscription and
the fallback are observable from the outside, and one of them has now run for
real.

## What is stale because of it

1. **`embarch-api/open.md`** — "**The study event stream has never met a real
   embarch-core.** `study-status --follow`/`study_watch` (decisions 48, 49) run
   only against a mock whose frames *copy* the wire format, so nothing tests the
   coupling." The first sentence is now false for `study_watch`. **Say precisely
   what is still true** rather than deleting the bullet: `study-status --follow`
   is a different call site and was not exercised, and neither was the drop path,
   the `lagged` frame, or a reconnect.
2. **`tasks/api/026-compact-api.md` is `blocked` on exactly this premise.** Its
   `In flux: yes` reads "the event-stream half of this file (decisions 48, 49)
   has never met a real `embarch-core`", and it parks the compaction of
   `embarch-api/decisions/core-link.md` — **which is at 12,266 of 12,288 bytes,
   22 bytes left, the tightest file in the suite.** Re-read that premise against
   what ran. If the live run confirms 48/49 rather than contradicting them, the
   reason for parking is weaker than it was.
3. **`tasks/api/001-sse-client.md` does not exist.** Both `open.md`'s bullet and
   `026`'s unparking condition name it as the debt that closes this, and there is
   no such file in `tasks/api/`. **So `026`'s stated unpark condition can never be
   met by the mechanism as written** — nothing will ever land a task that is not
   in the queue. Either re-file it with what is genuinely still unobserved, or
   change `026`'s condition to name something real.

## Why this matters more than its size

`core-link.md` at 22 bytes is not a ledger entry, it is a wall: **the next
`embarch-api` decision cannot be written where it belongs**, and the documented
failure mode is that it gets written in the wrong topic file instead and nothing
fails (`DOC-COMPACTION.md` §2 — `embarch-api` did exactly that on 2026-09-05 with
96 bytes left). The only thing standing between the queue and that outcome is a
`blocked` state resting on a premise this leg made partly false, pointing at a
file that is not there.

## Done when

- [x] `open.md`'s bullet says what was observed and what was not, with provenance.
- [x] `026`'s `In flux:` is re-judged against the live run and its unpark
      condition names something that exists — `tasks/api/059-sse-client-remaining-observations.md`,
      filed by this task, replaces the never-filed `tasks/api/001-sse-client.md`.
- [x] `026` stays `blocked`, now for the honest reason: `spec.md`/`open.md` are
      still both inside their own reserve lines and neither has been compacted
      by this unit — unrelated to the event stream, which is resolved for
      `core-link.md`/`study-events.md` as far as `study_watch` goes.
- [x] `core-link.md` was not compacted by this task.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — 11/11 doc checks,
      `cargo build`/`test`/`clippy --all-targets -D warnings` clean in
      `embarch-api` (no code changed by this unit).
