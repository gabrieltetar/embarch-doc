**Target:** suite/features.md — the `embarch-api` table
**Was:** no row for consuming embarch-core's study event stream; `run_study`/`study_status`/`study_*_data` is the whole studies surface listed there
**Now:** `study-status --follow` (CLI) and `study_watch` (MCP) consume `GET /study/{id}/events`; `lagged` is reported rather than treated as an error, and a dropped or refused stream falls back to polling. Verified `unit` only — never against a live embarch-core, never against a study fast enough to make Core actually lag.

Suggested row, if the table's shape still fits it:

| `study-status --follow` / `study_watch` — live study events over SSE, with a polling fallback | Shipped — never against a real Core | unit | 47, 48, 49 |

Account of the change: [embarch-api/interfaces/tools.md](../embarch-api/interfaces/tools.md) "Watching a study live", and [embarch-api/decisions/core-link.md](../embarch-api/decisions/core-link.md) 48/49. The unverified half is in [embarch-api/open.md](../embarch-api/open.md) and in `tasks/api/001-sse-client.md`.
