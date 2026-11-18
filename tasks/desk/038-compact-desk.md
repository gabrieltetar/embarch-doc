# 038 — `embarch-desk/spec.md` is in reserve

**State:** blocked
**Source:** desk 037 (EMB-165) added the draft-revision tools to `spec.md`, leaving it at 9,186 of 10,240 B (1,054 B left).
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/spec.md
**Size debt due:** 2026-12-01
**In flux:** yes. The agent-tool and draft surface changed in each of the last five desk units (restack, review threads, review replies, notes, draft revision), and EMB-207 (Backlog) may change what a draft stores; a rewrite now would be restated within a unit or two.
**Unparks when:** the next desk unit that writes `spec.md` runs out of its 1,054 B; the compaction rides in that unit. EMB-205, the other trigger as filed, has landed and was struck.
**Must not delete:** the invariants (no agent tool sends a draft, prose is never sent unseen) and the decision/EMB citations; move reference detail to `spec/` verbatim, as `spec/constants.md` was.

## What

Bring `spec.md` out of reserve by moving reference text into `spec/` verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-desk/spec.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
