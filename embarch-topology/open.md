# embarch-topology: open

**Status:** active, 2026-09-07.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **The durable half of a signal alert is not built, and the trigger is named rather than left as owed work.** Decision 18 holds the shape, the trigger — revisit when a signal is declarable **and** a route is physically real — and what has to move alongside it when it lands. **The first half has fired**; the second has not, because no capture has been read off a DUT over a direct route.

- **No signal tap has read a byte.** Resolution has touched physical hardware — a declared serial resolved to a real port and Core attempted a real open — but **that open failed by design, because the port was deliberately held busy to verify Core's effective baud.** None of this touches the signal entity, its route, or its storage.

- **One `detected_by` case stays accepted rather than fixed, and decision 24 says why:** when the VID gate itself runs and matches every candidate without narrowing, the VID rule is still credited — under-informative, not false, unlike the declared-serial case decision 24 already closed.

- **`NotFound`'s zero-ports lead-in is only as good as a synchronous, dependency-free WSL2 check can make it** (`tasks/topology/004`, decision 27): it names the split-host possibility and points at `embarch-topology status`, but can't embed that command's live, network-probed answer where `NotFound` is built — `embarch-core`, the consumer that actually hit this, links only `hardware`, never `software`'s `reqwest`/`tokio`. Closing that for real needs either giving `embarch-core` that dependency or a caller threading a pre-resolved answer through; nobody has asked for either yet.

- **One narrow bench fact is genuinely unknown and is not inferred here:** whether the DUT board's USB exposes a **second** serial interface for the outpost's dedicated UART, or whether it contends with the DUT's console. The larger question this waited on is settled — **there is no separate bridge to buy**, since the DUT board's own USB carries the outpost's UART and *is* a direct route.

- **The Nordic identity relation is verified by construction, not by every path it covers**, and no bench has exercised the path that can be wrong: a part falling back to other registers **comes back *mismatch* rather than *undeclared***. Decision 21 has the derivation and the terms that exposure is accepted on.

- **The nRF54L device-ID address is confirmed on one board, and what is left open is narrower than it was.** Decision 21 records the confirmation and its limit. Two things stay unresolved and neither is expensive: **the DUT's own readback has no independent corroboration**, because its firmware self-reports nothing for the relation to check, so its 64 bits rest on the address being right rather than the other way round; and **`nRF54L10`/`nRF54L05`/`nRF54LM20A` take the same arm with no silicon ever attached.** A bench that ever runs a self-reporting build on the DUT closes the first for free.

- **No agent can induce a topology mismatch, and that is why the evidence for the refusal path is operational rather than experimental.** Every route that would point a role at different silicon goes through `enroll`, which overwrites the record the test needs, and **there is no topology override on the store path** — the only variable in it is Windows' own `ProgramData`, which an agent cannot set for a service already running. The three identity refusals now on record happened because the bench genuinely changed underneath a probe. **This is worth stating rather than rediscovering**: the next reader who wants to test the gate will look for a way to fake one, and there isn't a legitimate one short of the owner moving hardware.

- **Call-site granularity is not fully specified.** Resolution and validation are fresh-every-call by construction, with no cache in the crate; **nothing states what a caller may assume beyond that**, so a consumer wanting to hold an answer across calls has no rule to read.

- **The token and config mirrors of `embarch-api`-internal logic are untouched by this crate's existence** and still raise the extract-or-CI-diff question independently. Extracting this crate removed the *topology* copy; **those two mirror internals, not a shared concern the way topology turned out to be.** Tracked in [embarch-umbrella/open.md](../embarch-umbrella/open.md).
