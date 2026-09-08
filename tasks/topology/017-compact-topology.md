# 017 — `spec.md` and `decisions/validation.md` are in reserve

**State:** open
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

## In flux: yes

`tasks/topology/013` is open against `decisions.md`'s own index and this
sub-project's validation group specifically (decision 23's ACL question), and
`009` just added decision 26 to the same `validation.md` file this task
targets. Whoever compacts should read both before cutting, in case 013 lands
first and adds more to the same file.

## Done when

- [ ] `spec.md` is out of reserve, or the task says why it cannot be and what
      was deleted instead.
- [ ] `decisions/validation.md` is out of reserve, same terms — prefer a split
      per [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 if a seam exists
      (e.g. splitting the Nordic-identity decisions 21/25 from the
      timestamp decision 26 into their own file).
- [ ] Whichever it was for each file — split or delete — is stated, with the
      byte numbers before and after.
