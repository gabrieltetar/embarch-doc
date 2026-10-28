# 125 — `serial_log` reads a declared signal, not a COM name copied into project config

**State:** done — api half shipped (decision 94); Core half filed as inbox drop, so the signal form is refused by today's Core until it lands
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — on 2026-10-08 `serial_log` on the DUT console failed with "The system cannot find the file specified" just after a reset (COM8, a CDC ACM port re-enumerating) while the signal path to the same console worked; 5 `serial_log` calls named the bench's project only to reach the DUT's port; the field config hard-codes 5 COM names, with comments that they move when an adapter is replugged, and the DUT console moved twice (UART bridge, then CDC ACM, then UART bridge)
**Scope:** api
**Hardware:** verify-only
**Owner:** no

## What

`serial_log` takes a project and a COM name, defaulting to the project's `serial_port` (`embarch-api/src/tools.rs:266-276`, `:1495`), and Core's `GET /serial-log` opens that name as given (`embarch-core/src/api.rs:804-846`). Declared signals already solve naming: a direct signal carries the port's USB serial and its baud, Core resolves it to whatever COM name the port has now, and `port_wait_ms` covers a CDC ACM port that is re-enumerating (core decision 79, amended 2026-10-06). Give `serial_log` a `signal` parameter that resolves the same way (USB serial to the current port, the signal's baud, `port_wait_ms`) and make it the documented form; `project` and `port` stay as the fallback for a port nobody declared. Use Core's resolver, the one exchange already uses (a `signal` query on `/serial-log`, a Core half to file with this), not a second resolver in the api.

## Why now

The COM-name path broke every time a console moved or a board reset, and each move meant editing COM names in project config while the signal kept working.

## Done when

- [x] `serial_log` (tool and `serial-log` subcommand) takes `signal`, reads the declared port at the signal's baud, and waits up to `port_wait_ms` for a re-enumerating port.
- [x] The Core half (`/serial-log` resolving a signal) is filed: `/home/gabriel/Github/embarch/embarch-doc/inbox/core-serial-log-resolves-a-declared-signal.md` (becomes a `core` task).
- [x] `project`/`port` still work, and the tool description says the signal form is preferred.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Debts

- **Core half open:** until `/serial-log` accepts `signal`, the api's signal form gets Core's 400. The api half was verified against a mock Core (request shape: `signal`, `port_wait_ms`, `duration_ms`, no `port`, `baud` only when given).
- **Hardware-verification debt:** once Core lands its half, run `serial_log signal=<DUT console> port_wait_ms=5000` across a DUT reset on a CDC ACM console and confirm lines arrive without "cannot find the file specified"; also confirm the signal's baud is the one used.
