# 068 — `embarch-umbrella` has two decisions over the per-decision cap, both untracked

**State:** claimed by agent/umbrella/068-two-decisions-over-cap, 2026-09-16 12:54
**Reserve (leg 118):** `embarch-umbrella/decisions/bind.md` is at 93.9% — 755 B left of 12288 — and
is already filed against `tasks/umbrella/009-compact-docs.md`, which is **blocked**. Neither
decision in this unit lives in `bind.md`; do not write into it. If your work spends reserve anywhere
in `embarch-umbrella`, file `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit.
**Source:** leg 117, 2026-09-16. `core/063` closed this gap for `embarch-core` decision 30 and named
the real finding as *"nothing is watching it."* I ran the census that implied: **five** decisions
suite-wide are over [`DOC-BUDGET.md`](../../DOC-BUDGET.md)'s **4,096 B per-decision cap** with no pin
in `scripts/decision-size-baseline.json`, so nothing reports them and no ledger gives them a clock.
`core/063` fixed one, `core/064` files another, `topology/047` files the largest. **Two of the five
are here**, which is more than any other sub-project.
**Scope:** umbrella
**Hardware:** none — doc prose only. No board, no probe, no live Core, no `doctor` run.
**Owner:** no
**Compacts:** `embarch-umbrella/decisions/probe-vendors.md`, `embarch-umbrella/decisions/locate-api.md`
**In flux:** no, both — and the distinction matters, so read it rather than trusting the word.
Decision 49's **routing half is settled**: [`open.md`](../../embarch-umbrella/open.md) records
in as many words that *"the list stays here"* and moves only if something other than `doctor`'s own
message ever consumes it. What is unmeasured there is *whether the nine vendor IDs are the right
nine* — a question about the list's **contents**, not about this decision's text or its home.
Decision 42 was settled by `umbrella/059`, which split `locate-api.md` out as its own file. Neither
entry is being rewritten by anything in flight.

## What

Two entries, both over cap, neither pinned:

```
6,962 B  embarch-umbrella/decisions/probe-vendors.md#49   (+2,866 B, 170% of cap)
5,157 B  embarch-umbrella/decisions/locate-api.md#42      (+1,061 B, 126% of cap)
```

For each, the same fork `core/063` faced:

- **One decision that has accreted several arguments** → split it into two numbered decisions and
  update `embarch-umbrella/decisions.md`'s index — number list **and** size column, same commit.
- **One decision stated at length** → compact under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full, including quoting every cut hunk
  verbatim rather than naming categories.

**Read each before choosing, and answer the fork separately for the two.** They are not the same
shape: decision 49's own opening is *"The question, as it was asked"* — an entry that narrates a
question and then answers it, which is the profile that compacts well. Decision 42's opening
sentence says `open.md` *"recorded [it] from three directions and never as its own item"*, which is
the profile that sometimes really is two decisions.

**A new decision number is the most expensive thing in this suite to reverse**, so the burden of
proof is on splitting: you have to name two claims a citation could want to point at *separately*.

## Why now

**Because the per-decision cap has no ledger and no clock.** The file-level ledger has both — a leg
spends its first unit on the oldest overdue entry, and `check-doc-size.py --pressure` lists every
file in reserve with the task that owns its debt. A decision that was never pinned is invisible to
all of it: `--decisions` prints only its top 20 by size, which is how `embarch-core` decision 30 sat
over cap until a reviewer opened the baseline file while checking something unrelated. Whether that
gap should be closed mechanically is the owner's call under `scripts/`
([`tasks/doc/052`](../doc/052-a-verbatim-split-silently-drops-the-decision-size-pin-of-every-decision-it-moves.md)
records the adjacent defect). **This task is only about the two entries that are actually over.**

## Watch for

- **Do not add pins to `scripts/decision-size-baseline.json` to make the numbers go away.**
  `scripts/` is owner-reserved, and pinning an over-cap decision is the papering-over move.
- **Decision 49 is cited from outside `embarch-umbrella`** — it is the vendor-ID routing decision
  and `doctor` check 5's behaviour hangs off it. Grep the whole doc repo for inbound `decision 49`
  and `decision 42` citations before renumbering anything, and remember a bare `decision 49` in
  another repo's file means *that* repo's 49.
- **Keep the "why not".** Decision 49's whole point is *why the list is not in `embarch-topology`* —
  that it is not the same fact that crate holds. That argument is the entry's reason for existing
  and a compaction that loses it invites the move being re-proposed. Cut narrative and single-machine
  measurements, not the reasoning.
- **If you only have budget for one**, do decision 49 — it is the larger breach and the one with
  cross-repo citations — and leave decision 42 with its remainder filed as its own task, the way the
  `study-designer` sweep chain does.
- **Report before/after byte counts and the margin left** for each entry you touch.

## Done when

- [ ] `embarch-umbrella` decision 49 is at or under 4,096 B, or split, with the branch justified.
- [ ] `embarch-umbrella` decision 42 likewise, **or** left untouched with a follow-up task filed
      naming it.
- [ ] `embarch-umbrella/decisions.md`'s index table matches — numbers and size column.
- [ ] Every inbound citation to a touched decision still resolves to the claim it was citing.
- [ ] If compacted: every cut hunk quoted verbatim in the task file, per `DOC-COMPACTION-PASS.md`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
