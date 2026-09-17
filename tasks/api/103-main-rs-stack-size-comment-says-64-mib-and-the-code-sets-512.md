# 103 — `main.rs`'s stack-size comment says 64 MiB and the code sets 512

**State:** open
**Source:** `api/102`'s worker, 2026-09-16, which found it while sweeping `src/main.rs` for citations
and correctly left it alone — it is not a decision citation, and a citation sweep that starts fixing
every wrong number it walks past is a sweep with no boundary.
**Scope:** api
**Hardware:** none — one comment, or one constant. Nothing is built for a board, no probe, no live
Core, no study.
**Owner:** no

**Doc-size reserve for `api`:** one file, `embarch-api/spec.md` at **9,102/10,240 B (1,138 B left)**,
filed as `tasks/api/083` and **blocked**. Nothing else in scope is in reserve.

## What

`src/main.rs`'s `async_main` comment says its stack-size fix uses **64 MiB**. The code sets
`512 * 1024 * 1024` — **512 MiB** — in **both** places: the spawned thread and the tokio runtime.
`src/study.rs` carries a comment about the same underlying bug and says **16 MiB**, which does match
its own `16 * 1024 * 1024`.

So one of three things is true, and **which one it is decides what the fix is**:

1. The comment is stale and 512 MiB is deliberate — then the comment changes and should say why the
   number grew.
2. The comment is right and 512 MiB is a slip — then the **code** changes, and this stops being a
   comment fix.
3. `main.rs` and `study.rs` want different numbers for good reason — then say so in one of them,
   because 64/512/16 across two files reads as drift whatever the truth is.

**Find out which before editing anything.** `git log -S'512 * 1024 * 1024' -- src/main.rs` and the
same for the comment text should show whether the two ever agreed, and `git log -S'16 * 1024 * 1024'
-- src/study.rs` gives the other half. If the history shows the constant was raised and the comment
was not, (1) is settled and the fix is one line.

**If the answer is (2)**, stop and say so rather than changing the constant: a stack size that was
raised to 512 MiB for a reason nobody wrote down is not a number to lower on a comment's word, and
that version of this task wants the owner.

## Why it is worth a unit at all

It is small, and it is the kind of small that costs an hour later. A reader debugging a stack
overflow in `embarch-api` reads the comment, believes 64 MiB, and goes looking for the wrong thing —
and the two files disagreeing by 32× makes it look as though there are two different limits in play
when there may be one. The whole citation-sweep chain exists on the argument that a comment nothing
verifies drifts; this is the same defect with no decision number attached, which is why nothing in
the chain's method would ever have caught it.

## Done when

- [ ] Which of the three cases it is, established from history rather than assumed, and said
      explicitly in the report.
- [ ] The resulting one-line fix made — or, for case (2), the task left `open` with what was found
      and why it is the owner's.
- [ ] `study.rs`'s 16 MiB checked against its own constant at the same time, so the pair is
      consistent afterwards.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/api-*` fragment.

## Not yours

`history/api.md` is assembled from fragments.
