# 144 — `embarch-core/open.md` is in reserve

**State:** blocked
**Source:** core 140 added the call-log `board` paragraph to `embarch-core/open.md`, leaving it at 4,260 of 5,120 B (83.2%, 860 B left).
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/open.md
**Size debt due:** 2026-12-07
**In flux:** yes. Core's lease, call-log and gated-call surface is moving (tasks core/141, 142 and 143 follow 140 and touch the same open questions), so a rewrite now would restate paragraphs about to change.
**Unparks when:** `tasks/core/143` has landed, or a Core unit lands that adds no open.md paragraph.
**Must not delete:** the scope-enforcement bullets (decisions 109 to 112, 118), the Windows ACL debt, and the call-log `board` bullet (decision 122) as stated.

## What

Bring `embarch-core/open.md` out of reserve: shorten the longest bullets, or move one section into `open/`, without dropping a fact or a decision pointer.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-core/open.md`.
- [ ] Nothing named under **Must not delete** is lost.
