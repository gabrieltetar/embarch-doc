# embarch-core interfaces: Topology

**Status:** active, 2026-09-07. Split out of [../interfaces.md](../interfaces.md) on 2026-09-07 (`tasks/core/020`) when that file reached its size cap — a reference table, not cut, per [../DOC-COMPACTION.md](../../DOC-COMPACTION.md) §3.

Index: [../interfaces.md](../interfaces.md). Conventions and rationale: [../interfaces.md](../interfaces.md), [../decisions.md](../decisions.md).

**`hardware_id` below is the probe/JTAG-read ID, and that is the suite's default, unprefixed name for it** — decision 56 (`../decisions/handshake.md`) settles it and cancels the rename decision 47 deferred. The only prefixed spelling is `probe_hardware_id` on `GET /dev-bench/hello`, where it has `self_reported_hardware_id` four fields away and needs to say which it is.

**`confirmed_at_utc_ms` on `/probes/enroll` and `/probes/enrolled` is enrolment time, not freshness** — the instant the record was last written, unmoving until someone re-enrolls. A live re-check's own instant is `POST /validate`'s `validated_at_utc_ms` (decision 50) and reaches neither of these two routes: decision 54 has why, and what a renderer should say instead of implying either route's timestamp answers "how stale is this identity check?".

| Method | Path | Body / Query | Response |
|---|---|---|---|
| `POST` | `/probes/enroll` | `{role, chip, probe_serial?}` | `{probe_serial, role, chip, hardware_id, confirmed_at_utc_ms}`. The **only** sanctioned way to write the enrollment table. Attaches, reads the live hardware ID, records it |
| `GET` | `/probes/enrolled` | — | `[{probe_serial, role, chip, hardware_id, confirmed_at_utc_ms, link_port_serial, link_port_interface}]` |
| `POST` | `/validate` | `{role}` | `200 {ok: true, …}` on a match; `409` with `{recorded_hardware_id, live_hardware_id, reason, fix_it_url}` on a real mismatch; `404` if nothing is enrolled under `role`. The explicit, non-destructive counterpart to the re-check `flash`/`reset`/`POST /study` already run mid-attach |
| `GET` | `/alerts` | `?limit=20` | Recent topology-mismatch alerts from the durable log, oldest first within the window |
| `POST` | `/dev-bench/link` | `{serial?, interface?}` — either alone; **neither is a `400`** | `204`. Declares dev-bench's runtime link. `interface` answers what a serial structurally cannot: one probe exposing two VCOMs gives both the same USB serial, and on the nRF54L15DK `zephyr,console` is VCOM1 at **interface 2** — the lowest-index fallback lands on a port that accepts bytes and never answers |
| `POST` | `/signals` | a `SignalLink`: `{name, origin_role, direction, route: {kind: "direct", port_serial} \| {kind: "via-dev-bench", rx_pin, tx_pin}}` | `204`; `400` for a blank name. Idempotent by name, and that overwrite **is** the migration path — moving the outpost onto dev-bench pins is one call. Core is deliberately the only writer: that crate's CLI hits the NTFS permission wall on the real deployment |
| `GET` | `/signals` | — | `[SignalLink]` |
| `DELETE` | `/signals/{name}` | — | `204`; `404` when nothing is declared under that name. The `404` is deliberate: a caller retracting a row it thought existed should learn it did not |
