# 135 — Core's side of publish: a signed `report-data.json` and a signed manifest

**State:** open
**Source:** `notes/hil/14-implementation-plan.md`, unit M1.8 ("Core's side of publish"), after M1.4 (decision 109), M1.6 (decisions 111, 112) and M1.7 (decisions 113 to 115), all landed
**Issue:** EMB-223
**Scope:** core
**Hardware:** none
**Owner:** no

## What

At publish, Core writes and signs `report-data.json` and the hash manifest for one study run, so embarch-api's `publish` (M1.10) can assemble a zip whose non-prose claims and Core-produced files carry Core's signature, and `verify` checks 5 and 6 (M1.11) have something to check against.

- **`report-data.json`**, written and signed by Core from its own run log and signed records, never from anything embarch-api sends. Milestone 1 has no Test phase, so this is **a Study's** `report-data.json` only: `embarch-study-designer/interfaces/hil-run.md`, "A Study's export and check", fixes what it holds (`run_status`, per-step outcome counts, the unit or declared subject, the attestation label, who gave the go and who published, the revision) and what it must not hold (no `tests`, `requirements` or `verdicts` keys). `notes/hil/06-report-and-publish.md` ("One zip", the `report-data.json` bullet, and "What Core's signature covers") is the fuller statement; the Test-phase claims it lists (verdicts, requirement roll-up, the atlas's requirement count) are out of scope here and should be named as such in the decision.
- **Notes and prose adoptions reach Core through a route that records the token's scope and the SHA-256 of the text**, so a note's or a prose block's attribution is Core's record rather than the zip's. Notes passed with the agent's token read **"relayed by the agent"**; with the person's token, as the person's (06, "The operator's notes").
- **The manifest**: Core hashes every file it produced for the run (captures, `events.json`, `measurements.json`, its signed record, `report-data.json`, the run log's segment) and signs a manifest over those. Files embarch-api produces (the PDF, the exports, `report.typ`, the Typst packages, the prose, the notes) are **listed as embarch-api's**: Core's signature says they were in the zip, not that they are faithful (06, "What Core's signature covers"). How embarch-api hands its own files' hashes to Core, and whether one route or two carries the publish, is this unit's design.
- **The run log's tail anchor**: `embarch-core/open.md` ("The run log's tail is not anchored") says M1.8's publish must record the head from `GET /study/{id}/log` beside the manifest hash. Decision 111 already gives the `published` entry and `POST /study/{id}/published`; build on that rather than beside it.

Signing reuses decision 110's key and envelope (`decisions/signing.md`). The route shapes are this unit's; embarch-api's `publish` (EMB-225, waiting on this issue) is their consumer, so state them in `interfaces/` precisely enough that the next unit can build against them without reading Core's source.

## Why now

M1.8 is the next unit on the milestone 1 path, and EMB-225 (the zip) and EMB-226 (`verify`) are both blocked on it.

## Dispatch notes

- **`embarch-core/open.md` is in reserve** (4,851 of 5,120 B, 269 B left). `tasks/core/133-compact-core-open.md` is parked on `In flux: yes` until this unit lands, and says the compaction rides in this unit: **compact `open.md` as part of this work**, out of reserve (at or under 3,919 B), moving settled detail into `open/` verbatim with links left, and honouring 133's **Must not delete** list (every open item's owner-run step, the `icacls` debts and unexercised paths, and every decision citation). Say in your report that you did, so the supervisor closes 133 at the fold.
- **Per-decision budgets near their limit** (`check-doc-size.py --pressure`): `signing#110` is over (-2,486 B) and `run-log#111` has 201 B left. Do not grow either entry; write this unit's reasoning as new numbered decisions (`scripts/check-task-numbers.py` does not number decisions; the next Core decision is 116), in a new or existing topic file under `decisions/`, with its row in `decisions.md`'s index.
- If the design needs a schema version bump in a shared crate (`embarch-study-designer`, `embarch-topology`, `embarch-core-client`), stop and report rather than make it: that is a cross-repo pass.

## Done when

- [ ] Publishing a fixture run through Core's routes yields a signed manifest and a signed `report-data.json`, each verifying with a standard DSSE check against Core's key, in a test.
- [ ] A note entered with the agent's token is recorded as "relayed by the agent", one entered with the person's token as the person's, each with the text's SHA-256; tested over HTTP.
- [ ] The publish records the run log's head beside the manifest hash, and `open.md`'s tail-anchor item is updated to say what remains (`verify` check 8 comparing it is M1.11's).
- [ ] `report-data.json` for a Study carries no `tests`, `requirements` or `verdicts` key; tested.
- [ ] The routes are in `embarch-core/interfaces/`, the decisions numbered from 116, `spec.md` amended where it describes the run log or signing.
- [ ] `embarch-core/open.md` out of reserve per `tasks/core/133`.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
