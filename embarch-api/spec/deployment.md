# embarch-api: spec — deployment and topology

**Status:** active, 2026-09-05.

Split verbatim out of [implementation.md](implementation.md) §4 on 2026-11-17 under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 (`tasks/api/161`). Current truth: [../spec.md](../spec.md). Why: [../decisions.md](../decisions.md).

## 4. Deployment and topology

Today `embarch-api` runs under WSL2, Core native on Windows, same physical machine, reached over the WSL2⟷Windows network boundary rather than loopback.

**Artifact transfer branches on topology class, and the reason is Session 0.** `Local` — same machine, or an explicit `base_url` — sends `firmware_path` as JSON. `WslHost` and `Remote` both **upload the artifact's bytes** as multipart. WSL2 needs it because `\\wsl.localhost\…` UNC shares come from a per-session network provider tied to an interactive logon, and a service runs in **Session 0**, which has none. **Failure signature:** the identical path resolves from an interactive shell and fails with "the network name cannot be found" from the service — not an account problem. **No UNC path is computed anywhere any more** ([decisions](../decisions/core-link.md) 15).

**`base_url = "auto"`** resolves per-process on first use — a short-timeout `GET /status` race over an ordered candidate list (loopback, the WSL2 default-gateway IP, a configured host), first answer wins, and a `401` **counts as an answer**: Core is there, the token is wrong. Cached for the process lifetime, never written back to config, so a WSL2 restart's new gateway IP is picked up next run. **Resolution must be lazy** — MCP start makes no Core call, and `list_projects` works with Core down. **No startup check runs** — every hardware-facing tool fails per-call instead, with the resolved-candidate list. Why not refuse, and why not warn at start: [decisions](../decisions/core-link.md) 14.
