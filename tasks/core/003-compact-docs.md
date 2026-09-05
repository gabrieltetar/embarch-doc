# 003 — embarch-core's spec.md and open.md are in reserve

**State:** claimed by agent/core/003-compact-docs, 2026-09-04 20:02
**Source:** scripts/check-doc-size.py --pressure
**Scope:** core
**Hardware:** none
**Compacts:** embarch-core/spec.md, embarch-core/open.md
**In flux:** no
**In reserve for this sub-project (supervisor, leg 007):** `embarch-core/open.md` 4810/5120 B — **310 B left**; `embarch-core/spec.md` 9537/10240 B — **703 B left**. Both are filed against *this* task, so getting them out of reserve is the job, not a debt to record. If you leave either in reserve, rewrite this task's `## Done when` to say why rather than closing it.
**Must not delete:** open.md's candidate fix for the 18 stale records (drop a leading run of discontinuous records at render time); decision 36's probe-rs counterfactual, which is **evidence and not proof** and reads as proof the moment it is shortened; the `validate_signal` has-no-caller-deliberately reasoning, which is a rejected alternative wearing a gap's clothes.

## What

`spec.md` is at ~93% of 10 KB and `open.md` at ~94% of 5 KB. Neither is a wall
yet; both are inside the reserve, so the next task that must write either will
be working in a few hundred bytes.

`open.md` had a pass on 2026-09-04 that took it 5086 → 4810 by sentence-level
cuts only, and its 26 questions were all kept — so **the cheap half is already
spent there**. Run `scripts/check-duplication.py embarch-core` before anything
else: that pass left one 13-word overlap between `decisions/studies.md` and
`open.md` on the `FlashedThisRun` reasoning, and a claim held in two files is a
`DOC-PROTOCOL.md` §3 error rather than a cold sentence.

`spec.md` has not had a §9 pass at all.

## Why now

It is in reserve, and Core is the sub-project every other one reaches through —
its `open.md` is where three other repos' blocked items are named.

## Done when

- [ ] Both files out of reserve, or this task rewritten to say why one of them
      should not be (an honest "this is the hot floor" is an answer).
- [ ] No question disappears from `collect-open-questions.py` unless you can
      name it as answered. **Merging two questions into one is not answering** —
      that was tried on 2026-09-04 and reverted.
- [ ] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [ ] Gate green, `changelog.d/core-*` fragment dropped.
