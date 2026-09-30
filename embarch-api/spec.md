# embarch-api: spec

**Status:** active, 2026-09-05.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Config: [interfaces/config.md](interfaces/config.md), [interfaces/dev-bench-config.md](interfaces/dev-bench-config.md). Tools/subcommands: [interfaces/tools.md](interfaces/tools.md), [interfaces/studies.md](interfaces/studies.md).

## 1. What it is

Three responsibilities on top of `embarch-core`: **(a)** Core's capabilities as MCP tools, **(b)** the same as CLI subcommands — a **superset**, `versions` has no tool — and **(c)** running a configured build command and feeding the artifact to Core's `/flash`.

**Subcommand presence is the mode switch.** No subcommand → an MCP stdio server; a subcommand → run that one operation and exit. Both front-ends call the same modules; neither is privileged.

Core owns all direct hardware access — `probe-rs` and `serialport` live exclusively there, and this crate links neither. **Core has no idea this crate, MCP or Claude Code exist.** `embarch-umbrella` sits on the far side of the same boundary: it writes this crate's config and shells out to its CLI, unknown here.

## 2. Invariants

- **Single user, single Core instance.** No multi-tenancy, permission model or database; each engineer runs their own stack.
- **Core's address is never hardcoded to loopback.** Always a config value — Core is expected to move to a LAN-reachable machine.
- **`build_command` is an argv array, never a shell string** — no quoting or shell-dialect ambiguity. A project needing shell features says so: `["bash", "-lc", "…"]`
- **`chip`, `flash_format` and `base_address` are opaque pass-through.** Not validated against probe-rs's target DB; that's Core's job, duplicating it here is a maintenance trap.
- **A fresh artifact is proven, never assumed.** The artifact path's existence and mtime are recorded *before* spawning; after a zero exit the file must exist and, if it existed before, be newer than the build start — otherwise a build that failed partway could silently "succeed" against a stale binary, the worst failure for hardware bring-up.
- **An expected failure comes back as tool content, not a protocol error**, so a calling agent sees the real compiler error and can reason about it. A protocol error is reserved for this crate's own config being unloadable at all; that exception and the CLI's exit-code shapes are in [tools.md](interfaces/tools.md).
- **This crate never knowingly runs a tree-mutating `git` subcommand**, named directly or behind a shell/exec wrapper. "Reflash" means build and flash the tree **as it stands**, then verify — never "make my tree be that version". Enforced against the config file, not just this code.
- **No inference presented as fact.** Anything about a DUT this crate can't observe is declared by the operator or reported unknown.
- **Every JSON object either front-end emits carries `schema_version`**, stamped in one place rather than per emitter, and there is no `error_kind` ([decisions](decisions/surface.md) 24, 50).
- **A live event stream is an optimisation, never the source of truth.** Losing it falls back to polling and is reported, never fails a call. Core's `lagged` frame is a fact to relay, not an error ([decisions](decisions/core-link.md) 48).

**§§3-7 — build orchestration, deployment and topology, modules, security, constants — moved verbatim to [spec/implementation.md](spec/implementation.md)** on 2026-09-29 under [DOC-COMPACTION.md](../DOC-COMPACTION.md) §2 (`tasks/api/083`); this file still answers what is true, that one answers how.
