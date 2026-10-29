# 004 — `embarch-chat/decisions/timeline.md` is over its cap: split it by mission, verbatim

**State:** claimed by agent/chat/004-split-timeline, 2026-10-28 22:17
**Source:** `chat/002` added decision 90 and left the file at 12,144 B of 12,288 B; `DOC-COMPACTION.md` §2. Decisions 92–93 (owner's session, 2026-10-26) then took it to 13,806 B, 1,518 B **over** the cap.
**Scope:** chat
**Hardware:** none
**Owner:** no

**Compacts:** embarch-chat/decisions/timeline.md
**Size debt due:** 2026-11-02
**In flux:** no, for the remedy this task now takes. Decisions 89 and 90 (what the CLI sends Claude, the agent report) are still moving — 90's hand-back source is assumed, not recorded on the wire — and that was this task's park until 2026-10-28. But `DOC-BUDGET.md` makes a split the default remedy: it moves entries verbatim, so it restates nothing and the in-flux objection cannot apply. Reopened by the 2026-10-28 22:15 leg on that reading. 89 and 90 are not squeezed by this task.
**Must not delete:** decision 89's rejected alternatives and its `[Recorded on CLI 2.1.287]` note; decision 90's `[assumed]` bracket until the hand-back is recorded. Under a verbatim split nothing is deleted at all.

## What

`decisions/timeline.md` holds 17 decisions (8, 50, 87, 51, 89, 90, 76, 79, 62, 68, 69, 67, 74, 85, 15, 16, 93) under one heading, "what the chat shows", and is 13,806 B against a 12,288 B cap. When this is done, a coherent mission group of the **settled** decisions has moved **verbatim** (no rewording, no trimming) into a new `embarch-chat/decisions/<topic>.md` with the same header shape as its siblings, `decisions.md`'s index table names the new file and its decision numbers and trims the moved ones from `timeline.md`'s row, and `timeline.md` sits below the reserve line (90% of its cap). Decisions 89 and 90 stay in `timeline.md` word for word. Pick the group with `scripts/check-doc-size.py --decisions` and the index's own mission text (time, usage, copy/export and long chats are one candidate; CLI rows are not, because 89 and 90 are those). Decision numbers address the sub-project, not a file, so code citations do not change; any doc link that names `decisions/timeline.md#…` for a moved decision does.

## Why now

The file is over its cap, so the next decision filed under this mission has nowhere to go but the wrong file, which is the failure `DOC-COMPACTION.md` §2 exists to prevent. Due 2026-11-02.

## Done when

- [x] `timeline.md` below the reserve line; the moved decisions byte-identical in their new file.
- [x] `decisions.md`'s index table updated; every link to a moved decision resolves.
- [x] Every `Must not delete:` item is still readable.
- [x] Gate green (`python3 scripts/check-docs.py`; no code changes, so no npm gate unless the worker touches `embarch-chat`).
- [x] `changelog.d/` fragment dropped.

## Done

Split by mission, verbatim: 15, 16, 67, 68, 69, 74, 85 moved to `decisions/readouts.md`; timeline.md 13,806 B to ~10.4 KB, readouts.md ~3.7 KB. 89, 90 untouched. No code change.
