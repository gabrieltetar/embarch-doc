# 107 — `embarch-umbrella/spec.md` is in reserve

**State:** done — command table moved verbatim to spec/commands.md
**Source:** umbrella 106 (EMB-299) added the `schema_version` contract to `spec.md`, leaving it at 9,161 of 10,240 B; umbrella 109 (EMB-344) added one sentence naming the release script, leaving 9,272 B (968 B left).
**Scope:** umbrella
**Hardware:** none
**Owner:** no

**Compacts:** embarch-umbrella/spec.md
**Size debt due:** 2026-12-08
**In flux:** no — for the move this task makes. Unparked at claim, 2026-11-25: this task's own remedy is a verbatim move into a topic file, and `DOC-BUDGET.md`'s split-first rule is that a verbatim move restates nothing, so flux cannot forbid one (the `core/093` precedent, 2026-09-28). The old answer, kept as history: *yes — the umbrella still gains commands and release machinery most weeks (signed suite releases are written but not yet run on a tag), so the spec is still moving.* That still governs any **squeeze** of `spec.md`; it does not govern moving text.
**Must not delete:** the decision numbers and issue keys cited in the command table and the release paragraph; move reference detail to a topic file verbatim and leave a link.

## What

Bring `spec.md` out of reserve by moving the longest sections into a topic file beside it, verbatim, leaving links.

## Dispatch note (supervisor, 2026-11-25)

**Move only; squeeze nothing.** Move whole sections byte-identical into `spec/` (beside `marketplace.md`) and leave a one-line link where each stood; rewrite no sentence, since the unpark above covers a move and nothing else. Grep `embarch-doc` and `embarch-umbrella` for links into the sections you move and repoint any that name the file and anchor. Leave every `decisions/` file alone: several sit within 200 B of their limit (`prune-policy`, `deploy`, `mirrors`, `budgets`). This is a burndown leg: author no new numbered decision. Doc-only unit, no code worktree. `embarch-umbrella/spec.md` is the only file in reserve for `umbrella` (968 B left).

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [x] `scripts/check-doc-size.py --pressure` does not list `embarch-umbrella/spec.md`.
- [x] Moved text is byte-identical in its new file; `check-links.py` green.
- [x] Gate green (`../../embarch-fleet/gate.md`).
