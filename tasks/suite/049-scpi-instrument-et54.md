# 049 — SCPI instruments: declare an ET54-series electronic load and drive it from Core, one-off and as a study step

**State:** claimed by agent/suite/049-scpi-instruments, 2026-10-28 16:04 — announced 15:33 (`ts` `1793223204.666079`); the window closed 16:03:24 with no reply (polled 16:03:34). Run by the supervisor (protocol §8).
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — an ET5410A+ was driven by a 14.8 KB bash wrapper that starts one PowerShell per command (about 1 s each). 16 logged runs sent 489 SCPI commands, 36 more ad-hoc Bash calls sent others, and a full reading (load plus two consoles) took about 4 s
**Scope:** suite
**Hardware:** verify-only
**Owner:** no

## What

Phase 2 of `embarch-host-study-proposal.md`, carried into a study step. `embarch-topology` gets an `instruments` table, copied from the `bootload_ports` pattern: `Instrument { name, protocol: scpi, port: UsbPortId { vid, pid, serial?, interface? }, baud, write_terminator, read_terminator, min_interval_ms, ack_ok?, ack_err? }`. `embarch-core` adds `POST /instruments/{name}/exchange`. It sends one line, returns the query's reply or the set's acknowledgement, paces commands by `min_interval_ms`, and refuses while a study or another exchange holds the port. `embarch-api` adds `declare_instrument`, `list_instruments`, `remove_instrument` and `instrument_exchange`. The host-study executor runs `HostAction::Instrument` through the same Core code. **Replies are recorded as raw text**, `R` prefix included. A numeric parse comes later, so a value is exact or absent.

## Why now

The e-load campaign of 2026-10-13/14 (11 test cases) found the ET54 facts below the hard way. All were seen on the unit or confirmed by its manual. Each one is a default the suite should own, not something every script has to learn again:

- **Link.** The CH340 (VID 0x1A86, PID 0x7523) has no USB serial and enumerates with the load off, so "no reply to `*IDN?`" is not "port missing". It runs at 9600 8N1. The load ignores a command terminated by CR alone; it needs LF. Replies end in CR LF.
- **Parser state.** A partial line poisons the next command, which then gets `Rcmd err`. Send one empty line after opening and drop its reply.
- **Acknowledgements.** A set answers `Rexecu success` or `Rexecu err`; an unknown command answers `Rcmd err`. **An unacknowledged set fails the step**, because the action was not carried out.
- **Pacing.** The vendor asks for at least 200 ms between commands.
- **Side effects.** A mode change turns the input off. Any command locks the front panel, and `SYST:LOCA` returns it.
- **Protections.** `LOAD1:ABNO?` latches until the operator presses ENT, and no SCPI command clears it. A study pairs this query with a `Prompt`. Safety limits (`VOLT1:VMAX`, `CURR1:IMAX`, `POWE1:PMAX`) are instrument settings written by steps, never study range checks.
- **Identity.** `*IDN?` can name the wrong model: a 5410A+ reports ET5420A+. Record it, but never match identity on it.

## Done when

- [ ] Topology: the table, validation (hex VID/PID, unique name) and a TOML round trip. An instrument is resolved by `UsbPortId`, and an ambiguous match is refused with every candidate named.
- [ ] Core: the route with pacing, a flush line on open, configurable ack strings, and 409 while the port is held. Unit tests over a fake port cover poisoning, acks and pacing.
- [ ] API: the four tools and their subcommands.
- [ ] `HostAction::Instrument` executes in a host study (after the core task "host-study-exchange-steps").
- [ ] Bench check, run by the supervisor on an ET5410A+: `*IDN?`, `MEAS1:ALL?`, `CH1:SW ON`/`OFF` read back and `LOAD1:ABNO?`. The time per command is recorded in the decision.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
