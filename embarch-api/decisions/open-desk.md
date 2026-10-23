# embarch-api decisions: The open desk

**Status:** active, 2026-10-22.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 85 — A call naming no project builds the open desk's repo

A tool call that omits `project`, or any call — tool or CLI — that names the literal `desk`, means **the project on the open desk's firmware repo** ([`embarch-desk`](../../embarch-desk/spec.md) decision 33). The open desk is read from the `open-desk.json` embarch-desk publishes beside its state, **not from its HTTP surface**, so a stopped desk still answers with the last desk opened and a call never waits on another service.

**The server's own config is one repo's; a desk is often another's.** The MCP server is started with one `--config`, so when that config lists no project on the desk's repo, the repo's own `embarch/embarch.toml` — what `embarch init` writes there — is loaded once and kept for the life of the process. **A repo with several projects is an error naming them, never a pick**: one repo can hold a board's application and its bench test, and building the wrong one is worse than being asked. A named project is never redirected.

**Rejected:** making `project` optional by reading the desk over HTTP (a dead desk would fail every unnamed call), and choosing the first of several matching projects.
