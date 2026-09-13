# 047 — Two `embarch-core` decision entries record a cross-repo hand-off as still owed, and both have landed

**State:** claimed by agent/core/047-cross-repo-handoff-claims, 2026-09-13 11:45
**Source:** leg 105 refill sweep, 2026-09-13. Both instances read in full before filing; the
`embarch-ui` code claims below are the scout's and are **to be re-verified by whoever takes this**,
not taken on trust.
**Scope:** core
**Hardware:** none — two paragraphs in two decisions files. No code, no wire, no board.
**Owner:** no

## What

`embarch-core`'s decision corpus does something this suite does deliberately and well: when a
defect belongs to another repo, it says so and files it rather than reaching across. The cost of
that discipline is that the entry then carries a **claim about another repo's present state**, and
nothing updates it when that repo acts. Two such claims are now stale.

**(a) `decisions/studies.md`, decision 54's *Consequences* paragraph** says:

> The `+1` in `embarch-ui`'s badge was written for the count convention and is therefore one short
> mid-run against the index convention — a real defect, in a repo this decision does not own; filed
> for its owner rather than fixed here.

The **same entry, two lines above**, already records the fix: the `embarch-ui` bracket is marked
*"historical as of the same day: `ui/010` landed `embarch-ui` decision 20 and the badge now renders
the step now running, `current_step + 2` clamped."* So one paragraph of one entry says the defect
is live and filed, and another says it landed. Verify against the code —
`embarch-ui/assets/app.js` and `embarch-ui/src/study_designer.rs` are where the badge and its pin
live — and then make the *Consequences* paragraph agree with the bracket, keeping the sentence
that explains **why** the two conventions diverged, which is the durable half.

**(b) `decisions/enrollment.md`, decision 57's "The label is the whole fix" paragraph** says:

> Filed to the queue rather than assumed: `tasks/umbrella/<NNN>` … and `tasks/ui/<NNN>` … — both
> dropped to `embarch-doc/inbox/` rather than filed here.

`embarch-doc/inbox/` holds nothing but its `README.md`. The umbrella half became
`tasks/umbrella/045` (landed). The UI half appears already satisfied — check
`embarch-ui/assets/app.js` and `embarch-ui/src/snapshot.rs` for the Topology tab's
`confirmed_at_utc_ms` cell and whether it is labelled "Enrolled" and cites `embarch-core`
decision 57 by name. Replace the two `<NNN>` placeholders with what actually happened.

## Why now

A `<NNN>` placeholder is a promise with no address, and a decision that says a defect is live in
another repo when it is not is worse than one that says nothing: a reader who trusts it goes
looking for a bug that is fixed, and a reader who checks it stops trusting the corpus. No gate sees
either — `check-decision-refs.py` resolves decision *numbers*, and `check-links.py` resolves
*links*; a prose claim about another repo's state is neither.

## Done when

- [ ] Decision 54's *Consequences* paragraph no longer describes the `embarch-ui` badge defect as
      live and filed, and the reason the two step conventions diverged is kept intact.
- [ ] Decision 57's two `tasks/<scope>/<NNN>` placeholders name what actually happened — the task
      that landed, or, if a half turns out **not** to be satisfied, a real task number filed by an
      `inbox/` drop rather than a placeholder left in place.
- [ ] Each claim about `embarch-ui` is checked against `embarch-ui`'s own code and the file:line
      said in the report. **Do not write `embarch-ui`** — it is not this scope's — and if either
      turns out unsatisfied, drop the task to
      `/home/gabriel/Github/embarch/embarch-doc/inbox/` (absolute path) instead of filing it.
- [ ] `grep -rn '<NNN>' embarch-core/` returns nothing that is a live promise.
- [ ] Gate green; `changelog.d/` fragment.

## Do not

**Do not delete either paragraph.** Both carry reasoning nothing else in the suite states —
decision 54's two-counters-one-name explanation, and decision 57's argument for why a second
persisted timestamp was the wrong fix. This is a correction to a claim about *another repo's
present state*, not a compaction.
