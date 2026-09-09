# 041 — `serial_log` — the workflow the user guide sells as the payoff — cannot be completed from a freshly `init`ed project, and `interfaces/tools.md` documents a fallback that does not exist

**State:** claimed — leg 060, 2026-09-09, `agent/api/041-serial-port-discovery`
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

## Supervisor's dispatch note, leg 060 (burndown)

**`tasks/core/009` is running RIGHT NOW, in this same leg, in `embarch-core`.** It is bounding
`duration_ms` with a named cap and a `400`. You own `embarch-api` only. **Do not describe Core's cap
in your docs** — you cannot know the number it picks and it may not land — and do not edit anything
under `embarch-doc/embarch-core/`. If your MCP-description work wants to mention a duration ceiling,
say only that Core bounds it and point at Core's own `/serial-log` row.

**Narrow the disposition to the two ends the task's own "Done when" requires**, and no further:
surface the already-existing `GET /serial-ports` / `list_serial_ports` pair on **both** front ends
(one MCP tool and one `embarch-api` subcommand), and correct
`embarch-api/interfaces/tools.md:28`'s fallback claim to describe real behaviour. Make
`serial_log`'s MCP description say whose machine the port namespace belongs to. **Do not** change
`embarch init` (that is `embarch-umbrella`, not yours) and **do not** change Core's error text.

**This leg runs under [burndown.md](../../../embarch-fleet/burndown.md): no new numbered decision.**
Surfacing an existing route on the existing front ends is mechanical; if you conclude it needs a
numbered `embarch-api` decision, record it as owed in `open.md` and say so in your report.

**Doc reserve for `api`, read this before you plan an edit:**

- `embarch-api/decisions/tool-wrapping.md` — **12222/12288 B, 66 bytes left.** This is the file a new
  MCP tool would naturally want to amend, and there is no room. Its compaction task
  `tasks/api/047-compact-api.md` is **blocked on `In flux: yes`**, so if your unit genuinely must
  write this file, **compact it as part of this unit**, carrying `047`'s `Must not delete:` list
  verbatim and closing only that file's item. Prefer a split ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2).
- `embarch-api/decisions/core-link.md` 212 B left, `embarch-api/spec.md` 815 B left,
  `embarch-api/decisions/build.md` 1154 B left — all in reserve and all parked. Plan your edits to
  land in `interfaces/tools.md` (not in reserve) wherever the content honestly belongs there.
- `embarch-api/open.md` was compacted to 3782 B (73.9%) last night and has real room. Use it.

**No hardware.** No live Core, no board, no `serial_log` call against a real port.
