# 050 — A container login starts claude inside the agent container

**State:** done — container login: spawn, handoff, transcripts and initialize golden-tested; hardware debt recorded
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

- [x] The spawn spec for a container login is golden-tested.
- [x] A handoff from a container chat produces a container chat's spawn spec.
- [x] `last_session` for a container login reads the exchange folder's transcripts.
- [x] A container login's `initialize` declares no host hook command.
- [x] The hardware-verification debt is recorded here.
- [x] Gate green (`npm ci`, `build`, `typecheck`, `test`, `test:webview`).

## Hardware-verification debt

Nothing started a container or a real `claude`: every test runs against a stand-in runtime that records its argv, environment and first stdin line. For the first container session on the owner's machine (after `embarch init --container` and `embarch agent up`), with `embarchChat.logins.<name>.container.record` set to the agent's `container.toml` and that login picked:

- A chat starts in the container: `docker ps` shows the `exec`, and `pwd` in the chat is `/work/<repo>`.
- Its transcript is found: `<exchange>/claude-config/projects/-work-<repo>/<session>.jsonl` exists, the chat resumes after an idle close and after a window reload, and `last_session` reads it.
- A handoff stays in the container: the fresh chat's process is another `docker exec`, never a host `claude`.
- No host hook runs: editing a file in the chat does not save an editor buffer, and no `diagnostics` tool is offered.
- `embarch agent down`, then a message: the chat line names `embarch agent up` (the runtime's "not running" text is matched, **unverified** for Podman).
- Unverified by construction: the panel's SDK file-checkpointing and interrupted-step-rerun variables do not cross `exec`, so a message's file rewind and the rerun after a reload may not work in a container chat.

## Decided here (see decision 122)

The container is read from `container.toml` (name from `--name=`, runtime, `/person/repo` and `claude-config` mounts), not from separate settings; the repo's folder under `/work` defaults to the host repo's name, overridable by `manifestPath`. A record that cannot be read refuses, never falls back to the host. The autosave hook and the diagnostics tool are dropped for a container login (they act on the editor with container paths); `handoff` and `last_session` stay. Filed `tasks/chat/051-compact-chat.md`: this unit moved `spec.md` and `open.md` into reserve.
