# 004 — `embarch-chat/decisions/timeline.md` is in reserve after decision 90

**State:** blocked — `In flux: yes`, until the hand-back's live wire shape is recorded (the debt in `tasks/chat/002`) and decision 90 stops being assumed
**Source:** `chat/002` added decision 90 and left the file at 12,144 B of 12,288 B; `DOC-COMPACTION.md` §2
**Scope:** chat
**Hardware:** none
**Owner:** no

**Compacts:** embarch-chat/decisions/timeline.md
**Size debt due:** 2026-11-02
**In flux:** yes — decisions 89 and 90 (what the CLI sends Claude, the agent report) are one subsystem still moving: 90's hand-back source is assumed, not recorded on the wire, and the next unit there will rewrite both. A split by mission (the CLI-lines decisions into their own file) is the likely shape once they settle.
**Must not delete:** decision 89's rejected alternatives and its `[Recorded on CLI 2.1.287]` note; decision 90's `[assumed]` bracket until the hand-back is recorded.

## What

The file is 144 B from its cap.

## Why now

`check-doc-size.py --pressure` fails on a file in reserve with no task naming it.

## Done when

- [ ] The file is clear of the reserve line, by a split or a squeeze, once `In flux` is `no`.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green.
