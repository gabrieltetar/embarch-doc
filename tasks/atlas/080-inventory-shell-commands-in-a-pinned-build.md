# 080 — Inventory the shell commands compiled into a pinned build

**State:** done
**Source:** Fleet Ready issue: sessions keep working out by hand, with throwaway scripts over the ELF and `compile_commands.json`, which Zephyr shell commands an image has and with what argument syntax.
**Issue:** EMB-157
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

An atlas build step that writes `shell.json` beside `kconfig.json`, and an MCP tool (plus a CLI verb) that returns one root command's table from it. For the pinned build it lists every root shell command present in the ELF, with the source file and line of its subcommand table; each subcommand with its mandatory and optional argument counts and its help text; and, for a dynamic device list, the devices in the image it would offer. It reads only build artifacts (`zephyr/zephyr.elf`, `compile_commands.json`, `zephyr/.config`, `zephyr/zephyr.dts` and the generated devicetree header).

Three traps from the session that found the gap are part of the task, not extras:

- A symbol filter must not drop names with digits (`i2c`).
- A subcommand guarded by a Kconfig that is off is in the source and **not** in the image, so it must be absent from the inventory, not listed from the source.
- A build directory rebuilt mid-session changes the answer, so the inventory records the ELF's modification time and the tool flags itself stale when the ELF changes.

## Why now

The owner moved the issue to Fleet Ready. The atlas already pins the build and reads its `.config` and devicetree, so it is the one place this list can be made once and cited.

## Dispatch notes

- **Do not change `live.py`'s read-only shell allowlist in this unit.** The issue names it as a future reader of the inventory, but that allowlist decides what runs on a board without the host asking; deriving it from a build could widen it. Leave it as it is and say in `DESIGN.md` that the inventory is a source it could later read.
- A build with no shell compiled in writes an inventory saying so, not an error.
- `embarch-atlas` keeps no numbered decisions; record the step and the tool in its `DESIGN.md`/`README.md` and `embarch-doc/embarch-atlas/` as the recent verbs were.
- An MCP tool changes the lookup counts: update every count and the test that pins the tool count, as `atlas/075` did.
- Tests use synthetic build artifacts, never a client build. The public-name guard (`test_public_guard`) must run, not skip: the supervisor links `.atlas-local` beside the worktree.
- No file of this sub-project is in reserve.

## Done when

- [x] For a pinned build, the atlas lists every root shell command present in the ELF, each with its source file and line.
- [x] Each subcommand's mandatory and optional argument counts and help text appear, and a subcommand compiled out by Kconfig is absent.
- [x] The inventory records the ELF modification time and flags itself stale when the ELF changes.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); docs updated, `changelog.d/` fragment dropped.

## Outcome

`q shell-commands [<root>] [--build DIR]` / MCP `shell_commands` shipped (lookups 22 to 23), and `build` writes `shell.json` beside `kconfig.json`. Read from the ELF's `shell_root_cmds` section and the `shell_static_entry` tables (stdlib reader of `dt.py`); source file and line from `nm -l` via `footprint.image`. Traps: root commands are found by section, not by a name regex (digits, `i2c`, kept); a Kconfig-off subcommand is not in the ELF so it is absent; `shell.json` records ELF size, mtime and hash and the answer says STALE against both the atlas's copy and the original build dir's ELF. A dynamic set names its getter and, for a `device` getter, lists the `device_area` objects; the getter's filter is not evaluated. No shell compiled in gives an inventory saying so. `live.py`'s read-only allowlist untouched; `DESIGN.md` names the inventory as a later source. Tests use a synthetic ELF32 built in `tests/test_shellcmds.py`.

**Not verified against a real image:** the struct layout (`shell_cmd_entry` = bool + pointer, `shell_static_entry` = four pointers + two count bytes, `device_area` objects starting with the name pointer) is from Zephyr's headers as remembered, not read from a build; the first real `build` should be checked once. No feature-inventory row: `features.d` has no atlas section.
