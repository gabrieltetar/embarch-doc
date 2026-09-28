# 071 — `embarch-ui/open.md` is in reserve

**State:** claimed by agent/ui/071-compact-ui-open, 2026-09-28 15:07
**Dispatch note (supervisor, 2026-09-28):** **the numbers below are stale.** The file grew after
this task was filed (the owner's 2026-09-19/20 `ui` decisions) and is now **6,630 / 5,120 B —
1,510 B over its cap and past its 2026-09-24 clock**, which makes it one of three files turning
`main`'s `check-doc-size.py` RED. So the order of goals is: **(1) under the 5,120 B cap** — that is
what fails the gate; **(2) out of reserve** (floor `max(1200 B, 10%)` from the top = **3,920 B**)
if it can be done without closing a question by attrition, otherwise say why not. Re-derive every
number yourself. The other two reds (`embarch-core/decisions/handshake.md`,
`embarch-ui/decisions/shell.md`) are not yours; `shell.md` is `tasks/ui/073` and runs **after** this
unit, so do not touch it, nor `decisions/shape.md` (94 B left, `069`), `decisions/topology-boards.md`
(111 B, `073`), `decisions/study-designer.md` (896 B, `072`) or `spec.md` (`069`). If a retired
entry's settled content must move into a decision file, it may not push any of those further in.
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by `tasks/ui/070`'s two new entries
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/open.md
**Size debt due:** 2026-09-24
**In flux:** no

## What

`open.md` is **5,027 / 5,120 B (98.2%), 93 B left**. Out of reserve when this
closes, or the task says why not.

Two entries landed with `ui/070`: the pointer to
`embarch-study-designer/open.md`'s saved-study-vs-edited-`.eap` question (which
lives there, not here — this half is only where a divergence would be *shown*),
and the two unrun hardware legs. **This file is the wrong place to squeeze
blindly**: every bullet in it is an open question, and deleting one is closing
it by attrition rather than by answering it.

The compaction that is actually available is **retirement**: the 250,000-row cap
entry carries a measurement table that has served its purpose, and the
decision-27 entry is explicitly marked *settled, permanently — not pending*,
which is a closed question sitting in a file whose whole contract is
unresolved-only.

## Why now

93 bytes left means the next open question cannot be filed without paying first,
and a file that refuses new open questions is the failure mode this budget is
least willing to have.

## Done when

- [ ] `open.md` out of reserve, or the task says why not.
- [ ] **No open question was closed to make room.** Anything removed is either
      already settled elsewhere and says where, or moves to a doc that owns it.
- [ ] The decision-27 entry's fate is decided explicitly: it says it is settled,
      so either it leaves this file or the sentence saying it is settled goes.
- [ ] Byte numbers before and after.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.
