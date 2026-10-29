# 006 — `/embarch-claude-md` cites a user-guide section that moved to the agent guide

**State:** open
**Source:** reviewer of `chat/005` (doc fold of the leg started 2026-10-29 15:03): `plugin/commands/embarch-claude-md.md` line 9 reads "The block (suite/user-guide.md §7.1)"; `suite/030` moved user-guide §7/§7.1 verbatim to [suite/agent-guide.md](../../suite/agent-guide.md) §1/§1.1, leaving user-guide §7 a two-line forwarding pointer.
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`embarch-chat/plugin/commands/embarch-claude-md.md` names the section its `CLAUDE.md` block comes from as `suite/user-guide.md` §7.1. Find which section of `suite/agent-guide.md` now holds that block (§1 or §1.1), repoint the citation there, and check the block the command carries still equals the guide's text. `chat/005` did the same for `/embarch-permissions`.

## Why now

The citation lands on a forwarding line rather than the block; `embarch-chat` decisions/library.md says each command carries the guide's text and cites where it comes from.

## Done when

- [ ] The command cites the `agent-guide.md` section that holds the block, and its block matches that section's.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10, the npm bullet); `changelog.d/` fragment.
