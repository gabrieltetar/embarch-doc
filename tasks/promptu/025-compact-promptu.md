# 025 — `embarch-promptu/open.md` is in reserve

**State:** claimed by agent/promptu/025-compact-promptu, 2026-11-25 01:05 — unparked for the verbatim move its What names
**Source:** promptu 024 (EMB-403) added the step 5 bullet to `open.md`, leaving it at 4,060 of 5,120 B (1,060 B left).
**Scope:** promptu
**Hardware:** none
**Owner:** no

**Compacts:** embarch-promptu/open.md
**Size debt due:** 2026-12-09
**In flux:** no — for the move this task makes. Unparked at claim, 2026-11-25: this task's own remedy is a verbatim move of the step 1 to 3 bullets into `open/`, and `DOC-BUDGET.md`'s split-first rule is that a verbatim move restates nothing, so flux cannot forbid one (the `core/093` precedent, 2026-09-28; the 2026-11-25 00:39 log entry for `promptu/024` said the same). The old answer, kept as history: *yes — steps 4 and 5 are both under way: the step 4 bullets (half-built, unmeasured drafter) and the four unrecorded step 5 choices change with each unit, so a rewrite now states something about to be wrong.* That still governs the step 4 and 5 bullets, which stay where they are, untouched.
**Must not delete:** every open question with its fork or EMB reference; the unmeasured-claims list; move resolved detail to a topic file under `open/` verbatim and leave a link.

## What

Bring `open.md` out of reserve by moving settled step 1 to 3 bullets into `open/` verbatim, leaving links.

## Dispatch note (supervisor, 2026-11-25)

**Move only; squeeze nothing.** Move the step 1 to 3 bullets (block mode, the forks F5 to F10, relabelling, the shell-write blind spot, step 2's review rounds, step 3's install wait, the rewrite model, and any other bullet about steps 1 to 3) byte-identical into a topic file under `open/` (beside `unmeasured.md`), and leave a one-line link in `open.md`. Leave the step 4 and step 5 bullets in `open.md` and do not edit them. Grep `embarch-doc` and `embarch-promptu` for links into `open.md` and repoint any that name a moved bullet. This is a burndown leg: author no new numbered decision. Doc-only unit, no code worktree. `embarch-promptu/open.md` is the only file in reserve for `promptu` (1,060 B left).

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-promptu/open.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
