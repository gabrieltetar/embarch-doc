# 124 — Let the signal_exchange tool and CLI pass match_after_echo, so a console with echo off returns at its prompt

**State:** claimed by agent/api/124-signal-exchange-takes-match-after-echo, 2026-10-26 04:32
**Dispatch note:** the bench check under Done when is not yours: write it as a hardware-verification debt in this file and ship the host-side half. `decisions/client-crate.md` is in reserve (11,581/12,288 B, filed under `tasks/api/140`); if `embarch-core-client` needs the field, record the decision in `decisions/surface.md` (5,145 B) or `failure-reporting.md`, not `client-crate.md`. `embarch-core-client` is path-depended on by `embarch-ui`: an additive optional field only.
**Source:** field use on a Zephyr USB CDC ACM shell, 2026-10-21: with `shell echo off`, every `signal_exchange` with `until: ":~$ "` ran to its full timeout (about 3 s per line) although the prompt came back in tens of milliseconds
**Scope:** api
**Hardware:** verify-only
**Owner:** no

## What

Core's exchange request has `match_after_echo` (`embarch-core/src/exchange.rs:59-64` at `40a58cc`): `until` is searched only after the echo of the written line, on by default. A shell with echo off never echoes, so the search never starts and the read runs to `timeout_ms` with `until_seen: false`. The MCP tool's `SignalExchangeParams` (`embarch-api/src/tools.rs:558-579` at `f82f8b6`) and the CLI have no way to turn it off, and the tool's description does not mention it. When done, both take an optional `match_after_echo` (default unchanged), pass it to Core, and the tool description says to set it to false for a console with echo off.

## Why now

Host-driven transfers turn the echo off on purpose: a Zephyr shell takes 22 ms per line with echo off and 505 ms with it on. A 36-line image upload through the tool then costs about 110 s of timeouts instead of about 1 s, and every reply reports `until_seen: false`, which reads as a failure.

## Done when

- [ ] `SignalExchangeParams` and the CLI take `match_after_echo`; a test shows it reaches Core's request body, and that leaving it out sends nothing, so Core's default holds.
- [ ] The tool description names the echo-off case.
- [ ] Bench check: after `shell echo off`, an exchange with `until: ":~$ "` and `match_after_echo: false` returns at the prompt with `until_seen: true`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.
