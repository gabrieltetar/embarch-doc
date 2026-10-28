# 120 — `GET /serial-log` resolves a declared signal (the Core half of api/125)

**State:** done — GET /serial-log resolves a declared signal (decision 101); hardware debt below
**Source:** `tasks/api/125` (2026-10-28): `embarch-api` now sends `GET /serial-log?signal=<name>&duration_ms=..[&baud=..][&port_wait_ms=..]` and no `port`. Core's `SerialLogQuery` (`src/api.rs`) still requires `port`, so an unchanged Core answers 400 to the signal form. Field use on a USB PD board: `serial_log` on a CDC ACM console failed "cannot find the file specified" right after a reset while the signal path to the same console worked. Filed from the api/125 worker's inbox drop by the 2026-10-28 14:33 leg.
**Scope:** core
**Hardware:** verify-only
**Owner:** no

**Reserve (supervisor, 2026-10-28):** `embarch-core/open.md` is 5028/5120 B (92 B left) and `spec.md`
9760/10240 B, both parked under `tasks/core/112` (blocked, `In flux: yes`). This unit must not grow
either; if it has to add an open question to `open.md`, it compacts that file in the same unit per
`DOC-COMPACTION.md` §2, keeping `core/112`'s `Must not delete:` list.

## What

Make `port` optional on `GET /serial-log` and add `signal` and `port_wait_ms` (default 0, cap `MAX_TIMEOUT_MS` as exchange has it). Exactly one of `port` / `signal`; both or neither is 400 naming both. With `signal`: resolve the declared signal with the resolver `POST /signals/{name}/exchange` already uses (`exchange::resolve_port_waiting(name, port_wait_ms)`, core decision 79) to the port's current name, open it at the signal's baud, and use an explicit `baud` query only as an override when given (the api sends none by default; do not apply the 115200 default in the signal form). An undeclared signal, one that is not a direct route, or an unresolvable USB serial is a 4xx naming which. The response's `port` is the name actually opened. Same hardware lock, same `duration_ms` cap, same `truncated`. Take the signal's direction into account the way exchange does (a read needs dut-to-host or bidirectional); if that is wrong for a pure host-to-dut signal, say so in the error.

## Why now

`embarch-api` shipped its half (decision 94) against this contract; until Core lands this, the signal form of `serial_log` is refused, and the COM-name fallback keeps breaking on every console re-enumeration.

## Done when

- [ ] `/serial-log?signal=` resolves, waits `port_wait_ms`, reads at the signal's baud; `port` still works unchanged.
- [ ] Tests: both-or-neither refused, undeclared signal, baud override, an unknown `port_wait_ms` above cap.
- [ ] Core's `/serial-log` interface doc and `spec.md`/`decisions.md` updated; changelog fragment.
- [ ] Hardware-verification debt written: one `serial_log signal=` call across a DUT reset on a CDC ACM console.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

## Hardware-verification debt

Not run (hardware-free unit). Needs: a DUT on a USB CDC ACM console declared as a direct signal, then `serial_log signal=<name> port_wait_ms=<~10000>` issued across a DUT reset (the port drops and re-enumerates under a new name); expect `200` with `port` = the new name and lines at the signal's baud. Also one `signal=` on a `host-to-dut` signal (expect `409`). The native Windows `embarch-core` build was not run (owner's debt).
