# 027 — `embarch-chat/spec.md`, `interfaces.md`, `open.md` and `decisions/shape.md` are in reserve

**State:** done, 2026-11-17
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

- [x] `scripts/check-doc-size.py --pressure` shows none of the three.
- [x] Every moved section is byte-identical in its new file, with a pointer where it was; `check-links.py` and `check-decision-refs.py` green.
- [x] Gate green (`../../embarch-fleet/gate.md`).

## Outcome

Four moves, all verbatim with a pointer left behind; no text shortened, no decision authored, decision 109's lines untouched.

- `spec.md` 9,594 to about 9,000 B: the handoff bullet (103) went to `spec/handoff.md`, and the three input invariants (Promptu never sends; a card only edits the draft; a reference is written from the desk's index) to `spec/input.md`, with one pointer line each.
- `interfaces.md`: the desk-calls table (not settings) went to `interfaces/desk.md`; every setting row stays, and decision 109's rows stay in "What the page is handed".
- `open.md`: "Structural limits" went to `open/limits.md`. No "Not yet seen" item was dropped: none has a measurement or owner's word that settles it beyond what the entries already record.
- `decisions/shape.md`: decisions 94 and 54 went to the new group file `decisions/rail.md` (2,831 B of 12,288, so 9,457 B of headroom); `decisions.md` has the new row, and the two citations of 94 in `assistant.md` and `promptu.md` were repointed with no change in length (`promptu.md` keeps its 204 B).

`check-doc-size.py --pressure` now reports all four as PAID. `check-docs.py` and `check-ownership.py --scope chat` are green.

## The human question

Can `spec.md` alone answer what someone needs to work on this component today? Yes. It keeps the status line, what the chat is, how it works (every bullet still states its rule and cites its decision), the invariants other than the three input ones, and what it does not do. The three input invariants and the handoff mechanics are one hop away and each has a pointer saying what it holds. Someone working on the input reaches `spec/input.md`, which `spec.md` already sends them to for the library, assistant and Promptu.
