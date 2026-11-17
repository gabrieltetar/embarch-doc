# 028 — Read where a dead session stopped, without parsing its transcript

**State:** claimed by agent/chat/028-read-where-a-dead-session-stopped, 2026-11-17 14:51
**Source:** EMB-189, filed by an audit after a resumed session had an agent write a throwaway script to dig the last turns out of a dead session's transcript; EMB-200, the reviewer's finding on the first landing
**Issue:** EMB-189
**Issue:** EMB-200
**Scope:** chat
**Hardware:** none
**Owner:** no

## Re-land, read first

This was built once, landed and **reverted on 2026-11-17**: the reviewer found
that the MCP tool reads the extension host's login (`CLAUDE_CONFIG_DIR` or
`~/.claude`), not the chat's own, against decision 101 (a chat keeps its login
for life; every other transcript read in a chat uses
`projectsRoot(this.opts.env ?? chatEnv())`, `src/wire/chat.ts`). A chat on a
second login would read another account's folder.

- **Code:** the build is commit `97cf346` on `embarch-chat`'s `main`, reverted
  by `3288cf6`. Start from `origin/main`, `git revert 3288cf6` to restore it,
  then pass the chat's own projects root to `lastSessionCall` from
  `src/hostHooks.ts` (it already takes a `root` nothing supplies; `HandoffPort`
  in `src/handoff.ts` carries no login today), with a test that a chat started
  on a `configDir` login reads that login's `projects/` folder.
- **Docs:** the doc half is commit `88f845e7` on `embarch-doc`'s
  `origin/agent/chat/028-read-where-a-dead-session-stopped`, never landed.
  Cherry-pick it, then make `spec/handoff.md` name the login the read uses.
- Everything below still stands; the first worker's choices (the MCP tool beside
  `handoff`, the CLI, the 30 s live-file rule for the CLI) were found sound.

## What

A session that dies at the usage limit, or whose window closes, leaves no
handoff. The next one in the same repo or worktree has nothing to pick up from
but the old transcript. `mcp__embarch-chat__handoff` writes a handoff from a
live session; nothing reads a dead session's state back.

Add a read-only verb beside the handoff tool, for example
`embarch-chat last-session [--cwd <path>] [--turns N]`, or an MCP tool of the
same shape, or both over one implementation.

- **Input:** a working directory, a repo or a worktree. The previous session's
  transcript is the newest `*.jsonl` under the login's `projects/<encoded cwd>/`
  folder. A session started in the main clone and then working in a worktree is
  filed under the main clone's folder, so the lookup tries both (the worktree's
  folder, then the main clone's, by `git rev-parse --git-common-dir`).
- **Output:** the last N user and assistant text turns, and each tool call as its
  name plus the first few hundred characters of its input, oldest first; plus any
  background tasks or monitors still pending when it stopped.
- **Never the current session.** The caller's own transcript is the newest file
  in the folder while it runs; exclude it (by the session id the caller runs
  under, where the chat has it, and otherwise by refusing a file still being
  written), and say in `spec.md` which rule you used.

Writing a `Handoff` desk line from what it reads is the issue's optional second
half; leave it out unless it falls out for free, and if you leave it, say so in
`open.md`.

`embarch-promptu` has its own transcript walker (`src/used.rs`, `src/calls.rs`);
it is another repo, so read it for the JSONL shape only and do not depend on it.

**Public repo.** Tests use synthetic JSONL fixtures in a temp `projects/` tree
and synthetic repos made with `git init` and `git worktree add`. No real
transcript, no real login path.

**Burndown leg: no new numbered decision.** Record the verb in `spec.md` and
`interfaces.md`; a real design fork goes to `scripts/fleet-linear.py file --from
decision`.

**What you may change.** Only `embarch-chat` and `embarch-doc/embarch-chat/`.

**Doc reserve.** Nothing of `embarch-chat`'s is in reserve. `decisions/promptu.md`
has 204 B left before its limit; this unit should not need to touch it.

## Why now

The owner moved it to Fleet Ready; a fleet leg re-landing an orphaned leg's work
needs the same thing.

## Done when

- [ ] One command, given a working directory, prints the previous session's last turns and tool calls without the caller knowing the transcript path.
- [ ] It finds a session filed under the main clone's folder when asked from one of its worktrees.
- [ ] It never prints the current session as "the previous one"; a test covers it.
- [ ] Called from a chat started on a `configDir` login, the tool reads that login's `projects/` folder; a test covers it, and `spec/handoff.md` names the login.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
