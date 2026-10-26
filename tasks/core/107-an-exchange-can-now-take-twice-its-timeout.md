# 107 — A console exchange can now take twice its `timeout_ms`, past the client timeout its cap was sized under

**State:** claimed by agent/core/107-exchange-twice-its-timeout, 2026-10-26 00:39
**Reserve, for the worker:** no `embarch-core` doc is in reserve today; `decisions/signal-exchange.md` is where decision 79 lives, check its size before amending.
**Source:** `core/097`'s reviewer, 2026-10-26 (below its bar, filed by the supervisor so it is not lost when the log folds).
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`core/097` (embarch-core `3dba64b`) gave a console exchange's write its own deadline of the request's
`timeout_ms`, and decision 79's amendment says *"The read's own deadline starts after the write."* So a
throttled device that takes its line just before the write deadline gets a second full `timeout_ms`
for the reply: one exchange can now hold `hw_lock` and the HTTP request for up to `2 × timeout_ms`
plus `port_wait_ms`. Decision 79 caps `timeout_ms` so that one exchange stays under the shared
client's 15 s timeout (decision 58's reason, as decision 79 cites it); at the cap that budget is now
exceeded, and the caller sees a client-side timeout rather than either a reply or the write-deadline
error `core/097` added.

When done, one exchange's total time is bounded by what the cap was sized for — most simply, the read
gets whatever remains of `timeout_ms` after the write rather than a fresh one — or decision 79 states
plainly that the budget is per direction and the cap is re-derived against the client timeout.

## Why now

The amendment landed today and is the only text that describes the new budget; it reads as if the
cap's rationale still holds. A slow device near the deadline is exactly the field case `core/097`
came from.

## Done when

- [x] A unit test with a fake port that takes its line just inside the deadline shows the whole
      exchange ending within the bound decision 79 states.
- [x] Decision 79 (`embarch-core/decisions/signal-exchange.md`) says how `timeout_ms` is split
      between write and read, and its cap rationale is true of that split.
- [x] Gate green (`../../../embarch-fleet/gate.md`). `changelog.d/` fragment.

## Outcome

One deadline for write and read (`src/exchange.rs`); write's port timeout set to the remainder per attempt; at least one read pass. Decision 79 amended. Native Windows build and real-port blocking-write behaviour: hardware/Windows verification debt (same as 097).
