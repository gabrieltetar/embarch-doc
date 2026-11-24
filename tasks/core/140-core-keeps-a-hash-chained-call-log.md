# 140 — Core keeps a hash-chained log of every hardware call made to it

**State:** done — call_log.rs layer chains every gated call; decision 122; host-tested, no hardware
**Source:** notes/hil/12-prevention.md — "What Core then guarantees, in code", item 3: Core logs every hardware call made to it in a hash chain of its own, beside the run log, Live included
**Issue:** EMB-249
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core keeps a call log: `call-log.jsonl` beside `run-log.jsonl` in
`token_store::local_data_dir()`, in the run log's line shape
(`{"entry": {...}, "hash": "<sha256 hex>"}`, `entry.prev` all zeros first,
`entry.seq`), which no sweep, discard or restart touches. Follow the run log's
chain (decision 111, `src/run_log.rs`).

- **One entry per call to a route in `lease::LEASE_GATED`**, a call the lease
  refuses included, with its status. It is logged by a layer outside
  `lease_middleware`, so a refusal is seen and a new gated route is logged with
  no handler change. A host study's or a dev-bench study's own steps stay in its
  `events.json`.
- **An entry holds** the time; the method and matched route; the path
  parameters; the request body's SHA-256, and the body itself when it is JSON
  under a small stated cap; the token's `Scope`; the lease holder and purpose, or
  none; the response status; the answer's SHA-256. Where the handler resolved a
  board (role, probe serial, chip), the entry names it, with `last_images`' hash
  for that chip or "unknown".
- **Folded reads.** Consecutive identical reads (same route, request, scope,
  lease, status and answer hash) fold: the first is chained at once and its
  answer cites it; the repeats are counted in memory and written as one fold
  entry (count, first and last time, the first entry's `seq`) when a different
  call arrives, the lease ends, or Core stops cleanly. A chained entry is never
  rewritten. The reads are `POST /live/mem-read`, `POST /live/core-state`,
  `GET /serial-log`, `POST /validate` and `GET /dev-bench/hello`; every other
  gated route is an action and never folds.
- **Each gated route's answer names its entry** in a response header (`seq` and
  `hash`; a folded repeat names the first entry and its repeat number).
  `GET /call-log?from=&to=` returns a range of entries and the head; it touches
  no hardware, so it goes in `LEASE_OPEN`, and the route sweep's count moves
  with it.
- **It is Core's calls, and the doc says so**: hardware reached without Core,
  such as the topology CLI's own hardware feature, is not in it.

## Why now

The owner's HIL Live phase (`notes/hil/14-implementation-plan.md`, "The later
phases, in outline"). The live log in a firmware repo, an atlas write-back's
receipt, the signed record and `verify` check 8 all cite this log
(`notes/hil/05-live.md`, "The live log"; `notes/hil/06-report-and-publish.md`,
check 8), and three Fleet Ready issues wait on it. The fail-closed rule, quota
and reserved tail come later with the attested phase and are not this task.

**Doc headroom:** Core's `decisions/run-log.md` decision 111 has about 200 B
left and `decisions/lease.md` decision 93 about 180 B. Record the call log as a
new decision; touch 111 or 93 only by a short pointer. `decisions/signing.md`
decision 110 is already over its cap; leave it alone.

## Done when

- [x] A test calls every route of `LEASE_GATED` and finds one entry per call,
      refused calls included, each with its token's scope.
- [x] The chain recomputes from the first entry in a test, and an edited,
      removed or reordered line is reported.
- [x] Five identical `mem-read` calls in a row give one chained entry and one
      fold entry with a count of four; a different call between two reads gives
      no fold.
- [x] Every gated route's answer names its entry, and `GET /call-log` returns
      that entry and the head.
- [x] `embarch-core/interfaces/call-log.md` gives the entry and fold shapes and
      says the log holds Core's calls only; a new `embarch-core` decision
      records the call log.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
