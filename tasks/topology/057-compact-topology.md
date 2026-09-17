# 057 — `spec.md` is in reserve

**State:** open — **unparked by leg 136, 2026-09-17, because this task's own condition was met and
nothing had acted on it.** It read *"unparks when `tasks/topology/056` lands, or is closed without
touching `spec.md`, whichever comes first"*; `topology/056` landed on 2026-09-17 (doc `b3c5827`,
fold `3d384c2`), and then `topology/058` — the follow-up 056 reserved the behaviour decision for —
landed too (code `b96f758`, doc `c34532e`) **without touching `spec.md` at all**, by its dispatch
note's instruction. So both halves of the condition are satisfied, not just one. The `058` worker
saw this and correctly declined to unpark a task it was told to leave alone; doing it is the
supervisor's job and this is it. **Filed by `topology/055` with two contradictory `**State:**`
lines — `open` here and `blocked` further down; leg 133 resolved that to the `blocked` the body
argues for.**
**Source:** `scripts/check-doc-size.py`'s reserve floor, hit by `tasks/topology/055`'s three
correctness fixes (identity-gate equality shortcut, role-uniqueness cardinality, the alert log
read-back caveat), 2026-09-17
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/spec.md
**In flux:** no — the sole file on the `Compacts:` line is settled (per-file answer, and here there
is only one file). The `yes` this line used to carry rested entirely on *"`tasks/topology/056` is
open against the same 'What validation asserts, and what it cannot' section `055` just edited"* —
`056` is done, and `058`, the behaviour decision `056` deferred, is done as well and deliberately
wrote nothing into `spec.md`. **Nothing is queued against that section any more**, so the reason for
the park is gone rather than merely stale. `spec.md` is at 9,826/10,240 B — **414 B left, the
tightest reserve in the suite** — so this is now the most urgent compaction debt on the board even
though its date is far out.
**Size debt due:** 2026-10-17
**Must not delete:** the three qualifiers `055` just added, because each one exists to stop a
reader relying on a guarantee the code does not provide — that `compare_self_reported` matches on
**case-insensitive string equality for any chip** before it ever reaches a declared relation, so
`Undeclared` is not the only non-match outcome; that role uniqueness is a **write-time rule in
`upsert_at`, not a store invariant**, and that the displaced-row guarantee covers only the *first*
duplicate (`find` returns one, `retain` deletes all); and that `alerts.jsonl` **is** persisted and
is merely never read back as an input. Shortening any of these into the original flat claim
re-introduces the defect `055` was filed to fix.

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

## In flux

**Yes** — recorded as the `**In flux:**` field above, and this section is the reasoning behind it.
`tasks/topology/056` (the probe-open failure raising neither a `TopologyMismatch` nor an
`alerts.jsonl` row) is still open against this same crate's validation surface and may touch
`spec.md`'s "What validation asserts, and what it cannot" section — the same section `055` just
edited. That is what holds this task `blocked`, and it is a dated park, not an absorbing one: the
`**Size debt due:**` above is what makes a leg spend its first unit here whether or not it is
blocked.

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
