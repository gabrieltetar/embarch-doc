# 001 — Consume Core's `/study/{id}/events` SSE stream from embarch-api

**State:** claimed by agent/api/001-sse-client, 2026-09-02 22:34
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

- [x] `embarch-api` subscribes and yields events incrementally.
- [x] `event: lagged` is handled and reported, with a test that provokes it.
- [x] A disconnected stream falls back to polling rather than failing the call.
- [x] Gate green ([embarch-parallel-agents.md](../../embarch-parallel-agents.md) §10).
- [x] `embarch-api/`'s `spec.md`/`decisions.md`/`open.md` updated; `changelog.d/`
      fragment dropped; `status.d/` fragment if it makes a suite-level fact false.
- [x] Hardware debt written down: nothing here is proven until a real study runs.

## What shipped

`embarch-core-client` grew `sse.rs` (a byte-fed SSE decoder, no I/O) and
`study_events.rs` (`StudyEvent` mirror, `StudyEventStream`, `follow_study` with
a polling fallback). `embarch-api` grew `study-status --follow`
(`--follow-timeout`, NDJSON under `--json`) and the `study_watch` MCP tool.
Design: [embarch-api decisions](../../embarch-api/decisions/surface.md) 47 and
[48, 49](../../embarch-api/decisions/core-link.md). Surface:
[tools.md](../../embarch-api/interfaces/tools.md).

16 tests in `tests/study_events_sse.rs`, all against a loopback mock.

## Hardware-verification debt

**Nothing below has run against a real embarch-core, and none of it can be
closed without a board.** The mock's frames are reproduced from `axum`'s own
`Event::field` writer and `KeepAlive::DEFAULT_KEEP_ALIVE`, and its JSON from
Core's `StudyEvent` — a *copy* of the wire format, which passes just as green
whether or not the copy is right.

**Rig:** the deployed Windows-service Core, the dev bench, and a DUT — the same
one a normal `run_study` needs. `embarch-api` from this branch, in WSL2.
Nothing here needs a new fixture beyond a study that captures samples.

1. **The happy path.** Submit any multi-step study, then
   `embarch-api study-status <id> --follow` in another terminal. Expect a
   `[live]` line, one `[step N]` line per step **as it completes rather than at
   the end**, and a terminal `[status]`. *Proves:* the frames Core really sends
   decode — the single assumption every mocked test rests on.
2. **`--json` against a real stream.** Same run, `--json`, piped through a
   line-by-line JSON reader. *Proves:* no real frame breaks NDJSON — notably a
   `StepCompleted` carrying `gatt_services`, which the mock's fixture omits
   because it is `#[serde(default)]`, and a `GattTranscript`, which the mock
   never sends at all.
3. **`lagged`, provoked for real.** The one thing the host-side tests
   structurally cannot do. Run a study with a **power tap** (high sample rate),
   follow it, and make the subscriber fall behind Core's broadcast buffer —
   easiest with `study_watch { include_samples: true, max_events: 1000 }` over
   MCP, or by suspending the CLI follower (`Ctrl-Z`) for a few seconds mid-run
   and resuming. Expect a `[lagged]` line naming a count, the stream continuing
   afterwards, and exit 0. *Proves:* Core's real lagged frame parses, and that
   what this treats as a reportable fact is the thing Core actually emits. **If
   no realistic study can outrun the buffer, that is worth recording too** — it
   would mean `lagged` is unreachable in practice, not that it is handled.
4. **A real disconnect mid-study.** Follow a running study, then restart Core
   (or drop the link). Expect a `[polling]` line naming the reason, polling to
   pick up the terminal status, and **exit 0**. *Proves:* the fallback fires on
   a real transport failure rather than only on a mock's `StreamTail::Cut`.
5. **Keep-alive over a genuinely idle stretch.** Follow a study with a step that
   sits idle for **over 45 seconds** (`FollowOptions::idle_timeout`) with no
   event. Expect the follow to survive on Core's keep-alive comments alone.
   *Proves:* the one constant here that is `[assumed]` — 45 s against `axum`'s
   15 s default keep-alive, read out of Core's dependency rather than measured
   against the deployed build. **If Core's keep-alive is configured or absent,
   this is where a long BLE step silently becomes a spurious fallback.**
6. **`study_watch` from an agent.** Call it over MCP against a running study
   with default arguments; check `complete`, `transport`, and that
   `sample_batches` counts rather than lists. *Proves:* the bound that makes the
   tool safe to call is real against a study's real event rate.

**Also not proven, and cheaper to note than to test:** `GattTranscript` decodes
(no mock sends one; step 2 covers it incidentally), and Core's `encode-error`
frame (unreachable by construction — it needs Core to fail serializing an event
it already holds).
