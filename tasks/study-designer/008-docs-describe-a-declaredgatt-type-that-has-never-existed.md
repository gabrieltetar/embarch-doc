# Withdraw the `Study.gatt` / `DeclaredGatt` field from the docs, or record it as unbuilt

**State:** closed
**Source:** owner's repo survey, 2026-09-06 — three documents describe a shipped feature no code in the suite implements
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-study-designer/interfaces/types.md:14` documents `gatt: Option<DeclaredGatt>`
as a `Study` field, `spec.md:58` lists it in "What a study carries", and `interfaces/limits.md:34`
gives it a `MAX_DECLARED_SERVICES` bound. `Study` (`src/study.rs:91-224`) has no such field, and a
suite-wide grep for `DeclaredGatt` / `declared_gatt` / `MAX_DECLARED_SERVICES` — plus
`git log -S DeclaredGatt` — returns nothing at all. **The type has never existed anywhere.**

`spec.md` stops asserting the field, `interfaces/types.md` and `interfaces/limits.md` drop the
phantom row and constant, and decision 45 in `decisions/declares.md` is restated as
designed-but-unbuilt with its trigger — its reasoning preserved, its number never reused.

## Why now

`../../DOC-PROTOCOL.md` makes `spec.md` "what is true now", and this is the largest single
divergence between these docs and the code: three documents describing a reconciliation feature
("live discovery wins, and the difference is reported") a reader could author against and find will
not deserialize.

## Done when

- [x] No file under `embarch-doc/embarch-study-designer/` names `DeclaredGatt`, `Study.gatt` or
      `MAX_DECLARED_SERVICES` as current truth.
- [x] Decision 45 is preserved with its reasoning but marked unbuilt, naming what would have to
      exist for it to be true.
- [x] The unbuilt state appears in `open.md` under an existing heading, phrased as a deferral with a
      trigger.
- [x] `grep -rn "DeclaredGatt" embarch-doc/embarch-study-designer/` returns only tombstone prose.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Closed 2026-09-08

Verified the absence first, as instructed: `grep -rn "DeclaredGatt\|declared_gatt\|MAX_DECLARED_SERVICES"`
across `embarch-study-designer/src/` and `git log -S` both return nothing — the type never existed
and was never removed. One correction to this task's own premise: `interfaces/limits.md:34` does
**not** currently give `MAX_DECLARED_SERVICES` a bound — that row is already absent (task
`study-designer/011`'s rewrite, or a predecessor, already removed it), so there was no limits.md row
left to touch. Only two files carried the phantom as current truth: `interfaces/types.md` (the
`Study` field table) and `spec.md` (the "What a study carries" table) — both rows deleted. Also
caught and fixed one adjacent stale reference the task file didn't name:
`decisions/seals.md`'s "outside every seal" list cited `gatt (decision 45)` as an existing field;
reworded to say decision 45's table would be the same story *if it existed*.

Decision 45 in `decisions/declares.md` keeps its number and full reasoning body, with a
"Designed, never built" status line added right after the heading and a closing paragraph naming
concretely what building it would take (a `DeclaredGatt` enum, a `gatt` field on `Study`, the
reconciliation pass in Core). `interfaces/types.md` gained a one-paragraph tombstone note under the
`Study` table pointing at decision 45 and `open.md`. `open.md` gained one bullet under the existing
"Missing authoring paths" heading, phrased as a deferral with a trigger (the first study needing to
declare a GATT table), not a to-do.

Checked `suite/features.md` and its `features.d/study-designer-150-declared-gatt-table-on-a.md`
fragment before deciding on a `status.d/` fragment: both already say "Design-only, no code" against
decision 45 — already correct, so this unit made no suite-level fact false and no `status.d/`
fragment was needed.

`spec.md` net *shrank* (9,183 → 9,136 B) since this was a deletion. `open.md` grew (4,331 → 4,662 B,
458 B left in its 5,120 B cap) from the one new bullet; recorded in
`tasks/study-designer/006-compact-study-designer.md`'s own text per this task's instruction, rather
than filing a new compaction task — `006` stays `blocked` (`In flux: yes`) and this doesn't change
that.

Changelog fragment: `changelog.d/study-designer-declaredgatt-tombstoned.removed.md`.

Gate: `python3 scripts/check-docs.py` — all 10 checks green (`check-client-names.py` included).
`scripts/check-ownership.py --scope study-designer` — OK, all 6 changed paths owned by
`study-designer`. No `cargo` half — this unit touches no code, per the dispatch note (there is
deliberately no code worktree).
