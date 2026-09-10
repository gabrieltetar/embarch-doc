# 019 — `decisions/enrollment.md` is in reserve

**State:** done — leg 064

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

- [x] `decisions/enrollment.md` is out of reserve, or the task says why it
      cannot be and what was deleted instead.
- [x] Prefer a split per [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 if a
      seam exists (e.g. decision 20's role-uniqueness half vs. its
      link-interface half, or splitting 27 out once a further enrollment
      decision would otherwise land here too) before deleting live reasoning.
- [x] Whichever it was — split or delete — is stated, with the byte numbers
      before and after.

## Resolution

Verbatim split, no reasoning cut. The seam was already visible in decision
20's own text ("Two independent gaps") and decision 27's fix for the same
failure mode: 14/15/16 are the human-interaction/disambiguation surface;
20/27 are what a *role* carries across an enrollment change (declared link
serial/interface) and how `NotFound` reports which fact excluded every
candidate — closer in mission to `links.md` than to enrollment's human
surface, but too big to merge into `links.md` (10,941 B) without pushing it
over cap. Moved 20/27 to a new `decisions/link-declares.md`, updated
`decisions.md`'s routing table (`check-decision-refs.py`'s topic-link check
depends on this), and re-pointed no other files — nothing else outside
`decisions.md` linked `enrollment.md` for #20/#27 specifically.

Before: `decisions/enrollment.md` 11,346 B (92.3%, 942 B left).
After: `decisions/enrollment.md` 4,034 B; `decisions/link-declares.md` 8,157 B
(new file, own headroom). `scripts/check-doc-size.py`, `check-decision-refs.py`
and the full `check-docs.py` gate all pass.

**Human question (`DOC-COMPACTION-PASS.md`):** can `embarch-topology/spec.md`
alone answer what someone needs to work on enrollment today? Yes for the
mechanics — `spec.md` already states the current enrollment surface, fields
and CLI/HTTP shape, which is what a change actually touches. No for the two
things a compaction pass cannot put there without turning `spec.md` into
`decisions.md`: *why* a role displaces rather than merges on upsert (decision
20's inherited-stale-link-serial trap), and *why* `NotFound`'s message can't
just call `embarch-topology status` inline (the `hardware`/`software`
feature-split reasoning in decision 27). Someone extending this code without
reading `link-declares.md` first will very plausibly re-introduce one of
those two exact bugs — that is what the split was for, not to make
`decisions.md` skippable.
