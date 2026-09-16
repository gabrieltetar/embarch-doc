# 048 — two `embarch-topology` decisions are over the per-decision cap, both below the census's cut

**State:** claimed by agent/topology/048-two-decisions-over-cap, 2026-09-16 14:24
**Source:** leg 118, 2026-09-16. Leg 117's suite-wide per-decision census reported five breaches and
filed four tasks, of which `topology/047` — decision 25, the largest decision entry in the suite — was
one. Leg 118 landed all four and then found the census had never been capable of seeing the rest:
`check-doc-size.py --decisions` prints the **twenty largest decisions in the suite** and marks which
are over cap, so an unpinned breach below that line is printed nowhere, and 27 pinned over-cap entries
fill the slots. Read through `decision_state()` directly, five unpinned breaches remain and two of
them are here. Neither is a regression and neither was touched by `topology/047`. The mechanism is
`tasks/doc/064` (owner-reserved; `scripts/`).
**Scope:** topology
**Hardware:** none — doc prose only. No board, no probe, no live Core, no deploy, no enrolment.
**Owner:** no
**Compacts:** `embarch-topology/decisions/validation.md`, `embarch-topology/decisions/link-declares.md`
**In flux:** no, both, and each was checked separately rather than answered once for the line.
Decision 21 is the Nordic arm the self-reported-ID gate gained; the arm landed, and what is still open
is a **hardware** gap — `nRF54L10`, `nRF54L05` and `nRF54LM20A` take that arm with no such silicon
ever on this bench. A hardware debt is not doc flux: a board would *add* a measurement, not rewrite
the decision. Decision 20 is the role-uniqueness and link-interface pair that closed the day the dev
bench went back to being an nRF54L15DK; both gaps named in it are closed.

## What

Two entries, both over the 4,096 B per-decision cap, neither pinned in
`scripts/decision-size-baseline.json`:

```
4,301 B  embarch-topology/decisions/validation.md#21      (+205 B, 105% of cap)
4,176 B  embarch-topology/decisions/link-declares.md#20   (+ 80 B, 102% of cap)
```

Both are small breaches — 80 B is under a paragraph. For each, the same fork `topology/047` faced and
answered with a compaction:

- **One decision stated at length** → compact under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full.
- **One decision that has accreted several arguments** → split into two numbered decisions and update
  `embarch-topology/decisions.md`'s index, same commit. **A new decision number is the most expensive
  thing in this suite to reverse**, so the burden of proof is on this branch.

Decision 20's own opening — *"Two independent gaps, one event"* — is worth reading against that fork
before choosing. It says in as many words that it carries two things. At 102% of cap the split is
still a hard case to make, and `topology/047` made the opposite call on a much more split-shaped
entry by asking the right question: **does any inbound citation want to point at the two halves
separately?** Answer that with a grep, not an impression.

## Watch for

- **The safety claims must not end up reading as tested.** Decision 21's whole point is that *"a
  comparison that could not be made is not a comparison that succeeded"*, and that the gate had never
  once run against Nordic silicon before that arm. Decision 20's role-uniqueness half exists because
  *nothing errored and the file looked correct* while two rows claimed the same role. Both are
  descriptions of silent failure, which is the category `DOC-COMPACTION-PASS.md` calls hot: cut
  narrative, never the mechanism.
- **Decision 25 is now 4,001 B with 95 B of margin** after `topology/047`. Do not spend that margin
  from the side — if your work touches `validation-classifier.md` at all, check its size before you
  push.
- **The `core/064` failure mode, which hit this class twice in leg 118 alone.** A cut justified as
  "provenance" or as "duplicates decision N" is exactly where a live claim goes missing: once when a
  retired decision's compaction cut a live-route behavioural fact (`tasks/core/065`), once when a
  "duplicates decision 35" justification covered only part of the cut paragraph
  (`inbox/umbrella-locate-api-list-targets-shape-orphaned.md`). If you justify a cut by pointing at
  another decision, **open that decision and confirm it covers the whole hunk, sentence by
  sentence** — not the topic.
- **Quote every cut hunk verbatim and completely** in this task file. Err toward over-inclusion.
- **Do not add pins to `scripts/decision-size-baseline.json`.** `scripts/` is owner-reserved, and
  pinning an over-cap decision is the papering-over move.
- **Grep the whole doc repo for inbound `decision 20` and `decision 21` citations first**, and
  remember a bare `decision 20` in another sub-project's file means *that* sub-project's 20.
- **Report before/after byte counts and the margin left** for each entry you touch.

## Dispatch note — leg 119, 2026-09-16

**In reserve for `topology`: nothing.** No `embarch-topology` file is inside the last 10% of its cap,
so you have file-level room and this is purely the per-decision cap. If your work does push a file
into reserve, file `tasks/topology/<NNN>-compact-topology.md` in the same commit
(`scripts/check-task-numbers.py --next topology` for the number — **do not read the directory**).

**The census that filed this task is itself unreliable, so do not use it to check your work.**
`check-doc-size.py --decisions` prints only the twenty largest decisions in the suite and 27 pinned
over-cap entries fill those slots, so it cannot confirm a smaller entry is now under cap
(`tasks/doc/064`, owner-reserved). Count the bytes of each entry you touch directly and report them.

## Done when

- [ ] `embarch-topology` decision 21 is at or under 4,096 B, or split, with the branch justified.
- [ ] `embarch-topology` decision 20 likewise, **or** left untouched with a follow-up task filed.
- [ ] The untested-silicon statement in decision 21 and the silent-failure mechanism in decision 20
      both survive.
- [ ] `embarch-topology/decisions.md`'s index matches, if anything was split.
- [ ] Every inbound citation to a touched decision still resolves to the claim it was citing.
- [ ] Every cut hunk quoted verbatim in this task file.
- [ ] No pin added to `scripts/decision-size-baseline.json`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
