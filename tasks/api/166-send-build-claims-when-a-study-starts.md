# 166 — embarch-api tells Core what it built when it starts a study

**State:** claimed by agent/api/166-send-build-claims-when-a-study-starts, 2026-11-21 22:07
**Source:** Fleet Ready issue: embarch-api does not send build claims when it starts a study. `embarch-core` decision 110 (`decisions/signing.md`) and `embarch-core/interfaces/signing.md`, landed with `tasks/core/129`; `notes/hil/14-implementation-plan.md`, M1.5's follow-up, before M1.10.
**Issue:** EMB-238
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Core's study routes, `POST /study` and `POST /host-studies`, take `build_commit`, `build_dirty` and `build_toolchain` query parameters and carry them in the signed run record's `claimed.build`, kept apart from what Core observed. **embarch-api sends none of them**, so every record's build claim is empty. A study started through the MCP tools or the CLI sends all three, from the build it is running; **a build with no git checkout sends none**, never a made-up value.

## Why now

Publish (M1.10) and `verify` (M1.11) show the build a report was made from, and the record is signed at the end of every run, so a run started before this lands carries an empty claim for good.

## Dispatch notes

- **`embarch-core-client` is a shared crate** (`embarch-ui` path-depends on it): keep the change additive, and expect the supervisor to build `embarch-ui` and `embarch-umbrella` against your branch before landing.
- Where each value comes from (the project checkout's `HEAD`, its dirty state, which toolchain string) is this unit's decision; say what "toolchain" means here and why, and what is sent when only some of the three are known.
- **Docs near their size limit**: `decisions/client-crate.md` has 10 B left and `interfaces/config.md` 920 B, both filed against `tasks/api/165`; do not add to either, so the decision goes in a new topic file or in `decisions/studies.md`. Also near their limit: `ledger` #98 (15 B), `bench-exchange` #89 (122 B), `failure-reporting` #67 (192 B).
- Out of scope: anything Core does with the claim (it already records it), and the signed challenge before a client sends its token.

## Done when

- [ ] A study started through the MCP tool and through the CLI sends all three parameters, and a test shows them on the request.
- [ ] A build with no git checkout sends none of them (a test).
- [ ] `spec.md`, `decisions/`, `interfaces/` updated; `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope api` on both branches).
