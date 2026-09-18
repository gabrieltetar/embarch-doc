# 116 — The `study_results/` size figure is 803 MiB in one place and 809 MiB in two others, and nothing says which

**State:** done 2026-09-17 leg 142 unit 1 — `agent/api/116-study-results-size-figure`
**Doc-size reserve for `api`** (leg 142, before dispatch): `embarch-api/decisions/failure-reporting.md`
710 B left, `embarch-api/spec.md` 1151 B left, `embarch-api/open.md` 665 B left — all three already
filed against a blocked compaction task. **`embarch-api/decisions/target-json.md`, the file this unit
edits, is not in reserve.** If this unit pushes any file into the last 10% of its cap, file
`tasks/api/<NNN>-compact-api.md` in the same commit.
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

- [x] The provenance of **both** figures is established from git history — which commit introduced
      each, citing the SHA, and what each one says it measured. `git log -S '803 MiB'` and
      `git log -S '809 MiB'` over `embarch-doc` is the whole method.

      **809 MiB** — `de07c827` ("The first doctor run against a Core that actually got deployed",
      2026-09-05 20:37:56). Its own prose: *"Check 16's first live reading is 809 MiB across 50
      entries."* This is the number `history/umbrella.md`'s changelog line carries (correctly,
      unchanged since) and the number `embarch-umbrella/decisions/bind.md` decision 22 cites
      (written by `0824325f`, 2026-09-06 01:30:24 — the previous day's reading, before the second
      one below existed).

      **803 MiB** (802.9 MiB precisely) — looked at first glance like a copy of 809 with a digit
      changed (same entry count, one day apart, and the commit that changes it, `fc4f4ac0`
      ["umbrella/027: doctor runs live, and the check waiting for a bench was waiting for a
      timeout", 2026-09-06 18:52:37], says nothing about `study_results/` in its own message). It
      is not a copy: the same commit independently fills in
      `embarch-umbrella/decisions/reporting.md` decisions 37/39 with *"**Verified live** [measured
      2026-09-06, `embarch doctor` and `embarch doctor --json` on the primary `wsl-host` bench]:
      `detail` read `study_results/ at /mnt/c/ProgramData/embarch/study_results: 50 entries, 802.9
      MiB`"* — a literal, dated capture of `doctor`'s own output. That is a second, genuine reading,
      one day after the first, and its precision (802.9, not a round 803) is not something a
      transcription of "809" would produce.
- [x] **Shown to be independent readings**, not a copy. `embarch-api/decisions/target-json.md`
      decision 77 now reads *"study_results/ at 803 MiB [measured 2026-09-06]"* — dated, not
      harmonised. The `embarch-umbrella` side (`bind.md`'s undated 809 MiB, `open.md`'s undated 803
      MiB) is not this worker's file; filed as a full task to
      `/home/gabriel/Github/embarch/embarch-doc/inbox/umbrella-date-the-study-results-size-figures.md`
      with the same provenance so the `umbrella` worker does not have to redo the archaeology.
- [x] (Not reached — history settled it; see above.)
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] No `changelog.d/` fragment — no reader-facing number changed, only a measurement date was
      added to an existing figure.
