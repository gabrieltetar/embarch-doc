# 143 — Client tools for Core's background signal capture

**State:** open
**Source:** `tasks/core/100` (landed 2026-10-26, code `embarch-core@845f3ea`): Core's `POST|GET|DELETE /signals/{name}/capture`, decision 92 in `embarch-doc/embarch-core/decisions/signal-capture.md`. `tasks/api/131` (`bench_exchange`) builds on the same routes but is a higher-level tool; it does not cover these raw ones. Filed from `inbox/api-signal-capture-tools.md` by the 2026-10-26 05:14 leg.
**Scope:** api
**Hardware:** verify-only — client wrappers testable against the mock Core; the two-console bench check is Core's debt in `tasks/core/100`.
**Owner:** no

## What

Add MCP tools and CLI twins over the three routes, so a session can record one console while driving another. `capture_start {signal, max_s?, max_bytes?}` returns Core's answer (`id`, `state`, ...). `capture_read {signal, after?, limit?, id?}` returns `{text, next_offset, state, running, total_bytes, gaps}`; the tool keeps no state, the caller passes `next_offset` back as `after`. `capture_stop {signal, after?}` stops and returns the final text. CLI: `capture start|read|stop <signal>`. Extend `embarch-core-client` with the three calls and Core's response type. Defaults and caps are Core's (`max_s` 60 up to 600, `max_bytes` 1 MiB up to 16 MiB); do not restate them, forward Core's `400`. A `409` on start names the running capture: surface the text. Because `POST` returns at once and each `GET` is short, the client's 15 s timeout needs no change for these calls. Keep the tool descriptions short and say what the offsets mean and that `reopening` plus a `gaps` entry is a re-enumerating USB device, not a failure.

## Why now

The field's 21 hand-written console listeners after `signal_exchange` shipped (1,237 s of tool time) are this tool; Core's half has landed. `tasks/api/131` needs it first.

## Done when

- [ ] `capture_start`, `capture_read` and `capture_stop` exist as MCP tools and CLI subcommands, with a parity test.
- [ ] `embarch-core-client` has the three calls, round-trip tested against the mock Core, including a `409` and a `404`.
- [ ] A read that passes `next_offset` back returns only new text.
- [ ] Bench verification (a capture on one console while exchanging on the other) filed as hardware-verification debt.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `spec.md`/`decisions.md`, `changelog.d/` fragment and the feature row updated. `decisions/client-crate.md` is in reserve under `tasks/api/140`: a new decision goes in another topic file.
