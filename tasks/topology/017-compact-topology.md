# 017 — `spec.md` and `decisions/validation.md` are in reserve

**State:** claimed by agent/topology/017-compact-topology, 2026-09-08 23:07
**Source:** `scripts/check-doc-size.py`'s reserve floor, hit by `tasks/topology/009`'s edits, 2026-09-07
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/spec.md, embarch-topology/decisions/validation.md
**Size debt due:** 2026-10-08

## What

`tasks/topology/009` (the additive `validate` timestamp) pushed two files into
reserve at once: `spec.md` is **9,602/10,240 B (93.8%), 638 B left**;
`decisions/validation.md` is **11,178/12,288 B (91.0%), 1,110 B left**. Neither
had a debt filed before this edit — `tasks/topology/014` covers `open.md` only.

## Why now

The debt is real once a file is within one amendment of its cap, and recording
it is the whole mechanism (`tasks/topology/014`'s own wording, same rule).

## In flux: no

**Corrected by the supervisor at `009`'s fold, leg 041, 2026-09-07.** The filer
wrote `yes` on two grounds and both had already expired when it wrote them:

- It said `tasks/topology/013` is *open* against `decisions.md`'s index and this
  sub-project's validation group. **`013` is `done`** — it landed in leg 035
  earlier today, on branch `agent/topology/013-decision-23-acl-rationale`. The
  filer was reading a task file it had not opened.
- It said `009` "just added decision 26 to the same `validation.md`". `009` is
  the unit that filed this task, and it has now landed. Its own edit is not
  future flux.

Nothing else is queued against `embarch-topology/spec.md` or
`decisions/validation.md`. Whoever compacts should still read decisions 20, 21,
25 and 26 as a group — they are four passes over the same chip-identity and
validate surface within two days, which is where a compaction most easily drops
a fact — but that is care, not flux.

**Left `open` rather than `blocked`** on purpose: a `blocked` compaction task is
the state nothing revisits, and `check-doc-size.py --pressure` calls that out as
its own problem. This one is dispatchable.

## Done when

- [ ] `spec.md` is out of reserve, or the task says why it cannot be and what
      was deleted instead.
- [ ] `decisions/validation.md` is out of reserve, same terms — prefer a split
      per [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 if a seam exists
      (e.g. splitting the Nordic-identity decisions 21/25 from the
      timestamp decision 26 into their own file).
- [ ] Whichever it was for each file — split or delete — is stated, with the
      byte numbers before and after.
