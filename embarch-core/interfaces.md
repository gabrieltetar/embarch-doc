# embarch-core: HTTP interface

**Status:** active, 2026-09-02.

Every route requires `Authorization: Bearer <token>`. Semantics and rationale: [decisions.md](decisions.md).

## Conventions

- `chip` is an opaque probe-rs target name (`nRF54L15`, `esp32c5`, `STM32F407VG`), not validated beyond what `probe.attach()` rejects. `format` is `elf`/`bin`/`hex`/`uf2`/`idf`; an unrecognised value is an error, never a silent default. `firmware_path` is read from **Core's own disk** — the caller gets the file there (spec §3).
- **Errors are plain text, not JSON**, on every non-2xx: the full `anyhow` chain (`{e:?}`, not `{e}` — `Display` silently dropped every underlying cause). Parse JSON only on 2xx. `internal_err` also logs the same chain server-side, so a failure is visible in `core.log` even if the caller drops the body. A `{code, message, cause}` JSON body is designed, **not built, and deferred as a cross-repo change** rather than a Core-local one (decision 12) — so an error's *kind* is available only as its HTTP status, and the status codes above are the whole vocabulary a caller can branch on.
- **Which routes take `hw_lock`:** anything that opens a physical connection (`/flash`, `/reset`, `/serial-log`, `/probes/enroll`, `/validate`) plus the three enrollment-file writers (`/dev-bench/link`, `POST /signals`, `DELETE /signals/{name}`), which race those writes rather than any hardware. Everything else — descriptor enumeration, file reads, `/resolve-chip` — takes nothing.
- **`404` is often an expected state, not a failure:** no dev-bench port (bench unplugged), no board enrolled under a role, a study with no `streams/`, an unmapped SoC. `502` means the bench itself is the problem; `503` means `hw_lock` is held.

## Hardware

| Method | Path | Body / Query | Response |
|---|---|---|---|
| `GET` | `/status` | — | `{ status: "ok", probes: [ProbeInfo], study_designer_schema_version: u32, core_version: String }` — **the whole field set, and a test on `StatusResponse`'s serialized keys fails if a field is added or removed without this row moving.** `study_designer_schema_version` is `embarch-study-designer`'s **host type** constant, the one guarding this hop. `core_version` is Core's own crate version, compiled in from `CARGO_PKG_VERSION` — the same string `embarch-core --version` prints; **warn, not refuse**, on a skew from it (decision 13). There is deliberately **no** `contract_version`; decision 13 has why. `probes` re-enumerates fresh on every call — cheap descriptor enumeration, no attach, which is why a UI can poll it |
| `POST` | `/flash` | JSON `{chip, firmware_path, format, probe_serial?, base_address?, erase?, manifest_path?}` **or** `multipart/form-data` with the same fields plus a `firmware` file part and an optional `manifest` part | `{ flashed: true, chip }`. `base_address` is hex or decimal, meaningful only for `format = "bin"` and silently ignored otherwise; a `bin` image with **no** base address is refused rather than defaulted to `0`. `erase` never becomes a chip erase in any backend (decision 32). The manifest is parsed **before** the flash and stored **after** it succeeds, keyed per chip; a flash carrying none *clears* that chip's |
| `POST` | `/reset` | `{chip, probe_serial?}` | `{ reset: true }`. Fires a real hardware pulse where the probe supports one, falling back to assert/deassert, then `Core::reset()` |
| `GET` | `/serial-log` | `?port=&baud=115200&duration_ms=2000` | `{ port, lines: [String] }` — a bounded snapshot, not a stream. **Meant for dev-bench's link, not a DUT's own console**: plenty of real DUTs have no wired console at all in the configs that matter |
| `POST` | `/resolve-chip` | `{soc: "nrf54l15"}` | `{chip: "nRF54L15"}`, or `404` naming the SoC. Case-insensitive exact match, no fuzzy matching, and the result is checked against probe-rs's own registry so a stale table entry fails like an unmapped SoC |
| `GET` | `/serial-ports` | — | `[DetectedPort]` — every USB serial port this machine enumerates, unnarrowed. Ports reporting no USB serial are omitted, since a `Direct` route is declared *by* that serial. Empty list is a `200`. Deliberately **not** `/dev-bench/port` with the filter off: that applies a VID gate, and a signal wire's bridge can carry any VID |

## Topology

