# 022 — The desk says when a repo has no `embarch-api` in its login

**State:** claimed by agent/desk/022-the-desk-says-when-a-repo-has-no-embarch-api-in-its-login, 2026-11-10 03:30
**Source:** Linear issue EMB-17
**Issue:** EMB-17
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

Claude Code keeps MCP servers per login, in `<CLAUDE_CONFIG_DIR>/.claude.json` (or `~/.claude.json` with no `CLAUDE_CONFIG_DIR`): at user scope under `mcpServers`, or per folder under `projects.<absolute path>.mcpServers`; a repo's own `.mcp.json` adds project servers. A login that registered `embarch-api` only per folder has none in a repo added later, nor in a Start work worktree, whose path is new. A session there has no build, flash or bootload tools and nothing says why.

Make the desk say so, **with this direction (decided at the split):**

- **The desk reads the login's `.claude.json`; it never writes it.** Claude Code rewrites that file while it runs, so a second writer risks losing one of the writes. Registering stays a command the user runs.
- **The check:** for a desk folder, `embarch-api` counts as registered if the login's user-scope `mcpServers`, that folder's `projects` entry, or the folder's `.mcp.json` names it. The login is the desk instance's (`src/service.rs` sets `CLAUDE_CONFIG_DIR` per instance).
- **Where it is said:** in the desk's answer for its folders (a field per folder, `GET` of the desks and `desks.json` if that is where folders are listed), and once at session start in a folder that lacks it, in the hook's session-start text beside the standing notes (decision 74). The worker picks the exact wording, which names the login's folder.
- **The command it gives registers at user scope**, `claude mcp add --scope user embarch-api -- <binary> --config <config>`, because user scope covers every worktree, as the other login already does. The binary and config come from an existing `embarch-api` entry in either login's `.claude.json` when there is one; otherwise the command says which two values to fill in. The worker confirms the `claude mcp add` flags against `claude mcp add --help`.
- Where `embarch setup` (`embarch-umbrella`) could register the server is out of scope; say so in the decision.

## Why now

EMB-17: a new client repo opened in the work login has no `embarch-api` tools, and the session finds out only when a build is asked for and no tool exists.

## Where to look

- `src/service.rs` — `claude_config_dir` per desk instance
- `src/memory.rs` — how the desk already resolves Claude Code's folder from `CLAUDE_CONFIG_DIR`
- `src/hook.rs`, `src/brief.rs` — the session-start text
- `src/store.rs` `Desk` and `src/server.rs` — a desk's folders and the routes that list them; `desks.json`
- `embarch-doc/embarch-desk/decisions/desks.md` (33, 35, 74, 77) and `spec.md`; `interfaces.md` for any field added to a route

## Dispatch notes

- Normal mode: a new numbered `embarch-desk` decision is expected. Number it per `DOC-CONVENTIONS.md`; check `main` before you commit, since `desk/020` and `desk/021` land before you.
- Tests use temporary `.claude.json` files; never read or write the real ones.
- Doc-size reserve at dispatch: `embarch-desk/decisions/access-point.md` is at 91.2% (1082 B left), already filed as `tasks/desk/023`. Put the new decision in `decisions/desks.md`, not there. Decisions 80 and 81 landed this leg, so the next number is 82 unless `main` says otherwise.
- Edit files with your Edit and Write tools, not inline Python or shell redirects.

## Done when

- [ ] A desk folder whose login has no `embarch-api` at user scope, in its `projects` entry or in its `.mcp.json` is marked as such in the desk's answer, with the command to register it.
- [ ] A session starting in such a folder is told once, with the same command.
- [ ] The desk never writes `.claude.json`; a test covers each of the three places that count as registered, and the missing case.
- [ ] A new `embarch-desk` decision records the check and why the desk does not register the server itself; `interfaces.md` lists any new field.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.
