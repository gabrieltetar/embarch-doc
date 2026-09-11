# embarch-core: open questions

**Status:** active, 2026-09-02.

What is unresolved and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Never exercised

- **`study_schema_mismatch` is reachable by nothing**: it names a member of the error `code` enum that does not exist. Deferred below.
- **The signal-tap path has never run against real hardware.** Unit-tested on Linux and native Windows; no real port has been resolved or read — this bench has no USB-UART bridge. `validate_signal` has no caller by design: resolving a route at use *is* the validation.
- **Decision 35's gate has never met ESP32-C5 silicon.** The Nordic arm is live and answers `match`; the Espressif relation is verified only by construction against the checked-out HAL headers and by unit test, that board being unplugged.
- **The Windows registry write for an *explicit* `EMBARCH_TOKEN` has never executed on real hardware.** A real install/start is verified with no explicit token; only an explicit one reaches that path, and the common case — auto-generated — never does.

## Unverified diagnoses

- **Whether probe-rs writes killed the nRF54L15 is evidence, not proof** (decision 36). One erase-and-program over J-Link recovered a board unresponsive across a whole session, but the counterfactual is not established: a full erase-and-reprogram may have cleared something else.

## Designed, not built

- **`core.toml`** (decision 11), narrowed to `bind`/`port`.
- **A `{code, message, cause}` JSON error body** — deferred with a trigger, not pending: the `code` enum is a wire contract three consumers branch on, so it is cross-repo work, not Core's alone. Cost and trigger: decision 12.
- **A subject discriminator on `Alert`**, so a signal mismatch would reach `/alerts` (decision 30). Not-needed-*yet*, with a named trigger: nothing can raise one until a direct route is physically possible.
- **An HTTP surface, SSE stream, or `embarch-api` tool for `dev-bench.log`** (decision 37). Nothing has asked; this suite's posture is not to build machinery first.

## Structural limits

- **Espressif-family dev-bench port selection has no current story.** Decision
  23's four removed env overrides had no stated replacement: `link_port_interface`
  answers an ambiguous-VCOM board, and the ESP32-C5-WROOM-1 DK is **[assumed]**,
  unmeasured, to enumerate as a single USB-Serial/JTAG interface with no VCOM to
  name — `tasks/core/028` cites `dev-bench/005`, which declined to assert it.
  Confirming the enumeration needs the board; the missing replacement knob
  outlives that confirmation.
- **A separate-machine deployment has no artifact transfer.** Multipart (decision 10) closed the WSL2 case; a LAN Pi remains reachable by design, unusable for flashing.
- **macOS is reasoned-only.** The elevation paths are written, unexercised; nothing here has run on a Mac.
- **The route sweep proves rejection, not reach.** Decision 42 asserts all 27 registered routes answer `401` without a token and with a wrong one; only `/status` asserts a *correct* token reaches its handler. A route wired to the wrong handler is not caught — per-route success cases would need per-route fixtures the auth sweep deliberately does without.

## Owed decisions

- **`GET /serial-log`'s caps have no numbered decision** — `tasks/core/009` shipped `serial::MAX_DURATION_MS` (10,000 ms) and a byte cap (`EMBARCH_SERIAL_LOG_MAX_BYTES`, 1 MiB default) with a `truncated: bool` shape, all reasoned not measured. Owed: why those numbers, and why a boolean rather than a byte count.

## Moved elsewhere, not resolved

- **Discarding a signal port's buffered input on open is not sufficient; the defence is now `embarch-ui`'s** (decision 30). A capture began with **18 stale records** seconds off — those bytes sit inside the USB-UART bridge, past an OS-level purge. Fix built as `embarch-ui` decision 19; unresolved is that it has never met the real prefix ([embarch-ui/open.md](../embarch-ui/open.md)).
