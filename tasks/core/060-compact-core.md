# 060 — Compact `embarch-core/decisions/streams.md` out of reserve

**State:** done — `agent/core/060-compact-core`, leg 116, 2026-09-16
**Source:** `suite/029` (leg 113, 2026-09-13). That unit added **decision 63** to this file and took it
from 9,356 B to **11,219 B**, which is 160 B inside the reserve floor. The supervisor trimmed the new
decision twice — 11,462 → 11,219 — and stopped, because the next cut came out of the clause naming why
the two alternative shapes were not taken, which is the one thing `suite/029` required the decision to
carry.
**Scope:** core
**Hardware:** none — doc prose only. No board, no probe, no live Core, no deploy.
**Owner:** no
**Compacts:** `embarch-core/decisions/streams.md`
**In flux:** no — decisions 30, 38 and 39 have been settled for weeks. **Decision 62 and decision 63
are both recent and both still live**, but neither is being rewritten: 62's own follow-up
(`embarch-ui/src/trace.rs`'s remaining duplication) changes `embarch-ui`, not this file, and 63's
implementation task (`tasks/core/061`) will *add* to its entry's accuracy rather than restate it. See
*Watch for* — this is the field answered per file, and the file is the whole task.
**Size debt due:** 2026-09-27

## What

`embarch-core/decisions/streams.md` is **11,219 / 12,288 B**, reserve floor **11,059 B**. Get it to
**11,000 B or less** — about 220 B, which is one paragraph, not one sentence.

**Read `DOC-BUDGET.md`'s split-first rule before compacting.** This file now holds **five** decisions
(30, 38, 39, 62, 63) across two visibly different subjects: manifest binding and rendering (30, 38, 39)
versus what the **stream index** reports about a tap (62, 63). A verbatim split restates nothing and is
the cheaper move if that seam is real. `scripts/check-doc-size.py --decisions` will tell you whether
this is many decisions or one sprawling one.

**If you split**, note that `tasks/doc/052` records that a verbatim split silently drops the
per-decision size pin of every decision it moves, and `tasks/doc/044` that a verbatim split is the one
move `check-decision-refs.py` cannot see. Both are owner-reserved and neither is fixed; check the pins
and the refs by hand afterwards and say in your report that you did.

## Watch for

- **Update `embarch-core/decisions.md`'s index table** — both the number list and the size column — in
  the same commit. Leg 113 set the streams row to `30, 38, 39, 62, 63 | 11.0 KB`; a split makes that
  row two rows.
- **Do not shorten decision 63's second paragraph.** `suite/029`'s `Done when` required the chosen
  shape to name why the other two were not taken, and that paragraph is the whole of it. If bytes have
  to come from 63, take them from its first or last paragraph.
- **Decision 62 quotes `embarch-ui` decision 10's column pin and cites reversals row 86.** Those are
  load-bearing citations, not decoration — `topology/043` is the cautionary case where a compaction
  target was arithmetically wrong and the sweep still had to be redone.

## Done when

- [x] `embarch-core/decisions/streams.md` is at or under 11,000 B, or split with each half under its
      own cap. **Split**, not squeezed: `decisions/streams.md` kept 30/38/39 (6,376 B / 6.2 KB) and
      `decisions/stream-index.md` took 62/63 verbatim (5,672 B / 5.5 KB). The seam the task file
      flagged was real — manifest binding/capture/rendering versus what the stream index reports back
      about a tap to a caller — and a verbatim move restates nothing, so nothing was shortened.
- [x] `embarch-core/decisions.md`'s index table matches, numbers and sizes. The streams row is now two
      rows: `30, 38, 39 | 6.2 KB` and `62, 63 | 5.5 KB` (`decisions/stream-index.md`).
- [x] `DOC-COMPACTION-PASS.md`'s question answered in the supervisor's log entry, in the runner's own
      words: can `spec.md` alone answer what someone needs to work on this component today? **No, and
      that is by design here.** `embarch-core/spec.md` states the current shape of the streams surface
      (what `streams/` holds, what a manifest mismatch does, what the stream index reports), but it
      does not carry the *why* — why a mismatch renders nothing instead of the nearest manifest, why
      the load route is a sibling path instead of a query flag, why the deferred-tap flag is a fourth
      boolean instead of a third meaning for `note`. Those arguments live only in `decisions/streams.md`
      and the new `decisions/stream-index.md`, and this split was designed so a reader working on
      either half — capture/manifest/render vs. what the index tells a caller — loads a smaller, more
      on-topic file than before, not so `spec.md` could absorb the difference.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `scripts/check-docs.py`: 11/11 PASS.
      `scripts/check-ownership.py --scope core`: 5 changed paths, all owned.
      `scripts/check-decision-refs.py`: all 2054 references resolve, all 35 topic-file links resolve,
      all 15 reversal-row citations resolve — checked by hand per `tasks/doc/052`/`044`: none of
      30/38/39/62/63 was individually pinned over the 4 KB per-decision cap before the split (confirmed
      via `check-doc-size.py --decisions`, which lists none of them), so no per-decision pin was dropped
      by moving 62/63 verbatim.

## Notes

**Hard constraints honoured:**
- Decision 63's second paragraph ("Neither alternative survives...") is untouched, moved verbatim.
- Decision 62's quote of `embarch-ui` decision 10's column pin and its citation of reversals row 86 are
  untouched, moved verbatim.
- `embarch-core/decisions.md`'s index table updated in this commit: one row split into two.

**One in-scope fix beyond the split:** `embarch-core/interfaces/studies.md` had a markdown link straight
at `decisions/streams.md` for the load route's citation. Per `DOC-CONVENTIONS.md` ("link the index, not
the topic file"), repointed it at `decisions.md` and switched the anchor text to the bare `decision 62`,
so it survives future splits the way `history/`'s links already do.

**One out-of-scope staleness found, dropped to inbox, not fixed here:**
`embarch-api/interfaces/studies.md` line 16 names `decisions/streams.md` in inline code (not a link, so
neither gate catches it) for decision 62, which now lives in `decisions/stream-index.md`. Filed at
`/home/gabriel/Github/embarch/embarch-doc/inbox/api-fix-streams-md-mention-after-core-060-split.md`
— `api` scope, not `core`'s to touch.

**No `status.d/` fragment filed**: nothing suite-level changed — this is an internal reorganisation of
one sub-project's own decisions file, no capability, spec fact, or interface shape moved.
**No `features.d/` fragment**: no capability shipped, retired, or changed maturity.
**Changelog fragment:** `changelog.d/core-streams-decisions-split.changed.md`.
