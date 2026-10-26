# 115 — Stamp each line of a signal capture with its receive time

**State:** open
**Source:** api/131 (decision 89 in `embarch-api/decisions/bench-exchange.md`): `bench_exchange` merges two consoles into one timeline, but `GET /signals/{name}/capture` carries a byte range with `offset`, `next_offset`, `elapsed_ms` and `gaps`, nothing per line, so the client can only stamp a line with the poll that first saw it (a ceiling, within its poll interval, default 100 ms). `tasks/core/101` stamps lines only inside a host-study tap, so it does not cover this. Filed from `inbox/core-capture-line-receive-times.md` by the 2026-10-26 leg.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

A capture (`embarch-core` decision 92) records, for each line it completes, the time that line's first byte was received, on one Core clock shared by every capture and by exchange replies. `GET /signals/{name}/capture` returns, beside `text`, a `lines` list (or a parallel array) of `{offset, rx_ms}` for the lines in the returned range, `rx_ms` relative to the capture's start with the capture's start time given in UTC ms, so two captures and an exchange can be merged exactly. A client that does not read the new field is unaffected (additive).

## Why now

`bench_exchange` shows a timeline whose order across consoles is only as good as its poll interval: a DUT log line and the command that caused it can land in one poll window and be ordered by arrival at the client, not by the wire. Core sees the bytes arrive; it is the only place the real time exists.

## Done when

- [ ] A capture read returns per-line receive times on a clock the exchange reply (`elapsed_ms` start) can also be placed on.
- [ ] Offsets in `lines` match `text` byte for byte, including across a `gaps` entry.
- [ ] Test with a scripted port: two lines written 200 ms apart carry receive times 200 ms apart (within a stated tolerance).
- [ ] `embarch-core` spec/decisions updated; gate green.
