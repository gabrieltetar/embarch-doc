# embarch-core interfaces: Logs

**Status:** active, 2026-09-07. Split out of [../interfaces.md](../interfaces.md) on 2026-09-07 (`tasks/core/020`) when that file reached its size cap — a reference table, not cut, per [../DOC-COMPACTION.md](../../DOC-COMPACTION.md) §3.

Index: [../interfaces.md](../interfaces.md). Conventions and rationale: [../interfaces.md](../interfaces.md), [../decisions.md](../decisions.md).

Pure local reads of Core's own current daily log file (`logs.rs`) — no hardware touched, no `hw_lock`. The CLI's `logs` subcommand is one implementation behind both routes.

| Method | Path | Body / Query | Response |
|---|---|---|---|
| `GET` | `/logs/recent` | `?tail=200` | `{lines: [String]}` — the tail of the current log file as it stands right now, not a stream |
| `GET` | `/logs/stream` | — | SSE. `event: lines`, a JSON array of newly-appended lines batched per ~750ms poll tick — one whole line per element with one exception: the very first line a subscriber receives may be short, since the offset it starts from is the file's length at attach time, which is newline-aligned only if the writer was idle then (`logs::FollowState`, decision 44). No replay of anything before attach, same posture as `/study/{id}/events` |
