# 003 — embarch-core's spec.md and open.md are in reserve

**State:** done by agent/core/003-compact-docs, 2026-09-04
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

- [x] Both files out of reserve. `spec.md` 9537 → 8988 B (87.8%), `open.md`
      4810 → 4504 B (88.0%). `--pressure` reports both `PAID`.
- [x] No question disappeared. All 16 of `open.md`'s bullets survive with their
      lead claims byte-identical except one reworded in place; none was merged
      into another. `collect-open-questions.py` diffed before and after.
- [x] `DOC-COMPACTION.md` §7's question answered in the commit message — the
      honest answer is **no**, and why is written there.
- [x] Gate green but for one pre-announced red, `changelog.d/core-*` dropped.
      `check-docs.py` is 6/7: the only failure is `install.py --check`, which
      renders the three generated READMEs' cross-repo link from the resolved
      repo path and so reports drift for any worktree at a different depth than
      the main checkout. The committed READMEs are untouched by this branch.

## What was cut, and what was not

The one `check-duplication.py` overlap is gone: `open.md`'s `FlashedThisRun`
bullet no longer restates decision 31's "`/flash` and `/study` are separate
calls" reasoning, which the decision owns. Four more single-claim-in-two-files
cases went the same way — the Raspberry Pi artifact-transfer limit (spec.md →
`open.md`, which owns limitations), `contract_version`'s retirement (`open.md` →
spec.md §2 and decision 13), "Core never orchestrates a build" (a §2 invariant
folded into §1's already-sharper "it is not a build system"), and §7 Security,
whose three facts were one invariant, one line already in the constants table,
and a pointer — folded into §2's auth invariant and the section dropped.

Cold under §9, dropped: the `GET /enroll` retirement date (decision 25 is its
tombstone), the `deploy-core`-reported-success-and-installed-nothing incident
behind `core_version` (decision 13), the 2026-08-21 date on the
`embarch-topology` move, and "count-based, so it needs no clock" beside
`EMBARCH_STUDY_RESULTS_KEEP` (decisions/streams.md).

All three `**Must not delete:**` items are present verbatim.

## Debt, for whoever compacts this next

**`spec.md` has 228 B above the reserve line and no cheap cut left.** The
obvious next move is §9's own — §5's result-layout tree is a reference table,
which §9 says belongs in `interfaces/`, and `interfaces.md` has 5 KB spare. It
was **not** done here because `embarch-study-designer/spec.md` cites
`embarch-core/spec.md` **§5** by section, and fixing that inbound link is
another sub-project's file. That makes it a supervisor's cross-repo pass;
dropped in `inbox/` as `core-spec-5-to-interfaces.md`.
