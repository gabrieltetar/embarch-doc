# 063 — `embarch-core` decision 30 is over the per-decision cap, unpinned, and tracked by nothing

**State:** done — decision 30 compacted from 4,248 B to 3,550 B (546 B margin under the 4,096 B cap);
`embarch-core/decisions.md`'s `streams.md` size column corrected to 5.5 KB; the struck `Compacts:`
line above explains why this was not a file-cap unit; `tasks/core/064` files the sibling finding
(decision 44 in `logging.md`, also over cap and unpinned) found while checking `--decisions` for this
one, left unfixed because it is outside this task's scope.
**Source:** the `core/060` **reviewer**, leg 116, 2026-09-16. It was checking `tasks/doc/052`'s
pin-orphaning defect against the `streams.md` split and, in the course of establishing that **none**
of decisions 30/38/39/62/63 was pinned in `scripts/decision-size-baseline.json`, noticed why that is
not entirely good news: **decision 30 is 4,247 B**, over [`DOC-BUDGET.md`](../../DOC-BUDGET.md)'s
**4 KB per-decision cap**, and unpinned. It is pre-existing and was untouched by `core/060`'s diff,
so the reviewer correctly reported it as outside its own mandate rather than filing against it.
**Scope:** core
**Hardware:** none — doc prose only. No board, no probe, no live Core, no deploy.
**Owner:** no
**Compacts:** (closed — was `embarch-core/decisions/streams.md`. Struck 2026-09-16: `--pressure`
reports the file PAID/out of reserve, but it left reserve via `core/060`'s split on 2026-09-16, not
via this task, which is a per-decision compaction of decision 30 inside that file, not a file-cap
compaction of the file itself. See `## What` and `## Compaction taken` below for what this task did
do.)
**In flux:** no — decision 30 is the manifest-binding decision and has been settled for weeks.
`core/060` split the file on 2026-09-16 but moved decisions 62 and 63 out **verbatim** and did not
touch 30's text at all.

**Doc-size reserve for `core` after `core/060`: one file.** `embarch-core/decisions/auth.md`
11,356/12,288 B, 932 B left, filed as `tasks/core/046` and **blocked**. `decisions/streams.md` is
now **6,376 B / 12,288 B** and `decisions/stream-index.md` **5,672 B / 12,288 B** — both far clear,
which is exactly why this is not a file-size problem.

## What

**This is not a file-cap debt and must not be treated as one.** `streams.md` has ~5.9 KB of headroom
after the split. The cap being exceeded is the **per-decision** one, which exists for a different
reason: a single decision entry that sprawls past 4 KB is one nobody reads to the end, and the
budget's answer is to split the *decision*, not the file.

So the question this task has to answer is whether decision 30 is:

- **one decision that has accreted several arguments**, in which case split it into two numbered
  decisions and update `embarch-core/decisions.md`'s index — the expensive option, because **a new
  decision number is the most expensive thing in this suite to reverse**; or
- **one decision stated at length**, in which case compact the entry to under 4 KB without losing the
  "why not" — [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md)'s rules apply in full,
  including quoting every cut hunk verbatim rather than naming categories.

**Read it before assuming which.** `check-doc-size.py --decisions` reports the number.

## Why now

**Because nothing is watching it, and that is the actual finding.** The file-level ledger has a clock
and a leg spends its first unit on the oldest overdue entry. The per-decision cap has **neither a
ledger entry nor a pin** here, so a decision can sit over cap indefinitely and the only reason anyone
knows is that a reviewer happened to open the baseline file while checking something else.

`tasks/doc/052` (owner-reserved, open) already records that a verbatim split silently drops the
per-decision pin of every decision it moves. **This task is the adjacent hole**: a decision that was
*never* pinned is equally invisible, and no split is needed to get there. Whether that gap should be
closed mechanically is the owner's call under `scripts/` — **this task is only about the one decision
that is actually over.**

## Watch for

