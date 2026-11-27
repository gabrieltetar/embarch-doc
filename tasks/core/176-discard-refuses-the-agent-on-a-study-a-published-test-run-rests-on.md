# 176 — Discard refuses the agent on a study a published Test run rests on

**State:** claimed by agent/core/176-discard-refuses-the-agent-on-a-study-a-published-test-run-rests-on, 2026-11-26 19:56
**Source:** EMB-582 — discard lets the agent drop captures a published Test run rests on
**Issue:** EMB-582
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core decision 112 (`decisions/run-log.md`) lets only the person's token discard a
run "with a `published` entry (the zip's captures rest on it)"; the agent's is
refused `403`. `RunLog::discard` checks that by `self.latest(study_id,
"published")`. Decision 149 (`core/175`) writes a Test run's `published` entry
with `run_id` and no `study_id`, so a study run of a published Test run has no
`published` entry under its own id, and if it ended clean the agent's token can
discard its `streams/`. The Test run's manifest then names files that are gone.
Decision 149 changed what retention reads (`unpublished_ids` handles the `run_id`
form) and left 112 standing. When this is done:

- **The agent's discard of a clean study that belongs to a published Test run is
  refused `403`**, with 112's message, the same refusal a published Study gets.
- **The person's token still discards it**, as 112 allows.
- **A clean study in an unpublished Test run is unchanged**: the agent may still
  discard it, as today.
- **A test covers each of the three**, against a run log carrying a Test run's
  `published` entry in 149's shape.

Find the Test run that holds a study the way retention already does
(`test_run_units`, `unpublished_ids`); do not add a second way.

## Where to look

- `src/run_log.rs`: `discard`, its `scope == Scope::Agent` branch
- `src/test_publish.rs`: the `published` entry the publish handler writes;
  `unpublished_ids`, `test_run_units`
- `embarch-doc/embarch-core/decisions/run-log.md` (112),
  `decisions/test-run-publish.md` (149)
- `embarch-doc/embarch-core/interfaces/run-log.md`: the discard row

## Where the doc goes

Amend 149 in place, or add a line to 112, saying that a study run of a published
Test run counts as published for the discard. Decision `run-log#111` has 120 B
left before its limit (`scripts/check-doc-size.py --pressure`): do not grow 111.
**`embarch-core/open.md` is in reserve** (893 B left; its compaction
`tasks/core/171` is blocked, In flux: yes): do not write it.

## Done when

- [ ] The agent's discard of a clean study in a published Test run is refused
      `403` with 112's message; a test covers it.
- [ ] The person's discard of it succeeds, and a clean study in an unpublished
      Test run is still the agent's to discard; a test covers each.
- [ ] 149 or 112 says a published Test run's studies are published for the
      discard.
- [ ] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).
