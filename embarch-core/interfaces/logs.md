# embarch-core interfaces: Logs

**Status:** active, 2026-09-07. Split out of [../interfaces.md](../interfaces.md) on 2026-09-07 (`tasks/core/020`) when that file reached its size cap — a reference table, not cut, per [../DOC-COMPACTION.md](../../DOC-COMPACTION.md) §3.

Index: [../interfaces.md](../interfaces.md). Conventions and rationale: [../interfaces.md](../interfaces.md), [../decisions.md](../decisions.md).

Pure local reads of Core's own current daily log file (`logs.rs`) — no hardware touched, no `hw_lock`. The CLI's `logs` subcommand is one implementation behind both routes.

| Method | Path | Body / Query | Response |
|---|---|---|---|
| `GET` | `/logs/recent` | `?tail=200` | `{lines: [String]}` — the tail of the current log file as it stands right now, not a stream |

`GET /logs/stream`, a live-tail SSE counterpart, was retired (`tasks/core/021`): no caller anywhere in the suite ever used it, and `embarch-ui` decision 13 structurally excludes an SSE source for this data. `decisions/logging.md` decision 44, the hold-past-`\n` rule that surface needed, is retired alongside it.
