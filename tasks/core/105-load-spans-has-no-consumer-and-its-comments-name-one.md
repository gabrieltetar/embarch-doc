# 105 — `GET .../load/spans` has no consumer anywhere, and Core's own comments still name the one that decided against it

**State:** claimed by agent/core/105-load-spans-has-no-consumer-and-its-comments-name-one, 2026-10-26 04:55
**Dispatch note:** `spec.md` (9,225/10,240 B, 1,015 B left), `open.md` (4,262/5,120 B, 858 B left) and `decisions/probes.md` are in reserve and parked under `tasks/core/112` (blocked, `In flux: yes`). If you add to `spec.md` or `open.md`, remove at least as much from the same file, keeping `core/112`'s `Must not delete:` list intact; a retirement should shrink them. `decisions/stream-index.md` (decisions 65 and 66) is 10,986/12,288 B, just under reserve: if your edit leaves it above 11,059 B, file `tasks/core/<next free NNN>-compact-core.md` in the same commit. `interfaces/streams.md` is 4,225 B. Write nothing in `embarch-api`, `embarch-ui` or `suite/`; drops and `status.d/` fragments only.
**Source:** DeepSeek V4 Pro suite review 2026-10-25 (cross-repo finding 2), verified by Opus against embarch-core@40a58ccb and embarch-ui@aa5ffdaa (with embarch-api@6d664853 for the client crate)
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`GET /study/{id}/stream/{name}/load/spans` was built (`tasks/core/076`, decision 65) for one caller, `embarch-ui`'s Trace tab. `tasks/ui/065` then checked the payload against `trace.rs`, and decision 66 settled that the UI keeps its own decode permanently. That leaves a route that nothing in the suite calls. `embarch-core-client` has no method for it, `embarch-api` has no tool for it, and `embarch-ui` calls only `get_study_load` (`/load`). Two source comments still describe the plan that decision 66 closed:

- `src/study.rs:4278-4282` says the route is served "for a caller (`embarch-ui`'s Trace tab) that wants the timeline itself".
- `src/outpost_load.rs:28-37` calls the duplicated timeline arithmetic "temporarily tolerated", lasting "until the `embarch-ui` follow-up" makes the browser stop computing its own. That follow-up was taken, and the duplication stayed, permanently.

Decide whether the route stays, and record the decision as a numbered `embarch-core` decision. Either way, make the comments true.

- **Retire it.** This is the default `tasks/core/021` set when it retired `GET /logs/stream`: that route had no consumer anywhere, and the decision meant to create one had decided against it. Remove the route, its handler, `spans_answer`/`SpansAnswer` (if nothing else uses them) and the route auth sweep's row. Keep the shared `decode_with_cap` that `/load` needs. Retire decisions 65 and 66 the way `core/021` retired decision 44.
- **Keep it**, naming who it is for. If that caller is an agent, say so, and drop the client and tool follow-up to `inbox/` for `api`. Do not write `embarch-api` from here.

## Why now

- Server side: `src/api.rs:171`; `src/study.rs:4290-4296`.
- Client side: there is no `load/spans` anywhere in `embarch-api` (`crates/embarch-core-client/src/client.rs:2153-2158` is `/load` only). `embarch-ui` `src/main.rs:946` calls `get_study_load` and nothing else.
- Decision 66 (`embarch-core/decisions/stream-index.md`) says the split "is not waiting on `embarch-core` — it is permanent". `suite/features.md:37` says no live study has hit this route yet.
- Decision 64's own closing sentence has already been corrected for the same reason. These two comments were missed.

## Done when

- [ ] A numbered `embarch-core` decision says whether the route stays and why. If it stays, the decision names its caller. If it goes, it cites `core/021` as the precedent.
- [ ] If retired: the router, the route auth sweep's row count and `interfaces/streams.md` all agree, and `/load` still serves the same `LoadSummary` (the existing `/load` tests pass unchanged).
- [ ] No comment in `src/` says `embarch-ui` consumes this route, or calls the duplicated timeline temporary.
- [ ] Any `embarch-api` or suite-doc change the decision implies is dropped to `inbox/`, not written from here. `suite/features.md`'s row gets a `status.d/` fragment.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
