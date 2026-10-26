# 147 — `bench_exchange` orders its timeline by Core's per-line receive times when Core sends them

**State:** open
**Source:** the 2026-10-26 leg, landing `core/115` (`embarch-core@731e875`, decision 94): capture `GET`/`DELETE` now return `started_utc_ms` and `lines: [{offset, rx_ms}]` (each line's first-byte time), and the exchange reply returns `started_utc_ms`. `embarch-api` decision 89 (`decisions/bench-exchange.md`) stamps each line with the client poll that first saw it because Core sent no per-line time; its own Least-sure line was whether 100 ms polling orders two consoles correctly.
**Scope:** api
**Hardware:** verify-only — host-testable against a scripted Core; the order check on two real consoles is the debt `api/131` already recorded.
**Owner:** no

## What

`embarch-core-client`'s `SignalCaptureResponse` (api decision 88) gains `started_utc_ms` and `lines` as `Option` fields (decision 58: an older Core sends neither, and that reads as "unknown", not as "no lines"), and the exchange response gains `started_utc_ms` the same way. `bench_exchange` places a captured line at `started_utc_ms + rx_ms` and an exchange reply at its `started_utc_ms` when Core sent them, and falls back to today's client-observed poll time when it did not. Each answer's `time_basis` says which basis each row used, so a mixed timeline (one console from an old Core path, one from the new) never reads as exact.

## Why now

Core is the only place the real arrival time exists, and it now serves it; until the client reads it, `bench_exchange`'s cross-console order is still only as good as its poll interval.

## Done when

- [ ] The client decodes the three new fields as optional; an old-Core body decodes to `None`, and a test proves it.
- [ ] Against a scripted Core sending `lines`, two lines on two consoles 30 ms apart inside one poll window come out in wire order; against one that does not, the poll-time fallback still works and `time_basis` says so.
- [ ] Decision 89 amended (or a new decision) for the new basis; gate green (`../../embarch-fleet/protocol.md` §10); `embarch-ui` still builds against the crate.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
