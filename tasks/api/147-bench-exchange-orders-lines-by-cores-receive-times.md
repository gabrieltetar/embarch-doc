# 147 — `bench_exchange` orders its timeline by Core's per-line receive times when Core sends them

**State:** done on agent/api/147-bench-exchange-core-rx-times, 2026-10-26
**Source:** the 2026-10-26 leg, landing `core/115` (`embarch-core@731e875`, decision 94): capture `GET`/`DELETE` now return `started_utc_ms` and `lines: [{offset, rx_ms}]` (each line's first-byte time), and the exchange reply returns `started_utc_ms`. `embarch-api` decision 89 (`decisions/bench-exchange.md`) stamps each line with the client poll that first saw it because Core sent no per-line time; its own Least-sure line was whether 100 ms polling orders two consoles correctly.
**Scope:** api
**Hardware:** verify-only — host-testable against a scripted Core; the order check on two real consoles is the debt `api/131` already recorded.
**Owner:** no

## Dispatch note, 2026-10-26 07:22 leg

**Shared crate.** `embarch-core-client` is path-depended on by `embarch-ui`. Add the three fields as
`Option` with `#[serde(default)]` (decision 58; `api/146` just applied the same rule to `last_images` at
`embarch-api@903c76c`), change nothing else public, and grep the `embarch-ui` main checkout (read only)
for `SignalCaptureResponse` and the exchange response type; the leg builds `ui` against the merge. Core's
wire shape is `embarch-core` decision 94 (`embarch-doc/embarch-core/decisions/signal-capture.md`); read
it, do not guess field names, and do not touch `embarch-core`.

**Reserve.** `embarch-api/decisions/client-crate.md` 11,581 / 12,288 B (707 B left, filed under
`api/140`) and `embarch-api/open.md` 4,297 / 5,120 B (823 B left, filed under `api/144`). Amend decision
89 in `decisions/bench-exchange.md`, which has room; at most one line in `client-crate.md`.

**Isolation.** Do not reach the owner's live services. No live Core (scripted/mock Core only), no desk on
`:4891`, no geckodriver on `:4444` and no UI on `:4899`, no real serial ports or debug probes, no owner
data directories (fresh temp dirs only), and no MCP tools at all. Kill only processes you started, by PID.

## What

`embarch-core-client`'s `SignalCaptureResponse` (api decision 88) gains `started_utc_ms` and `lines` as `Option` fields (decision 58: an older Core sends neither, and that reads as "unknown", not as "no lines"), and the exchange response gains `started_utc_ms` the same way. `bench_exchange` places a captured line at `started_utc_ms + rx_ms` and an exchange reply at its `started_utc_ms` when Core sent them, and falls back to today's client-observed poll time when it did not. Each answer's `time_basis` says which basis each row used, so a mixed timeline (one console from an old Core path, one from the new) never reads as exact.

## Why now

Core is the only place the real arrival time exists, and it now serves it; until the client reads it, `bench_exchange`'s cross-console order is still only as good as its poll interval.

## Done when

- [x] The client decodes the three new fields as optional; an old-Core body decodes to `None`, and a test proves it.
- [x] Against a scripted Core sending `lines`, two lines on two consoles 30 ms apart inside one poll window come out in wire order; against one that does not, the poll-time fallback still works and `time_basis` says so.
- [x] Decision 89 amended (or a new decision) for the new basis; gate green (`../../embarch-fleet/protocol.md` §10); `embarch-ui` still builds against the crate.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Result

Client: `SignalCaptureResponse.started_utc_ms`/`lines` (`Option<Vec<CaptureLine>>`) and `SignalExchangeResponse.started_utc_ms`, all `Option`+`serde(default)`; test proves old-Core bodies read `None`. `bench_exchange` anchors Core's UTC clock at the earliest capture start, pairs `lines` entries with raw lines in order, places unlistened replies at `started_utc_ms` (never before their write), and `time_basis` is now built per signal. Decision 89 amended. `embarch-ui` constructs neither struct literally (grep), so the additive fields do not touch it; ui was not built here.

**Hardware-verification debt:** none new; the two-real-consoles order check stays `api/131`'s debt, and the anchor error (one capture-start latency) and cross-capture wall-clock alignment (`embarch-core` 94, assumed) are unmeasured.
