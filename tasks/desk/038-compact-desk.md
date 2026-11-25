# 038 — `embarch-desk/spec.md` is in reserve

**State:** claimed by agent/desk/038-compact-desk, 2026-11-25 01:03 — unparked for the verbatim split its What names
**Source:** desk 037 (EMB-165) added the draft-revision tools to `spec.md`, leaving it at 9,186 of 10,240 B (1,054 B left). On 2026-11-23 the owner's archive route took `interfaces.md` into reserve too, at 14,073 of 15,360 B; its HTTP surface is in flux with the rest.
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/spec.md
**Size debt due:** 2026-12-01
**In flux:** no — for the move this task makes. Unparked at claim, 2026-11-25: this task's own remedy is a verbatim move into `spec/`, and `DOC-BUDGET.md`'s split-first rule is that a verbatim move restates nothing, so flux cannot forbid one (the `core/093` precedent, 2026-09-28). The old answer, kept as history: *yes — the agent-tool and draft surface changed in each of the last five desk units (restack, review threads, review replies, notes, draft revision), and EMB-207 (Backlog) may change what a draft stores; a rewrite now would be restated within a unit or two.* That still governs any **squeeze** of `spec.md`; it does not govern moving text.
**Must not delete:** the invariants (no agent tool sends a draft, prose is never sent unseen) and the decision/EMB citations; move reference detail to `spec/` verbatim, as `spec/constants.md` was.

## What

Bring `spec.md` out of reserve by moving reference text into `spec/` verbatim, leaving links.

`interfaces.md` was struck off the `Compacts:` line on 2026-11-24: `desk/042`
paid it in its own unit, moving two route rows verbatim into
`interfaces/draft-note-routes.md` (14,073 to 12,723 B, out of reserve).

## Dispatch note (supervisor, 2026-11-25)

**Move only; squeeze nothing.** Move whole sections byte-identical into `spec/` (beside `constants.md`, `non-goals.md`, `suite-desk.md`) and leave a one-line link where each stood; rewrite no sentence, since the unpark above covers a move and nothing else. Keep §2's invariants in `spec.md`. Grep `embarch-doc` and `embarch-desk` for links into the sections you move and repoint any that name the file and anchor. This is a burndown leg: author no new numbered decision. Doc-only unit, no code worktree. `embarch-desk/spec.md` is the only file in reserve for `desk` (1,015 B left).

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-desk/spec.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
