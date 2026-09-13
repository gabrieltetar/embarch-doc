# dev-bench/020 review finding: decision 39 misattributed on DevBenchLogLevel citation

**State:** closed — leg 103, 2026-09-12. Fixed and landed on `main` as `656516b`
("dev-bench/020 fold fix"), ahead of this dispatch reaching a worker — found
the code worktree already clean and `656516b` an ancestor of `origin/main`.
Re-derived both decision 39 bodies to confirm the fix is right
(`embarch-dev-bench/decisions/logging.md` #39 = runtime log-level-from-study,
matching the `DevBenchLogLevel` comment; `embarch-study-designer/decisions/streams.md`
#39 = the `StreamTap` inbound-pipeline unification) and checked the other five
`decision 39` occurrences in `serial_protocol.h` (stream-tag retirement,
`StreamTap` schema-v9, `GattTranscript` encode/split-out comments,
`dbm_encode_transcript_entry` area) — all genuinely about the stream-pipeline
unification and correctly attributed to `embarch-study-designer`. No code or
doc edit needed in this unit.
**Source:** embarch-reviewer, reviewing dev-bench/020 (code merge `adbc380`, doc merge `b1a026b`)
**Scope:** dev-bench
**Hardware:** none — this is a citation-text correctness question, no board involved

## What

`app/src/serial_protocol.h`, the hunk at `@@ -241,8 +240,8 @@` (comment above
`#define DBM_LOG_LEVEL_OFF 0`), rewrites a bare `design.md §3 decision 39` cite
to `` `embarch-study-designer` decision 39 ``. The claim in that comment: that
`DevBenchLogLevel`'s postcard discriminants are deliberately the same numbers
as Zephyr's own log severity levels, so no translation table is needed — dated
"Schema v13, decision 39."

`embarch-study-designer` decision 39 (`decisions/streams.md`) is "One generic
inbound stream pipeline; the write direction explicitly not accepted" — about
unifying power/GATT-transcript/outpost capture into `StreamTap`s. Nothing in
its body is about log-level discriminants or Zephyr severity numbers.

`embarch-dev-bench`'s own decision 39 (`decisions/logging.md`) is "A study
says how loud the bench should be, filtered at runtime rather than compiled
in" — the decision that actually governs `DevBenchLogLevel`/verbosity
crossing on `StudyStart`. That is the on-topic decision for this comment, not
study-designer's stream-pipeline decision of the same number.

Three other citations to `embarch-study-designer` decision 39 in the same file
(the stream-tag retirement at `enum dbm_tag`'s `GattTranscriptRecord`, the
`StreamTap` schema-v9 comment, and the `dbm_encode_frame`/`GattTranscript`
comment) are all genuinely about the stream-pipeline unification and are
correctly attributed. Only the `DevBenchLogLevel` occurrence is off — it reads
as a case of the flagged failure mode: a bare cite matched to the surrounding
paragraph's mention of `embarch-study-designer`'s `DevBenchLogLevel` type
rather than to what decision 39 actually says in either repo, and the two
repos' decision 39s collide by number.

## Why this matters

Not a decision this unit updated — the number was already `39` before the
rewrite (only the `design.md §3` prefix was dropped/replaced). The rewrite
picked the wrong repo for one of five same-numbered occurrences, so the
comment now cites a real, resolvable decision that does not say the thing
attributed to it.

## Undo

Merge SHA `adbc380` (`embarch-dev-bench`). Revert is not clean (48-citation
commit touching many nearby hunks) — simplest fix is a follow-up one-line edit
changing that single occurrence's `` `embarch-study-designer` decision 39 ``
to plain `decision 39` (dev-bench's own, this repo's existing bare-citation
convention), not a revert of the whole unit.

## Dispatch note (leg 103)

Re-derive from the decision bodies in both repos before editing, and check the other four
same-numbered occurrences in that file while you are there — the finding says they are correct,
so confirm rather than assume. No build is possible in a fleet worktree (the Zephyr toolchain
is absent); a comment-only change is fine, but say so in your report rather than claiming a
green build.

**Doc-size reserve for `embarch-dev-bench`:** `open.md` (338 B left), `spec.md` (780 B left) and
`decisions/link.md` (1,047 B left) are all in reserve, with their compaction tasks
(`tasks/dev-bench/012`, `tasks/dev-bench/014`) blocked on `In flux: yes`. Keep your doc edit
small; if you must spend the last of a reserve, compact that file as part of this unit carrying
the parked task's `Must not delete:` list.

## Done when

- [x] The `DevBenchLogLevel`/Zephyr-severity comment in `serial_protocol.h` cites
      dev-bench's own decision 39, not embarch-study-designer's. (Landed as
      `656516b`, already on `main`.)
