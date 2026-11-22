# 112 — The Study Designer keeps a study's measurement declarations through a save

**State:** claimed by agent/ui/112-the-study-designer-keeps-a-studys-measurements, 2026-11-22 03:03
**Source:** `tasks/suite/057` (2026-11-21), `embarch-study-designer` decisions 99 and 100: `Study` gained `measurements`. Read off the code while landing it: `api_studies_save` rebuilds the saved `Study` from the tab's rows through `build_authored`, and `study_builder` sets `measurements` empty, so a hand-written study carrying declarations, opened in the tab and saved, would lose them with nothing said. Not run against a real saved study.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

A saved study's `measurements` survive the Study Designer: loading a study shows that it declares measurements (at least their names and count), and saving it writes them back unchanged. Authoring them in the tab is this unit's choice to make or defer; if deferred, say so in a decision, and never drop them silently.

## Why now

`tasks/core/132` makes Core compute the declared measurements, and the HIL procedure has the agent write them into a study file. A person who opens that study in the tab to change a step would otherwise strip what the agent declared, and the run would report no measurements.

## Dispatch notes

- The declaration's shape is `embarch-study-designer/interfaces/hil-declarations.md`; the crate's `validate_measurements` refuses what Core could not compute. Call it before a save writes a file, the way the save already refuses rows that would fail at run time.
- `features.d/ui-025-...` says the tab authors every field but `measurements`; amend it in this unit to what is true after it.
- Out of scope: anything Core computes. `tasks/core/132` (Core computes the declarations) runs beside this unit.
- **Nothing in `embarch-ui/` is in reserve**, 2026-11-22 (`spec.md` 8,487 of 10,240 B). Decisions near their size limit, not to grow: `trace-view` #10 (0 B), `gatt-capture` #17 (4 B), `trace-chart` #10 (14 B), `launcher` #28 (22 B), `tab-folders` #100 (113 B). A new topic file, or `study-authoring.md`, is the home.

## Done when

- [x] A study file with `measurements`, loaded and saved through the tab's routes, keeps them byte-for-byte equal (a test).
- [x] A save whose declarations `validate_measurements` refuses is refused with its message (a test).
- [x] `spec.md`, `decisions/` updated; `changelog.d/` fragment dropped.
- [x] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope ui` on both branches).

## Outcome

Decision 104 (`embarch-ui/decisions/study-authoring.md`). Load returns `measurements` verbatim; Save, Run and Pre-flight send them back and refuse what `validate_measurements` refuses (`400`, `measurements: ...`). The tab lists their names in the build-options summary; authoring them is deferred (stated in 104). Test: `a_study_keeps_its_measurements_through_load_and_save` in `embarch-ui/src/main.rs`. Not run against a real saved study or a browser (no hardware involved; the JS change is unexercised beyond the route test). `features.d/ui-025` amended.
