# 009 — A live call that can change the board carries no read-only hint

**State:** done
**Dispatch note (leg started 2026-10-29 15:03):** nothing in `embarch-doc/embarch-atlas/` is in doc-size reserve. The repo's own `DESIGN.md` is the contract until it moves (its `CLAUDE.md`). Gate: the worktree's own venv (`.venv/bin/pytest -q`), never the main checkout's; `test_public_guard` must run, not skip (the `.atlas-local` link is made beside your worktree). Invent part and chip names in tests — `test_public_guard` refuses real ones — and run `python3 ../embarch-fleet/scripts/check-client-names.py --repo .` before committing; there is no `check_public.py`. `atlas/008` just landed the chip-mismatch refusal in `live.py`: build on it. Set this file's `State:` to `done` when you close it.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — of 142 `shell` calls, sessions used it to switch a power path, set a port power budget 23 times and drive GPIO outputs, all through a tool that declares `readOnlyHint`; none ran in plan mode (all 142, and all 46 `reg_read` calls, ran in auto mode), so the hazard is latent, not observed
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Every atlas MCP tool declares `readOnlyHint` (`embarch-atlas/src/embarch_atlas/mcp_server.py:41`, b2f5067), and DESIGN.md "MCP server" states the trade-off: `shell` carries the hint "although a command can change the board's state", so plan mode can call it. The same holds for `reg_read` with `allow_clear=true`, which clears a latched flag on purpose. A host that trusts the hint (plan mode, an auto-approval rule, a permission classifier, a fleet worker's tool allowlist) cannot tell a state read from a state change. When done, the hint is true for every tool that carries it. `shell` runs only commands that a per-project list in `atlas.toml` (`[live] read_only = ["device list", "kernel *", "i2c read*", ...]`, with a shipped default for Zephyr's own read commands) marks as reads, and refuses any other command with the name of the second tool. A new tool, `shell_run`, takes any command and declares no read-only hint, so the host asks or classifies it as a write. `reg_read` refuses `allow_clear=true` and names `reg_read_clear`, a tool with no read-only hint. The CLI keeps one verb each, since the CLI has no hint.

## Why now

The trade-off was made on 2026-10-06 so the live tools would work in plan mode. Field use shows the shell is mostly a write path in practice: the commands that change a port's state are the ones a session runs most often in a row. Splitting the tools now costs one list and two thin wrappers. After hosts and allowlists depend on the current names, the same split would break them.

## Done when

- [x] `shell` refuses a command that matches no `read_only` pattern, and the refusal names `shell_run`; a test covers a listed read, an unlisted write and a glob.
- [x] `shell_run` and `reg_read_clear` exist without `readOnlyHint`; `reg_read` refuses `allow_clear=true` and names `reg_read_clear`.
- [x] The default `read_only` list covers Zephyr's read-only shell commands (`device list`, `kernel thread stacks`, `kernel uptime`, `i2c read`, `i2c read_byte`) and nothing that writes; `i2c scan` stays out, because it addresses every device on the bus.
- [x] DESIGN.md "MCP server" states which tools carry the hint and why, replacing the 2026-10-06 trade-off sentence; the `atlas-use` skill names the write tools.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Notes

`embarch-doc/embarch-atlas/` has no spec/decisions/open (design.md is a placeholder; the repo's `DESIGN.md` is the contract), so the design change is in `DESIGN.md` "MCP server" and "The live shell". `[live] read_only` replaces the default list when set; commands containing `; | & `` $(` or newlines never match. Hardware-verification debt: none run live (tests use a fake embarch-api); a host's plan-mode behaviour with the new hints is unobserved.
