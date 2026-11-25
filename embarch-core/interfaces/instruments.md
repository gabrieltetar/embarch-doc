# embarch-core: instrument routes

**Status:** active, 2026-10-28. Bench instruments driven over a USB serial line ([decision 104](../decisions/instruments.md)); the declaration is [embarch-topology decision 49](../../embarch-topology/decisions/instruments.md). Index: [../interfaces.md](../interfaces.md).

| Method | Path | Body / query | Response |
|---|---|---|---|
| `PUT` / `GET` | `/instruments` | `PUT` an `Instrument`: `{name, protocol?: "scpi", port: UsbPortId, baud, write_terminator?: "\n", read_terminator?: "\r\n", min_interval_ms?: 0, ack_ok?, ack_err?, safe_off?: [line]}` (`safe_off`: topology decision 49; stored, not yet sent) | `PUT` echoes what was stored, replacing an instrument of the same name; **`400`** for a name that is not a path segment, a zero baud, an empty terminator, `ack_err` without `ack_ok`, a `safe_off` line that is empty, holds CR or LF or is over 4096 bytes, or a port identity one live port could match together with another instrument's. `GET` returns the list, empty when none |
| `DELETE` | `/instruments/{name}` | — | `204`, or `404` when nothing is declared under `name` |
| `POST` | `/instruments/{name}/exchange` | any JSON body | **Always `409`**, before any lock or port, with a text naming a host study's `Instrument` step; no caller is admitted, so no reply body exists. The route stays so an older client reads a reason, not a `404` |

On a `--service` Core, `PUT` and `DELETE` answer `403` to the agent's token and are the person's ([decision 132](../decisions/auth.md#132--an-attested-core-takes-identity-declarations-from-the-persons-token-only)). Both writers take `hw_lock` and, with the refused exchange, are lease-gated; `GET /instruments` takes neither. A host study's `Instrument` step runs the exchange's own body (`{line, query?, timeout_ms?, port_wait_ms?}` and the reply it gave before the route was closed, `ack`, `flush_reply`, `paced_ms`), with the same pacing.
