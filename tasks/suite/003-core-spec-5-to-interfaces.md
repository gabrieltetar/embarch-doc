# Move embarch-core/spec.md §5 into interfaces.md, and fix the one inbound §5 citation

**State:** open — **not announced; the §4 window has not started.**
Leg 007 filed this from an `inbox/` drop but had **no Slack surface** (no connector tool
in the supervisor agent's toolset), so it could neither announce this nor poll
`#embarch-fleet`. `embarch-fleet/ops.md` §4 requires the announcement before a `suite`
task runs. **The next leg must announce it and start a fresh 30-minute clock** — there is
no prior `ts` to complete, unlike `suite/001`, which leg 006 had already served.
**Source:** tasks/core/003-compact-docs.md, the compaction pass that could not do it
**Scope:** suite
**Hardware:** none

## What

`embarch-core/spec.md` §5 is the on-disk result layout — `study_results/<id>/`,
`events.json`, `streams/index.json`, the five tap file shapes. It is a reference
table, and `DOC-COMPACTION.md` §9 says a reference table belongs in
`interfaces/`, loaded deliberately. `embarch-core/interfaces.md` is at
9,953/15,360 B and already documents every route that serves those files.

Move the block, drop spec.md's §5 heading, renumber §6 → §5, and point at
interfaces.md from spec.md's header line.

**The reason this is `suite` and not `core`:**
`embarch-study-designer/spec.md` line 66 cites `embarch-core/spec.md` **§5** as a
markdown link plus a bare section number
**by section number**. `check-links.py` skips anchors and `check-decision-refs.py`
only resolves decision numbers, so nothing would catch the break — and fixing it
means writing another sub-project's file, which a worker may not do. One repo,
one commit, but two sub-project directories.

Check the whole repo for other `embarch-core/spec.md §N` citations first; that
grep found one, on 2026-09-04.

## Why now

Not urgent. `embarch-core/spec.md` came out of reserve at 8,988/10,240 B
(87.8%) and this is the only structural cut left in it — everything else in the
file passed §9's hot test. So the next task that must add anything real to
Core's spec re-enters reserve almost at once, and this is the ~640 B that buys
it room. Filing it now so the finding is not re-derived: the worker that found
it holds no state.

## Done when

- [ ] §5's block lives in `embarch-core/interfaces.md`, `spec.md` points at it,
      and `spec.md`'s remaining sections are renumbered.
- [ ] `embarch-study-designer/spec.md`'s citation resolves to wherever the
      layout now is, and no other `embarch-core/spec.md §N` citation dangles.
- [ ] `scripts/check-docs.py` green; `changelog.d/` fragment dropped.