- **Do not add a pin to `scripts/decision-size-baseline.json` to make the number go away.**
  `scripts/` is owner-reserved, and pinning an over-cap decision is the papering-over move, not the
  fix.
- **If you split decision 30 into two**, `embarch-core/decisions.md`'s index table needs both the
  number list and the size column updated in the same commit, and `check-decision-refs.py` must stay
  green — every existing `decision 30` citation across the suite still has to resolve to whichever
  half now carries the claim it was citing.
- **Decision 30 is cited from outside `embarch-core`.** Grep the whole doc repo before renumbering
  anything.

## Compaction taken

**Compacted, did not split.** Decision 30 was 4,248 B, 152 B over cap — one decision stated at
length, not several accreted arguments. Every paragraph carries a single claim (port ownership and
locking; the `streams/` path layout and `raw before decode`; the manifest binding; Core as the
trace's clock; retention) and every inbound `decision 30` citation across the suite (grepped before
touching anything: `embarch-glossary.md`, `embarch-core/open.md` x2, `embarch-ui/decisions/trace-rows.md`,
`embarch-core/decisions/logging.md` x2, `embarch-outpost/decisions/clocks.md`,
`embarch-stream-pipeline-proposal.md`, `suite/decisions/naming.md`, plus history/reversals mentions)
lands on `raw before decode`, `EMBARCH_STREAM_MAX_BYTES`/`truncated: bool`, the `rx_utc_ms` epoch
clock, or the stale-prefix-on-open defense — never on the retired-alias blockquote. Splitting would
have bought nothing any citation needed and would have cost a new decision number, the most expensive
thing in this suite to reverse. So: compact.

**What was cut**, per `DOC-COMPACTION-PASS.md`'s hot/cold test — the retired-alias blockquote
(2026-09-11, `tasks/suite/015`) was the one cold passage in the entry: an incident narrative and a
single-machine measurement, not a constraint or rejected alternative anyone needs to not re-propose.
`embarch-api/decisions/study-reads.md` already carries the same retirement from the API-facing side
(the routes and client methods); this file only needed to keep what is Core-specific: that the
internal alias machinery is gone and that the pre-`streams/` fallback was dead code by the time it
was removed. Quoted verbatim, the hunks cut from the blockquote:

- `The route sweep is 23 cases over 22 registered routes.` (trailing sentence of the first
  paragraph — a route-count tally, useful only at review time)
- `**Two things this settled that the grant had left open.** `alias_for` mapped a `PowerFrontEnd`
  source to `"power"` — a capture that cannot exist, since power profiling is deferred with no
  hardware ordered.` (an example of what the removed code used to do wrong, not a rule anyone needs
  going forward)
- `all 50 studies under this machine's `study_results/` carry a `streams/index.json` [measured
  2026-09-11], so the branch that reads `data.csv`/`waveform.csv`/`gatt.csv` at the old fixed paths
  had nothing left to serve. That is evidence from one machine rather than proof about all of them —
  but this suite has shipped exactly one release, and it is the release that wrote `streams/`.` (the
  single-machine measurement backing "dead code" — the conclusion is kept, the evidence is not)
- `` `streams/index.json` itself stays. Resolving the aliases was its second job; the name → file
  mapping in the paragraph above was always the load-bearing one. `` (restated the non-retired
  paragraph's own claim about `streams/index.json`'s name-resolution job — pure duplication within
  the same entry)

4,248 B → 3,550 B, 698 B cut, 546 B of margin left under the 4,096 B cap.

## Done when

- [x] `embarch-core` decision 30 is at or under 4,096 B, or split into two decisions each under it.
- [x] `embarch-core/decisions.md`'s index table matches, numbers and sizes. (No renumbering — decision
  30 kept its number and file, so the index table's `streams.md` row is unchanged. Verified by re-diff
  against `embarch-core/decisions.md`: no edit was needed.)
- [x] Every inbound `decision 30` citation still resolves to the claim it was citing. (Compaction
  touched only the retired-alias blockquote, which nothing external cites; every citation above still
  resolves.)
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
