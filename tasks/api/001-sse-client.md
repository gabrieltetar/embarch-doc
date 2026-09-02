# 001 — Consume Core's `/study/{id}/events` SSE stream from embarch-api

**State:** open
**Source:** [embarch-core/open.md](../../embarch-core/open.md) — "`embarch-api` consumption of `GET /study/{id}/events` (decision 24). The SSE endpoint has no CLI or MCP consumer."
**Scope:** api
**Hardware:** verify-only

## What

`embarch-api` learns to subscribe to `GET /study/{study_id}/events` and surface
`StepCompleted` / `SampleBatch` / `StatusChanged` as they arrive, instead of
polling `GET /study/{study_id}`. Polling stays — this is an addition, not a
replacement. The `event: lagged` frame is a real case Core emits deliberately for
a slow subscriber and must be handled explicitly, not treated as a stream error.

## Why now

Core has broadcast every study event since the endpoint shipped and nothing
consumes it, so `study_status` still tells an agent nothing until a step is over.
It is single-repo, entirely host-side, and the server half already exists and is
deployed — which is what makes it a first worked example for this queue rather
than the most valuable thing in it.

## Done when

- [ ] `embarch-api` subscribes and yields events incrementally.
- [ ] `event: lagged` is handled and reported, with a test that provokes it.
- [ ] A disconnected stream falls back to polling rather than failing the call.
- [ ] Gate green ([embarch-parallel-agents.md](../../embarch-parallel-agents.md) §10).
- [ ] `embarch-api/`'s `spec.md`/`decisions.md`/`open.md` updated; `changelog.d/`
      fragment dropped; `status.d/` fragment if it makes a suite-level fact false.
- [ ] Hardware debt written down: nothing here is proven until a real study runs.
