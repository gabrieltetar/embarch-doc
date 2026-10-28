# embarch-core: instrument routes

**Status:** active, 2026-10-28. Bench instruments driven over a USB serial line ([decision 104](../decisions/instruments.md)); the declaration is [embarch-topology decision 49](../../embarch-topology/decisions/instruments.md). Index: [../interfaces.md](../interfaces.md).

| Method | Path | Body / query | Response |
|---|---|---|---|
| `PUT` / `GET` | `/instruments` | `PUT` an `Instrument`: `{name, protocol?: "scpi", port: UsbPortId, baud, write_terminator?: "\n", read_terminator?: "\r\n", min_interval_ms?: 0, ack_ok?, ack_err?}` | `PUT` echoes what was stored, replacing an instrument of the same name; **`400`** for a name that is not a path segment, a zero baud, an empty terminator, `ack_err` without `ack_ok`, or a port identity one live port could match together with another instrument's. `GET` returns the list, empty when none |
| `DELETE` | `/instruments/{name}` | — | `204`, or `404` when nothing is declared under `name` |
| `POST` | `/instruments/{name}/exchange` | `{line, query?: false, timeout_ms?: 2000, port_wait_ms?: 0}` — `line` without a terminator | `{instrument, port, baud, line, query, reply, terminated, ack?: "ok"\|"refused"\|"unacknowledged", flush_reply, paced_ms, elapsed_ms, started_utc_ms}`. `reply` is the raw line before the read terminator; `ack` is absent for a query and for an instrument with no `ack_ok`. **`400`** for an empty line, a CR or LF in it, or a timeout outside 1..=10,000; **`404`** undeclared; **`409`** while a study holds `study_lock`, or the port is not enumerated after `port_wait_ms`, or the identity matches several ports |

Both writers and the exchange take `hw_lock` and are lease-gated; `GET /instruments` takes neither. A host study's `Instrument` step runs the exchange's own body, with the same pacing.
