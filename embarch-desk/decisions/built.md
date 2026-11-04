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
The card records "the next session in this repo is this item" for 10 minutes, then the browser follows a `vscode://vscode-remote/wsl+<distro>/<path>?windowId=_blank` link (plain `vscode://file` off WSL) and, four seconds later, `vscode://anthropic.claude-code/open?prompt=…`, which pre-fills the Claude Code panel (documented as never auto-submitted). The first session starting in that repo takes the claim. **`windowId=_blank` is load-bearing:** without it VS Code opens the folder in the last-focused window, replacing that window's folder and ending the chat running there. With it, the folder gets a new window, or its own window brought up when it is already open. **Rejected:** the desk spawning `code` itself — under a systemd service there is no VS Code CLI environment to reach.

### 26 — A branch naming a card's issue claims the session
`user/abc-123-…` puts a session on the card that already carries `ABC-123`. It never creates a card; an unknown key still asks (7).

### 27 — A systemd user service beside Claude Code
On the owner's machine that is WSL, not a Windows service beside Core: it runs `claude -p` and resolves repo paths locally, and the browser reaches it through `embarch-ui`. The unit carries the installing shell's `PATH`, because a user service starts without the user's own bins and the desk runs `claude`, `gh`, `git` and `wslpath`. **Rejected:** a Windows service (every polish call and path crosses the boundary; deploys need UAC), hosting inside `embarch-ui` (sessions lost while the UI is closed), a spool file ingested later (no live tiles).

### 28 — The browser reaches the desk only through `embarch-ui`
`/api/desk/{*rest}` is forwarded with the desk token added server-side. The token never enters the page, so no other site open in the browser can make the desk write to Linear or Harvest as the user.

### 69 — A second desk runs as a named instance, with time and draft-only writes switchable
`embarch-desk service install --instance NAME --port N` writes `embarch-desk-NAME.service`: the same binary with its own port, config and data folders, its own `CLAUDE_CONFIG_DIR` and `GH_CONFIG_DIR`, and its settings stated in the unit (`EMBARCH_DESK_TIME`, `EMBARCH_DESK_DIRECT_WRITES`, applied at each start). Two settings are new, and both leave a desk without them as it was: **`time`** (on) — off captures no spans, so no tiles, hand or timer, and the timer route refuses; **`direct_writes`** (off) — on makes the agent issue and comment tools send at once, where the rule "no agent tool sends a draft" otherwise holds. The owner's personal dev desk (4892) runs with time off and direct writes on; the work desk runs neither change. **Rejected:** a separate binary or fork (two codebases for one join), a Harvest-less flag per desk (a desk's Harvest binding is already optional).

### 70 — A suite's Start work makes a folder per issue, and a session can open with no item
Decision 43's one worktree beside the main clone cannot work for repos that reach each other by sibling path: Cargo path dependencies and `../embarch-doc/` links would resolve against main. With `EMBARCH_DESK_SUITE_ROOT` in a desk's environment (`service install --suite-root`), Start work makes `<root>/.dev-worktrees/<key>/` instead: worktrees on Linear's branch for the code repo and `EMBARCH_DESK_SUITE_DOCS`, and a symlink to the main clone for every other clone in the root, the same result fleet legs get by hand. **The issue's Project name is the clone's folder name**, so there is no map to keep. An issue with no Project, or one that names no clone, is refused before it moves. The window opens the code repo's worktree alone, whose local settings get `additionalDirectories` for the issue's folder, so the existing link and mailbox work unchanged. `POST /items/{id}/repos`, and the `desk_add_repo` tool, replace a symlink with a worktree on the branch that the card's worktree is on. A tool rather than a written procedure, because `rm -rf link/` with a trailing slash deletes the main clone's contents. A chat cannot edit through a symlink anyway: Claude Code refuses a write that resolves outside its allowed directories [measured 2026-11-04, `claude -p`].

**A session can open on no work item.** `POST /mailbox` takes `{"kind":"open","folder"}`, and the window whose folder matches starts a chat marked untracked, so the desk never asks it for an item (`desk_set_work_item` can still attach one). A caller supplies only the folder, so the invariant of 46 holds: nothing outside Start work can hand a window a prompt.

### 71 — A page drawing its own view of a desk can read every open issue
`/linear/mine` lists what is assigned to the user, so an issue an agent files with no assignee never reaches a page built on it. `GET /linear/open` lists every open issue in the same scope, under the same cap. `GET /linear/issue/{key}/states` gives the states of an issue's team by its key, because `/items/{id}/states` needs a card and making one just to fill a menu would put the issue on the desk. Issue rows now name their `project`, so a page can group them by repo, and each `sessions` row in `/view` carries the `folder_uri` and `session_uri` a card's `live_sessions` row already had, because a chat on no work item has no card to read them from. All of this is reads and added fields, so existing clients and a desk's behaviour are unchanged. **Rejected:** assigning every issue to the user (an agent's filing would need a second step to be seen), and a card per issue (a list of issues is not a list of work items).
