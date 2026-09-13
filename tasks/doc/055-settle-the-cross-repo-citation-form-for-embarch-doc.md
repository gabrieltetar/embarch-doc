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

## Done when

- [ ] `DOC-CONVENTIONS.md` states which relative form is canonical for a sibling-repo source
      comment citing `embarch-doc`, and why (auditability of depth vs. resistance to depth drift).
- [ ] Existing sites in the non-canonical form are either left as a documented exception or queued
      as their own per-sub-project follow-ups — this decision must not itself become a suite-wide
      rewrite task.
