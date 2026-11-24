# 099 — The agent guide's permission lists match the Live design and today's tools

**State:** done — status.d/doc-agent-guide-permissions.md carries the 58-tool allow/ask lists and the atlas lists; supervisor folds into agent-guide.md §1.1
**Source:** `notes/hil/05-live.md` ("Reach and permission") and `notes/hil/07-procedure-doc.md` ("Gaps it closes"), against `suite/agent-guide.md` §1.1
**Issue:** EMB-269
**Scope:** doc
**Hardware:** none
**Owner:** no

## What

`suite/agent-guide.md` §1.1 (dated 2026-10-29) tells a session which
`embarch-api` tools to allow and which to ask about. It is out of date three
ways:

- It puts ten reads and lease calls under ask that the Live design makes free:
  `reset`, `reset_dev_bench`, `signal_exchange`, `mem_read`, `core_state`,
  `bench_exchange`, `validate`, `lease_take`, `lease_renew`, `lease_release`.
- It lists no tool of the atlas's MCP server.
- Its count and date are stale. `embarch-api/src/tools.rs` registers tools the
  section never names (`build_each`, `bundle`, `publish` among them), and
  `instrument_exchange` is gone (`api/178`).

**The route: you write a `status.d/doc-agent-guide-permissions.md` fragment,
and the supervisor applies it.** `suite/agent-guide.md` is a shared suite-level
doc, which `check-ownership.py` refuses to every worker (protocol §3, §9). The
fragment carries §1.1's replacement allow and ask lists, the new atlas list,
and the count and date, written out in full so the fold is a paste rather than
a rewrite. Put any placement the section's own rule does not settle at the top
of the fragment, named for the owner.

The direction, from the design notes:

- **allow** gains the ten tools above.
- **ask** keeps flashing and bootloading, plus `answer_prompt`, `run_study`,
  `run_host_study`, `ledger_add` and the identity tools, which stay on the MCP
  surface of today's unattested Core.
- **The atlas's MCP server** gets its own list (read
  `embarch-atlas/src/embarch_atlas/mcp_server.py` on `origin/main`): allow
  `reg_read`, `shell`, `shell_run`, `live_stacks`, `core_state`; ask
  `reg_read_clear`, `reg_read_bank`.
- `build_each`, `bundle`, `publish` and any other unlisted tool are placed by the
  section's own rule.
- Do not write that the identity tools leave the MCP surface on an attested
  Core. That Core does not exist yet.

Read every tool name from `embarch-api/src/tools.rs` on `origin/main` (each
`#[tool]` entry) and check that every one sits in exactly one list. Read the
section's other paragraphs too: if prose elsewhere in §1.1 names a moved tool as
asking, the fragment rewrites that sentence as well.

`embarch-chat`'s permissions command keeps its own copy of these lists. It is
`chat/033`'s file, not this unit's. Name in the fragment what it would need to
match, and the supervisor files it.

## Why now

The HIL Live phase is being planned from `notes/hil/14-implementation-plan.md`,
and its guide must not disagree with §1.1. An engineer writing
`.claude/settings.local.json` from §1.1 today gets an ask prompt on every reset
and register read.

## Done when

- [x] A `status.d/doc-agent-guide-permissions.md` fragment carries §1.1's replacement lists: every tool `embarch-api/src/tools.rs` registers sits in exactly one of allow and ask, with today's count and date.
- [x] In it, the ten tools 05 makes free sit under allow.
- [x] In it, an atlas list names its seven live tools, with `reg_read_clear` and `reg_read_bank` under ask.
- [x] Any placement the rule does not settle is named at the top of the fragment.
- [x] `python3 scripts/check-docs.py` passes, and `check-ownership.py --scope doc` is green.
