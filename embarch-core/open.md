# embarch-core: open questions

**Status:** active, 2026-09-02.

What is unresolved, and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Never exercised

- **`study_schema_mismatch` is reachable by nothing**: it names a member of the error `code` enum that does not exist. Deferred below.
- **The signal-tap path has never run against real hardware.** Unit-tested at its scope boundaries and compiled into both a Linux and a native Windows Core, but **no real port has ever been resolved or read** — resolution matches on a USB serial, and this bench has no USB-UART bridge. `validate_signal` has **no caller anywhere**, deliberately: resolving a route at the moment of use *is* the validation and returns the same error, so calling both would check twice and report once.
- **Decision 35's gate has never met ESP32-C5 silicon.** The Nordic arm is live and answers `match`; the Espressif relation is verified only by construction against the checked-out HAL headers and by unit test, that board being unplugged.
- **The Windows registry write for an *explicit* `EMBARCH_TOKEN` on an installed service has never executed on real hardware.** A real service install and start is verified, but that run set no explicit token, and only an explicit one reaches that path; the common case, an auto-generated token, never does.

## Unverified diagnoses

- **Whether probe-rs writes are what killed the nRF54L15 is evidence, not proof** (decision 36). One erase-and-program over J-Link recovered a board unresponsive across a whole session — the strongest available evidence — but **the counterfactual is not established**: a full erase-and-reprogram may have cleared something else.

## Designed, not built

- **`core.toml`** (decision 11), narrowed to `bind`/`port`.
- **A `{code, message, cause}` JSON error body** — **deferred with a trigger, not pending**: the `code` enum is a wire contract three consumers branch on, so it is cross-repo work rather than Core's alone. Cost and trigger: decision 12.
- **A subject discriminator on `Alert`**, so a signal mismatch would reach `/alerts` (decision 30). Not-needed-yet with a named trigger: nothing can raise one until a direct route is physically possible.
- **An HTTP surface, SSE stream, or `embarch-api` tool for `dev-bench.log`** (decision 37). Nothing has asked, and this suite's posture is not to build the machinery first.

## Structural limits

- **`EMBARCH_TOKEN` is one shared static token, not per-caller credentials**, and there is no TLS. Source of truth: [embarch-token.md](../embarch-token.md) §8.
- **A separate-machine deployment still has no artifact transfer.** Multipart (decision 10) closed the WSL2 case; a LAN Pi remains reachable by design and unusable for flashing in practice.
- **macOS is reasoned-only.** The elevation paths are written and unexercised; nothing in this suite has run on a Mac.
- **The route sweep proves rejection, not reach.** Decision 42 asserts all 26 registered routes answer `401` without a token and with a wrong one; only `/status` asserts that a *correct* token reaches its handler. A route wired to the wrong handler, or one whose handler is unreachable for some other reason, is not what this catches — nothing has needed that, and per-route success cases would need per-route fixtures the auth sweep deliberately does without.
- **`FlashedThisRun` is unreachable from Core alone** (decision 31), by construction, and `embarch-api` is what makes it reachable.
- **`GET /study/{id}/events` offers no `Last-Event-ID` and no replay** (decisions 24, 41): a reconnect resumes at "now" with no way to ask for what it missed. Both consumers — `embarch-api`'s `study-status --follow` and `study_watch` (`embarch-api/decisions/core-link.md` 48, 49) — fall back to polling `GET /study/{id}` on a drop rather than pretending to resume, so this is closed as not needed yet; a resumable subscriber would be new Core-side design.

## Moved elsewhere, not resolved

- **Discarding a signal port's buffered input on open is not sufficient, and the defence is now `embarch-ui`'s** (decision 30). A capture still began with **18 stale records** seconds from the rest with the purge reporting no error: those bytes are inside the USB-UART bridge, where an OS-level purge does not reach — **a limit of the purge, not a defect to fix here**, so the clear stays, being correct and free. This bullet's candidate fix is built as `embarch-ui` decision 19; what is still unresolved is that it has never met the real prefix ([embarch-ui/open.md](../embarch-ui/open.md)).

- **The nRF54L15 hardware-ID register address**, and the end-to-end validation of the moved identity gate, are `embarch-topology`'s open questions since decision 22's move. Relocating the code changed nothing about whether that address is confirmed against real silicon.
