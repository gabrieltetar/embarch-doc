# HIL notes: the procedure document itself

**Status:** draft, 2026-11-15.

## Its form

**A suite guide of record plus a thin skill.**

- **`suite/hil-guide.md`** holds the procedure: written for the agent first, readable by an engineer. It is a guide, so it may restate what it needs rather than only link ([DOC-PROTOCOL.md](../../DOC-PROTOCOL.md) §3).
- **The `embarch-hil` skill, shipped with embarch-api**, installed when `embarch init` registers the MCP server, so every firmware repo with EmbArch gets it. It loads when a task needs hardware, holds the "which mode" table, and points at the guide's section for the mode. Same owner as the tools it describes; the precedent is the atlas's `atlas-use` skill.

**One file to start, split into one file per mode if it outgrows the studies guide (about 23 KB)**; the skill points at sections either way.

## An outline of the guide

1. **Choosing a mode**: the table in [01-modes.md](01-modes.md#how-an-agent-picks-a-mode), and the fleet's exclusion.
2. **Before any hardware**: `status` (Core reachable, the lease, `last_images`), `lease_take` with a purpose, the saved bench live, `validate`.
3. **Live**: reach, what is free and what asks, the atlas or raw path, the live log, writing a finding back, when to escalate.
4. **Study**: from the question to a published zip, with the BLE GATT data-acquisition example.
5. **Test**: selecting from a suite, the test plan, the DUT's inputs and hooks, starting a Core-run Test, prompts between benches, reading verdicts and coverage, publishing.
6. **Publishing**: the zip, the audit appendix, the operator's notes.
7. **What the agent never does**: answer an operator prompt on its own, decide a verdict, run hardware from the fleet, `git checkout` to reach a revision a study asks for, read a truncated capture as complete.

## Gaps it closes

Gaps in today's agent-facing docs, found while gathering these notes:

- **[agent-guide.md](../../suite/agent-guide.md) never says which kind of hardware work to do.** It lists 54 tools and how to permit them, and nothing about studies against live reads against test runs.
- **The atlas's live tools appear nowhere in the suite's agent docs.** `reg_read`, `shell`, `shell_run`, `live_stacks` and `core_state` are documented only in the `embarch-atlas` repo's `DESIGN.md`, which is local and unpublished.
- **The lease is in the tool reference, not in any procedure**: when to take it, for how long, when to let it go.
- **§1.1's permission lists disagree with the Live mode**: `reset`, `signal_exchange` and `shell_run` move to allow ([05-live.md](05-live.md#reach-and-permission)).
- **The [studies guide](../../suite/studies-guide.md) is written for an engineer** and stops at reading captures: nothing on reporting or publishing.
- **The ledger has no procedure at all**: tools only ([embarch-api ledger tools](../../embarch-api/interfaces/tools-ledger.md)).

## Open

- **Whether `embarch-chat`'s prompt library gets buttons for the three modes.** Later, once the guide exists.
