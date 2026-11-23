# 093 — `shell_commands` decodes each help string and lists `kernel`'s subcommands

**State:** claimed by agent/atlas/093-shell-commands-help-text-and-kernel-subcommands, 2026-11-23 13:36
**Source:** Fleet Ready issue, a session listing a board image's shell commands before running them
**Issue:** EMB-234
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

On a Zephyr 4.4 (NCS 3.4) image for nRF54L15, `shell_commands command=i2c`
gives the right subcommands, argument counts and source lines, but every help
string is garbage bytes (`�\u000b҆�\u0018\b`), and `shell_commands
command=kernel` prints only the root entry although `kernel reboot cold` runs
on the same image. When this is done each help string reads as it does in the
source, and `kernel` lists the subcommands the image compiles in. The worker
finds why: the help pointer's offset in `struct shell_static_entry` for this
Zephyr version, a pointer that needs a different section's base, or a
subcommand set that is a dynamic or section-array form `_walk` does not follow.
Whatever the cause, a help pointer that does not land on printable text prints
nothing rather than bytes.

## Why now

The tool exists so an agent can check which shell commands an image has before
running one; garbage help and a missing `kernel` tree make it answer wrongly on
a current Zephyr.

## Where

- `embarch-atlas/src/embarch_atlas/shellcmds.py`: `_Image.ptr` and `cstr`,
  which read the help pointer, and `_entry` (the line that builds each
  entry's `help`); `_walk` for the subcommand set.

## Done when

- [ ] A test with a Zephyr 4.4 style entry layout decodes the help text as
      plain ASCII.
- [ ] A test shows `shell_commands command=kernel` on such an image listing
      `reboot`.
- [ ] A help pointer that does not reach printable text gives an empty help,
      never bytes.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `DESIGN.md` and `embarch-doc/embarch-atlas/` updated where they describe
      the shell inventory, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
