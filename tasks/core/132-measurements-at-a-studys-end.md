# 132 — Core computes the declared measurements and writes `measurements.json` as each study ends

**State:** done
**Source:** Fleet Ready issue: Core does not compute measurements when a study ends. `notes/hil/14-implementation-plan.md`, unit M1.7 (after M1.2, landed as `tasks/study-designer/085`); `notes/hil/02-study.md`, "Measurements"; `embarch-study-designer/interfaces/hil-shapes.md` for `measurements.json`, field by field, and `hil-reducers.md` for the reducers' `Input`.
**Issue:** EMB-222
**Scope:** core
**Hardware:** none
**Owner:** no

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

- Read `hil-shapes.md`'s `measurements.json` section and the declaration shape, `embarch-study-designer/interfaces/hil-declarations.md` (decisions 99 and 100, landed by `suite/057`), before writing; do not invent a second shape for either.
- **Three things `suite/057` left to this unit**: calling `validate_measurements` when a study is submitted, beside `validate_record_checks` (nothing calls it yet); the window's `from_utc_ms` and `to_utc_ms`, which a declaration cannot carry; and **what stamps a marker** (`from_marker`, `to_marker` are free names, unchecked, and a name nothing produces reads `value: null`, `parse_failed`). Say in a decision what a marker is.
- **Decisions near their size limit**: `signing` #110 is already over its limit, so do not grow it; `lease` #93 has 182 B left. A new topic file is the home.
- **`tasks/ui/112` runs beside this unit** (the Study Designer keeps a study's declarations through a save); it calls `validate_measurements` before a save. Nothing in it is yours, and nothing here is its.
- **In reserve, 2026-11-22: `embarch-core/open.md`, 4,764 of 5,120 B (356 B left)**, filed against `tasks/core/133`, `blocked` on `In flux: yes`, whose `Unparks when:` says the compaction rides in the next core unit that runs out of room in it. If this unit's `open.md` edit does not fit, **compact `open.md` in this unit** per that task (move settled detail verbatim into `open/`, keep its `Must not delete:` list) and say so in the closing note; if it fits, leave the file in reserve and `core/133` as it is. `spec.md` is 8,014 of 10,240 B, out of reserve (`core/130` paid it). Decisions near their size limit: `signing` #110 (over), `lease` #93 (182 B left), `run-log` #111 (201 B left).
- Out of scope: verdicts (a Study has none), `report-data.json` and publish (M1.8).

## Done when

- [x] A recorded capture yields the expected `measurements.json` (a fixture test).
- [x] A value from an uncharacterised bench board reads `u_source: undeclared`.
- [x] `spec.md`, `decisions/`, `interfaces/` updated; `changelog.d/` fragment dropped.
- [x] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope core` on both branches). The native Windows build is a debt, recorded.

## Closing note

Decision 113 (`embarch-core/decisions/measurements.md`): Core's receipt stamp is the clock; a marker is the first word of a `Text` tap's line; the window is the capture's span; `rate_check` tolerance `0.05 + 2/(n-1)` is **[assumed]**; a declared `U` is honoured for a `dut` value only. `validate_measurements` now runs in `validate_study`. `open.md` took its edit within its 356 B and stays in reserve, so `core/133` is untouched; the new open item went into `open/never-exercised.md`. `signing` #110 only shrank.

**Debts.** Native Windows build not run (host-side only). Hardware-verification debt: reduce a real study's captures (a `rate` and an `interval` over a bench console) and read `measurements.json`; also the person-token scope on `study_value` has never been seen end to end.
