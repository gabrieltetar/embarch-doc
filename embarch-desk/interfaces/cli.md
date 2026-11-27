# embarch-desk: connectors and CLI

**Status:** active, 2026-11-17. Split out of [../interfaces.md](../interfaces.md) verbatim when that file reached its reserve line; nothing restated.

## Connectors and CLI

**Connectors** (pasted tokens, [decision 16](../decisions.md)): Linear personal API key per workspace (GraphQL), or, for a workspace that gives no key, a sign-in through Linear's MCP server whose account keeps `[linear.mcp]` (`client_id`, `refresh_token`, `expires_ms`) and is answered through the server's tools (68); Harvest personal access token (REST v2, every account it reaches); GitHub token or the user's `gh` login (REST; PR search by key, within the desk's repos when it names some). A kind is `linear`, `harvest` or `github`; a `[[slack]]` table saved before decision 66 still loads, is never read and is written back on save.

**CLI:** `serve`, `hook`, `mcp`, `service install|uninstall|status` (a systemd user unit, written by the `embarch-user-unit` crate, decision 94), `connect <kind> <label>` (token on stdin; `connect linear <label> --mcp` prints the sign-in link instead and waits for the browser), `disconnect`, `get <route> [--post <json>] [--count-by <field>] [--raw] [--config-dir <dir>] [--port <n>]` (a route's shape from a shell: top-level keys, each list's length, one sample row, rows counted by a field; `--raw` the JSON; no token handled by the caller), `ignore list|add|remove`, `desks` (the UI's marked `*`, and inside a session the one it works on), `status`.

**`get`** reaches the default instance, or a named one with `--config-dir` (where its `desk-token` is read, never generated) and `--port`, else `EMBARCH_DESK_CONFIG_DIR` / `EMBARCH_DESK_PORT`. **It masks, never refuses:** a value under a key naming a secret (`token`, `secret`, `password`, `authorization`, `api_key`, `bearer`, `credential`) prints as `***` whatever its type, and so does the desk's own token inside any string, in the shape and in `--raw`.
