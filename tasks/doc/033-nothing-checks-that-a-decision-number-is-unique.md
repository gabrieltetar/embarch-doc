# Nothing in the gate checks that a decision number is unique within its sub-project, and the convention that says it must be is the one every worker reads

**State:** open
**Source:** supervisor, leg 061, 2026-09-09 — caught by hand while reading `outpost/015`'s diff before merging it
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is a new or extended check under `scripts/`, which
`protocol.md` §3 reserves to the owner; no agent can write it, and dispatching
this would produce a red `check-ownership.py` for whoever took it. Filed here so
it is visible in the queue rather than nowhere. Set by the supervisor, leg 062,
2026-09-09, at the moment of filing the drop.

## What

`embarch-outpost/decisions.md` opens with the rule, in bold, as its third line:

> **Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused
> ([DOC-CONVENTIONS.md](../../DOC-CONVENTIONS.md)). `scripts/check-decision-refs.py` resolves every one.

The second sentence is what makes the first sentence look enforced. It is not. `check-decision-refs.py`
resolves a **citation** to a decision — it answers "does decision N exist in this sub-project" — and
that predicate is satisfied *more* easily, not less, when two files both define N.

`outpost/015` authored a new decision and numbered it **23**. `embarch-outpost` decision 23 already
existed in `decisions/manifest.md`'s sibling `decisions/wire.md` (*"`src/outpost_priv.h` is the
definition; the other three copies are diffed against it"*). The worker's branch therefore landed
two `### 23` headings in one sub-project's `decisions/` directory, and:

- `check-docs.py` passed **11/11**, including `check-decision-refs.py`.
- The worker reported the gate green, correctly.
- `decisions.md`'s index listed `23` twice — on the `manifest.md` row and the `wire.md` row — and
  nothing read that as a contradiction.

The supervisor renumbered it to 24 in the fold. It was caught only because leg.md requires reading
the diff by hand when a unit authors or retires a decision, which is a rule about supervisor
attention rather than a check.

## Why this one matters more than an ordinary gate gap

**A duplicate decision number is silent and permanent, and it corrupts every citation to it
retroactively.** `DOC-CONVENTIONS.md` says numbers are never renumbered or reused precisely because
citations to them are scattered across code comments, other sub-projects' docs, and this log. Once
two decisions share a number:

- Every existing citation to `decision 23` becomes ambiguous — including ones written months
  earlier that were unambiguous when written.
- `check-decision-refs.py` keeps passing, so nothing degrades.
- The fix stops being free the moment anything cites the new one, because by then *neither* number
  can move without breaking a citation, and the convention forbids renumbering either.

This is the same failure class the suite has already paid for twice, from the other direction:
`api/031` and `api/052`'s "a citation stripped of its qualifier lands on a real but wrong decision".
That one produces a wrong pointer to a right decision; this one produces a right pointer to two
decisions. Both read as authoritative and survive every check.

## Why a supervisor cannot be the mechanism

Three legs in a row have now found a class of defect that `check-decision-refs.py` looks adjacent to
and does not cover. Leg 060's `umbrella/042` entry names one of them explicitly: the script
*"resolves a decision number and falls back to 'defined somewhere in this sub-project,' so a citation
naming the wrong file still resolves — third unit this leg to hit the same blind spot."* Uniqueness
is the same blind spot from the definition side rather than the citation side, and it is cheaper to
check than either: it is a `grep` for `^### <N>` per sub-project and a duplicate test.

The reason this is filed rather than fixed is that `scripts/` is owner-reserved
(`protocol.md` §3), and correctly so. But note what that means here: **the rule is documented in a
reserved file, asserted as enforced in every sub-project's `decisions.md` header, and enforced
nowhere.** An agent reading that header has every reason to believe a collision would fail the gate.

## Done when

- [ ] Something in `check-docs.py` fails a sub-project whose `decisions/` tree defines the same
      decision number twice. A `^### <digits>` scan per sub-project is sufficient; it does not need
      to understand the decisions.
- [ ] It also catches the index form — a number appearing on two rows of `decisions.md`'s table —
      or says explicitly why that is out of scope.
- [ ] Whatever the check is, `decisions.md`'s boilerplate sentence names **it** rather than
      `check-decision-refs.py`, so the assertion and the enforcement are the same thing. If the
      decision is not to build the check, that sentence should stop claiming enforcement.
- [ ] A worker's task template or `protocol.md` §5's worker contract tells a worker authoring a new
      decision to take the next free number by scanning, not by reading the index — the index was
      accurate here and the worker still collided.

## What is already fixed, so nobody re-does it

`outpost/015`'s decision is **24**, renumbered by the supervisor in that unit's fold across
`embarch-outpost/decisions.md`, `decisions/manifest.md`, `decisions/clocks.md`, `spec.md` and its
`changelog.d/` fragment. `wire.md` keeps 23. Verified no duplicate `^### N` remains in
`embarch-outpost/decisions/`. **This task is about the missing check, not about that unit.**

## The sweep is done, and it changes the shape of the check

I ran the duplicate scan across all nine sub-projects. **One other hit, and it is not a defect** —
which is the most useful thing this drop has to say, because a naive check would have failed it.

`embarch-ui` defines `### 10` **three times**, on purpose:

| file | heading |
|---|---|
| `decisions/topology-tab.md` | `### 10 — Routing half: the Topology tab gains a DUT signal's route` |
| `decisions/trace-view.md` | `### 10 — Trace half: a Trace view renders an outpost capture post-hoc` |
| `decisions/trace-chart.md` | `### 10 — Chart half: the trace chart is navigable, and the study's steps are projected onto its axis` |

That is **one** decision whose mission split put its three halves in three topic files, and
`decisions.md`'s index disambiguates them explicitly — `10 (routing)`, `10 (trace)`, `10 (chart)`.
Nothing is ambiguous, no citation is corrupted, and renumbering any of them would break the
convention rather than serve it.

So the two cases are distinguishable, and the distinguishing evidence is already written down:

- **`embarch-ui`'s 10** — every heading names itself a *half* of one decision, and every index row
  carries a parenthesised qualifier.
- **`embarch-outpost`'s would-be second 23** — two unrelated subjects (a header-file source of
  truth, and an operator override posture), and an index that listed the bare number `23` twice with
  no qualifier.

**The index is the discriminator, not the headings.** A bare number on two rows is a collision; the
same number on several rows each qualified is a split. That makes the check a `decisions.md` table
check rather than a `grep` over headings — which is both easier to write and the form that does not
need a hand-maintained allowlist for `embarch-ui`.

Whoever takes this should also decide whether the split convention deserves recording in
`DOC-CONVENTIONS.md`, since it currently exists only as three files that happen to follow it and one
index that happens to qualify them. It is the thing the check has to be built around and it is
written nowhere.
