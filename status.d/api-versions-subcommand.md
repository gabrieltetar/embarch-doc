**Target:** suite/features.md § embarch-api — a new row, and the "CLI subcommands mirroring every tool" row
**Was:** "CLI subcommands mirroring every tool (kebab-case, unlike the snake_case tools) | Shipped | hw | §5a"
**Now:** the CLI is a superset, not a mirror: `versions` is a subcommand with no MCP tool.

New row for the same table:

| `versions` — the compiled study-designer host type schema version, readable without a config or a live Core | Shipped | unit | 52 |

Why it exists and why not a `status --json` field: [embarch-api/decisions/surface.md](../embarch-api/decisions/surface.md) 52. `doctor` check 11's own row is unaffected — it still compares `embarch`'s own constant until `embarch-umbrella` points it here.
