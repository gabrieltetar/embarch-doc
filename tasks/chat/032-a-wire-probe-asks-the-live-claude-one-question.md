# 032 — A wire probe asks the live `claude` one question

**State:** claimed by agent/chat/032-a-wire-probe-asks-the-live-claude-one-question, 2026-11-17 23:00
**Reserve:** `embarch-chat/spec.md` 9,119 of 10,240 B (1,121 B left), already filed against `tasks/chat/031-compact-chat.md` (open); decision 96 in `decisions/promptu.md` has 204 B left. Put the probe's description in a topic file under `embarch-chat/spec/` or `interfaces/`, not in `spec.md`.
**Source:** Fleet Ready issue: each CLI update ends with a throwaway script to see what the wire does now, and one such script's key filter hid a field and led to a wrong first reading.
**Issue:** EMB-163
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

A developer tool in `embarch-chat`, `tools/wire-probe.mjs`, spawns the real `claude` with the panel's own flags (`claudeArgs`, reused from the test build, not a copied list) under a chosen `--config-dir` and `--bin`, with an optional `--model`. It sends `initialize`, then each `--send <json>[@<delay-ms>]` in order, and prints every line that comes back with its milliseconds since spawn, unfiltered, the `initialize` answer whole. A `--list <fixture>` mode prints a recorded fixture under `test/fixtures/wire/` one row per line: direction, type, and subtype or request id. It is a probe, not a test: `npm test` does not run it, and nothing in the extension imports it.

## Why now

The owner moved the issue to Fleet Ready. `test/record.mjs` records a whole session for a fixture and `test/live.smoke.mjs` runs a fixed script; neither answers one question against a new CLI version before `TESTED_RANGE` in `src/wire/version.ts` is raised.

## Done when

- [ ] One command spawns the real `claude` with the panel's flags under a given config dir and binary, sends given requests with delays, and prints every reply line with its time since spawn.
- [ ] The same tool lists a wire fixture one line per entry.
- [ ] Whatever can run without a live `claude` is tested: argument parsing, the `--send` delay syntax, and `--list` against a committed fixture.
- [ ] The chat docs say where the probe is and when to reach for it, without growing `embarch-chat/spec.md` (in reserve, see the dispatch note).
- [ ] Gate green (`../../embarch-fleet/gate.md`, the npm bullet), `changelog.d/` fragment dropped.
