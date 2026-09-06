# 014 — `embarch-core/decisions/studies.md` crossed into reserve

**State:** open
**Source:** `core/012` spent this file's headroom adding decision 43; `DOC-COMPACTION.md` §2
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/decisions/studies.md
**In flux:** **No.** Every decision in this file describes a path that is
shipped, deployed and has been exercised against the live bench — the study
loop, the version gate and the handshake. Nothing here is a design mid-rewrite.

**One caveat that is not a reason to park.** Decision 43's *Declined* paragraph
rests on a fact about another repo — that `embarch-ui` renders `current_step + 1`
— and an `inbox/` drop was filed asking `embarch-ui`'s owner to fix the
resulting mid-run off-by-one. If that lands, the sentence becomes historical, but the
decision it supports does not change: Core's numbering stays either way. Do not
delete the clause on the grounds that it is now out of date; date it.

**Must not delete:**
- Decision 40's **"the resilience fix is what found the cause of the fault it
  was written to tolerate"** account, and specifically **the occurrence counts
  13/15/17/17/13/17**. Those are measurements, and the paragraph's whole point
  is that they distinguish a crash with variable timing from a buffer boundary.
  A shortened version that keeps the conclusion without the numbers asserts a
  diagnosis this suite paid for three times to get right.
- The same entry's note that **the wrong number had become the name of a bug**.
  It is the only record that two well-evidenced host-side readings were wrong,
  which is the reason the entry is long.
- Decision 33's **"`timeout_ms` means 'how long this step may take', never 'how
  long until I hear back'"** sentence, and its *Declined* case for not moving
  the sleep host-side. Cut, the decision reads as arbitrary and someone folds
  `delay_before_ms` back out of the deadline.
- Decision 43's **"neither is wrong for its own job; sharing a name is"**, and
  the observed value `current_step: 1, total_steps: 2`. Without the observation
  the entry reads as a style preference and the next reader renumbers the field.
- Decision 31's distinction between what Core **verifies** and what it merely
  **records** — `Declared` versus verified provenance. `embarch-ui` renders that
  distinction on decision 11's orders, so flattening it here licenses flattening
  it there.

## What

`decisions/studies.md` is **11,176 B against a 12,288 B cap**; the reserve line
is 11,059. It was 8,998 B before `core/012`, so decision 43's 2.2 KB is what
crossed it — the file had 2,061 B of clearance and one entry with a live
observation, a rejected alternative and a cross-repo consequence spent it.

The cheapest real reduction is **decision 40**, at roughly a third of the file
and written as narrative because the narrative was the finding at the time. It
can become a statement plus its evidence without losing either. A **mission
split** is the other move `tasks/README.md` names and is probably better here:
this file already holds three unrelated missions — the study loop, the version
gate, and handshake identity — and the last two are one entry each.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it, and the
commit that spends the reserve is the one that files it (`DOC-COMPACTION.md`
§2). This task is that filing. Nothing else in `embarch-core` is in reserve.

## Done when

- [ ] `decisions/studies.md` is clear of its reserve line (under 11,059 B), by
      shortening or by a mission split.
- [ ] If it splits, `decisions.md`'s index table gains the new row and every
      number still resolves — `scripts/check-decision-refs.py` is the check.
- [ ] Every `Must not delete:` item above is still readable.
- [ ] Decision 40's occurrence counts are byte-for-byte unchanged or omitted
      entirely, never paraphrased.
- [ ] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words: *what does someone starting on `embarch-core`'s
      study path tomorrow lose if this paragraph is gone?*
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
