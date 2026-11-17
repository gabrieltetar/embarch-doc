# 027 — `embarch-chat/spec.md`, `interfaces.md`, `open.md` and `decisions/shape.md` are in reserve

**State:** claimed by agent/chat/027-compact-chat, 2026-11-17 13:42
**Source:** the continue-after-limit branch added decision 109 (a turn the usage limit cuts off goes on at the reset; the rail's Limits menu) and left `spec.md` at 9,594 of 10,240 B, `interfaces.md` at 13,880 of 15,360 B and `open.md` at 4,341 of 5,120 B. Decision 110 (nothing in the chat scrolls sideways, EMB-116) left `decisions/shape.md` at 11,381 of 12,288 B.
**Scope:** chat
**Hardware:** none
**Owner:** no

**Compacts:** embarch-chat/spec.md, embarch-chat/interfaces.md, embarch-chat/open.md, embarch-chat/decisions/shape.md
**Size debt due:** 2026-11-23
**In flux:** no — but leave decision 109's own lines as written in all three files (its spec bullet, its interfaces rows, its open.md entry): built 2026-11-16 and never seen on a real limit hit. Everything else in them is settled, `decisions/shape.md` included.
**Must not delete:** any setting row in `interfaces.md`, any "Not yet seen" or "Waiting on the owner" item in `open.md` that is still true, or any status claim in `spec.md`'s `**Status:**` line.

## What

Bring the three files out of reserve. `spec.md`: move a whole section that has a natural home (§2's input and assistant bullets already have `spec/input.md`) into its `spec/` topic file, verbatim, leaving a one-line pointer. `interfaces.md`: 56 B over; tighten or move one table whose rows are not settings (the desk calls, say) into a topic file. `open.md`: drop each "Not yet seen" item that has since been seen, after checking the owner's word or a measurement for it, and otherwise split "Structural limits" into `open/limits.md`. `decisions/shape.md`: move whole decisions that settle a separate thing (the mark, 54, or the rail, 94) into their own group file, verbatim, and update `decisions.md`'s index row; never shorten a decision's text.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; decision 109's spec bullet, settings rows and open entry spent the reserve of all three.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` shows none of the three.
- [ ] Every moved section is byte-identical in its new file, with a pointer where it was; `check-links.py` and `check-decision-refs.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
