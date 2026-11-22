# embarch-core open: designed, not built

**Status:** active, 2026-11-22. Moved out of [../open.md](../open.md) verbatim by `tasks/core/135` (the compaction of `tasks/core/133`). Current truth: [../spec.md](../spec.md).

## Designed, not built

- **`core.toml`** (decision 11), narrowed to `bind`/`port`.
- **A `{code, message, cause}` JSON error body** — deferred, cross-repo: the `code` enum is a wire contract three consumers branch on (decision 12).
- **A subject discriminator on `Alert`** so a signal mismatch reaches `/alerts` (decision 30); not needed until a direct route is physically possible.
- **An HTTP surface, SSE stream, or `embarch-api` tool for `dev-bench.log`** (decision 37); nothing has asked.
- **A byte count alongside `GET /serial-log`'s `truncated: bool`** — rejected (decision 58) until a caller must tell 1 byte lost from 900 KB.
