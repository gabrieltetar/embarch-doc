**Target:** suite/features.md § `embarch-api` — two missing rows, no existing row is wrong
**Was:** the table's last two rows are `| PATH/toolchain preflight | **Moved** … |` and `| The UNC artifact path | **Retired** — it only ever worked against a foreground Core, never the installed service | hw | §9 |`
**Now:** the `--json`/MCP surface carries `schema_version` on every object as of 2026-09-03, and `error_kind` is retired unbuilt.

Nothing in the table became false — it simply has no row for either, and both are
caller-facing contract facts of the kind it inventories. Two rows, alongside the
existing `**Retired**` precedent:

| `schema_version` on every `--json`/MCP object, stamped by one serializer | Shipped | unit | 24, 50 |
| `error_kind` — a machine-readable failure kind | **Retired** — documented from the first commit, never built; needs Core to serve error codes at all | n/a | 16, 50 |

Why, and what a caller branches on instead:
[embarch-api/decisions/surface.md](../embarch-api/decisions/surface.md) 50 and
[embarch-api/open.md](../embarch-api/open.md)'s "Unfinished couplings".
