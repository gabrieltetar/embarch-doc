# 034 — decision 50's closing paragraph names three consumers that no longer describe reality after decision 54

**State:** open
**Source:** reviewer, `core/027` (merge `56cb0b1`, `embarch-doc`; no `embarch-core` merge — code branch had zero commits). Filed from `inbox/` by leg 066.
**Scope:** core
**Hardware:** none
**Owner:** no

**Re-scoped on filing (leg 066, 2026-09-10).** The drop said `Scope: doc`; the file it changes is
`embarch-core/decisions/surfaces.md`, which is a `core` doc directory and belongs to a `core`
worker. `doc` scope would have made it undispatchable to the one actor who can fix it. Nothing else
in the drop was altered — everything from `## What` down is the reviewer's own text, including the
`## Reviewer notes` section, which answers three questions this task does not depend on and is kept
because it is the record that they were checked.

## What

`embarch-core/decisions/surfaces.md` decision 50's closing paragraph reads:

> Three consumers are filed and blocked on this task: `tasks/api/045`,
> `tasks/umbrella/041`, `tasks/ui/020`; each mirror keeps deserializing
> regardless of when, or whether, it picks the new field up.

All three are now resolved, and none the way this sentence still implies
("filed and blocked"):

- `tasks/api/045` landed (folded in `a687baf`, "the validate mirror, MCP tool
  and CLI carry validated_at_utc_ms").
- `tasks/umbrella/041` and `tasks/ui/020` both closed **unsatisfiable** (folded
  in `e0dc52b`, "two unsatisfiable tasks closed") — this is exactly the premise
  decision 54 (`core/027`, same file, immediately below decision 50) builds on:
  "`tasks/umbrella/041` and `tasks/ui/020` — the two consumers decision 50
  filed to actually *show* it — both closed unsatisfiable."

Decision 54 does not contradict decision 50's design (it correctly narrows it:
50's additive field on `POST /validate` stands, 54 only declines to *also*
persist a second field elsewhere). The contradiction is textual, not design:
decision 50 itself was never amended and still asserts three tasks are "filed
and blocked" when, as of this same diff's own decision 54, two are closed
unsatisfiable and one landed a leg ago. A reader who opens decision 50 alone —
which is what a forward-reference is for — gets a stale status for all three
named consumers, with no pointer forward to decision 54, which is the one
place that status is actually current.

## Why now

`core/027` was in the best position to write the one-line amendment (it
authored decision 54 immediately below decision 50 in the same file, and
already had all three consumers' final states in hand from `tasks/core/027`'s
own dispatch note), but the task's `Done when` didn't ask for it, so it wasn't
done. This is the stale-forward-reference shape the reviewer brief specifically
names: "a decision left claiming filed consumers that no longer exist."

## Done when

- [ ] Decision 50's closing paragraph in `embarch-core/decisions/surfaces.md`
      is amended to say `tasks/api/045` landed, `tasks/umbrella/041` and
      `tasks/ui/020` closed unsatisfiable, and to point forward to decision 54
      for what replaced the latter two's intent.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

## Reviewer notes (not part of the task)

- Item 2 checked out: `EnrolledBoard` is `embarch_topology::hardware::EnrolledBoard`
  (real dependency, `Cargo.toml` `embarch-topology = { path = "../embarch-topology", ... }`),
  not an `embarch-core` type — decision 54's cross-repo-storage argument is factually correct.
- Item 3 checked out: `embarch-topology` decision 26 does say renaming/adding a
  field to the enrolled record is a cross-repo, out-of-crate-scope change
  ("`suite`-scoped work outside a `topology` worker's reach... half-landing it
  here is exactly this suite's worst-named failure mode") — decision 54's
  paraphrase ("exactly the reasoning decision 26 already gave") is accurate,
  not a borrowed citation.
- Item 4 (the two inbox drops) are both reachable: each has a `Done when` that
  closes even with zero code shipped today, by folding the reasoning into the
  target repo's own doc comments/spec — not conditional on something that
  doesn't exist.
- No `embarch-decision-reversals.md` row: decision 54 doesn't decline an arm
  decision 50 itself promised (50 only promised the additive `/validate` field,
  which it delivered); it resolves two already-closed-unsatisfiable follow-ups.
  Not a reversal shape.
