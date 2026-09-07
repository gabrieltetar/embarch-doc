# 014 — `embarch-core/decisions/studies.md` crossed into reserve

**State:** done, 2026-09-06
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

## Reserve line (supervisor, leg 024, measured at dispatch)

`check-doc-size.py --pressure` right now, for `embarch-core` only:

- `embarch-core/decisions/studies.md` — 11,176 / 12,288, **1,112 bytes left**, reserve line 11,059.
  This task is its filing; clearing it is the unit.

**Nothing else in `embarch-core` is in reserve** — `spec.md`, `open.md`, `interfaces.md` and the
other `decisions/` files all have room. If your work pushes one of them into reserve, or leaves one
there that nothing has filed, file `tasks/core/<NNN>-compact-core.md` in the **same commit**
(`tasks/README.md` has the shape). The path is `tasks/core/`, your own scope — not `tasks/doc/`,
which `check-ownership.py` refuses to a worker.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it, and the
commit that spends the reserve is the one that files it (`DOC-COMPACTION.md`
§2). This task is that filing. Nothing else in `embarch-core` is in reserve.

## Done when

- [x] `decisions/studies.md` is clear of its reserve line (under 11,059 B), by
      shortening or by a mission split.
- [x] If it splits, `decisions.md`'s index table gains the new row and every
      number still resolves — `scripts/check-decision-refs.py` is the check.
- [x] Every `Must not delete:` item above is still readable.
- [x] Decision 40's occurrence counts are byte-for-byte unchanged or omitted
      entirely, never paraphrased.
- [x] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words: *what does someone starting on `embarch-core`'s
      study path tomorrow lose if this paragraph is gone?*
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## What shipped

A **mission split**, not prose surgery. `decisions/studies.md` held three
missions; the two that are one entry each — the version gate (31) and handshake
identity (35) — moved **verbatim** into a new `embarch-core/decisions/handshake.md`,
whose mission is what Core establishes about a bench *before* any step runs.
`decisions.md` gained the row, and its stale size column was corrected on every
row (`platform.md` was listed at 5.8 KB against a real 8.2 KB).

- `decisions/studies.md` — 11,176 → **8,318 B** (cap 12,288, reserve line 11,059).
- `decisions/handshake.md` — new, **3,730 B**.
- `decisions.md` — 1,618 → 1,704 B.

`check-doc-size.py --pressure` now reports `embarch-core/decisions/studies.md`
**PAID at 67.7%**, and nothing in `embarch-core` is in reserve.

**Nothing in a decision entry was deleted.** A diff of the pre-image against the
two files concatenated shows exactly three changes: `studies.md`'s own summary
line, the new file's header, and the dated bracket on decision 43 below. Decision
40's occurrence counts are byte-for-byte untouched, as is the note that the wrong
number had become the name of a bug; decision 33's `timeout_ms` sentence and its
*Declined* case, decision 43's "neither is wrong for its own job" and its observed
`current_step: 1, total_steps: 2`, and decision 31's verified-versus-`Declared`
distinction are all where they were.

Decision 43's cross-repo fact is **dated, not deleted**: `embarch-ui` renders
`current_step + 1` is now marked `[embarch-ui, 2026-09-06; a badge fix is filed in
that repo, and when it lands this sentence and the *Declined* clause's "for free"
become historical — Core's numbering does not change]`.

**Why no prose was cut.** The second-pass test is "would someone about to change
this code make a wrong move without it". Every long paragraph left in `studies.md`
answers yes: 40's silence-then-reset account is the only thing that stops the next
reader re-diagnosing a truncation as a framing bug; 43's two-counters observation
is the only thing that stops them renumbering the public field; 33's *Declined*
case is the only thing that stops `delay_before_ms` being folded back out of the
deadline. The one genuinely cold item — the study id `3785bd198cc3a62d…` — is
30 bytes and, per decision 19/20 in this same file, unfollowable anyway once the
service restarts. `DOC-COMPACTION-PASS.md` says not to run the density pass twice;
this file had had one, and the remaining bytes are rules.

No code change: this unit is docs only, so `agent/core/014-compact-core` in
`embarch-core` ends with no commit.
