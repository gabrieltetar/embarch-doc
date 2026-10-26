# 085 — A tap's table is re-read when its card loads, so the post-run re-read is not a frozen mid-run snapshot

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-ui finding 7), verified by Opus against embarch-ui@aa5ffdaa
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`table_for` (`src/studies_api.rs:724-750`) caches one parsed CSV under the key `(study_id, tap)` alone. It never revalidates it and has no refresh route. Both `/rows` (`:230`) and `/series` (`:276`) go through it. Opening a study that is still running loads its Data cards (`lsRenderData`, `assets/app.js:7871-7874`), and that read caches whatever part of the rendered CSV Core has written by then. When the run ends, the post-run re-read (`lsRefreshCaptures`, `:7489-7498`) asks for the same key and gets the cached table back. The read succeeds, so it replaces what the live feed built with that early, partial snapshot. Every later page and plot bin comes from it too, until another tap is viewed or the process restarts. A study with one data tap hits this every time. Suggested direction: the contract the other two caches state, "loading the view is the refresh". A first-page read (or a dedicated load) re-fetches, and paging and binning reuse what that load produced.

## Why now

The trace and time-chart caches both say why they cannot go stale: "loading the view is the refresh, rather than there being a staleness rule nobody can see" (`src/main.rs:145-148`, `src/time_chart.rs:1300-1303`). The table cache is the one that does not. Decision 33 (`decisions/live-study.md`) says a live plot "is labelled a preview and re-rendered from the file when the run ends". With this cache, the file it reads can be the preview.

## Done when

- [ ] A test against a stub Core serves a short CSV, reads `/rows`, then serves a longer CSV for the same study and tap. A first-page read returns the longer table, and later pages and `/series` bins agree with it.
- [ ] Paging through one loaded table still costs one Core fetch, not one per page.
- [ ] A browser check against `stub_core.py` that opens a running study and lets it finish shows the full table in the Data card after the post-run re-read.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` and `open.md` are in reserve with parked compaction debts (`tasks/ui/078`, `tasks/ui/074`).
