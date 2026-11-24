# embarch-api: instrument tools

**Status:** active, 2026-10-28. Bench instruments Core drives over a USB serial line ([decisions](../decisions/instruments.md) 97); see [tools.md](tools.md) for the one-table premise. Each tool is also a kebab-case subcommand. **There is no exchange tool or subcommand**: Core refuses `POST /instruments/{name}/exchange` to every caller, `409` (embarch-core decision 104), and an instrument is reached only by a host study's `Instrument` step, run with `run_host_study`.

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `declare_instrument` | `name`, `port`, `interface?`, `preset?`, `baud?`, `write_terminator?`, `read_terminator?`, `min_interval_ms?`, `ack_ok?`, `ack_err?` | Core `PUT /instruments`. `port` is `VID:PID[:SERIAL]` in hex; terminators are `lf`/`cr`/`crlf`; `preset: "et54"` fills the rest, explicit fields win; without a preset `baud` is required. Replaces an instrument of the same name |
| `list_instruments` | — | Core `GET /instruments`; an empty list when none |
| `remove_instrument` | `name` | Core `DELETE /instruments/{name}`; `removed: false`, not an error, when none |

**Nothing here has met an instrument** — see [decision 104](../../embarch-core/decisions/instruments.md)'s bench check.
