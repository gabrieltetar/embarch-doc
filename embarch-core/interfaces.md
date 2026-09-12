# embarch-core: HTTP interface

**Status:** active, 2026-09-07.

Every route requires `Authorization: Bearer <token>`. Semantics and rationale: [decisions.md](decisions.md).

## Conventions

- `chip` is an opaque probe-rs target name (`nRF54L15`, `esp32c5`, `STM32F407VG`), not validated beyond what `probe.attach()` rejects. `format` is `elf`/`bin`/`hex`/`uf2`/`idf`; an unrecognised value is an error, never a silent default. `firmware_path` is read from **Core's own disk** — the caller gets the file there (spec §3).
- **Errors are plain text, not JSON**, on every non-2xx: the full `anyhow` chain (`{e:?}`, not `{e}` — `Display` silently dropped every underlying cause). Parse JSON only on 2xx. `internal_err` also logs the same chain server-side, so a failure is visible in `core.log` even if the caller drops the body. A `{code, message, cause}` JSON body is designed, **not built, and deferred as a cross-repo change** rather than a Core-local one (decision 12) — so an error's *kind* is available only as its HTTP status, and the status codes above are the whole vocabulary a caller can branch on.
- **`GET /serial-log` has a caller-side ceiling nothing declares.** `embarch-core-client`'s `default_serial_timeout_secs()` is **15**, so a `duration_ms` at or above 15,000 can never succeed: the client gives up with `operation timed out` while Core goes on holding `hw_lock` for the whole requested duration [measured 2026-09-06, `duration_ms=15000` against the live Core]. **Core's own side of that bound shipped in `tasks/core/009`**: `duration_ms` over `serial::MAX_DURATION_MS` (10,000, comfortably under the client's 15,000) is now a `400` naming the cap and the value, checked before `hw_lock` is taken, and the capture is byte-capped too (`EMBARCH_SERIAL_LOG_MAX_BYTES`, default 1 MiB), reporting `truncated: true` rather than silently returning a partial capture. The client-side gap this bullet first described is unchanged — nothing prevents a caller from asking for a `duration_ms` under Core's cap but still at or above the client's own timeout.
- **Which routes take `hw_lock`:** anything that opens a physical connection (`/flash`, `/reset`, `/serial-log`, `/probes/enroll`, `/validate`) plus the three enrollment-file writers (`/dev-bench/link`, `POST /signals`, `DELETE /signals/{name}`), which race those writes rather than any hardware. Everything else — descriptor enumeration, file reads, `/resolve-chip` — takes nothing.
- **`404` is often an expected state, not a failure:** no dev-bench port (bench unplugged), no board enrolled under a role, a study with no `streams/`, an unmapped SoC. `502` means the bench itself is the problem. **`503` means `hw_lock` was contended and the wait timed out** (decision 14, built `tasks/core/013`): a caller that meets the lock already held waits up to 500 ms, then gets `503` with a plain-text body naming the route currently holding it (e.g. `hw_lock held by POST /flash; POST /reset refused after waiting 500ms`) — a caller can branch on this status and does not need to guess whether Core is hung.

## Routes, split by mission

Split out of this file on 2026-09-07 (`tasks/core/020`) when it reached its size cap ([DOC-COMPACTION.md](../DOC-COMPACTION.md) §3) — a reference table, not cut, the same way [decisions.md](decisions.md) splits into `decisions/<topic>.md`.

| Load this for | Routes |
|---|---|
| [Hardware](interfaces/hardware.md) — flash, reset, chip resolution, serial-port enumeration | `/status`, `/flash`, `/reset`, `/serial-log`, `/resolve-chip`, `/serial-ports`, `/dev-bench/port` |
| [Topology](interfaces/topology.md) — probe enrollment, live validation, signals | `/probes/enroll`, `/probes/enrolled`, `/validate`, `/alerts`, `/dev-bench/link`, `/signals`, `/signals/{name}` |
| [Logs](interfaces/logs.md) | `/logs/recent` |
| [Studies](interfaces/studies.md) — the dev-bench handshake and the async study job | `/dev-bench/hello`, `/study`, `/study/{id}`, `/study/{id}/events`, `/study/{id}/steps`, `/study/{id}/streams`, `/study/{id}/stream/{name}` |
| [Result layout on disk](interfaces/result-layout.md) — not a route group, what the Studies routes above read | — |
| [Constants and knobs](interfaces/constants.md) — not a route group, spec §5's values | — |
