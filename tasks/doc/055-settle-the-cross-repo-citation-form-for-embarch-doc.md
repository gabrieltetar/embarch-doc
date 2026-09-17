# 055 — Settle which relative form a sibling repo's source comment uses to cite embarch-doc

**State:** open
**Source:** `inbox/doc-settle-cross-repo-citation-form.md`, dropped by `tasks/umbrella/062`'s
worker (four more shallow `../embarch-doc` sites), which itself followed `tasks/umbrella/061`.
Both units found the depth defect and were explicitly told not to touch citation *form*; this is
that deferred call. Filed by the leg of 2026-09-13 17:0x.
**Scope:** doc
**Hardware:** none — prose/convention decision only.
**Owner:** required — the answer belongs in `DOC-CONVENTIONS.md`, which
`check-ownership.py --supervisor` classifies as reserved to the owner.

## What

The suite has at least two conventions for citing an `embarch-doc` file from a sibling repo's
source comment, and `DOC-CONVENTIONS.md` settles neither:

1. **Relative-from-file, depth-correct** — `../../embarch-doc/embarch-core/spec.md`. Used by
   `embarch-umbrella/src/setup.rs`, `main.rs`, `config.rs`, `doctor.rs` after `061`/`062`. This is
   the form that keeps getting the depth wrong: two units in a row found sites collapsed to
   `../embarch-doc/...`, one level too shallow, apparently by copying a wrong site as precedent.
2. **Suite-root-relative, no `../`** — `embarch-doc/embarch-umbrella/spec.md`. Used by
   `embarch-umbrella/src/main.rs:3` and `:127`, and reportedly by `embarch-core`'s own comments.
   It cannot have a depth bug because it encodes no depth — but it is not a valid relative path
   from any file, so an editor's follow-link does not resolve it.

A third form (plain GitHub URLs, e.g. `embarch-umbrella/src/deploy.rs`) is out of scope: it is not
a relative path and does not share the defect.

## Why now

Two consecutive units in the same repo hit the same defect family, and nothing stops the next
writer reaching for form 1 and getting the depth wrong again. A form already immune to the bug
exists in the suite but is not documented as the answer.

## A fourth defect family, added by leg 122 (2026-09-16): the `:line` suffix

`topology/046` found a cross-repo citation that was **wrong the day it was written**:
`bin/main.rs` cited `embarch-core/decisions/surfaces.md:17` for a claim whose text had moved to
`embarch-core/decisions/enrollment.md:10` when that file split out two days earlier. The repo,
the path *and* the relative depth were all fine. **The line number was the defect.**

That is a different failure from the three above and it is worse in one specific way: a wrong
depth breaks a follow-link visibly, while a wrong line number lands the reader on a real
sentence about something else. `topology/046`'s reviewer confirmed both surviving line-anchored
citations resolve correctly *today* — which is exactly the property that expires without notice
the next time either target file is edited.

Nothing can check this: `check-decision-refs.py` resolves decision *numbers*, walks `*.md` only,
and never leaves the doc repo, so a `file:line` citation in another repo's source is invisible to
every gate the suite has.

**So this task should settle whether a `:line` suffix is allowed at all in a cross-repo citation**,
alongside the relative-form question. The obvious alternative — cite the decision number, or the
section heading, and let the reader search — is stable under edits by construction. Note that the
same `topology/046` comment also cites `embarch-core/decisions/enrollment.md:10`, which sits inside
a **retired** decision whose body explicitly says the fact outlived it; the reviewer judged that
acceptable and had no better anchor to propose. If line anchors go away, that case needs an answer.

## Done when

- [ ] `DOC-CONVENTIONS.md` states which relative form is canonical for a sibling-repo source
      comment citing `embarch-doc`, and why (auditability of depth vs. resistance to depth drift).
- [ ] It also says whether a `:line` suffix is permitted in such a citation, given that nothing
      checks one and that a stale one reads as a real citation of the wrong sentence.
- [ ] Existing sites in the non-canonical form are either left as a documented exception or queued
      as their own per-sub-project follow-ups — this decision must not itself become a suite-wide
      rewrite task.
