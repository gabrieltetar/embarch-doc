# embarch-topology: open

**Status:** active, 2026-09-07.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **The durable half of a signal alert is not built, and the trigger is named rather than left as owed work.** Decision 18 holds the shape, the trigger — revisit when a signal is declarable **and** a route is physically real — and what has to move alongside it when it lands. **The first half has fired**; the second has not, because no capture has been read off a DUT over a direct route.

- **No signal tap has read a byte.** Resolution has touched physical hardware — a declared serial resolved to a real port and Core attempted a real open — but **that open failed by design, because the port was deliberately held busy to verify Core's effective baud.** None of this touches the signal entity, its route, or its storage.

- **`NotFound`'s zero-ports lead-in is only as good as a synchronous, dependency-free WSL2 check can make it** (`tasks/topology/004`, decision 27): it names the split-host possibility and points at `embarch-topology status`, but can't embed that command's live, network-probed answer where `NotFound` is built — `embarch-core`, the consumer that actually hit this, links only `hardware`, never `software`'s `reqwest`/`tokio`. Closing that for real needs either giving `embarch-core` that dependency or a caller threading a pre-resolved answer through; nobody has asked for either yet.

- **One narrow bench fact is genuinely unknown and is not inferred here:** whether the DUT board's USB exposes a **second** serial interface for the outpost's dedicated UART, or whether it contends with the DUT's console. The larger question this waited on is settled — **there is no separate bridge to buy**, since the DUT board's own USB carries the outpost's UART and *is* a direct route.

- **The nRF54L device-ID address is confirmed on one board, and what is left open is narrower than it was.** Decision 21 records the confirmation and its limit. Two things stay unresolved and neither is expensive: **the DUT's own readback has no independent corroboration**, because its firmware self-reports nothing for the relation to check, so its 64 bits rest on the address being right rather than the other way round; and **`nRF54L10`/`nRF54L05`/`nRF54LM20A` take the same arm with no silicon ever attached.** A bench that ever runs a self-reporting build on the DUT closes the first for free.

- **Nothing can cheaply detect a caller writing a second predicate beside a call it never makes to this crate.** `api/038`'s mirror and `embarch-umbrella/src/token.rs`'s were both found by reading a call site, not by a check; a general detector would have to recognize duplicated *logic*, not a duplicated *file*, and no cheap static check does that. This is a standing limitation, not open work — both known instances are already closed (`api/038`, `umbrella/036`); nothing points at further work here.