| Method | Path | Body / Query | Response |
|---|---|---|---|
| `POST` | `/probes/enroll` | `{role, chip, probe_serial?}` | `{probe_serial, role, chip, hardware_id, confirmed_at_utc_ms}`. The **only** sanctioned way to write the enrollment table. Attaches, reads the live hardware ID, records it |
| `GET` | `/probes/enrolled` | — | `[{probe_serial, role, chip, hardware_id, confirmed_at_utc_ms, link_port_serial}]` |
| `POST` | `/validate` | `{role}` | `200 {ok: true, …}` on a match; `409` with `{recorded_hardware_id, live_hardware_id, reason, fix_it_url}` on a real mismatch; `404` if nothing is enrolled under `role`. The explicit, non-destructive counterpart to the re-check `flash`/`reset`/`POST /study` already run mid-attach |
| `GET` | `/alerts` | `?limit=20` | Recent topology-mismatch alerts from the durable log, oldest first within the window |
| `POST` | `/dev-bench/link` | `{serial?, interface?}` — either alone; **neither is a `400`** | `204`. Declares dev-bench's runtime link. `interface` answers what a serial structurally cannot: one probe exposing two VCOMs gives both the same USB serial, and on the nRF54L15DK `zephyr,console` is VCOM1 at **interface 2** — the lowest-index fallback lands on a port that accepts bytes and never answers |
| `POST` | `/signals` | a `SignalLink`: `{name, origin_role, direction, route: {kind: "direct", port_serial} \| {kind: "via-dev-bench", rx_pin, tx_pin}}` | `204`; `400` for a blank name. Idempotent by name, and that overwrite **is** the migration path — moving the outpost onto dev-bench pins is one call. Core is deliberately the only writer: that crate's CLI hits the NTFS permission wall on the real deployment |
| `GET` | `/signals` | — | `[SignalLink]` |
| `DELETE` | `/signals/{name}` | — | `204`; `404` when nothing is declared under that name. The `404` is deliberate: a caller retracting a row it thought existed should learn it did not |

## Studies

Async and job-based rather than blocking, unlike everything above: a study's BLE steps can take unbounded time. One study in flight at a time via `study_lock`; no cancel endpoint; the in-memory job registry has no expiry and does not survive a restart. Design of record: [embarch-study-designer/decisions.md](../embarch-study-designer/decisions.md) §5.1.

| Method | Path | Body / Query | Response |
|---|---|---|---|
| `GET` | `/dev-bench/hello` | — | `{schema_version, compatible, firmware_version, hardware_id, probe_hardware_id, link_identity}` — opens the link just long enough to handshake, reports it, closes. `link_identity` is `match`/`mismatch`/`not-reported`/`undeclared`; both IDs are reported rather than only enforced, because reading them side by side is what writing a new chip's relation requires. `409` if a study is in flight |
| `POST` | `/study` | `Study` (JSON), plus `?allow_version_mismatch=1` and `?flashed_firmware_version=<string>` | `202 {study_id, status: "accepted"}`. `409` if a study is running, **or** on the version gate (`requires.dev_bench_version` against what the bench reported, before `StudyStart` is sent, so no step runs). `400` on a `steps_crc`/`streams_crc`/`protocols_crc` mismatch — each named separately — a protocol `validate_protocol` refuses, a `RunProtocol` naming a protocol or entry state the study does not carry, a tap naming an undeclared signal, or a blank `requires`. `502` for dev-bench link failures specifically. `study_id` is a random hex string, not a UUID |
| `GET` | `/study/{id}` | — | `{status: "pending"\|"running"\|"completed"\|"failed", current_step?, total_steps?, result?, reason?}`. `result` is `events.json` read off disk on demand — never a resident copy (`StudyResult` is ~1.3 MB by type). `404` for an unknown id, **including one from before a restart** — indistinguishable by design |
| `GET` | `/study/{id}/events` | — | SSE. One JSON `StudyEvent` per frame (`StepCompleted`/`SampleBatch`/`GattTranscript`/`StatusChanged`), pushed as Core processes it, filtered to this `study_id`. A slow subscriber gets `event: lagged` rather than silently missing messages. **No `Last-Event-ID`, no replay** (decision 41): a reconnect starts at "now," with no way to ask for what it missed — `GET /study/{id}` is the authoritative record a caller falls back to |
| `GET` | `/study/{id}/steps` | — | `{study_name?, timed, steps: [{index, step_name, outcome, reason?, delay_before_ms?, started_utc_ms?, ended_utc_ms?}]}`. A disk read, so a study outlives the process that ran it. `timed` is false for a pre-2026-08-27 study and for an empty list, deliberately. `outcome` is a bare `"Pass"`/`"Fail"`/`"TimedOut"` with `reason` beside it, not `Outcome`'s tagged JSON |
| `GET` | `/study/{id}/streams` | — | `{streams: [{id, name, encoding, alias, rendered, note?}]}` — what the taps captured and, the reason this route exists, **why a trace has no names when it has none**. `rendered` is a boolean, not a file name: a caller never opens the file |
| `GET` | `/study/{id}/stream/{name}` | `?raw=1` | One tap's capture as bytes. By default the rendered file where the encoding has one (`text/csv`); `?raw=1` serves the `.bin`. A tap with no rendering serves raw either way; a `Text` tap comes back `text/plain`. `404` if the study declared no such tap (listing the ones it did) or if it captured nothing. Names resolve through `streams/index.json`, so only a declared name resolves to any file |
| `GET` | `/study/{id}/power-data` · `/waveform-data` · `/gatt-data` | — | Raw CSV for the `power`/`waveform`/`gatt` alias. **Aliases kept for one release**; they fall back to the pre-`streams/` fixed paths for older results |
