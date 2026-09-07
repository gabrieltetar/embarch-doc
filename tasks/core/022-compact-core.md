# 022 — `embarch-core/interfaces.md` is 833 bytes from its cap

**State:** blocked
**Source:** `core/018` spent the reserve adding the three missing routes
(`GET /dev-bench/port`, `GET /logs/recent`, `GET /logs/stream`); `DOC-COMPACTION.md` §2
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/interfaces.md, embarch-core/open.md
**Size debt due:** 2026-09-26
**In flux:** yes — two other queued units touch this exact file. `tasks/core/021`
(retire `GET /logs/stream`, which has no consumer anywhere) would delete the row
`core/018` just added, and `tasks/api/032` names `/probes/enrolled`'s row as
missing a field (`link_port_serial` is already listed, but that task should be
checked against the current row before this compaction touches it). Shortening
prose now, ahead of either landing, risks compacting a row that is about to be
deleted or a row about to be corrected — the same trap `DOC-COMPACTION-PASS.md`
warns against. Unparked by `core/021` and `tasks/api/032` landing (or being
closed as not-applicable), whichever is later.
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

`interfaces.md` is **14,527 B against a 15,360 B cap** — 833 bytes, inside the
last 10%. The next `core` unit that writes this file may find it capped
before finishing.

## Why now

`check-doc-size.py` fails the gate on a file in reserve with no task naming
it (`DOC-COMPACTION.md` §2). This task is that filing — `core/018` is the
commit that spent the reserve, by closing three genuinely missing rows rather
than by bloating an existing one, so the fix here is compaction of what is
already long-winded, not reversal of `core/018`.

## Done when

- [ ] `core/021` and `tasks/api/032` have landed or been closed, and this
      task is re-read against the resulting file before any edit.
- [ ] `interfaces.md` is clear of the 90%-of-cap reserve line.
- [ ] Every `Must not delete:` item above is still readable, verbatim or
      faithfully restated.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

**Widened 2026-09-07 by the reserve floor.** `check-doc-size.py`'s reserve was 90% of a limit; a percentage of a small cap is not runway, and the corpus reached `suite/features.md` with 36 bytes left and `embarch-api/decisions/core-link.md` with 22. Reserve is now `max(1200 B, 10%)` from the top, so the paths added to the `**Compacts:**` line above crossed on the rule change, not on an edit. **Prefer a SPLIT** — [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split restates nothing, so it costs no argument, and a file warned 1.2 KB out still has a seam to cut. Squeeze only where there is none.
