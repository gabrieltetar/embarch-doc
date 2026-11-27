# 050 — A container login starts claude inside the agent container

**State:** claimed by agent/chat/050-a-container-login-starts-claude-inside-the-agent-container, 2026-11-26 18:52
**Source:** EMB-461 — embarch-chat can only start claude in the engineer's own account
**Issue:** EMB-461
**Scope:** chat
**Hardware:** verify-only
**Owner:** no

## What

Every chat spawns `claude` on the host (`src/wire/process.ts`, `spawn`), a login
is a `CLAUDE_CONFIG_DIR` (`src/logins.ts`), `last_session` reads that login's
`projects/` (`src/handoff.ts`), and the panel declares its own hooks and MCP
servers in `initialize` (`claudeArgs`, chat decisions 61, 65). The HIL design has
embarch-chat start `claude` inside the agent's container
(`embarch-doc/notes/hil/12-prevention.md`; `embarch-doc/embarch-hil-evidence-proposal.md`,
"The work, by sub-project"). The owner may strike this unit (plan choices 11
and 22). When this is done:

- **A login of kind `container`**: the agent container's name, the runtime
  binary, the host repo path and the exchange folder, read from what
  `embarch agent` records (`embarch-doc/embarch-umbrella/decisions/agent-container.md`,
  `agent-runtime.md`, read only).
- **The spawn**: `claudePath` is the runtime, and the args start
  `exec -i -u agent -w /work/<manifest path> <name> claude`, then today's flags.
  The environment passed is only what the flags need, never the host's.
- **Transcripts** come from `<exchange>/claude-config/projects/`, the project
  folder named for the container's working path; `last_session` reads there for
  this login.
- **A handoff from a container chat starts a container chat.**
- **Hooks and MCP servers**: the decision lists each hook and MCP server the panel
  declares in `initialize`, where each runs, and what host state it reads or
  starts. A container login declares no hook that runs a host command and none
  that starts a host-side session.
- **A container that is not running** gets a chat line naming `embarch agent up`.

## Where to look

- `src/wire/process.ts` (`SpawnSpec`, `claudeArgs`, `spawn`), `src/chats.ts`,
  `src/logins.ts`, `src/loginGate.ts`, `src/handoff.ts`, `src/lastSessionCli.ts`
- `embarch-doc/embarch-chat/decisions/logins.md` (amend it)

## Where the doc goes

`decisions/logins.md` amended (8,156 B; check its limit with
`scripts/check-doc-size.py --pressure` first), or a new decision beside it.
`promptu#96` has 204 B left: do not grow it.

## Hardware verification

Leave a debt for the first container session on the owner's machine: a chat
starts in the container, its transcript is found, a handoff stays in the
container, and no host hook runs.

## Done when

- [ ] The spawn spec for a container login is golden-tested.
- [ ] A handoff from a container chat produces a container chat's spawn spec.
- [ ] `last_session` for a container login reads the exchange folder's transcripts.
- [ ] A container login's `initialize` declares no host hook command.
- [ ] The hardware-verification debt is recorded here.
- [ ] Gate green (`npm ci`, `build`, `typecheck`, `test`, `test:webview`).
