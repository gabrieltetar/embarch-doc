# 086 — The shared crate's HIL verdict rules: verdicts, guard band, acceptance width and the requirement roll-up

**State:** done
**Source:** Fleet Ready issue: the shared crate has no verdict rules, so a verdict is not decided by code and `verify` cannot recompute one. `notes/hil/14-implementation-plan.md`, unit M1.3 (after M1.1, landed as `tasks/study-designer/084`); `notes/hil/03-test.md`, "The verdict"; `notes/hil/06-report-and-publish.md` for the roll-up and its qualifiers.
**Issue:** EMB-218
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

The verdict rules in the crate's host-only half: **the six verdicts**; **the mapping from Core's step outcomes** to a verdict and its `reason`; **the guard band on both sides of a limit**; **the acceptance-width rule, 2 × max(w, U)**, so a limit narrower than the acceptance width is refused; **the severity order** used to combine verdicts into a run summary with per-verdict counts; and **the requirement roll-up** with its qualifiers and the gap rule (which `skipped` reasons make a requirement `not verified`). Each rule carries a behaviour version on the same terms as the reducers (`study-designer/085`).

## Why now

Core's Test route and `verify` need them. A Study has no verdict, so milestone 1 builds this ahead of its first user, by the owner's order; the plan notes it may move to the Test phase if fleet capacity is short.

## Dispatch notes

- **Write against `interfaces/hil-shapes.md`, "The six verdicts"**, and decisions 90 and 91, as `study-designer/084` left them: the strings, the closed `reason` list, the severity numbers and the qualifier spellings are fixed there. How a verdict is reached, and the order in which reasons apply, is this unit's.
- **One known gap in the shapes, found by `084`'s reviewer**: `notes/hil/03-test.md` makes an observation-prompt timeout `inconclusive`, and the closed `reason` list has no reason for it. Decide it here, amending `hil-shapes.md` and the decision in the same commit.
- **Behaviour versioning is shared with `study-designer/085`** (reducers), which has landed: use its `Registry` and behaviour mechanism (decisions 92 and 93, `decisions/hil-reducers.md`), and the `reducers` feature or a sibling of it.
- **`interfaces/hil-shapes.md` is in reserve** (11,205 of 12,288 B; out of reserve at 11,059 B), and its compaction, `tasks/study-designer/087`, is parked on `In flux: yes` until this unit lands. **Compact that file as part of this unit**, after your own edits to it: a verbatim split into a sibling `interfaces/` file with links left behind is the expected move, and it must keep 087's **Must not delete** list (the *(shape)* markers and the pointers to decisions 90 and 91, the six verdicts and their `reason` lists, and the `measurements.json` key table, moved verbatim if moved). Do not edit 087; the supervisor closes it at this unit's fold.
- **The crate is `no_std` with four consumers building it four ways** (see `085`'s dispatch note); the rules go behind the same host-only feature, and every existing consumer builds unchanged.
- **Decisions near their size limit**: `versioning` #12 (67 B, pinned), `protocols` #58 (121 B), `authoring` #73 (130 B). New decisions go in a HIL topic file.
- Out of scope: Core calling the rules (the Test phase), the report's rendering of a verdict (M1.9, M1.10).

## Done when

- [x] A fixture per verdict, per qualifier and per roll-up case passes.
- [x] A limit narrower than the acceptance width is refused, and a result inside either guard band is `inconclusive` with `guard_band`.
- [x] `check-doc-size.py --pressure` no longer lists `interfaces/hil-shapes.md`.
- [x] `spec.md`, `decisions/`, `interfaces/` updated; `changelog.d/` fragment dropped.
- [x] Gate green (`../../embarch-fleet/gate.md`, the shared-crate bullet; `check-ownership.py --scope study-designer` on both branches).

## Outcome

Decisions 95 to 98 (`decisions/hil-verdicts.md`); `interfaces/hil-verdicts.md`; code `src/verdicts.rs` behind feature `verdicts = ["alloc"]`, fixtures in `tests/fixtures/verdicts/`. The observation-prompt gap is closed with the reason `observation_unanswered` (95). `hil-shapes.md` compacted by moving the characterisation section verbatim to `interfaces/hil-characterisation.md`; 11,205 B to under 10,000 B. **Debts:** none hardware. Core and `verify` must turn `verdicts` on (a Cargo feature edit in `embarch-core` and `embarch-api` when they first call the rules).
