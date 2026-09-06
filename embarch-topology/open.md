# embarch-topology: open

**Status:** active, 2026-09-02.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **The durable half of a signal alert is not built, and the trigger is named rather than left as owed work.** Decision 18 holds the shape, the trigger — revisit when a signal is declarable **and** a route is physically real — and what has to move alongside it when it lands. **The first half has fired**; the second has not, because no capture has been read off a DUT over a direct route.

- **No signal tap has read a byte.** Resolution has touched physical hardware — a declared serial resolved to a real port and Core attempted a real open — but **that open failed by design, because the port was deliberately held busy to verify Core's effective baud.** None of this touches the signal entity, its route, or its storage.

- **Two reporting defects are now measured rather than reasoned, and neither is fixed here.** A live two-probe resolution 2026-09-06 credited `detected_by` to `segger-vid-match` for a choice that rule left **three-way** ambiguous (`tasks/topology/003`), and `embarch-topology dev-bench` run from WSL blamed the USB cable for a board that was attached and working (`tasks/topology/004`). Both task files carry the measurements. **What makes them more than label errors: `detected_by` is what an operator reads to decide how much to trust a port, and it names the weakest rule consulted rather than the one that chose.**

- **One narrow bench fact is genuinely unknown and is not inferred here:** whether the DUT board's USB exposes a **second** serial interface for the outpost's dedicated UART, or whether it contends with the DUT's console. The larger question this waited on is settled — **there is no separate bridge to buy**, since the DUT board's own USB carries the outpost's UART and *is* a direct route.

- **The Nordic identity relation is verified by construction, not by every path it covers**, and no bench has exercised the path that can be wrong: a part falling back to other registers **comes back *mismatch* rather than *undeclared***. Decision 21 has the derivation and the terms that exposure is accepted on.

- **Call-site granularity is not fully specified.** Resolution and validation are fresh-every-call by construction, with no cache in the crate; **nothing states what a caller may assume beyond that**, so a consumer wanting to hold an answer across calls has no rule to read.

- **The token and config mirrors of `embarch-api`-internal logic are untouched by this crate's existence** and still raise the extract-or-CI-diff question independently. Extracting this crate removed the *topology* copy; **those two mirror internals, not a shared concern the way topology turned out to be.** Tracked in [embarch-umbrella/open.md](../embarch-umbrella/open.md).
