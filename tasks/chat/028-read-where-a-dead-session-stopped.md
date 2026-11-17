# 028 — Read where a dead session stopped, without parsing its transcript

**State:** claimed by agent/chat/028-read-where-a-dead-session-stopped, 2026-11-17 14:26
**Source:** EMB-189, filed by an audit after a resumed session had an agent write a throwaway script to dig the last turns out of a dead session's transcript
**Issue:** EMB-189
**Scope:** chat
**Hardware:** none
**Owner:** no

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

- [x] One command, given a working directory, prints the previous session's last turns and tool calls without the caller knowing the transcript path.
- [x] It finds a session filed under the main clone's folder when asked from one of its worktrees.
- [x] It never prints the current session as "the previous one"; a test covers it.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
