# 027 — `embarch-topology/open.md` files a live question against `tasks/topology/020`, which is done

**State:** done — leg 078, 2026-09-10
**Reserve for this scope:** `embarch-topology/spec.md` is 9,195/10,240 B (1,045 B left, 89.8%) and
its compaction task `topology/024` is `blocked`. `open.md` — the file this unit writes — is not in
reserve. Stay out of `spec.md` unless the task needs it.
**Source:** leg 076's refill sweep. `embarch-topology/open.md:17` ends its bullet with
`` (`tasks/topology/020`) ``; `tasks/topology/020-crate-md-decisions-4-and-8-claim-a-uniqueness-the-crate-cannot-enforce.md`
reads `**State:** done — leg 050, 2026-09-08`.
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

An `open.md` bullet points at a task as the place its question is being handled, and that task
landed two days ago. Either the bullet is stale in full — 020 answered it and it should be struck —
or 020 answered part of it and what remains needs restating in its own words, without the pointer.

**Read `tasks/topology/020` and the commit that closed it before deciding which**, and say in the
bullet what is actually still open now. Do not simply delete the pointer and leave the rest of the
sentence standing: a bullet whose "and this is being handled at X" clause is removed reads as a
question nobody is looking at, which may or may not be true.

## Why now

A pointer to a completed task is the cheapest possible way for an open question to become invisible:
whoever reads the bullet follows the pointer, sees `done`, and concludes the question is closed.
Nothing checks this — `check-links.py` resolves the path (the file still exists until its fold
removes it) and no gate compares a cited task's `State:` against the citing text. `embarch-topology`
also has zero open tasks right now, so a worker dispatched to this scope has nothing else to take.

## Done when

- [x] `embarch-topology/open.md:17`'s bullet either states what remains open in its own words with
      no task pointer, or is deleted with the `changelog.d` fragment saying 020 closed it.
- [x] `grep -rn 'tasks/topology/020' ` across the corpus returns no citation that reads as live debt.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.

## Resolution

The bullet's content (no cheap detector for a caller-side second predicate) is itself what
`020` produced as its answer — it is a standing, permanent limitation, not a pointer to future
work. Removed the `(tasks/topology/020)` citation and replaced it with a plain statement that
both known instances (`api/038`, `umbrella/036`) are already closed and nothing further is
pending. The remaining corpus citations of `tasks/topology/020` (`crate.md`, `embarch-api`'s
`core-link.md`, task `024`) are provenance for a decision already made, not live-debt pointers,
so they were left alone. Nothing suite-level changed — no `status.d/` fragment filed.
