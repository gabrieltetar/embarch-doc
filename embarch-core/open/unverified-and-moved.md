# embarch-core open: unverified, and moved elsewhere

**Status:** active, 2026-11-22. Moved out of [../open.md](../open.md) verbatim by `tasks/core/135` (the compaction of `tasks/core/133`). Current truth: [../spec.md](../spec.md).

## Unverified diagnoses

- **Whether probe-rs writes killed the nRF54L15 is evidence, not proof** (decision 36): a J-Link erase-and-program recovered the board, but a full reprogram may have cleared something else.

## Moved elsewhere, not resolved

- **Discarding a signal port's buffered input on open is not sufficient; the defence is now `embarch-ui`'s** (decision 30). A capture began with **18 stale records** seconds off — those bytes sit inside the USB-UART bridge, past an OS-level purge. Fix built as `embarch-ui` decision 19; unresolved is that it has never met the real prefix ([embarch-ui/open.md](../../embarch-ui/open.md)).

