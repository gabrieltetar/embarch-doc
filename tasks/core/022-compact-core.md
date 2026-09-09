# 022 — `embarch-core/interfaces.md` is 833 bytes from its cap

**State:** open — **reopened by the supervisor in `core/009`'s fold, leg 060, 2026-09-09.** `009`
closed it on the grounds that `open.md`'s item was done, and its pass was real (5,051 B → 4,669 B,
one answered bullet deleted and three squeezed). But **`open.md` is still in reserve**: the floor is
`max(1200 B, 10%)` from the top, i.e. 3,920 B for this file's 5,120 B cap, so 4,669 B is 91.2% and
still inside it. `check-doc-size.py` reports a reserved file as "filed" whenever a task *file* names
it, **regardless of that task's state** — so closing this left the ledger pointing at a closed task
and the debt would have gone unowned with nothing failing. That is the `tasks/doc/028` class again:
a hand-written `State:` field nothing verifies. `interfaces.md`'s item stays closed (2026-09-07,
by the split); **only `open.md`'s remains, and it needs a further ~750 B.** No longer in flux for
this file — `009` acted as the flux-maker and the compaction is a squeeze on a small file now, which
is why `DOC-COMPACTION.md` §2's prefer-a-split guidance may not have anything left to cut here.
**Source:** `core/018` spent the reserve adding the three missing routes
(`GET /dev-bench/port`, `GET /logs/recent`, `GET /logs/stream`); `DOC-COMPACTION.md` §2
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/open.md
**Size debt due:** 2026-09-26
**In flux:** **no, for the one file still on the `Compacts:` line.** Corrected 2026-09-09 by
`tasks/doc/030`, which found that this field is answered *per file* and had been left behind by a
file that is already paid. The block below is about **`interfaces.md`** — every example in it is a
route row, and `interfaces.md`'s item closed on 2026-09-07 with the split. `open.md` is open
questions, holds none of those rows, and this task's own `State:` line already says *"No longer in
flux for this file — `009` acted as the flux-maker."* Kept verbatim below rather than deleted,
because it is the live judgement the moment `interfaces.md` re-enters reserve:

> **Was `In flux: yes` for `interfaces.md`:** two other queued units touch this exact file. `tasks/core/021`
> (retire `GET /logs/stream`, which has no consumer anywhere) would delete the row
> `core/018` just added, and `tasks/api/032` names `/probes/enrolled`'s row as
> missing a field (`link_port_serial` is already listed, but that task should be
> checked against the current row before this compaction touches it). Shortening
> prose now, ahead of either landing, risks compacting a row that is about to be
> deleted or a row about to be corrected — the same trap `DOC-COMPACTION-PASS.md`
> warns against. Unparked by `core/021` and `tasks/api/032` landing (or being
> closed as not-applicable), whichever is later.
**Must not delete:** the `GET /serial-log` caller-side-ceiling paragraph
(measured 2026-09-06, `duration_ms=15000` against the live Core) — it is a
cross-repo measurement, not a general description, and reads as an inference
once summarised. The `404`-is-often-expected / `502`-vs-`503` vocabulary
paragraph in the Conventions section — it is what stops a caller inventing a
`503` branch that can never fire. `GET /study/{id}`'s `current_step` semantics
paragraph, specifically the "consequence, not an invariant" sentence — decision
43's whole point is that nothing checks it before reporting `completed`, and a
shortened form that drops the caveat restates the bug this doc exists to
prevent.

## What

`interfaces.md` was **14,527 B against a 15,360 B cap** — 833 bytes, inside the
last 10%. The next `core` unit that writes this file may find it capped
before finishing.

**`interfaces.md`'s item is closed, 2026-09-07, by `tasks/core/020`** — a worker
in flux on this exact file (`020`'s `hardware_id` rename touches the
`/dev-bench/hello` row) split it into `interfaces/hardware.md`,
`interfaces/topology.md`, `interfaces/logs.md`, `interfaces/studies.md` and
`interfaces/result-layout.md`, with `interfaces.md` reduced to Conventions plus
an index (`DOC-COMPACTION.md` §3's sanctioned split, the same shape
`decisions.md` uses). Every `Must not delete:` item below carried over verbatim.
This was a **split**, not a squeeze — no row's prose was shortened — so the
quoted "in flux" warning above still holds for whatever `core/021`/`api/032` touch:
they now land against `interfaces/logs.md` and `interfaces/topology.md`
respectively, unaffected by the file move. **`open.md` was never parked on those
two** and the sentence that said it was is corrected here, 2026-09-09
(`tasks/doc/030`): they are `interfaces.md` rows, `open.md` holds no rows, and
`tasks/core/009` compacted `open.md` on 2026-09-09 as the actor making its own
flux. It is `open`, dispatchable, and needs a further ~750 B.

## Why now

`check-doc-size.py` fails the gate on a file in reserve with no task naming
it (`DOC-COMPACTION.md` §2). This task is that filing — `core/018` is the
commit that spent the reserve, by closing three genuinely missing rows rather
than by bloating an existing one, so the fix here is compaction of what is
already long-winded, not reversal of `core/018`.

## Done when

- [x] `core/021` and `tasks/api/032` have landed or been closed, and this
      task is re-read against the resulting file before any edit. —
      superseded: `open.md` was the last remaining item on this task
      (`interfaces.md` closed 2026-09-07, above), and `tasks/core/009`'s
      dispatch note authorised compacting `open.md` now, as the actor
      making its flux, rather than waiting further.
- [x] `interfaces.md` is clear of the 90%-of-cap reserve line. — done
      2026-09-07 by the split.
- [x] Every `Must not delete:` item above is still readable, verbatim or
      faithfully restated. — re-checked 2026-09-09: all three still stand,
      untouched by this task's own edit to `open.md`. The `GET /serial-log`
      caller-side-ceiling paragraph was separately amended (not deleted) by
      `tasks/core/009` itself, which shipped Core's own side of that cap.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

**Closed 2026-09-09 by `tasks/core/009`.** `open.md` compacted from 5,051 B
to 4,669 B (5,120 B cap): one bullet deleted as answered (`GET
/study/{id}/events`'s no-replay note explicitly declared itself "closed
rather than owed" — `DOC-COMPACTION-PASS.md`'s "a question may disappear
only if you can name it as answered"), three live bullets squeezed, and one
new bullet added recording `core/009`'s owed decision (its cap values and
`truncated` shape, withheld from `decisions.md` under that leg's burndown
constraint). Still short of clearing the reserve band outright (91.1% of
cap) — `open.md`'s remaining bullets are all live, unanswered questions with
no further seam to cut without losing a fact — so the next unit to write
here should expect the reserve warning again and file fresh debt rather than
assume this task still covers it.

**Widened 2026-09-07 by the reserve floor.** `check-doc-size.py`'s reserve was 90% of a limit; a percentage of a small cap is not runway, and the corpus reached `suite/features.md` with 36 bytes left and `embarch-api/decisions/core-link.md` with 22. Reserve is now `max(1200 B, 10%)` from the top, so the paths added to the `**Compacts:**` line above crossed on the rule change, not on an edit. **Prefer a SPLIT** — [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split restates nothing, so it costs no argument, and a file warned 1.2 KB out still has a seam to cut. Squeeze only where there is none.
