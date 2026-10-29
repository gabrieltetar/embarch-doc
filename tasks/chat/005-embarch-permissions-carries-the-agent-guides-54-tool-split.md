# 005 — `/embarch-permissions` carries the agent guide's 54-tool split and cites its new home

**State:** open
**Source:** `tasks/suite/030`'s fold, 2026-10-29: `suite/user-guide.md` §7.1 moved to [suite/agent-guide.md](../../suite/agent-guide.md) §1.1 and its lists grew from 26 to all 54 `embarch-api` tools. `embarch-chat` [decisions/library.md](../../embarch-chat/decisions/library.md) says the command follows that page's rule and carries its lists dated.
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`embarch-chat/plugin/commands/embarch-permissions.md` cites "suite/user-guide.md §7.1" and carries a split dated 2026-10-23 that names 36 tools. The citation still resolves (user-guide §7 is now a forwarding line), but the lists lag: 18 tools reach the command's "in neither list → ask" fallback, and 7 of them the guide now puts on **allow** (`capture_read`, `capture_start`, `capture_stop`, `lease_show`, `ledger_pending`, `ledger_show`, `list_instruments`). Bring the command's split and its date in line with `agent-guide.md` §1.1, and repoint the citation there.

## Why now

The guide is the rule the command says it follows; until it matches, a user running `/embarch-permissions` is asked about read-only tools the guide allows, and the "tool in neither list" summary names 18 tools as unclassified that are classified.

## Done when

- [ ] The command's allow and ask lists equal `agent-guide.md` §1.1's, re-dated.
- [ ] The command cites `suite/agent-guide.md` §1.1.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10, the npm bullet); `changelog.d/` fragment.
