# embarch-core: open questions

**Status:** active, 2026-09-02.

What is unresolved and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Never exercised

- **Seven paths have never met their real counterpart** (`POST /bootload`, signal tap, decisions 35, 106, 89, 92, 93), each with its owner-run step: [open/never-exercised.md](open/never-exercised.md).

- **Decision 108's rename has not reached the installed service.** Built natively on Windows in a scratch copy on 2026-11-10, never deployed, so the bench's Core still serves `firmware_version`, and a caller built after the rename reports the bench's build as unknown against it. Owner-run: deploy (`embarch-dev-workflow.md` §4a), then `embarch-api dev-bench-hello` prints `dev_bench_version`.

## Unverified diagnoses

- **Whether probe-rs writes killed the nRF54L15 is evidence, not proof** (decision 36): a J-Link erase-and-program recovered the board, but a full reprogram may have cleared something else.

## Designed, not built

- **`core.toml`** (decision 11), narrowed to `bind`/`port`.
- **A `{code, message, cause}` JSON error body** — deferred, cross-repo: the `code` enum is a wire contract three consumers branch on (decision 12).
- **A subject discriminator on `Alert`** so a signal mismatch reaches `/alerts` (decision 30); not needed until a direct route is physically possible.
- **An HTTP surface, SSE stream, or `embarch-api` tool for `dev-bench.log`** (decision 37); nothing has asked.
- **A byte count alongside `GET /serial-log`'s `truncated: bool`** — rejected (decision 58) until a caller must tell 1 byte lost from 900 KB.


## Structural limits

- **Espressif-family dev-bench port selection has no current story.** Decision 23's removed env overrides had no replacement: `link_port_interface` answers an ambiguous-VCOM board, and the ESP32-C5-WROOM-1 DK is **[assumed]** to enumerate as one USB-Serial/JTAG interface with no VCOM to name (`tasks/core/028`). Confirming needs the board; the missing knob outlives it.
- **A separate-machine deployment has no artifact transfer.** Multipart (decision 10) closed WSL2; a LAN Pi cannot flash.
- **macOS is reasoned-only.** Nothing here has run on a Mac.

## Moved elsewhere, not resolved

- **Discarding a signal port's buffered input on open is not sufficient; the defence is now `embarch-ui`'s** (decision 30). A capture began with **18 stale records** seconds off — those bytes sit inside the USB-UART bridge, past an OS-level purge. Fix built as `embarch-ui` decision 19; unresolved is that it has never met the real prefix ([embarch-ui/open.md](../embarch-ui/open.md)).
