# embarch-umbrella decisions: Check 10, is our MCP server registered and answering

**Status:** active, 2026-09-05.

**Split out of [doctor.md](doctor.md) on 2026-09-05, entries moved verbatim** — save decision 40's codes paragraph, rewritten here to record `no-cli`'s reuse. That file's mission is what `doctor` checks about *this machine* — probes, benches, flash tools; these two are one check against a different system, the agent CLI's own config and a JSON-RPC handshake with a server spawned out of it.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md)'s check 10 row. What a check hands back — `code`, `path`, `--json` — is [reporting.md](reporting.md).

### 23 — Check 10 spawns `embarch-api` and confirms the MCP handshake completes, not just that a registration entry exists

**The failure mode the check exists to catch — registered but broken — is exactly the one it cannot detect:** adding a registration says nothing about whether the registered command actually starts and speaks the protocol. It would spawn the exact registered command with a short timeout and send a minimal initialize handshake, **reporting success, failure and timeout distinctly.** A hand-rolled one-shot JSON-RPC exchange is sufficient; a full client is not needed for one round trip.

**Built 2026-09-04; amended 2026-09-05 by decision 40.** Check 10 spawns the registered command with piped stdio, writes one `initialize` request and waits 10 s for a matching JSON-RPC response — no session, no client, no second request, and the three outcomes carry distinct `code` values into `--json` (decision 37). All of that stands. **Where it got the command line did not:** it read `claude mcp get embarch`'s human output, a format that turned out not to exist, so from 2026-09-05 it reads the agent CLI's own config instead.

**Two states the decision did not name, and both are warns rather than either verdict.** No agent CLI here at all was already a warn and stays one — **though not for the reason given here**: decision 40 found `claude` is never on `PATH`, so that arm was the only one this check could reach from a terminal. The other is a registration with nothing to spawn, which keeps the warn for the reason that outlived the parse — an entry proves nothing, so a check that cannot start the server must not invent a verdict about it.

**Timeout is Fail, not Warn, and stays its own code.** A server that takes longer than 10 s to say hello is a finding either way; the separate code is what makes a badly chosen budget visible as itself rather than as a mystery failure. The 10 s is assumed, not measured.

### 40 — Check 10 reads the agent CLI's own config for the command to spawn, and knows our server by the binary it names rather than by the key it sits under

**Decision 23's parse target does not exist.** Read for the first time on 2026-09-05 (Claude Code 2.1.261), `claude mcp get <name>` prints the name, `Scope:` and `Status:` — **no `Command:`, no `Args:`** — and there is no `--json` on `mcp get` or `mcp list`, so **check 10 could only reach `unreadable-entry` and its handshake was unreachable code.** Two more from that sitting: the working registration is keyed `embarch-api` while `MCP_SERVER_NAME` is `embarch`, so `doctor` said *not registered* beside a server the same session was using; and `claude` lives inside the VS Code extension, never on `PATH`, so from a terminal only the `no-cli` arm was reachable at all.

**Read `~/.claude.json`, keep the spawn** — its `projects.<absolute cwd>.mcpServers` entries carry `command` and `args` already structured. Trusting `Status: ✔ Connected` instead **loses on the third finding rather than on taste**: reading it still means running `claude`, so that route reaches no verdict on the machine it was written for, and it hands the answer back to the CLI's own health check, which is what decision 23 built a spawn to reproduce independently.

**Identity is the command, not the key**: `embarch`, else any entry whose `command` names an `embarch-api` binary (`file_stem`, so `.exe` counts), else the key `embarch-api` — and the verdict names which it found. Local scope for the working directory is searched before user scope, so *registered* stays a question about where `doctor` ran. `.mcp.json` is not searched: `init` never writes it (decision 12).

**`env` closes; the environment does not.** The entry's `env` is applied on the spawn, but **the server still starts in `doctor`'s environment** rather than the CLI's — decision 23's gap shrunk, not closed.

**The code set is unchanged, and `no-cli` is reused deliberately.** It used to mean *`claude` is not on `PATH`*; it now names the state this decision replaced that one with — *there is no agent-CLI config to read*. To a consumer both are the same fact, there is no agent CLI here to consult, and both take the same action, so a new code would split a set nothing branches on. A remote-transport entry likewise shares `unreadable-entry` rather than taking a code of its own, since `init` writes only stdio and both are the same actionable thing. **A code whose referent moves under a stable name is the one way [decision 37](reporting.md)'s promise breaks silently, and no check in the gate can see it** — so a reuse is written down here or it is not a reuse.

**Unverified live**; the lines a healthy and a degraded run should print are pinned in `tasks/umbrella/011`.
