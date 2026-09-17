# 057 — `spec.md` is in reserve

**State:** open
**Source:** `scripts/check-doc-size.py`'s reserve floor, hit by `tasks/topology/055`'s three
correctness fixes (identity-gate equality shortcut, role-uniqueness cardinality, the alert log
read-back caveat), 2026-09-17
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/spec.md
**Size debt due:** 2026-10-17

## What

`tasks/topology/055` corrected three `spec.md` sentences that overstated guarantees the code does
not provide (identity-gate `Undeclared` framing, "a role is unique," and "the only state that
persists"). Each correction is a genuine addition — a qualifier or caveat the original sentence was
missing — not padding, and together they pushed `spec.md` from 9,001/10,240 B (87.9%) to
**9,826/10,240 B (96.0%), 414 B left**. No debt was filed against `spec.md` before this edit;
`tasks/topology/014`/`017` cover `open.md` and `decisions/validation.md` respectively, not this file.

## Why now

The debt is real once a file is within the last 10% of its cap, and recording it is the whole
mechanism (`tasks/topology/014`'s own wording, same rule).

## In flux: yes

`tasks/topology/056` (the probe-open failure raising neither a `TopologyMismatch` nor an
`alerts.jsonl` row) is still open against this same crate's validation surface and may touch
`spec.md`'s "What validation asserts, and what it cannot" section — the same section `055` just
edited. Set `**State:** blocked`.

**State:** blocked — unparks when `tasks/topology/056` lands (or is filed away without touching
`spec.md`), whichever comes first.

## Done when

- [ ] `spec.md` is out of reserve, or the task says why it cannot be and what was deleted instead.
- [ ] Prefer a split per [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 if a seam exists (the
      "Shape" / "Storage and roles" / "What validation asserts" sections are already distinct
      missions) before deleting live reasoning.
- [ ] Whichever it was — split or delete — is stated, with the byte numbers before and after.

## Must not delete

- The three `055` corrections themselves: the identity-gate equality-shortcut clause, the
  role-uniqueness write-time-vs-store-invariant clause plus its "first row only" caveat, and the
  alert-log read-back qualifier. These are the fixes this debt exists to preserve room for, not
  candidates for the cut.
- Decision 20/21/27's cross-references in "Storage and roles" and "What validation asserts" — each
  is the only place `spec.md` sends a reader to the decision with the actual reasoning; deleting the
  citation without deleting the claim it backs turns a sourced statement into an unsourced one.
