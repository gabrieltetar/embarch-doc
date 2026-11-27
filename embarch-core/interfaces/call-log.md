# embarch-core: the call log

**Status:** active, 2026-11-26 (`tasks/core/140`, `tasks/core/181`, [decision 122](../decisions/call-log.md), [156](../decisions/call-log.md), [158](../decisions/call-log.md), [161](../decisions/call-log-quota.md)). Index: [../interfaces.md](../interfaces.md).

**It holds Core's calls only.** Hardware reached without Core (the topology CLI's own hardware feature, a probe tool by hand) is not in it. A host or dev-bench study's own steps stay in its `events.json`.

| Method | Path | Query | Response |
|---|---|---|---|
| `GET` | `/call-log` | `?from=&to=` (entries, `from` inclusive, `to` exclusive; default the whole log, at most 1000) | `200 {verified, error, length, head, from, to, truncated, entries, pending_fold}`; `entries` are `{entry, hash}` lines; `pending_fold` is `{first_seq, repeats}` or null; `size_bytes` and `quota_bytes` are the file's size and its quota. Lease-open, token required, not itself logged |
| `PUT` | `/call-log/quota` | body `{quota_bytes}` (at least 1) | `200 {quota_bytes, previous_bytes, size_bytes}`; `400` for 0; **`403` for the agent's token on every Core**; enters a `quota` entry. Lease-open, not gated, so a full log's person reaches it |

Every route in `lease::LEASE_GATED` answers with `X-Embarch-Call-Seq` and `X-Embarch-Call-Hash`, the entry its call became. A folded repeat names the first entry and adds `X-Embarch-Call-Repeat: <n>` (1 for the first repeat).

`call-log.jsonl` sits beside `run-log.jsonl`; a line is `{"entry": {...}, "hash": "<sha256 hex of the entry's JSON>"}`; every entry has `type`, `seq` (its position) and `prev` (the previous hash, 64 zeros first).

**A `call` entry:**

| Field | Holds |
|---|---|
| `at_utc_ms` | when the request arrived |
| `method`, `route` | the method and the registered path pattern (`/signals/{name}/exchange`) |
| `params` | the path parameters, `{name: value}` |
| `body_sha256`, `body` | the request body's hash; the body itself when JSON of at most 4096 bytes, else null |
| `scope` | `agent` or `person`, the token's |
| `lease` | `{holder, purpose}` of the live lease, or null |
| `status` | the response status; `409` is a call the lease refused |
| `answer_sha256` | the answer body's hash (null if it could not be read) |
| `board` | null, or `{role, probe_serial, chip, image_sha256}` where the handler named a board (every route that acts on one does; null for an undeclared signal and for the instrument exchange, partial for an unknown role or probe); `image_sha256` is the hash Core last flashed to that chip, or `"unknown"` |

**A `fold` entry** stands for identical reads after a `call` entry: `{type: "fold", first_seq, count, first_utc_ms, last_utc_ms, method, route, scope, status, answer_sha256}`. `count` is the repeats, not counting the first. Folded reads: `POST /live/mem-read`, `POST /live/core-state`, `GET /serial-log`, `POST /validate`, `GET /dev-bench/hello`. It is written when a different gated call arrives, the lease is released, or Core stops cleanly.

**A `start` entry** is written at every start, after the port is bound and the safe-off has run and before the first route is served. **A `stop` entry** is written at a graceful stop (SCM Stop, SIGTERM, Ctrl-C), after the pending `fold` and the safe-off. A kill, a crash or a power loss writes no `stop`. Both are in the one chain; neither has a `route`, `method` or `scope`, so a reader filters on `type`. [Decision 156](../decisions/call-log.md).

| `start` field | Holds |
|---|---|
| `at_utc_ms`, `mode` | when the entry was written; `service` or `development` (`GET /status`'s) |
| `previous` | exactly one of `"clean stop"` (the log's last entry is a `stop`), `"not a clean stop"` (it is anything else), `"log started anew"` (the log was empty) |
| `previous_stop_utc_ms` | `at_utc_ms` of the last `stop` entry in the log, whichever `previous` says; null when there has never been one |
| `last_images` | always `"unknown"`: the last-flashed-image log is in memory, so after a start no board's last flasher is known |
| `safe_off` | the safe-off results, below |

| `stop` field | Holds |
|---|---|
| `at_utc_ms`, `mode` | as above |
| `cancelled_study` | the id of the study or Test run cancelled by the stop, or null |
| `study_ended` | `true` when none was in flight or it released the study lock (its teardown ran) within the wait; `false` when the wait ran out |
| `hw_lock_held` | `true` when `hw_lock` was still held when its wait ran out (the safe-off ran regardless) |
| `safe_off` | the safe-off results, below |

**A `safe_off` entry** is written when a study's teardown could not be logged and Core ran its safe-off in place: `{type: "safe_off", at_utc_ms, why, result}`, one per safe-off result (below), into the reserved tail. [Decision 158](../decisions/call-log.md).

**The refusal.** While Core cannot write this log (an append failed, or free space is below the reserved tail) every gated route answers `503` with a plain-text body naming the call log and the reason: `Core cannot write its call log (<reason>), so it refuses hardware calls until it can; ...`. `POST /study/{study_id}/cancel` is never refused. The next append that succeeds with room left ends it: after a failed write the first refusal is itself entered (`status` 503) and the next call is served; a refusal for want of space is not entered. The call-log, key and run-log reads are not gated and stay readable.

**The quota (decision 161).** `call-log-quota.json` (`{"quota_bytes": n}`) sits beside the log; with none, the quota is 1 GiB. A gated call carrying the agent's token is refused `503` once the file is at 90 % of the quota, the person's at 100 %; the plain-text body names the size, the quota and `PUT /call-log/quota` under the person's token (`EMBARCH_PERSON_TOKEN`) or freeing the store. A refusal for the quota is not entered; a cancel is never refused; the `start`, `stop` and `safe_off` entries land past it. The `403` body of the agent's `PUT` names the person's token and that `GET /call-log` is readable. A `quota` entry is `{type: "quota", at_utc_ms, scope, from_bytes, to_bytes}`.

**A safe-off result** is `{kind, name, line?, result, reply?, error?}`: `kind` is `instrument`, `signal` or `declarations` (the table could not be read; `name` is `instruments` or `signals`). `result` is one of `"sent"` (`reply` is what came back, empty when the instrument is not read), `"no safe-off declared"` (no `line`), `"port absent"`, `"not writable"` (a signal Core does not write) or `"failed"`; the last three carry `error`. An instrument with several lines has one result per line, in declaration order, and a port absent ends its lines with one `"port absent"` result. Instruments come first, in declaration order, then signals.
