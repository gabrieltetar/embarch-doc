# 168 — `publish` lists every number in the report, names each prose block's author, and writes revisions

**State:** open
**Source:** `notes/hil/14-implementation-plan.md`, unit M1.10 ("The zip"), its second half
**Issue:** EMB-225
**Scope:** api
**Hardware:** none
**Owner:** no

## Dispatch notes

- `tasks/api/167` landed the zip (`embarch-api` decisions 112 to 114, `interfaces/publish.md`). Its worker named the hooks: `publish_report::ReportInputs` and `appendix_source` for the oracle listing and the authorship rows, the `adopted` rows and `notes/operator-notes.txt` for authorship, and the Core-fetch step in `publish::run` as what a revision built from the earlier zip replaces.
- **`embarch-api/open.md` is in reserve** (4,294 of 5,120 B). `tasks/api/169-compact-api.md` is parked on `In flux: yes` until this unit lands and says the compaction rides here: **compact `open.md` out of reserve (at or under 3,919 B) as part of this unit**, moving settled detail into `open/` verbatim with links left, and keep 169's **Must not delete** items. Say so in your report.
- Core serves a pending revision's `measurements.json` only after the manifest exists (EMB-241, Fleet Ready for `embarch-core`); 167 publishes with a warning in that case. Leave that behaviour alone here unless EMB-241 has landed when you start.

## What

The rest of M1.10, on top of `tasks/api/167`'s zip.

- **The numeric-oracle listing** in the audit appendix's Prose row (`notes/hil/02-study.md`, "The run's files are the numeric oracle", and `notes/hil/06-report-and-publish.md`, "The audit appendix"): every number in the prose files and in `report.typ`'s text that cites a measurement by name (`#m("rate")`, `[rate]`) and matches it to the significant digits written, every tagged number (`(derived)`, `(spec)`, `(inference)`, `(analysis)`), every number that cites nothing but equals some measurement listed as **unbound**, and every numeric literal of `report.typ` that reaches the page listed as **hardcoded**. A picture that is not drawn by the plot helper from a signed file, an embedded image or SVG included, is refused at publish (02).
- **Authorship per prose block**: each block names `agent (<model id>)` or a person, an adoption reads "agent, reviewed by <name>", and the token's scope Core recorded for it (`embarch-core` decision 117, `POST /study/{id}/adopt`) is what the appendix prints (02, "Who writes each prose section").
- **Revisions**: `publish` of a run already published writes `-r2`, then `-r3`, each naming the revision it supersedes and that revision's manifest hash, and never overwrites an earlier zip. **A revision is built from the earlier zip**, its captures included, so a run whose captures retention has swept still republishes (06, "A publish is never overwritten"). `embarch-core/open.md` records that Core's `report-data` route answers `404` once a run's directory is swept: say in this unit's decision what a republish does then.

## Why now

The second half of EMB-225; `verify` (EMB-226) checks the oracle listing (check 4) and the revision chain.

## Done when

- [ ] A fixture report's prose and `report.typ` list each cited, tagged, unbound and hardcoded number in the appendix, in a test per kind; an embedded image is refused.
- [ ] Each prose block's author and the scope Core recorded are in the appendix.
- [ ] Publishing a fixture run again writes `-r2`, keeps the first zip byte for byte, and names r1 and its manifest hash.
- [ ] `interfaces/` and `spec.md` amended; new numbered decisions.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
