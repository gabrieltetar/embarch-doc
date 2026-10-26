# embarch-api decisions: Reaching Core

**Status:** active, 2026-09-06.

Address resolution and artifact transfer — how a call finds Core and gets bytes to it. The shared
client crate itself (extraction, the auth funnel, the stack, older-Core parsing, one WSL2
predicate, and the crate's home) split out to [client-crate.md](client-crate.md) on 2026-09-11,
`api/067`, once this file went over cap — a real topical seam (address resolution vs. the crate
that does the addressing) rather than a squeeze. The event stream split out to
[study-events.md](study-events.md) on 2026-09-07. The per-machine logfile split out to
[logging.md](logging.md) on 2026-09-10.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The client
crate: [client-crate.md](client-crate.md). The event stream: [study-events.md](study-events.md).
The logfile: [logging.md](logging.md).

### 11 — `base_url = "auto"`, resolved per-process at first use
The WSL2⟷Windows split reaches Core at a host-gateway IP that **changes across WSL2 restarts**, so a literal address in config is guaranteed to go stale — and did. Resolution belongs here rather than in a setup step precisely because the value has to be right **at the moment a build is flashed**, not at the moment setup last ran, and this is the process present then. It does not weaken decision 7: `auto` makes localhost merely one candidate, and an explicit URL still wins outright. Mechanism: [../spec.md](../spec.md) §4.

### 14 — Starting with Core unreachable is a warning, not a refusal
The eager check previously **refused to start the MCP server at all**, which meant every tool vanished from the agent's view with no way to learn why — directly contradicting the rule that failures should come back as text an agent can reason about. **Amended 2026-10-26 (api/136): no startup check runs at all.** MCP start makes no `GET /status` call; the warning the earlier text promised was never built, and a startup log line reaches the logfile, never the agent, while a per-call failure carries the message to the agent that needs it. So the posture is the second half only: every hardware-facing tool fails per-call with the failure plus the resolved-candidate list, rather than never being callable, and `list_projects` is unaffected. A probe would add a request at start for a signal nobody reads; revisit only if something consumes it.

### 15 — Artifact transfer branches on topology class, not on a guess about shared filesystems
Originally scoped to trigger only for a genuinely remote Core, on the theory that local and WSL2-host topologies always share a filesystem. **That premise was false for WSL2 specifically**, when Core runs as the installed Windows service rather than in the foreground — and every earlier "confirmed working" claim for the UNC mechanism had been validated against a *foreground* Core. Both WSL2-host and remote now upload bytes; only a same-machine or explicitly-addressed Core keeps sending a path. `artifact_path_for_core` and its UNC computation are **fully retired rather than left unchanged as originally planned** — [../spec.md](../spec.md) §4 has the Session 0 mechanism and the failure signature.

### 17 — (Retired 2026-10-26, api/136) Checking Core's contract version
Retired: it was never built, and could not be. Core serves no contract version, deliberately ([surface.md](surface.md) 14), so there is nothing to compare, and with decision 14 amended there is no startup status call to carry a warning. Version skew shows where a call is made: `post_study` still reads `GET /status` and refuses across a schema-version mismatch.

### 26 — `serial_log`'s `serial_port` field was never meant to reach a DUT
**Corrected 2026-09-09** (`api/041`): originally justified by calling a DUT's serial console "a different, project-specific port that config already covers" — treating DUT-UART capture as intended, on par with the bench's. Never true: Core's serial link was only ever meant to reach the bench; the field existing doesn't mean pointing it at a DUT was supported, only that nothing stops it. **No such fallback mechanism was ever built** — see `interfaces/tools.md`'s `serial_log` row.

Decisions 36, 37/38, 55, 58, 62 and 66 — the shared client crate's extraction, its auth funnel,
its stack, its older-Core parsing, its one WSL2 predicate, and its home — moved to
[client-crate.md](client-crate.md) on 2026-09-11 (`api/067`).
