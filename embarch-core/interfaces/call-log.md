# embarch-core: the call log

**Status:** active, 2026-11-23 (`tasks/core/140`, [decision 122](../decisions/call-log.md)). Index: [../interfaces.md](../interfaces.md).

**It holds Core's calls only.** Hardware reached without Core (the topology CLI's own hardware feature, a probe tool by hand) is not in it. A host or dev-bench study's own steps stay in its `events.json`.

| Method | Path | Query | Response |
|---|---|---|---|
| `GET` | `/call-log` | `?from=&to=` (entries, `from` inclusive, `to` exclusive; default the whole log, at most 1000) | `200 {verified, error, length, head, from, to, truncated, entries, pending_fold}`; `entries` are `{entry, hash}` lines; `pending_fold` is `{first_seq, repeats}` or null. Lease-open, token required, not itself logged |

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
| `board` | null, or `{role, probe_serial, chip, image_sha256}` where the handler named a board; `image_sha256` is the hash Core last flashed to that chip, or `"unknown"` |

**A `fold` entry** stands for identical reads after a `call` entry: `{type: "fold", first_seq, count, first_utc_ms, last_utc_ms, method, route, scope, status, answer_sha256}`. `count` is the repeats, not counting the first. Folded reads: `POST /live/mem-read`, `POST /live/core-state`, `GET /serial-log`, `POST /validate`, `GET /dev-bench/hello`. It is written when a different gated call arrives, the lease is released, or Core stops cleanly.
