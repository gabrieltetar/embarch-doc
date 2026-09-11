# 026 — `embarch-api/decisions/core-link.md` is 22 bytes from its cap

**State:** claimed — leg 073, 2026-09-10. Dispatched as this leg's first unit: it is the nearest
non-blocked entry on the size ledger (due 2026-09-14, `open.md` 5068/5120 and `spec.md` 9441/10240)
and `In flux:` is `no` for both files on the `Compacts:` line.
Previously: open — corrected from `blocked` by the supervisor at `api/035`'s fold, leg 072, on its
own reviewer's finding (`inbox/api-026-blocked-on-nothing.md`, resolved here rather than filed as a
task). `api/035` re-judged the park correctly and then left the state behind: the unpark condition
it wrote — *"actually compacting `spec.md` and `open.md`, which is this task's own remaining job"* —
is a description of dispatching the task, not an external precondition, and `blocked` has to keep
meaning "nothing here can be done" (`tasks/doc/030`). Nothing external blocks it now, so it is
dispatchable and `queue-status.py` should say so.
**Source:** `api/022` spent the reserve writing decision 55; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/spec.md, embarch-api/open.md
**Size debt due:** 2026-09-14
**In flux:** no — corrected from `yes` by the supervisor at `api/035`'s fold, for the same reason
the state was: the argument written below concludes that neither file on the `Compacts:` line is in
flux any more, and `yes` is the answer that forces `blocked`. What follows is `api/035`'s own
re-judgement, unchanged, and it is the evidence for `no`. Re-judged by `api/035` (2026-09-10)
against `embarch-api/spec.md`
and `embarch-api/open.md`, the two paths actually left on the `Compacts:` line
above. The premise this field used to state — "the event-stream half of this
file has never met a real `embarch-core`" — no longer applies to either of
them: that half of `core-link.md` split out into `decisions/study-events.md` on
2026-09-07 and was closed separately (see below), and `api/035` confirmed on
the bench that `study_watch` has since met a real, installed `embarch-core` and
received pushed live frames plus an observed polling fallback — decisions 48/49
are, so far, confirmed rather than contradicted. What has not run is
`study-status --follow`, the drop path, `lagged`, and a reconnect —
`tasks/api/059-sse-client-remaining-observations.md` (`api/001`, the task this
line and `open.md` used to name for that debt, was never filed and cannot
unpark anything). None of that touches `spec.md`/`open.md`, which stay blocked
on their own terms: both are still inside their own reserve lines (see the
`api/054` closing note below) and neither has been compacted by this unit.
Unparked by actually compacting `spec.md` and `open.md`, which is this task's
own remaining job — no other landing is a precondition for that half.
**Must not delete:** decision 15's *failure signature* — the identical path
resolving from an interactive shell and failing with "the network name cannot be
found" from the service. It is a measurement, and it reads as an inference once
the A/B test is summarised away. Decision 36's **rejected** `Builder::thread_stack_size`
and the 64 MiB-insufficient/512 MiB-needed pair: both are empirical, and a
shortened form that keeps only "512 MiB" makes the number look chosen.
Decision 26's *correction* — that DUT-UART capture was never an intended use — is
the whole entry; the fallback chain it describes is the disposable half.
Decision 55's `default_headers` rejection — corrected by `api/027`, 2026-09-10, to
drop the false "leaves the sweep nothing to assert" clause and mark the
handle-hands-out-`http()` reason as prospective, not current. Preserve the
corrected form, not the original.

## What

`decisions/core-link.md` is **12,266 B against a 12,288 B cap** — 22 bytes. The
next `api` unit that writes this file cannot write anything into it.

**The move is a split, not a shortening, and the split is not blocked.** This
file already carries six unrelated missions: address resolution (11, 14, 17),
artifact transfer (15), the shared-client extraction (37, 38), the event stream
(48, 49), the per-machine logfile (43), `serial_log`'s port fallback (26), and
now the auth funnel (55). `api/023` did exactly this to `shape.md` — moved
entries **verbatim** into `decisions/tests.md` and updated the index — and a
verbatim move states nothing new, so `In flux: yes` does not forbid it. Splitting
the event stream (48, 49) out is the obvious cut: it is the flux, and it is the
half a live run will rewrite.

Actual compaction of the remaining entries waits for `api/001`.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it, and the
commit that spends the reserve is the one that files it (`DOC-COMPACTION.md` §2).
This task is that filing.

