# 008 — `embarch-promptu/decisions/patterns.md` is in reserve

**State:** open
**Source:** promptu 007 (EMB-196) added the footer and log pointers to decisions 13 and 14, leaving `decisions/patterns.md` at 11,138 of 12,288 B (reserve from 11,059 B; it stood at 11,058 B on `main`, at the edge).
**Scope:** promptu
**Hardware:** none
**Owner:** no

**Compacts:** embarch-promptu/decisions/patterns.md
**Size debt due:** 2026-11-24
**In flux:** no, for a verbatim split. Decisions 9, 13, 24 and 42 still move with the owner's rewrite settlement (model and wait, owed in `embarch-promptu/open.md`), so they stay in place, untouched; the split moves only decisions whose subject is settled, word for word, which restates nothing (`DOC-BUDGET.md`'s split-first rule). Was `yes` with this task blocked until EMB-197 landed; it landed in `embarch-chat` `f79c167` on 2026-11-17, so the park's own unpark condition has fired.
**Must not delete:** decision 42 whole, the "Amended by 42" pointers on 9, 13, 14 and 24, and the rejected-alternative lists of 9, 13 and 24.

## Dispatch notes

- Unparked by the supervisor: `Unparks when:` read "the owner records the rewrite's model and wait …, or EMB-197 lands, whichever is first", and EMB-197 (the chat's Promptu card, `promptu original <run>`) is on `embarch-chat`'s `main`.
- Docs only, `embarch-doc/embarch-promptu/`; no code branch.
- **Do not move 9, 13, 24 or 42**: each is amended by 42, or is 42, and is restated once the owner settles the rewrite. Decision 14 is not in this file.
- Candidates for the move, settled: 22, 23, 25, 26, 27, 28 (the pass's and the patterns' questions, fork S1 to S8), and if a seam needs them, 10, 11, 12, 31, 41. Only 80 B are needed to leave the reserve; move by mission, not by size, and put the moved decisions in one new `decisions/<topic>.md`.
- Inbound links: only `embarch-promptu/decisions.md`'s index row names `decisions/patterns.md` [checked at dispatch]; nothing in `history/` cites it, so no citation pins a decision in place. Run `scripts/check-decision-refs.py` after the move anyway.

## What

Bring `decisions/patterns.md` out of reserve: move whole decisions whose subject is settled (the pass's and patterns' questions, 22 to 28 but not 24) into a new topic file verbatim, leaving the index row in `decisions.md` updated. Never shorten a decision-bearing sentence.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-promptu/decisions/patterns.md`.
- [ ] Moved decisions are byte-identical in their new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
