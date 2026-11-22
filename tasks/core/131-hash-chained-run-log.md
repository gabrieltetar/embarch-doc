# 131 — Core keeps a hash-chained run log, and retention sweeps no capture before publish

**State:** done — on agent/core/131-hash-chained-run-log, 2026-11-21
**Source:** Fleet Ready issue: Core has no hash-chained run log. `notes/hil/14-implementation-plan.md`, unit M1.6 (after M1.5, landed as `tasks/core/129`); `notes/hil/13-research-phase.md`, "Many scans, few reports", for the discard rules; `notes/hil/06-report-and-publish.md` for what publish and `verify` check 8 read from the log.
**Issue:** EMB-221
**Scope:** core
**Hardware:** none
**Owner:** no

## What

- **One run-log entry per study run**, device and host studies both, each chained to the one before it by hash, so a reader can recompute the chain and see a run removed or reordered. The log is **never swept**: retention, a discard and a restart all leave it whole.
- **The manifest hash added on publish**: a way to record, against a run's entry, the hash of the manifest it was published under. Publish itself is M1.8's (`embarch-core`) and M1.10's (`embarch-api`); this unit provides the append and a test that drives it with a fixture hash.
- **Retention sweeps no capture before publish.** Today `EMBARCH_STUDY_RESULTS_KEEP` sweeps by count at `POST /study` (`interfaces/result-layout.md`). An unpublished run is a recorded scan, and its captures stay until something discards them.
- **A discard of a run's captures**, by either token, leaving the run's log entry and capture hashes in place and recording "captures discarded" with the scope of the token that did it. **Except** a run that failed, errored or was inconclusive, or one a published zip rests on: only the person's token may discard those, and the agent's is refused.
- **A route returning a publish's entry and the log head**, which publish and `verify` check 8 read.

## Why now

M1.8 (Core's side of publish) needs it, and M1.6 was waiting only on M1.5's signing, which landed.

## Dispatch notes

- **This is the first route Core refuses by scope.** Decision 109 carries the scope on every request and refuses nothing by it; read it, and `token_store::Scope`, before writing the discard. Say in your decision how the refusal reads to an agent (status and message), since an agent will meet it.
- **"A pending requirement" is a Test-phase thing** that milestone 1 does not have; leave the hook where it would go and say so in `open.md`, rather than inventing a requirement store.
- Whether the log entry carries the run record's hash (`record.dsse.json`, decision 110) is yours to decide; say why either way.
- **Decision 110's declarations ledger is in memory** (`open.md`), so a run's record vouches only from `witnessed_since_utc_ms`. Persisting it is not in this unit's ask and Core's protected store is the attested phase's; if the run log is a natural home for it anyway, say so in `open.md` rather than building it.
- **Changing retention changes what an engineer's disk holds.** Record the cost in the decision, and what an engineer does about it (the discard route).
- **If this unit would bump a schema version** (`GET /status`'s `schema_version` or the shared crate's `HOST_TYPE_SCHEMA_VERSION`), stop and report it rather than bump: a schema bump needs an announcement window the supervisor runs.
- **`embarch-core/spec.md` is in reserve: 9,529 of 10,240 B, 711 B left**, and its compaction task, `tasks/core/130`, is parked on `In flux: yes`. That park does not cover you: **compact `spec.md` as part of this unit** by moving reference text verbatim into a new `spec/` file with a link left behind, until `check-doc-size.py --pressure` no longer lists it. Carry `core/130`'s **Must not delete** list: the invariants (every route takes the token but `POST /auth/challenge`, the route sweep, the two scopes) and every decision citation. Say in your closing note that you did, and the supervisor closes `core/130` at the fold.
- **Decisions near their size limit**: `signing` #110 is already 2,521 B over, so do not grow it; `lease` #93 has 182 B left. A new topic file (`decisions/run-log.md`) is the expected home for this unit's decision.
- Out of scope: `report-data.json`, the manifest and its signing (M1.8), the zip (M1.10), `measurements.json` (M1.7).

## Done when

- [x] The chain recomputes in a test, and a test shows a tampered or removed entry breaks it.
- [x] A discard of a failing run's captures with the agent's token is refused, the same discard with the person's token succeeds, and both leave the entry and its capture hashes in place.
- [x] Retention no longer sweeps an unpublished run's captures (a test).
- [x] `spec.md`, `decisions/`, `interfaces/`, `open.md` updated; `spec.md` out of reserve; `changelog.d/` fragment dropped; a `status.d/` fragment for `embarch-token.md` if the token's lifecycle or a refusal by scope changes what it says.
- [x] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope core` on both branches). The native Windows build is a debt, recorded, not a gate item.

## Closing note

Built `src/run_log.rs` (decision 111, `decisions/run-log.md`, `interfaces/run-log.md`): chained `run-log.jsonl`, four lease-open routes, the discard refused `403` to the agent on a run that did not end clean or is published, and retention (`stream_store::sweep_study_results`, `GET /studies`) that spares unpublished runs. No schema version bumped (new routes only). The log entry carries the record's hash (reasons in the decision).

**`spec.md` compacted in this unit**: §3's deployment and release-assets text moved verbatim to `spec/deployment.md`, a pointer left under the same `### Release assets` heading so the proposal's anchor still resolves; the invariants and every decision citation kept. 7,965 B now, out of reserve. **The supervisor can close `core/130` at the fold.**

**Debts:** native Windows build not run (host-side only); `run-log.jsonl` `icacls` lockdown unrun (in `open.md`); no client sends the person token yet (`tasks/api/162`, `tasks/ui/111`), so the discard is unexercised over a real Core.
