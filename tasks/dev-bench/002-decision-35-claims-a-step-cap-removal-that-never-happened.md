# Reconcile decision 35 with a step cap that was never removed

**State:** done — leg dev-bench/002, 2026-09-08
**Source:** owner's repo survey, 2026-09-06 — a decision asserting an SRAM refactor that is not in the tree
**Scope:** dev-bench
**Hardware:** none
**Reserve (leg 055, 2026-09-08):** `embarch-dev-bench/open.md` 4782/5120 B (338 B
left) and `spec.md` 9460/10240 (780 B) are both inside their reserve, with
`tasks/dev-bench/012-compact-dev-bench.md` already filed against them — so record
nothing new, plan to fit, and say so in the task file if you could not.
**Owner:** no

## What

`embarch-doc/embarch-dev-bench/decisions/link.md:41` says "One step decoded at a time from the
retained span, and the local step cap goes away… the ceiling disappears, and the crate's constant
goes back to being the one authority", and `decisions/dispatch.md:27` repeats it as done. The code
still holds the cap: `app/src/serial_protocol.h:55` `#define DBM_MAX_STEPS_PER_STUDY 16` with a
20-line comment defending it, `:714` `struct dbm_step steps[DBM_MAX_STEPS_PER_STUDY];`,
`app/src/serial_protocol.c:1419` refusing `steps_len > 16`, and
`app/tests/serial_protocol/src/main.c:1164` pinning that refusal.

**Doc-only: do not implement the refactor.** The doc stops asserting a change that is not in the
tree — decision 35's reasoning preserved but restated as unimplemented, either moved to `open.md`
under a named trigger or kept in `link.md` with an explicit "not implemented as of `<date>`; the
16-step ceiling and the host/wire divergence it names are both still live". `dispatch.md:27`'s
parenthetical is split, since decision 40's half (the retired `gatt_activity` field) genuinely did land.

## Why now

`embarch.md` §3 makes `spec.md`/`decisions.md` the source of truth for what is true now. A decision
claiming an SRAM refactor happened is the divergence `../../embarch-decision-reversals.md` exists to
make visible, and it currently hides a real host-accepts-20 / wire-refuses-20 gap.

## Done when

- [x] No doc states the 16-step cap was removed. Confirmed against source first (`app/src/serial_protocol.h:55` `DBM_MAX_STEPS_PER_STUDY 16` with its 20-line defending comment, `:714`'s `steps[DBM_MAX_STEPS_PER_STUDY]`, `serial_protocol.c`'s `steps_len > DBM_MAX_STEPS_PER_STUDY` refusal, and `app/tests/serial_protocol/src/main.c`'s `test_study_start_rejects_too_many_steps` pinning it) — the code is unambiguous and unanimous, so **the doc was wrong, not the code**: decision 35 in `decisions/link.md` claimed a refactor that was never built. Amended in place (not retired — its reasoning is sound as a *plan*), titled "not implemented as of 2026-09-08", with an amendment paragraph citing the exact lines above and stating plainly that the paragraph above it is the plan, not the record.
- [x] The still-live divergence (crate `MAX_STEPS_PER_STUDY` = 64, bench = 16) is stated once, in decision 35's amendment in `decisions/link.md`, which is where a reader following the crate/bench divergence already lands (indexed from `decisions.md`, linked from `spec.md`'s "Current truth").
- [x] Decision 35's number is not reused or renumbered; `scripts/check-decision-refs.py` still resolves every reference to it (1247 references resolve, unchanged count from before this edit plus the new amendment citation).
- [x] `decisions/dispatch.md:27` no longer bundles an unimplemented change with an implemented one — its parenthetical now says only decision 40's field retirement landed, and points to decision 35's amendment for the rest.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10): `check-docs.py`, `check-doc-size.py`, `check-decision-refs.py`, `check-client-names.py --repo <code worktree>`, `check-ownership.py --scope dev-bench` (doc worktree) and `--code-repo --scope dev-bench` (code worktree) all pass. Code worktree (`embarch-dev-bench`) has **zero diff** — this is a doc-only correction per the task's own "What" section ("do not implement the refactor"), so there is nothing for that repo's own build/test/lint gate to run against; its west/Zephyr toolchain is also not present in this environment, consistent with the standing note that this worktree cannot carry it. Branch pushed anyway (same tip as `main`) so the code-side branch exists for the fold.
- [x] `spec.md`/`decisions.md`/`open.md` updated — neither `spec.md` nor `open.md` mentioned the step cap or decision 35 at all (checked by grep), so nothing there was false and both stayed untouched, honoring their reserve. `decisions.md`'s index row for `link.md` needed no change (it only lists decision numbers, not content). `changelog.d/dev-bench-decision-35-not-implemented.fixed.md` dropped. No `status.d/` fragment: grepped `embarch.md`, `suite/features.md`, `suite/roadmap.md` and `embarch-decision-reversals.md` for any mention of this step cap or decision 35 — none exists, so no suite-level doc's fact was made false by this correction.

**Compaction debt:** editing decision 35 pushed `embarch-dev-bench/decisions/link.md` into reserve (91.5% of its 12,288 B cap, 1,047 B left) — filed as `tasks/dev-bench/014-compact-dev-bench.md` in this same commit, `In flux: yes` (decision 13 also just amended, 2026-09-07).
