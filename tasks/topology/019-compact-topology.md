# 019 — `decisions/enrollment.md` is in reserve

**State:** claimed — leg 064

*Dispatch note, leg 064: `In flux: no` for the single file on the `Compacts:` line, so this is an
ordinary compaction unit. **Read `DOC-BUDGET.md`'s split-first rule before compacting anything** —
a verbatim split restates nothing and is the cheaper move where the file turns out to be many
decisions rather than one sprawling one (`check-doc-size.py --decisions` answers which). Answer
`DOC-COMPACTION-PASS.md`'s human question in your report, in your own words: can
`embarch-topology/spec.md` alone answer what someone needs to work on enrollment today? Other
`topology` reserve: nothing else is filed against this scope beyond `tasks/topology/014`/`017`
(`open.md`, `spec.md`, `decisions/validation.md`) — leave those files alone.*
**Source:** `scripts/check-doc-size.py`'s reserve floor, hit by `tasks/topology/004`'s decision 27, 2026-09-07
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/decisions/enrollment.md
**Size debt due:** 2026-10-14

## What

`tasks/topology/004` (`NotFound` naming the excluding rule, plus the link-serial/
interface clearing affordance) added decision 27 to `decisions/enrollment.md`,
pushing it to **11,346 / 12,288 B (92.3%), 942 B left**. No debt was filed
against this file before this edit — `tasks/topology/014`/`017` cover `open.md`,
`spec.md` and `decisions/validation.md` only.

## Why now

The debt is real once a file is within one amendment of its cap, and recording
it is the whole mechanism (`tasks/topology/014`'s own wording, same rule).

## In flux: no

Decisions 14–16/20/27 in this file are each closed, landed units; nothing
queued against `embarch-topology` as of 2026-09-07 touches this file further.

## Done when

- [ ] `decisions/enrollment.md` is out of reserve, or the task says why it
      cannot be and what was deleted instead.
- [ ] Prefer a split per [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 if a
      seam exists (e.g. decision 20's role-uniqueness half vs. its
      link-interface half, or splitting 27 out once a further enrollment
      decision would otherwise land here too) before deleting live reasoning.
- [ ] Whichever it was — split or delete — is stated, with the byte numbers
      before and after.
