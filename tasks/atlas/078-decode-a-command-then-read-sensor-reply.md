# 078 — Decode the raw reply of a sensor that has no registers

**State:** claimed by agent/atlas/078-decode-a-command-then-read-sensor-reply, 2026-11-18 03:47
**Source:** Fleet Ready issue: a session debugging a sensor that read zero on the bench converted its raw I2C reply (a status byte and a 24-bit count) to a physical value by hand, because `reg_read` decodes registers and this part has none.
**Issue:** EMB-177
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

An offline `embarch-atlas` verb, for example `embarch-atlas decode <DT label> <hex bytes>`, and the matching MCP tool, that decodes the reply frame of a command-then-read part: one with no register map, where firmware sends a command, waits, and reads a fixed frame. Given the bytes an engineer already read (for example with the shell's `i2c direct_read`) and the node's devicetree label, it prints each status bit by name, the count in decimal, and the physical value from the datasheet's transfer function, for example `(count - Output_min) * (Pmax - Pmin) / (Output_max - Output_min) + Pmin`, with the datasheet page cited. The range, unit and transfer-function variant come from the build's devicetree node; the frame layout and the transfer function come from the part's datasheet distillation. A count below `Output_min` is reported as the negative value the equation gives, and said to be below the minimum, never clamped: that is the case a driver hides, and the reason the verb exists.

It sends nothing to the board. Reading the bytes stays the engineer's (or the live module's) job; this unit decodes what was read.

## Why now

The owner moved the issue to Fleet Ready. The atlas already decodes a register read against its records, so a frame-based part is the gap, and the session that found it was exactly the one where the driver's own reading could not be trusted.

## Dispatch notes

- If the datasheet records have no kind for a reply frame's layout or a transfer function, add one in the repo's `DESIGN.md` record schema and in `embarch-doc/embarch-atlas/design.md`, the way `applicability` and `state` were added (that doc's "Protocol records"). A part or node the records do not cover answers with what is missing, never a guessed layout.
- `embarch-atlas` keeps no numbered decisions; record the verb in its `DESIGN.md`/`README.md` and `embarch-doc/embarch-atlas/` as the recent `q` verbs were.
- An MCP tool changes the lookup counts: update every count and the test that pins the tool count, as `atlas/075` did.
- Tests use synthetic records and a synthetic devicetree, never a client document or part. The public-name guard (`test_public_guard`) must run, not skip: the supervisor links `.atlas-local` beside the worktree.
- No file of this sub-project is in reserve.

## Done when

- [ ] Given the hex bytes of a status-plus-count reply and the node's label, the atlas prints each status bit, the count and the physical value, with the datasheet page cited.
- [ ] A count below the transfer function's minimum is reported as a negative value, not clamped.
- [ ] A part with no frame layout or transfer function in its records gets an answer naming what is missing.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); docs updated, `changelog.d/` fragment dropped.
