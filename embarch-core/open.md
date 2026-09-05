# embarch-core: open questions

**Status:** active, 2026-09-02.

What is unresolved, and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Never exercised

- **`study_schema_mismatch` is reachable by nothing**: it names a member of the error `code` enum that does not exist. Deferred below.
- **The signal-tap path has never run against real hardware.** Unit-tested at its scope boundaries and compiled into both a Linux and a native Windows Core, but **no real port has ever been resolved or read** — resolution matches on a USB serial, and this bench has no USB-UART bridge. `validate_signal` has **no caller anywhere**, deliberately: resolving a route at the moment of use *is* the validation and returns the same error, so calling both would check twice and report once.
- **Decision 35's gate has never met ESP32-C5 silicon.** The Nordic arm is live and answers `match`; the Espressif relation is verified only by construction against the checked-out HAL headers and by unit test, that board being unplugged. Noted so the two are not conflated.
- **The Windows registry write for an *explicit* `EMBARCH_TOKEN` on an installed service has never executed on real hardware.** A real service install and start is verified, but that run set no explicit token, and the registry path is only reached when one is set. Narrow: the common case, an auto-generated token, never touches it.

## Unverified diagnoses

- **Whether probe-rs writes are what killed the nRF54L15 is evidence, not proof** (decision 36). One erase-and-program over J-Link recovered a board unresponsive across a whole session — the strongest available evidence — but **the counterfactual is not established**: a full erase-and-reprogram may have cleared something else.
- **Discarding a signal port's buffered input on open is not sufficient** (decision 30). With the clear in place a capture still began with **18 stale records** carrying a cycle count seconds from the rest, and the purge reported no error — so the bytes are presumably inside the USB-UART bridge or in flight, beyond an OS-level purge. The clear stays, being correct and free. The working defence is `embarch-ui` refusing the DUT clock when a capture's two clocks contradict, which costs the microsecond axis for the whole capture. **Candidate fix:** drop a leading run of records whose cycles are discontinuous with the bulk, at render time, where the whole file is in hand.

## Designed, not built

- **`core.toml`** (decision 11), narrowed to `bind`/`port`.
- **A `{code, message, cause}` JSON error body** — **deferred with a trigger, not pending**: the `code` enum is a wire contract three consumers branch on, so it is cross-repo work rather than Core's alone. Cost and trigger: decision 12. (`core_version` shipped; the `contract_version` beside it is retired — decision 13.)
- **A subject discriminator on `Alert`**, so a signal mismatch would reach `/alerts` (decision 30). Not-needed-yet with a named trigger: nothing can raise one until a direct route is physically possible.
- **An HTTP surface, SSE stream, or `embarch-api` tool for `dev-bench.log`** (decision 37). Nothing has asked, and this suite's posture is not to build the machinery first.

## Structural limits

- **`EMBARCH_TOKEN` is one shared static token, not per-caller credentials**, and there is no TLS. Source of truth: [embarch-token.md](../embarch-token.md) §8.
- **A separate-machine deployment still has no artifact transfer.** Multipart (decision 10) closed the WSL2 case; a LAN Pi remains reachable by design and unusable for flashing in practice.
- **macOS is reasoned-only.** The elevation paths are written and unexercised; nothing in this suite has run on a Mac.
- **`FlashedThisRun` is unreachable from Core alone** (decision 31), by construction — `/flash` and `/study` are separate calls with nothing linking them, and the alternative is a persisted "last thing I flashed" record this suite forbids. `embarch-api` is what makes it reachable.
- **`GET /study/{id}/events` offers no `Last-Event-ID` and no replay** (decisions 24, 41). Now consumed by `embarch-api`'s `study-status --follow` and `study_watch` (`embarch-api/decisions/core-link.md` 48, 49), but a reconnect resumes at "now" with no way to ask for what it missed; both consumers fall back to polling `GET /study/{id}` on a drop rather than pretending to resume. Resumable subscribers would be new Core-side design, closed here as not needed yet.

## Moved elsewhere, not resolved

- **The nRF54L15 hardware-ID register address**, and the end-to-end validation of the moved identity gate, are `embarch-topology`'s open questions since decision 22's move. Relocating the code changed nothing about whether that address is confirmed against real silicon.
