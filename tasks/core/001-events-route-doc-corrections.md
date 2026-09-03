# 001 — Correct two facts about `GET /study/{id}/events` in embarch-core's docs

**State:** open
**Source:** found while building `embarch-api`'s consumer of that route (`tasks/api/001-sse-client.md`); both facts read out of `embarch-core/src/study.rs`
**Scope:** core
**Hardware:** none

## What

Two statements in `embarch-core`'s own docs about its SSE route are wrong, and
an `embarch-api` worker cannot fix them — they are another sub-project's docs
(`embarch-parallel-agents.md` §3).

1. **`embarch-core/interfaces.md` line 47 lists three event kinds; Core emits
   four.** `StudyEvent` in `src/study.rs` has `StepCompleted`, `SampleBatch`,
   **`GattTranscript`** and `StatusChanged`, and `event_study_id` matches all
   four. A client written from that row alone would not decode transcript
   entries at all.
2. **`embarch-core/open.md` says "The SSE endpoint has no CLI or MCP
   consumer."** It has both as of this batch: `embarch-api`'s
   `study-status --follow` and its `study_watch` tool
   (`embarch-api/decisions/core-link.md` 48, 49). That line is the `Source:` of
   `tasks/api/001-sse-client.md` and should be removed or rewritten to whatever
   is still open about the route.

Worth considering alongside them, but a decision rather than a correction:
the route serves no `Last-Event-ID` and the broadcast channel keeps no replay,
so a disconnected subscriber cannot resume without a silent hole. `embarch-api`
handles that by falling back to polling and saying so. If Core ever wants
resumable subscribers that is a Core-side design, and stating the absence in
`interfaces.md` would stop the next client from assuming otherwise.

## Why now

The first is a wire-format fact a consumer is now depending on, and it was wrong
in the doc a consumer would read. The second is a queue-hygiene fact: the task
queue is a view of the `open.md` files (`embarch-parallel-agents.md` §4), so a
line left saying something untrue can be re-dispatched as new work.

## Done when

- [ ] `embarch-core/interfaces.md`'s `/study/{id}/events` row names all four
      `StudyEvent` kinds, `GattTranscript` included.
- [ ] `embarch-core/open.md` no longer claims the endpoint has no consumer.
- [ ] A decision taken on whether the no-replay/no-`Last-Event-ID` property is
      stated in `interfaces.md`, or deliberately left unstated.
- [ ] Gate green (`embarch-parallel-agents.md` §10).
- [ ] `changelog.d/` fragment dropped if anything reader-facing changed.
