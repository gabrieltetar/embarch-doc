# 083 — Live Study renders only the study and the project that are open now

**State:** claimed by agent/ui/083-live-study-renders-only-the-open-study-and-project, 2026-10-26 03:42
**Doc reserve (dispatch, 2026-10-26):** `embarch-ui/spec.md` 9,099 / 10,240 B (1,141 B left, filed against `tasks/ui/089`, open) and `embarch-ui/open.md` 4,366 / 5,120 B (754 B left, filed against `tasks/ui/088`, blocked). The task's own pointers to `ui/078`/`ui/074` are stale; those two are the live filings. Prefer `decisions/live-study.md`, as the task says; if you must write either reserved file, keep it to a clause. `ui/082` (landed `5928bdb`) changed the same Live Study path: build on it.
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-ui findings 3 and 13), verified by Opus against embarch-ui@aa5ffdaa
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Two ways the Live Study tab shows something that no longer belongs to what is open.

**A slow read for one study renders under another.** `lsOpenStudy` sets the shared `lsStudyId` and calls `lsLoadRecord` (`assets/app.js:7380-7399`). `lsLoadRecord` then writes the shared `lsRecord` and `lsTaps` after its `await fetch` and renders the steps, status, provenance and stream list (`:7409-7481`). Nothing checks that the study it was asked for is still the open one. Two cases trigger it: clicking two studies in quick succession, or a run ending (`lsOnFinished`, `:7638-7643`) just as another study is opened. If the older study's response lands last, its steps, status and provenance render under the newer study's id, and `lsRefreshCaptures` fetches the newer study's captures by the older study's tap names. One caller already guards this way (`:8217`, `if (lsStudyId !== id ...) return`); the loaders do not.

**The saved-study picker keeps the previous repo's studies.** `lsLoadSavedStudies` (`:7190`) runs once, at init (`:8226`). A project switch (`sdOpenProject`, `:5663-5682`) reloads the Study Designer's list, the board catalog and the saved benches, but not this picker. After a switch, Run posts a slug from the old repo. That either 404s or, when the new repo has a study with the same slug, runs that study under the old one's displayed name.

Suggested direction: a per-open token that each loader checks after every `await` before writing, plus a picker reload on the switch path. How to structure it is the worker's call.

## Why now

spec.md:55: "Switching reloads every project-scoped surface — catalog, saved benches, studies, taps". The picker is a studies surface the switch path missed. The record race puts one run's verdict under another run's id. That is a misattribution, not a cosmetic glitch, and the Live Study tab is where a run's result is read.

## Done when

- [x] A browser check against `stub_core.py` delays the first study's `/api/studies/{id}` response, opens a second study before it returns, and finds only the second study's steps, status and provenance on screen once both have returned.
- [x] The same holds when the delayed read is the post-run re-read of a study that just finished.
- [x] After a project switch, the Live Study picker lists only the new project's saved studies, without visiting another tab first.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` and `open.md` are in reserve with parked compaction debts (`tasks/ui/078`, `tasks/ui/074`), so prefer `decisions/live-study.md`.

## Done

Decision 60 (`embarch-ui/decisions/live-study.md`). Browser checks: `tests/browser/drive_race.py`, `drive_switch.py` (fail unfixed, pass fixed). Not fixed, noted in decision 60: later per-tap loaders read `lsStudyId` at fetch time; badge not cleared on open. **Incident:** an early ad-hoc UI run used the default desk port and one click of "Open project" may have POSTed `desk: none` to the owner's real desk (:4891); not verifiable without its token. Later runs set `EMBARCH_DESK_PORT` to a dead port.