`embarch-api`'s whole decision corpus is narrow — `zephyr.md` 11,056,
`interfaces/config.md` 11,008, `build.md` 10,934, `surface.md` 10,928, all a
paragraph short of the 11,059 B reserve line and therefore invisible to the
size check. [embarch-api/open.md](../../embarch-api/open.md) carries that as a
standing hazard, and leg 015 is what it is written from: with 96 bytes left, an
entry went into whichever file had room rather than the file whose topic it was.

## Done when

- [x] `decisions/core-link.md` is clear of the 11,059 B reserve line. Done by
      `agent/api/046-older-core-parse-rule`, 2026-09-07: 10,731 B after the
      split (and decision 58's addition), well clear of the line.
- [x] Whatever moved, moved **verbatim** unless `api/001` has landed; every
      `Must not delete:` item above is still readable at its new address.
      Decisions 48 and 49 moved verbatim into the new
      `decisions/study-events.md`; every item this task's `Must not delete:`
      names lives in `core-link.md`, which was not touched except to add
      decision 58 and retitle its own scope line — untouched otherwise.
- [x] `decisions.md`'s index table names the new file, its decision numbers and
      both files' sizes, and `check-decision-refs.py` resolves every number.
- [x] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words: *can `spec.md` alone answer what someone needs to
      work on reaching Core today?* — yes: nothing in the split changed what
      `spec.md` says, only where the decisions justifying it live.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10) — green for the
      `core-link.md`/`study-events.md` split itself (`check-docs.py` all 10
      green on `agent/api/046-older-core-parse-rule`); left unchecked because
      `spec.md` and `open.md` — both still named under **Compacts:** above and
      both still inside their own reserve lines — are untouched by this unit.

**Closed by `agent/api/046-older-core-parse-rule` (task `api/046`), 2026-09-07:
only the `core-link.md` split above**, which was blocking decision 58. This
task stays `blocked` — `spec.md` and `open.md` are unaddressed, and
`In flux: yes` above (the event-stream half, now in `study-events.md`) still
applies to that file's *remaining* compaction, which still waits on
`tasks/api/001`.

**`open.md`'s item closed by `agent/api/031-config-example` (task `api/031`),
2026-09-09**, per `.claude/leg.md`/`DOC-COMPACTION.md` §2's exception for a
file whose own compaction is blocked `In flux: yes`: the actor making the flux
is the only one who can shorten it without writing a clean statement of
something about to be wrong, and `api/031` was writing into `open.md` anyway.
`open.md` went from 4,802 B to 3,782 B (added the `artifact_path_for_core`
load-refusal gap, cut resolved historical narrative — the itemised
per-file compaction-debt ledger, now redundant with the filed
`tasks/api/*-compact-api.md` themselves — and tightened several bullets).
**This task stays `blocked`**: `spec.md` (still inside its own reserve line)
and `decisions/core-link.md` (parked, `In flux: yes` above) are still
unaddressed, and only `api/001` landing unparks the latter.

**`decisions/core-link.md`'s item closed by `agent/api/054-decision-26-retire-or-retitle` (task
`api/054`), 2026-09-10**, per the same `In flux: yes` exception used for `open.md` above: leg 070
cleared the file's own 206-byte reserve as part of paying it forward, so this unit paid the
compaction rather than parking it further. Decision 26 was retitled about intent rather than
tombstoned — its correction (a DUT console was never a supported `serial_log` target) is true and
current, so it stays `active`, not `retired`; only the disposable fallback-mechanism prose (per this
task's own `Must not delete:` note) was cut. `core-link.md` went from 12,082 B to 11,962 B. This
task stays `blocked`: `spec.md` and `open.md` remain, both still inside their own reserve lines, and
neither is addressed by this unit.

**Widened 2026-09-07 by the reserve floor.** `check-doc-size.py`'s reserve was 90% of a limit; a percentage of a small cap is not runway, and the corpus reached `suite/features.md` with 36 bytes left and `embarch-api/decisions/core-link.md` with 22. Reserve is now `max(1200 B, 10%)` from the top, so the paths added to the `**Compacts:**` line above crossed on the rule change, not on an edit. **Prefer a SPLIT** — [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split restates nothing, so it costs no argument, and a file warned 1.2 KB out still has a seam to cut. Squeeze only where there is none.
