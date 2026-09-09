# `study-designer/007`'s Source cites the wrong `open.md`

**State:** claimed by leg 049, 2026-09-08
**Source:** owner's session 2026-09-07, found while parking the bench queue
**Scope:** study-designer
**Hardware:** none

## What

`tasks/study-designer/007-bond-clearing-has-never-been-observed-firing.md` says its
`**Source:**` is `embarch-study-designer/open.md`. That file has never carried the sentence
it quotes. The bullet lives in **`embarch-dev-bench/open.md`**, under `## Never exercised` —
verify that before editing rather than trusting this drop.

Point the `Source:` line at the file that actually carries it. **Re-quote from the file as it
stands now**: that bullet was amended on 2026-09-07 to record the attempt and the owner's
parking of it, so the sentence in the task is a prefix of a longer bullet, and copying the old
quote forward would recreate the same defect one revision later.

**Do not change `**State:** blocked`, and do not treat this as a reason to run the task.**
007 is parked by the owner until he says otherwise — this is doc hygiene on a parked file, and
a unit that quietly unparks a bench task would undo a decision the owner made deliberately.

## Why now

Dead and misdirected citations were most of a day's queue on 2026-09-07 — `topology/005`
(74 of them), `study-designer/016` and `017`, `dev-bench/013`. This is the same class, and
**no gate catches it**: the `Source:` line is backticked prose rather than a markdown link, so
`check-links.py` never resolves it and `check-decision-refs.py` has no decision number to
check. It was found by reading, which is the only way it can be.

## Done when

- [ ] 007's `**Source:**` names `embarch-dev-bench/open.md` and quotes that file verbatim as
      it stands at the time of the fix.
- [ ] `**State:** blocked` and its parking note are unchanged.
- [ ] Nothing else in 007 is edited — its `Done when` list is deliberately unmet.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

## Supervisor notes — leg 049

**A one-line result is the correct one here, and I do not want you to find adjacent work to justify
the run.** This is a two-line `Source:` correction on a parked task file. A worker given twenty
minutes and a one-line fix has an obvious failure mode — it goes looking for something bigger, and
what it finds is out of scope, half-understood, or both. Report the small result plainly and stop.
The previous leg dispatched a one-line unit on exactly these terms and it worked.

**The three constraints in the task body are hard, and the second is the one that matters most.**
`study-designer/007` is **parked by the owner**, deliberately. Do not change its `**State:**
blocked`, do not change its parking note, do not touch its `Done when` list, and above all do not
treat "the quote was wrong" as evidence the task can now run. A unit that quietly unparks a bench
task would undo a decision the owner made and nothing in the gate would notice.

**Re-quote from `embarch-dev-bench/open.md` as it stands at the moment you make the edit, and
verify the bullet is actually there before you edit anything.** The task itself warns that the
bullet was amended on 2026-09-07 to record the attempt and the parking, so the sentence currently in
007 is a *prefix* of a longer bullet. Copying the old quote forward recreates the identical defect
one revision later, which would be the fourth instance of stale-citation-fixed-with-a-stale-citation
in this queue's recent history. If the bullet is **not** in `embarch-dev-bench/open.md` where the
task says it is, stop and report that rather than hunting for a file that fits.

**Scope note.** You own `study-designer`. `embarch-dev-bench/open.md` is a file you **read** to get
the quote right — it is not yours to edit, and it should need no edit.

**Doc-size reserve for `study-designer`** — for completeness; nothing here should approach it, since
this unit edits a task file and nothing else. `decisions/registry.md` 461 B left (filed against
`tasks/study-designer/019`), `spec.md` 1057 B and `open.md` 789 B (both parked behind
`tasks/study-designer/006`, `In flux: yes`).

**A `changelog.d/` fragment is very likely not owed** — nothing shipped and no behaviour changed.
Say so rather than inventing one. **Do not touch hardware.**
