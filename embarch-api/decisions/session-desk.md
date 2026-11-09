# embarch-api decisions: The session's desk

**Status:** active, 2026-11-09.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 85 — A call naming no project builds the session's desk's repo

A tool call that omits `project`, or any call — tool or CLI — that names the literal `desk`, means **the project on the firmware repo of the desk this session works on** ([`embarch-desk`](../../embarch-desk/spec.md) decisions 33, 77): the desk holding its folder, else its work item's. Sessions on different desks build their own at the same time, and the desk the UI shows changes none of them. Claude Code gives the MCP server and every shell the session's id (`CLAUDE_CODE_SESSION_ID`) and starts them in its folder; embarch-api asks the desk service's `GET /desks` with both as headers, over a local socket with a short timeout. **While the service is stopped, or outside a session, the desk holding the folder is read from the `desks.json` embarch-desk publishes beside its state**, so a call never waits on another service. A session on no desk gets an error asking for a project, never the UI's desk.

**The server's own config is one repo's; a desk is often another's.** The MCP server is started with one `--config`, so when that config lists no project on the desk's repo, the repo's own `embarch/embarch.toml` — what `embarch init` writes there — is loaded once and kept for the life of the process. **A repo with several projects is an error naming them, never a pick**: one repo can hold a board's application and its bench test, and building the wrong one is worse than being asked. A named project is never redirected.

Until 2026-11-09 (EMB-94) this read the one desk open suite-wide from `open-desk.json`, and a switch made for one client's session moved every other session's build. **Rejected:** the desk service alone (a dead desk would fail every unnamed call); the published file alone (a session outside every desk's folders would lose its work item's desk); choosing the first of several matching projects.
