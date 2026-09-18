# 116 — The `study_results/` size figure is 803 MiB in one place and 809 MiB in two others, and nothing says which

**State:** open
**Source:** `embarch-reviewer` on landed unit `umbrella/082` (`embarch-doc@f61b43ff`), leg 141,
2026-09-17. **The reviewer deliberately did not file this as a finding** — it is pre-existing,
`umbrella/082` neither introduced nor touched it, and flagging it as a fault in that diff would have
been wrong. It ruled it out of scope and named it, which is the right call and the reason it is here
rather than only in a review transcript.
**Scope:** api
**Hardware:** none — three numbers in three markdown files, and a decision about how to label them.
**Do not run `du` against the real `study_results/` to settle it**: a fourth reading taken today
answers a different question than either of the two on record and would make this worse, not better.
**Owner:** no

## What

The same measurement — the size of the deployed machine's `study_results/` directory, **50 entries**
in every statement of it — appears with two different byte counts:

- **803 MiB**, in `embarch-api/decisions/target-json.md` decision 77, written 2026-09-17 by
  `tasks/api/109`.
- **809 MiB**, in `embarch-doc/history/umbrella.md` and in
  `embarch-doc/embarch-umbrella/decisions/bind.md`.

The `embarch-umbrella/open.md` bullet that also carried **803 MiB [measured 2026-09-06]** was
rewritten by `umbrella/082` and no longer carries the figure at all, so the surviving statements are
the three above.

**Two readings of the same directory days apart is the innocent explanation and is probably the
right one** — `study_results/` grows as studies run, and 6 MiB across 50 entries is an ordinary
week. **One transcription error propagated is the other**, and it is not excluded: the entry count
is identical in every statement, which is what you would expect from a copy and *not* what you would
expect from two independent `du` runs a week apart.

Neither is established. What is certain is that **no statement of the figure says when it was
taken**, except `umbrella/open.md`'s now-deleted one, which is the only one that did.

## Why now

Cheap, and it is a claim about evidence rather than a claim about the system — the class this suite
treats as load-bearing, and the same class `tasks/umbrella/083` is open for. It is also the kind of
thing that gets more expensive the longer it sits: each figure is now cited by something, and a
later reader reconciling them has strictly less to work with than a reader today, who can still
reach the commits that introduced both.

**It is filed under `api` because decision 77 is `api`'s** and is both the newest statement and the
one with the minority number. If settling it turns out to require editing the `umbrella`-side
figures, **that half is not this worker's** — `embarch-umbrella/` is another sub-project's row
(`protocol.md` §3) — and it goes to `inbox/` as a task for `umbrella`, with whatever this unit
established.

## Done when

- [ ] The provenance of **both** figures is established from git history — which commit introduced
      each, citing the SHA, and what each one says it measured. `git log -S '803 MiB'` and
      `git log -S '809 MiB'` over `embarch-doc` is the whole method.
- [ ] Either the two are shown to be **independent readings**, in which case **each surviving
      statement gains its measurement date** and nothing is harmonised — two dated readings of a
      growing directory is correct data and the fix is labelling, not agreement; or one is shown to
      be a **copy of the other with a digit changed**, in which case the wrong one is corrected in
      the file this worker owns and the rest goes to `inbox/`.
- [ ] If the history cannot settle it — both introduced in commits whose messages say nothing —
      **say so and stop.** Do not pick the more plausible one. Mark the `api` statement as
      *"[measured <date>; an independent 809 MiB reading exists in `embarch-umbrella`, provenance
      unresolved]"* and file the `umbrella` half to `inbox/` so the same marker can go there. An
      honest unresolved pointer is worth more than a harmonised number nobody can defend.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment only if a reader-facing number changed.
