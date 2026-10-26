# embarch-core interfaces: Host studies

**Status:** active, 2026-10-26.

Index: [../interfaces.md](../interfaces.md). Rationale: [../decisions/host-study.md](../decisions/host-study.md) (decision 95). Reads back through the Studies routes ([studies.md](studies.md)) unchanged.

| Method | Path | Body / Query | Response |
|---|---|---|---|
| `POST` | `/host-studies` | `HostStudy` (JSON, `embarch-study-designer`) | `202 {study_id, status: "accepted"}`. `400` for a study that fails its own checks, names a `Prompt`, `Instrument`, `Repeat` or `line_counts` (not executed yet), or a `streams` tap that is not `Text` + `WholeStudy` on a declared direct signal, has an `Exchange` timeout over 10,000 ms, or names a signal that is undeclared or not writable; the body names the list and step. `409` while any study holds `study_lock`, a tap's port is held by a capture or another tap or cannot be opened, or a lease is live without its token. `422` for an unknown field. |
| `POST` | `/study/{id}/cancel` | — | `202 {study_id, status: "cancelling"}` for the running host study; the step in flight finishes, the rest are skipped, the teardown runs. `409` for a bench study or one not running; `404` for an unknown id. |

**`GET /study/{id}/steps` rows of a host study** carry, beyond the bench fields: `list` (`Steps`|`Teardown`), `detail` (`marker_seen`, `empty_reply` = zero bytes back, `until_not_seen`, `refused`, `port_lost`, `port_unavailable`, `exchange_failed`, `waited`, `cancelled`), `note?`, `reply` (raw, capped), `reply_truncated`, `reply_bytes`, `elapsed_ms`. `GET /study/{id}` returns `events.json` with `completed`, `stopped_reason`, `teardown_failures`. SSE adds `HostStepCompleted`.

**Taps (decision 98).** Each `streams` tap is a capture opened at submission and held until the teardown ends; its files are `streams/<name>.txt` and `.arrival.csv` (read through the stream routes), and `events.json`'s `streams` lists per tap `id`, `name`, `signal`, `port`, `state` (`stopped` normally), `bytes_written`, `truncated`, `gaps`.
