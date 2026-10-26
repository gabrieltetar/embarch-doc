# 080 — A console's unfinished line is capped like a finished one, instead of growing for the rest of the run

**State:** done — agent/ui/080-console-partial-line-is-capped, 2026-10-26
**Dispatch note:** the compaction tasks named under Done when are renumbered: `spec.md` (9,099/10,240 B, 1,141 B left) is filed under `tasks/ui/089` (open), and `open.md` (4,366/5,120 B, 754 B left) under `tasks/ui/088` (blocked). Put the change in `decisions/live-study.md` (8,985 B, decision 32) as the task says; add at most a phrase to `spec.md`. If a browser drive is run, it must stay isolated from the live desk the way `ui/091` made `drive_topology.py` isolated, and must never reach a live Core or the desk on :4891.
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-ui finding 5), verified by Opus against embarch-ui@aa5ffdaa
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`Console::push_chunk` appends every chunk to `partial` (`src/live_study.rs:142`). Bytes leave `partial` only when a `\n` turns them into a line. `MAX_CONSOLE_LINE_BYTES` (8 KB) cuts a *finished* line (`:151-160`), and `MAX_CONSOLE_LINES`/`MAX_CONSOLE_BYTES` bound only finished lines (`:178`). So a `Text` tap that never sends a newline grows `partial` for the whole run. Every console frame re-sends the whole of it (`:1333`, `:1372`), and so does every snapshot (`to_json`, `:190-196`): server memory grows linearly, and the bytes sent to each browser grow quadratically. Suggested direction: once `partial` reaches the line cap, publish it as a finished line marked `truncated`, the same way an over-long finished line is treated, and keep counting. Decision 32's rule that a partial line is never *padded* into a line the tap did not send stays. A cut line is already marked as cut.

## Why now

Decision 32 (`decisions/live-study.md`) names exactly this input and the required behaviour: "a `Text` tap streaming a megabyte with no newline is a binary tap somebody declared wrong, and the honest answer is to say so rather than grow". The code grows.

## Done when

- [x] A unit test pushes several megabytes containing no `\n` through `push_chunk`. `partial` never exceeds the line cap, the surplus appears as lines marked truncated, and those lines count towards the ring's `dropped`/`total`.
- [x] A console frame's size stays bounded while that tap keeps streaming.
- [x] The existing tests for a chunk ending mid-line still pass, so a short partial line is still shown dim and never padded.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` and `open.md` are in reserve with parked compaction debts (`tasks/ui/078`, `tasks/ui/074`), so prefer `decisions/live-study.md` (decision 32).
