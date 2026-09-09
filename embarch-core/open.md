# embarch-core: open questions

**Status:** active, 2026-09-02.

What is unresolved, and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Never exercised

- **`study_schema_mismatch` is reachable by nothing**: it names a member of the error `code` enum that does not exist. Deferred below.
- **The signal-tap path has never run against real hardware.** Unit-tested and compiled for both Linux and native Windows, but no real port has been resolved or read — this bench has no USB-UART bridge. `validate_signal` has no caller anywhere, deliberately: resolving a route at the moment of use *is* the validation, so calling both would check twice and report once.
- **Decision 35's gate has never met ESP32-C5 silicon.** The Nordic arm is live and answers `match`; the Espressif relation is verified only by construction against the checked-out HAL headers and by unit test, that board being unplugged.
- **`GET /logs/stream` has no consumer, and its torn-write path has never met a real tear.** `embarch-core-client` has no method for it; the UI's Debug tab uses `/logs/recent`. Decision 44's hold-the-partial rule is exercised only against a synthetic half-line.
- **The Windows registry write for an *explicit* `EMBARCH_TOKEN` on an installed service has never executed on real hardware.** A real service install and start is verified, but that run set no explicit token, and only an explicit one reaches that path; the common case, an auto-generated token, never does.

## Unverified diagnoses

- **Whether probe-rs writes are what killed the nRF54L15 is evidence, not proof** (decision 36). One erase-and-program over J-Link recovered a board unresponsive across a whole session — the strongest available evidence — but **the counterfactual is not established**: a full erase-and-reprogram may have cleared something else.

## Designed, not built

- **`core.toml`** (decision 11), narrowed to `bind`/`port`.
- **A `{code, message, cause}` JSON error body** — **deferred with a trigger, not pending**: the `code` enum is a wire contract three consumers branch on, so it is cross-repo work rather than Core's alone. Cost and trigger: decision 12.
- **A subject discriminator on `Alert`**, so a signal mismatch would reach `/alerts` (decision 30). Not-needed-yet with a named trigger: nothing can raise one until a direct route is physically possible.
- **An HTTP surface, SSE stream, or `embarch-api` tool for `dev-bench.log`** (decision 37). Nothing has asked, and this suite's posture is not to build the machinery first.

## Structural limits

- **Espressif-family dev-bench port selection has no current story.** Decision
  23's four removed env overrides had no stated replacement: `link_port_interface`
  answers an ambiguous-VCOM board, and the ESP32-C5-WROOM-1 DK is **[assumed]**,
  unmeasured, to enumerate as a single USB-Serial/JTAG interface with no VCOM to
  name — `tasks/core/028` cites `dev-bench/005`, which declined to assert it.
  Confirming it needs the board.
- **A separate-machine deployment still has no artifact transfer.** Multipart (decision 10) closed the WSL2 case; a LAN Pi remains reachable by design and unusable for flashing in practice.
- **macOS is reasoned-only.** The elevation paths are written and unexercised; nothing in this suite has run on a Mac.
- **The route sweep proves rejection, not reach.** Decision 42 asserts all 27 registered routes answer `401` without a token and with a wrong one; only `/status` asserts that a *correct* token reaches its handler. A route wired to the wrong handler is not what this catches — nothing has needed that, and per-route success cases would need per-route fixtures the auth sweep deliberately does without.

## Owed decisions

- **`GET /serial-log`'s caps have no numbered decision** — `tasks/core/009` shipped `serial::MAX_DURATION_MS` (10,000 ms) and a byte cap (`EMBARCH_SERIAL_LOG_MAX_BYTES`, 1 MiB default) with a `truncated: bool` shape, all reasoned not measured, withheld from `decisions.md` under that leg's burndown constraint. Owed: why those numbers, and why a boolean rather than a byte count.

## Moved elsewhere, not resolved

- **Discarding a signal port's buffered input on open is not sufficient; the defence is now `embarch-ui`'s** (decision 30). A capture began with **18 stale records** seconds off, purge reporting no error — those bytes sit inside the USB-UART bridge, past where an OS-level purge reaches, so the clear stays (correct and free). Candidate fix built as `embarch-ui` decision 19; unresolved is that it has never met the real prefix ([embarch-ui/open.md](../embarch-ui/open.md)).
