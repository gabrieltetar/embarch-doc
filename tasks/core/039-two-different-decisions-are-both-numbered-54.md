# 039 — Two different `embarch-core` decisions are both numbered 54

**State:** done — leg 078, 2026-09-10
**Reserve for this scope:** `embarch-core/decisions/flashing.md` 11,487/12,288 B (801 B left) and
`decisions/surfaces.md` 11,937/12,288 B (351 B left) are both in reserve, and both their compaction
tasks (`core/035`, `core/038`) are `blocked` on `In flux: yes`. Keep the "this decision moved" note
to one short line. If your edit will not fit, compact *that file* as part of this unit, carrying the
parked task's `Must not delete:` list, and close only that file's item there.
**Source:** leg 077, 2026-09-10, found while picking the next free decision number for `api/044`.
A live instance of the gap `tasks/doc/033` describes — nothing checks that a decision number is
unique — so this is the defect, not the missing check.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Two decisions in `embarch-core` carry the number 54:

- `embarch-core/decisions/flashing.md:46` — *"`Backend::NrfJprog` retired: a fourth backend no
  bench, doctor run, or record ever selected"*
- `embarch-core/decisions/surfaces.md:45` — *"`EnrolledBoardResponse` does not grow a persisted
  validation timestamp; the existing field gets an honest label instead (`tasks/core/027`)"*

They are unrelated, and both are cited elsewhere in the suite. **"decision 54" in `embarch-core`
currently resolves to whichever file the reader opened first**, and `check-decision-refs.py` is
green on both because it resolves a number against the sub-project rather than against a file —
the same blind spot leg 076 hit from the other direction with `umbrella/042`.

## What to do

**Renumber exactly one of them, and the citation sweep is the work.** Whichever moves, every
reference to it across the suite has to move with it, and a reference that says only "decision 54"
without a file has to be read for which one it meant — that reading is the part no script can do.

Prefer renumbering the **later-written** one to the next free number (57, after `core/037` took 55 and `api/044` took 56),
and leave a one-line note at the old number's home saying it moved, so a stale citation lands
somewhere that explains itself rather than somewhere plausible and wrong.

**Do not add the uniqueness check here** — `scripts/` is the owner's, and `tasks/doc/033` already
holds that half.

## Resolution

**Renumbered `decisions/surfaces.md`'s 54 to 57.** It is the later-written of the
two: it references decision 50 ("2026-09-07", "immediately below") and
`tasks/core/027`, both after `flashing.md`'s 54 (suite review, 2026-09-06). Core
already had decisions up to 56 (`decisions/handshake.md`), so 57 is the next free
number in this sub-project.

**Old-number tombstone:** `decisions/surfaces.md` keeps a one-line `### 54 —
moved to decision 57 (...)` stub in place, so a stale citation that lands in
this file rather than `flashing.md` finds an explanation instead of a
plausible-but-wrong match. `flashing.md`'s own decision 54 is untouched.

**Citation sweep**, read one by one:

- `embarch-core/decisions.md` (the sub-project's decision index/table) — the
  `surfaces.md` row listed `50, 55` with no 54 at all (already missing/stale
  before this task); updated to add `54 (moved to 57)` and `57`.
- `embarch-core/decisions/surfaces.md` itself — the internal
  "See decision 54, immediately below" (in decision 50's own paragraph, same
  file) → "decision 57, below".
- `embarch-core/interfaces/topology.md:9` — "decision 54 has why" clearly means
  the `EnrolledBoardResponse`/label decision (same paragraph discusses
  `confirmed_at_utc_ms` vs `validated_at_utc_ms`) → updated to 57.
- `embarch-core/decisions/flashing.md:44` ("nrfjprog itself was retired by
  decision 54, below") and `embarch-core/decisions/auth.md:22` ("its decision
  54", explicitly `embarch-api`'s own numbering) both read as the *other*
  decision 54 (flashing's own, and api's separate sub-project numbering
  respectively) — left unchanged.
- `tasks/core/035-compact-core.md` (two hits) — both read as flashing's
  `Backend::NrfJprog` decision ("retiring `Backend::NrfJprog`") — left
  unchanged.
- `history/core.md` (two hits, "Decision 50's closing paragraph... points to
  decision 54" and "decision 54 says label it Enrolled") — these read as the
  moved (surfaces) decision, but `history/core.md` is **not** this scope's to
  hand-edit (`check-ownership.py --scope core` refuses it; it is
  assembled by `build_changelog.py` from `changelog.d/` fragments) — left as
  historically-accurate-at-the-time prose, uncorrected. Not a live citation in
  the same sense as a decisions/interfaces file.
- `embarch-api/*`, `embarch-study-designer/*` decision-54 citations found by
  grep are each that sub-project's **own independent** decision 54 (api:
  bearer-sweep exhaustiveness; study-designer: GATT-activity field retirement)
  — unrelated, untouched.
- `tasks/umbrella/045-relabel-confirmed-at-utc-ms-if-doctor-ever-renders-it.md`
  (three hits) and (per `embarch-fleet/supervisor-log.md`'s 2026-09-10 17:35
  entry) `embarch-ui`'s `src/snapshot.rs`/`assets/app.js` cite the moved
  decision but sit outside `core` scope — dropped to
  `embarch-doc/inbox/umbrella-ui-decision-54-renumbered-to-57.md` rather than
  edited here.

**Manual grep for the bare old number**, `grep -rn "decision 54" embarch-core/
history/core.md tasks/core/` (this repo's core-owned paths): every remaining
hit resolves to `flashing.md`'s own untouched decision 54 or `auth.md`'s
citation of `embarch-api`'s separate decision 54, confirmed above.

## Done when

- [x] Exactly one of the two is renumbered; both numbers are unique within `embarch-core`.
- [x] Every citation of the moved decision, in every repo, points at the new number — the body of
      this task names each one found and says how it was read. (Two citations outside `core`'s
      ownership were dropped to `embarch-doc/inbox/` instead of edited directly — see above.)
- [x] `scripts/check-decision-refs.py` green, and a manual grep for the bare old number is recorded.
- [x] `changelog.d/` fragment.
