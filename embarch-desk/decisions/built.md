# embarch-desk decisions: What building v1 settled

**Status:** active, 2026-10-23.

Commits and bench activity from hooks, the 8-hour gap, the state file, Open in VS Code, branch claims, the service, the proxy.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 22 — Commits and bench activity are read from PostToolUse, not reported by their tools
A `Bash` call whose command contains `git commit`, followed by a HEAD the session has not seen, becomes one tile line with the commit's subject. An `mcp__…embarch-api__` build, flash, bootload, reset or study call becomes bench activity, failed when its response says `isError`. Lines and bench seen before the session has a work item are held and move onto it when it gets one.

### 23 — A gap over 8 hours ends a span
Idle gaps count (11), so a three-hour lunch is session time — but a VS Code window left open overnight is not a night of work. 8 hours is a guess that separates the two; activity that runs across midnight splits at midnight instead.

### 24 — One JSON state file, flushed every two seconds
Owned by the one process that serves it, rewritten atomically, with acted-on tiles moving to `history/YYYY-MM.jsonl` after a week. Hooks fire on every tool call, so writes mark the state dirty and a flusher persists it. **Rejected:** SQLite — queries for free, one compiled C dependency for kilobytes a day.

### 25 — *Open in VS Code* is two links and a claim
The card records "the next session in this repo is this item" for 10 minutes, then the browser follows a `vscode://vscode-remote/wsl+<distro>/<path>` link (plain `vscode://file` off WSL) and, four seconds later, `vscode://anthropic.claude-code/open?prompt=…`, which pre-fills the Claude Code panel (documented as never auto-submitted). The first session starting in that repo takes the claim. **Rejected:** the desk spawning `code` itself — under a systemd service there is no VS Code CLI environment to reach.

### 26 — A branch naming a card's issue claims the session
`user/abc-123-…` puts a session on the card that already carries `ABC-123`. It never creates a card; an unknown key still asks (7).

### 27 — A systemd user service beside Claude Code
On the owner's machine that is WSL, not a Windows service beside Core: it runs `claude -p` and resolves repo paths locally, and the browser reaches it through `embarch-ui`. The unit carries the installing shell's `PATH`, because a user service starts without the user's own bins and the desk runs `claude`, `gh`, `git` and `wslpath`. **Rejected:** a Windows service (every polish call and path crosses the boundary; deploys need UAC), hosting inside `embarch-ui` (sessions lost while the UI is closed), a spool file ingested later (no live tiles).

### 28 — The browser reaches the desk only through `embarch-ui`
`/api/desk/{*rest}` is forwarded with the desk token added server-side. The token never enters the page, so no other site open in the browser can make the desk post to Slack or Harvest as the user.
