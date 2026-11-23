# 137 — Core takes the earlier zip's own files, so a run swept by retention still republishes

**State:** open
**Source:** `embarch-core/open.md` — "A revision after the retention sweep has no captures to hash"; `notes/hil/06-report-and-publish.md` — "A revision is built from the earlier zip, its captures included, so retention sweeping a published run's captures never stops a republish" (owner, 2026-11-20)
**Scope:** core
**Hardware:** none
**Owner:** no

## Dispatch notes

- `embarch-core` decision 116 (`decisions/publish.md`, `interfaces/publish.md`) makes publish two routes. Today `POST /study/{id}/report-data` answers `404` once the run's directory under `study_results/` is swept, and Core keeps nothing of a publish but its run-log entry (decision 118: the manifest hash and `log_head`). So a republish after the sweep has no files to hash and no record to rebuild `report-data.json` from.
- `embarch-api` decision 117 (`embarch-api/decisions/publish-revisions.md`) refuses such a republish and writes nothing, because Core cannot sign another revision. That is the gap from 06's design this task closes on Core's side; `tasks/api/172` makes embarch-api send the files and is parked until this lands.
- **What Core can trust is its own signature and its own log.** The earlier zip carries `manifest.dsse.json`, signed by Core, whose SHA-256 the run log recorded at that publish; every Core file in the zip is a subject of that manifest. How Core takes them (a body on `report-data`, a separate upload route, a staging directory) and what it refuses is this unit's design, in a numbered decision.
- Per-decision budgets near their limit in `embarch-core`: `run-log#111` (201 B left), `lease#93` (182 B); `signing#110` is already over. Put the new decision in `decisions/publish.md` beside 116, or in a new topic file, rather than growing those.

## What

For a run whose directory has been swept, Core accepts the earlier revision's Core-produced files from the caller, checks them against what Core itself signed and logged, and then answers `report-data` and `publish` for the next revision exactly as it does for a run still on disk. A file that is not a subject of a manifest Core signed and logged for that run is refused; nothing the caller supplies is taken on its word.

## Why now

`publish` and its revisions landed with `tasks/api/167` and `168`; the republish-after-sweep refusal is the one place the built system departs from the design note the owner reviewed. M1.14's first real publish does not need it, but every published run reaches the sweep eventually.

## Done when

- [ ] A test: a run published once, its directory swept, the earlier revision's files handed back, and `report-data` then `publish` write `r2` with a manifest naming the revision it supersedes.
- [ ] A test for each refusal: a manifest whose hash the run log never recorded for this run, a file that is not one of its subjects, a file whose bytes do not match its digest.
- [ ] A run still on disk publishes exactly as before.
- [ ] `interfaces/publish.md` amended; a new numbered decision for how the files are taken and what is refused; the `open.md` item closed or narrowed.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
