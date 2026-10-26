# 082 — A live run's badge says running and names its step, instead of "pending" for the whole run

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-ui finding 14), verified by Opus against embarch-ui@aa5ffdaa
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

A `LiveSession` starts with `status: "pending"` (`src/live_study.rs:847-850`). Two things can change it. A `StatusChanged` event does, but embarch-core sends that only when a run fails or completes (embarch-core `src/study.rs:770`, `:3264`); its job is `running` from creation and no event says so. A `Polled` item does, and it is also the only thing that sets `total_steps` (`:1096-1110`). The shared client's `follow_study` makes one status read at subscribe time and passes it on only when the study is already terminal (embarch-api `crates/embarch-core-client/src/study_events.rs:591-604`). So on the live path the snapshot and every step frame carry `pending`, with no `total_steps`. `lsRenderStatus` shows the counter only for `running` (`assets/app.js` `lsRenderStatus`), so the badge reads "pending" from the first step to the last. It even overwrites the `running 3/7` that `lsLoadRecord` drew from the job record a moment earlier. Suggested direction: start the session from a real status read, with status and total_steps, and/or treat a step arriving as proof that the run is running. Fix it in this repo. A change to `follow_study` itself is `embarch-api`'s scope and goes there as its own drop if wanted. The same review has an api finding about that function's first poll.

## Why now

Decision 20 (`decisions/study-designer.md`): "The run badge counts the step *now running*", because "while a study runs this badge is the *only* thing on the run card saying where it is". Decision 31 kept that badge when the tab moved from polling to SSE, and on the SSE path it no longer counts anything.

**Sequencing:** the inbox drop `api-study-follow-ends-on-unknown-or-interrupted-study.md`, filed the same day, edits the same `follow_study` path this one traces back to. Land them one after the other, not in parallel.

## Done when

- [ ] A unit test feeds a session the item sequence a live run produces (subscribe, a non-terminal status read, step completions, then completed). The status it serves reads `running`, with `total_steps` set, from the first item on, and `current_step` follows the steps.
- [ ] A browser check against `stub_core.py` shows the badge as `running N/M` during a stubbed live run, and never `pending` after the first step.
- [ ] A terminal status is still never un-said by a later non-terminal reading (decision 33).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` and `open.md` are in reserve with parked compaction debts (`tasks/ui/078`, `tasks/ui/074`).
