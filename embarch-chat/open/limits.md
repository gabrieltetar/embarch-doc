# embarch-chat open: structural limits

**Status:** active, 2026-11-17.

Split out of [../open.md](../open.md) on 2026-11-17, verbatim: limits that come from VS Code or the CLI and wait on no one. Current truth: [../spec.md](../spec.md). Why: [../decisions.md](../decisions.md).

## Structural limits

- **A change dropped in a per-change diff is not reported to the CLI** (decision 64): the permission answer has no field for it, so Claude learns of it only by reading the file.
- **An MCP call cannot move to the background** (decision 70): the CLI never registers one as a foreground task, so a long `embarch-api` flash holds its turn.
- **The activity-bar count appears only once the list has been opened** (decision 35): VS Code builds a view lazily. The status-bar count always shows.
- **A new Claude Code panel session's login is recorded at its first resume, not at its start** (106): the panel gives the wrapper no session id for a new session. Until then it is on the window's pick, so a pick changed before that first resume moves it.
- **Two windows on one folder share one pick** (106): the wrapper follows the window last picked or focused, and the other window's item can say otherwise until it is focused.
