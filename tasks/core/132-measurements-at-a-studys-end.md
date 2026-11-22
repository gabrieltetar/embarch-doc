# 132 — Core computes the declared measurements and writes `measurements.json` as each study ends

**State:** blocked
**Source:** Fleet Ready issue: Core does not compute measurements when a study ends. `notes/hil/14-implementation-plan.md`, unit M1.7 (after M1.2, landed as `tasks/study-designer/085`); `notes/hil/02-study.md`, "Measurements"; `embarch-study-designer/interfaces/hil-shapes.md` for `measurements.json`, field by field, and `hil-reducers.md` for the reducers' `Input`.
**Issue:** EMB-222
**Scope:** core
**Hardware:** none
**Owner:** no
**Unparks when:** `tasks/suite/057` lands: a study cannot declare a derived measurement until `Study` has a field for it.

## What

Core turns on the shared crate's `reducers` feature and, as each study ends, computes every measurement the study declares over its own captures and writes `measurements.json` in the shape `hil-shapes.md` fixes:

- **`by` and `instrument` from what the step addressed**, never from the study, so a study cannot mark a DUT's word as the bench's.
- **`resolution` and `uncertainty` from the bench board's or instrument's own declaration**, and where it has none — every bench board in milestone 1, since no release ships a characterisation — **`u_source: undeclared`**, read as "U undeclared".
- **A value the study declares for itself** (a `dut` source's resolution and `U`, a declared sample rate) carries `u_source: study`, and a declared rate gets its `rate_check` against Core's own sample count. The tolerance rule is this unit's to state.
- **`declared_by`** from the scope each declaration was made with (decisions 109 and 110), **`bench_image: unverified`** for every bench board, and the DUT image recorded as a claim.
- `measurements.json` joins the run record's subjects (decision 110 already names it), and `incomplete` carries a truncated capture or a record gap.

## Why now

M1.8 (Core's side of publish) and M1.9's `report.typ` read `measurements.json`, and nothing writes it.

## Dispatch notes

- Read `hil-shapes.md`'s `measurements.json` section and `suite/057`'s declaration shape before writing; do not invent a second shape for either.
- **Decisions near their size limit**: `signing` #110 is already over its limit, so do not grow it; `lease` #93 has 182 B left. A new topic file is the home.
- **`embarch-core/spec.md` is in reserve** (`tasks/core/130`, parked); if `tasks/core/131` has not already brought it out, compact it as part of this unit the way that task's dispatch note says.
- Out of scope: verdicts (a Study has none), `report-data.json` and publish (M1.8).

## Done when

- [ ] A recorded capture yields the expected `measurements.json` (a fixture test).
- [ ] A value from an uncharacterised bench board reads `u_source: undeclared`.
- [ ] `spec.md`, `decisions/`, `interfaces/` updated; `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope core` on both branches). The native Windows build is a debt, recorded.
