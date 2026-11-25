# 159 — A Test run's go takes the lease and starts the run

**State:** open
**Source:** EMB-365 — a Test run cannot hold the bench lease or start on the person's go
**Issue:** EMB-365
**Scope:** core
**Hardware:** none
**Owner:** no

## What

A Test run outlives the session that prepared it, has gaps between its
studies, and starts only on the engineer's go (`notes/hil/03-test.md`, "A run",
items 1 and 4, and "Selecting and rerunning"; `notes/hil/12-prevention.md`,
item 5). Today the lease belongs to a session (`src/lease.rs`, `LeaseSlot`),
nothing starts on a go, and a running study refuses every gated route but its
cancel only while `study_lock` is held (`core/143`). When this is done:

- **`POST /test-runs/{run_id}/go`, the person's token only** (the agent's is
  refused `403`). The body carries the nonce `core/158`'s card issued
  (`go:<run_id>:<run_hash>`, decision 133's store), `run.json`'s hash and the
  run id; each must match, the nonce is used once, and an expired one is
  refused. Each refusal names which of replayed, expired or mismatched it is.
  Also refused, saying why: the session that prepared the run no longer holds
  the lease; an input the card listed as unconfirmed is still unconfirmed.
  Decision 134 records that the registered hash goes stale after a later
  confirmation (`confirmed` is blanked before hashing); decide whether the go
  re-expands or requires a fresh prepare, and say so in the decision.
- **The lease moves to the run.** The holder becomes the run; the session's
  lease token is refused `409` naming the run on every gated route until the
  run ends; at the end or on a cancel the lease returns to the session under its
  old token with its TTL restarted.
- **A run lock**, held from the go to the end and checked by `lease_middleware`
  as `study_lock` is, so the gaps between a run's studies are guarded too.
  Reads of the run's status are open. The exceptions the executor will add (a
  prompt's answer, the setup calls between benches) are EMB-366's, not this
  unit's; leave a clear place for them.
- **`POST /test-runs/{run_id}/cancel`** is admitted from either token, is not
  lease-gated, ends the run, and is recorded in the run log with its token's
  scope.
- **The idle release** (decision 123, `IDLE_RELEASE`) never takes a run's
  lease, so a run longer than 30 minutes keeps it.

The executor that actually runs the studies is EMB-366 and is not this unit:
here the run's state is "started" between the go and an end or a cancel, and a
test can end it through whatever seam you leave for the executor.

## Why now

`core/158` landed the prepare route, the card and the go nonce; this is the
route that consumes the nonce. EMB-366 (the executor) waits on it.

## Where to look

- `src/lease.rs` (`LeaseSlot`, `admit`, `IDLE_RELEASE`), `src/api.rs`
  (`lease_middleware`, `STUDY_CANCEL_ROUTE`), the `core/158` test-runs module
- `embarch-doc/embarch-core/decisions/lease.md` (93), `lease-idle.md` (123),
  `host-study.md` (95), `test-runs.md` (134), `interfaces/test-runs.md`
- `embarch-doc/notes/hil/03-test.md`, `12-prevention.md`

## Where the doc goes

A new core decision for the go and the run's lease, amending 93 and 123 by a
dated pointer each. **Decisions over their per-decision limit: do not grow
their bodies** — `lease.md` 93 (51 B over), `host-study.md` 95 (799 B over),
`definitions.md` 133 (233 B over), `stopping-a-study.md` 128 (114 B over),
`signing.md` 110, `analog-capture.md` 127. A dated one-line pointer on 93 and
123 naming the new decision is the amendment. `run-log.md` 111 has 120 B left.
`open.md` sat 7 B above reserve at `core/158`; keep this unit's open items in
the new decision. `interfaces/test-runs.md` gains both routes, and
`DOCUMENTED_ROUTE_COUNT` moves with them. If your work pushes a file into
reserve, file `tasks/core/<NNN>-compact-core.md` in the same commit per
`tasks/README.md`.

## Done when

- [ ] A go with the agent's token is refused `403`; a replayed, expired or
      mismatched go is refused naming which.
- [ ] After the go, a reset with the session's lease token is refused `409`
      naming the run; after the run ends, it is admitted again.
- [ ] A cancel with either token ends the run and is recorded with its scope.
- [ ] A run longer than 30 minutes keeps its lease (test the idle release
      against a run holder, with a fake clock).
- [ ] Decisions 93 and 123 amended by pointer; the new decision records it.
- [ ] Gate green.
