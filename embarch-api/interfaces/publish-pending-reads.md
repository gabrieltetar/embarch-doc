# embarch-api: what `publish` reads of Core before the manifest exists

**Status:** active, 2026-11-23. Split verbatim from [publish.md](publish.md) (`tasks/api/172`); the section below is unchanged.

## What publish reads of Core before the manifest exists

`GET /study/{id}/publish/{revision}/files/{name}` serves the run's own files, `measurements.json` among them, at the pending revision, before the manifest exists (`embarch-core` decision 116, since `core/136`), so the PDF and the exports are built from it. A `404` there is still read as "absent", and **if the manifest then names it the zip carries a warning that the PDF and exports were built without it**; a Core that serves the pending revision never takes that path, and no real Core has yet been met ([../open.md](../open.md)). The captures and the step outcomes come through the existing `GET /study/{id}/stream/{name}`, `/streams` and `/steps` routes, which serve today.
