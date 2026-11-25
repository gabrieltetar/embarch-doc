# 158 — Core prepares a Test run and serves its go card

**State:** done — POST /test-runs and the go card served; gate green on Linux, native Windows build a debt
**Source:** EMB-364 — Core cannot prepare a Test run or render what the go would start
**Issue:** EMB-364
**Scope:** core
**Hardware:** none
**Owner:** no

## What

The go card shows the person exactly what will run, from Core's own record of
it. No Core route takes a `run.json` today. `notes/hil/03-test.md` ("A run",
"Selecting and rerunning", "The verdict") says `run_test` prepares a run and
never starts one: embarch-api sends `run.json` and its definitions with the
agent's token, and Core re-expands it, registers a prepared run with its id,
and renders that run's card; Core refuses a `run.json` it does not reproduce
from confirmed definitions and inputs. When this is done:

- **`POST /test-runs`** (agent token) takes `run.json` and the hashes of its
  definitions. Core re-expands through the crate's `hil_expand::expand`
  (`study-designer/096`, decision 111) from the definitions it keeps
  (`core/157`, decision 133) and its premade suites, compares
  `RunJson::hash()`, and refuses a mismatch naming the first differing key. A
  reused `run_id` is refused (plan choice 9).
- **A prepared run** is registered under its id: `run.json` kept by hash, and
  the session's lease holder at that moment recorded with it.
- **`GET /test-runs/{id}/card`** serves the card's data: the tests per bench,
  every prompt with its kind, each energising step with its lines (the crate's
  `hil_check::energises`), each custom or derived test's diff against what was
  confirmed, every input still unconfirmed, every limit with its `U` and `w`,
  and the duration bound from `hil_expand::duration_bound`. Every string the
  agent wrote is marked as such, so a surface escapes it.
- **With the person's token the card carries a nonce for the go**, valid ten
  minutes and single use (plan choice 10, the lifetime). With the agent's token
  it carries none. `core/157` already issues a single-use ten-minute nonce for a
  confirmation card (decision 133, in memory); reuse that store's shape if it
  fits, and say so in the decision either way.
- **An unconfirmed input does not refuse the prepare**: it is listed on the
  card, and the go (a later unit) refuses it.

The decision must name plan choices 9 and 10 as the owner's to strike. Starting
a run is out of scope: nothing here powers anything or takes the bench.

## Why now

`study-designer/096` (EMB-355) landed `expand`, `RunJson::hash()` and
`duration_bound`, and `core/157` (EMB-363) landed the definitions store and the
confirmation nonce, which together were this issue's blockers. It heads the
Test chain: EMB-365 (the go and the lease) and everything after it wait on it.

## Where to look

- `src/api.rs` (the router, `AppState`, `DOCUMENTED_ROUTE_COUNT`), and
  `core/157`'s definitions and confirmation handlers and its nonce store
- `src/token_store.rs` (`PERSON_ROUTES`, `CONFIRMATION_ROUTES`) for how a route
  is scoped to one token
- `embarch-study-designer/src/hil_expand.rs` (`expand`, `RunJson`,
  `duration_bound`), `src/hil_check.rs` (`energises`), behind the `hil-test`
  feature Core already enables
- `embarch-doc/notes/hil/03-test.md`, "Selecting and rerunning";
  `notes/hil/12-prevention.md`, items 4 to 6;
  `embarch-doc/embarch-study-designer/interfaces/hil-run.md`

## Where the doc goes

A new decision in a new `decisions/test-runs.md`, and a new
`interfaces/test-runs.md` giving the routes and the card's shape.
**Decisions near or over their per-decision limit; do not grow them:**
`definitions.md` 133 (233 B over), `run-log.md` 111 (120 B left), `lease.md` 93
(51 B over); reference them from the new decision instead. No `core` file is in
reserve. If your work pushes one into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md`.
Do not edit `embarch-study-designer/interfaces/hil-run.md`: it is the
study-designer's, and it is in reserve.

## Done when

- [x] A fixture `run.json` Core reproduces is registered and its card served;
      the same with one limit edited is refused, naming the limit.
- [x] The card lists an unconfirmed input, each prompt's kind, each energising
      step and the duration bound.
- [x] The nonce is in the card for the person's token only.
- [x] A reused `run_id` is refused.
- [x] A decision and `interfaces/test-runs.md` give the routes and the card's
      shape.
- [x] Gate green; the native Windows build recorded as a debt.

## Debts

- **Native Windows build not run** (`embarch-core`): host-side half shipped; the Linux gate is green. Verify with `cargo build` from the main checkout over UNC once landed.
- **Three gaps, in decision 134's "Not here"**: a study file is not checked against `study.hash`; the benches that exist are assumed from `run.json`; the registered run's hash includes the confirmations at the prepare (EMB-365 decides). Filed as issues where another repo owns the fix.
