# 137 — Make `study-status --follow` and `study_watch` end on an unknown or interrupted study instead of waiting forever

**State:** claimed by agent/api/137-study-follow-ends-on-unknown-or-interrupted-study, 2026-10-26 02:57
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-api finding 1), verified by Opus against embarch-api@6d664853
**Scope:** api
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 leg

**Doc reserve in `embarch-api/`:** `decisions/client-crate.md` is 11,581 / 12,288 B (707 B left),
filed as `api/140` (open, not yours). Decision 48 lives in `decisions/study-events.md`, which is not
in reserve; amend it there or add the new decision there, and keep out of `client-crate.md`. If your
work pushes any other `embarch-api/` file into reserve, file `tasks/api/<NNN>-compact-api.md` in the
same commit. `ui/082` (the live-run badge on this same `follow_study` path) is **not** running this
leg, so you are the first of the pair. `embarch-core-client` is path-depended on by `embarch-ui` and
`embarch-umbrella`: keep its public API source-compatible, or say plainly in your report what a
consumer must change. Never edit `embarch-core`; the Core line numbers above are context only.
Never touch the live Core.

## What

`follow_study` subscribes first, then polls once, and treats only `completed` and `failed` as terminal. Two inputs that can never produce a terminal event therefore follow forever. The first is a `study_id` Core has no record of: Core's `/study/{id}/events` handler opens a stream for any id without looking it up, and its keep-alives hold the client's 45 s idle timeout open. The opening poll's 404 is logged at `debug` and dropped once a stream is open. The second is a study Core reports as `interrupted`: a `.partial` record with no job behind it, which Core will not move off by itself. Without `--follow-timeout`, the CLI never exits. With the MCP `study_watch`, every window returns `complete: false` and the description tells the agent to call again.

When this is done, a follow whose opening poll says the study does not exist ends with an error naming the id, and `interrupted` ends a follow as its own outcome, never rendered as `completed` or `failed`. One direction to consider: make a 404 from the opening poll fatal even with a stream open, and let only non-404 poll failures keep following live. Also add `interrupted` to `is_terminal_status`, or to a sibling that both call sites use. The CLI exit code and the MCP `complete`/status fields for `interrupted` are the worker's call, as long as they are documented.

## Why now

- `crates/embarch-core-client/src/study_events.rs:212`: `is_terminal_status` is `completed | failed` only.
- `study_events.rs:606-616`: the opening poll's error is swallowed whenever the stream opened.
- `embarch-core` `src/study.rs:3435-3460` (at `40a58cc`): the SSE handler subscribes for any id. `src/study.rs:3286-3290` and `:4019-4022`: a `.partial` with no job is served as `interrupted`.
- `src/cli.rs:1488`'s comment says an unknown id is "reached only when there is no live stream and polling failed too", and against a running Core that path is unreachable. `decisions/study-events.md` 48 says "the only genuine failure is neither mechanism answering". The client's own `StudySummary` doc (`client.rs:550-557`) already names `interrupted` as distinct.
- A related gap: `study_status`'s tool description (`src/tools.rs:1597`) lists four statuses and omits `interrupted`.
- A Core restart *mid-watch* mostly ends with a polling error rather than a hang (`study_events.rs:699-702`). The hang needs an unknown id or an already-interrupted study.

**Sequencing:** the inbox drop `ui-live-run-badge-says-running-and-names-its-step.md`, filed the same day, traces its stuck badge to this same `follow_study` path. Land them one after the other, not in parallel.

## Done when

- [ ] Against the mock Core, `study-status <unknown-id> --follow` with no `--follow-timeout` exits non-zero within a few seconds, and its message names the id as unknown. `--json` ends with a `summary` line saying the same.
- [ ] Against the mock Core, following a study whose `GET /study/{id}` answers `interrupted` ends promptly and reports `interrupted` by name, not as `completed` or `failed`. Its exit code is documented in `interfaces/studies.md`.
- [ ] `study_watch` on the same two inputs returns before `wait_secs` runs out. Its result says which case applied, and its description states what `complete` means for `interrupted`.
- [ ] A non-404 failure of the opening poll, with a live stream open, still follows live as today. A running study that later completes or fails behaves as today. Existing follow tests stay green.
- [ ] `study_status`'s tool description lists `interrupted`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated (decision 48 amended or a new decision for the 404 and `interrupted` rules), `changelog.d/` fragment dropped.
