# 041 — `serial_log` — the workflow the user guide sells as the payoff — cannot be completed from a freshly `init`ed project, and `interfaces/tools.md` documents a fallback that does not exist

**State:** open
**Source:** suite review pass 2026-09-06, dimension 7 (the newcomer). Code-confirmed.
**Scope:** api
**Hardware:** none. The `GET /serial-ports` route and the `list_serial_ports` client wrapper both already exist and are tested.
**Owner:** no

## What

`suite/user-guide.md:200` sells *"Flash it, then show me the serial log for the first 5 seconds
after reset"* as one of three headline agent workflows. Following it from a freshly `init`ed
project cannot work, and nothing on the path says why.

- **`embarch init` never writes `serial_port`.** The field appears nowhere in
  `embarch-umbrella/src/`, and §5.1's example config in the guide has no such field.
  `embarch-api/interfaces/config.md:45` marks it optional, default `none`.
- **Neither front end falls back.** `embarch-api/src/tools.rs:899-906` and `src/cli.rs:821-832`
  both go straight to `"no serial port given and project '{}' has no configured serial_port"`.
- **`embarch-api/interfaces/tools.md:28` documents a fallback that does not exist:** *"`port`
  falls back further to Core's `GET /dev-bench/port` before erroring — and this link is meant for
  the bench, not a DUT's own console."*
- **Nothing can list the ports.** `GET /serial-ports` exists (`embarch-core/src/api.rs:83`) and
  `list_serial_ports` exists on the shared client
  (`embarch-api/crates/embarch-core-client/src/client.rs:1490`), but **no MCP tool, no
  `embarch-api` subcommand and no `embarch-core` subcommand reaches it** — Core's subcommands are
  `Run Install Uninstall Start Stop Update DetectDevBench ChipList FlashBackend Logs DevBenchLogs`.
- **`serial_log`'s MCP description is the shortest in the surface** (`src/tools.rs:883`) and says
  neither whose machine the port namespace belongs to nor how to find a value — while every other
  tool's description carries its traps at length.
- **Core's failure names nothing useful.** `embarch-core/src/serial.rs:15` →
  `failed to open serial port '<name>'`, wrapped as a 500. It does not say the port is on Core's
  machine, and nothing lists what Core does see.

On the suite's own primary topology the correct value is a **Windows COM name** and the caller is
a WSL2 process, so an agent's first guess (`/dev/ttyACM0`) is both reasonable and wrong, and the
error is indistinguishable from a cabling problem. The guide *does* warn "check it appears on the
machine Core runs on" — but for **probes**, in the `doctor` failures table, not for serial ports.

Candidate direction: the property is that a newcomer or agent can get from `embarch init` to a
serial log without opening the UI. Reachable by surfacing the existing `GET /serial-ports` on both
front ends, by having `init` write a commented `serial_port` with a discovery hint, or by making
the error name where to look. `interfaces/tools.md:28` must be corrected either way.

## Why now

This also lands on `embarch.md` §5 — *"every hardware-facing capability reachable by an agent and
directly by a human alike"* — because port enumeration is today reachable only from the UI, which
is not in the suite archive at all. Nothing catches it: `tasks/api/034`'s planned parity test
compares tools to subcommands and cannot see a Core route neither reaches, and `tasks/api/036`
does the same job for a different endpoint and would not add this one.

## Done when

- [ ] A caller with no `serial_port` configured can discover a valid value from a binary
      `embarch setup` installs, or gets an error that names where to look.
- [ ] `embarch-api/interfaces/tools.md:28` describes real behaviour.
- [ ] `serial_log`'s MCP description says whose machine the port name belongs to.
- [ ] Gate green; `changelog.d/api-*` fragment.

**Not in scope here:** `tasks/core/009` bounds `/serial-log`'s `duration_ms` and its `hw_lock`
hold. That is a different defect on the same route.
