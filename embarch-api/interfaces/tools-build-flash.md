# embarch-api: build and flash tools

**Status:** active, 2026-09-02. Split out of [tools.md](tools.md) 2026-09-10 (`tasks/api/053`) — see that file's header for the one-table premise this section still honours.

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `build` | `project`, `P` | Runs the configured or call-time-assembled build command. Selection is validated against the live scan **before** assembly. Returns success, exit code, truncated stdout/stderr, artifact path, and whether a fresh artifact was found |
| `flash` | `project`, `P`, `firmware_path?`, `erase?` | Core `POST /flash` with the resolved chip, format and offset. `firmware_path` flashes an already-built or one-off file — bypassing *build*-target resolution, but a `zephyr-west` project still needs enough selection to resolve the **chip**, none being stored |
| `build_and_flash` | `project`, `P`, `erase?` | Runs `build`, flashing only if it succeeded **and** the freshness check passed. Returns both sub-results |
| `reset` | `project`, `P` | Core `POST /reset` with the resolved chip. Same selection as `flash`, same reason |
| `serial_log` | `project`, `port?`, `baud?`, `duration_ms?` | Core `GET /serial-log`, opening the named port on **Core's own machine** — not the caller's. Falls back to the project's configured port and baud, then 115200 / 2000 ms; **no further fallback exists** — a `port` unresolved either way is a plain error naming the project, not a reach for `GET /dev-bench/port` (that link is dev-bench's, a different question — see `list_serial_ports` below). `duration_ms` is bounded by Core's own cap on this route — see Core's `/serial-log` interface doc for the current number |
| `list_serial_ports` | — | Core `GET /serial-ports`: every USB serial port **Core's own machine** currently enumerates, unnarrowed. Use it to discover a value for `serial_log`'s `port` when a project has no configured `serial_port` — the value wanted is whatever Core's OS recognises (e.g. a Windows COM name when Core runs on Windows and the caller is WSL2), not a port name guessed from the caller's own machine. An empty list is a real answer, not an error. Also what makes a declared signal's `direct`-route `port_serial` findable at all — see [tools-topology.md](tools-topology.md) |

**`erase` defaults to `false` and is never implicitly `true`.** The MCP description and the CLI help both spell out what it does to a board, at a length no other argument here gets — that wording is itself the design point, and [decisions](../decisions/tool-wrapping.md) 41 is where it is argued and where a change to it belongs. Core performs the erase and decides whether a target supports one; a refusal comes back verbatim.

**Why `build` and `flash` stay separate as well as bundled:** the common agent workflow wants one call, and bundling prevents flashing a stale artifact after a build error — but iterating on compiler errors should not touch hardware every call, and a re-flash after a board reset should not need a rebuild.
