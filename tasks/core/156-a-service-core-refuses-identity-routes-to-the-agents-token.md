# 156 — A service Core refuses the identity routes to the agent's token

**State:** done — service Core refuses identity routes to the agent token (decision 132)
**Source:** EMB-331 — an attested Core takes identity declarations from the agent's token
**Issue:** EMB-331
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Decision 109 says nothing is refused by scope, and only a discard is (decisions
111, 112). On an attested Core, which board, probe, instrument or signal is
which is the person's act, and the agent only proposes it
(`embarch-doc/notes/hil/12-prevention.md`, "Identity is the person's act too").
When this is done:

- With `--service`, these routes answer `403` to the agent's token, naming the
  person's surfaces (embarch-ui, the CLI with the person's token):
  `POST /probes/enroll`, `DELETE /probes/enrolled/{role}`,
  `PUT /probes/enrolled/{role}/board`, `DELETE /probes/by-serial/{serial}`,
  `POST /dev-bench/link`, `POST /signals`, `DELETE /signals/{name}`,
  `PUT /instruments`, `DELETE /instruments/{name}`, `PUT /bootload/ports`,
  `DELETE /bootload/ports`.
- A development Core is unchanged: it keeps taking them, labelled as the
  agent's as today.
- One table of the person's routes, with a test that every route of the router
  is classed, like `every_route_is_either_lease_gated_or_lease_open`.

The owner may strike this: the alternative is the standalone pass, where the
person's token first leaves the agent's reach. The decision must say so.

## Why now

The identity gate and the `bench` mark trust what was declared, and the
identity store's "Core is its only writer" means little if the agent's token
writes through Core. EMB-335 (the identity tools' refusal message) waits on it.
Where: `src/api.rs` (the router and that test), `src/token_store.rs`
(`Scope`).

## Where the doc goes

Amend decision 109 (`decisions/auth.md`) if it has room, else a new decision
with a dated pointer on 109; `interfaces/topology.md` and
`interfaces/instruments.md` name the scope each route takes. **Decisions near
or over their per-decision limit (`check-doc-size.py --pressure`):**
`signing.md` 110, `analog-capture.md` 127, `host-study.md` 95,
`stopping-a-study.md` 128, `lease.md` 93 (all over), `run-log.md` 111 (120 B
left), `instruments.md` 104 (144 B); do not grow any of them. If your work
pushes a file into reserve, file `tasks/core/<NNN>-compact-core.md` in the same
commit per `tasks/README.md`.

## Done when

- [x] A test walks the person's routes: each is `403` to the agent's token in
      service mode and served in development mode; the person's token is
      served in both.
- [x] Every route of the router is classed as the person's or not, by a test.
- [x] Decision 109 amended or pointed at; the interface docs name the scope
      each route takes.

## Outcome

New decision 132 (not an amendment: 109's file has room but 109 is a different claim; it carries a dated pointer). `token_store::PERSON_ROUTES` is the one table; `person_middleware` (inside auth, outside lease) answers 403 to the agent's token when `AppState::person_only` (set from `--service`) is true, so tests run both modes. Two tests: every `AUTH_CASES` route is in exactly one of `PERSON_ROUTES`/`AGENT_ROUTES`, and a walk of all eleven routes as each token in each mode. Debts: native Windows build not run from a worktree; embarch-api's identity tools show the 403 unexplained until EMB-335; the agent can still use the person's token if it can read the file (standalone pass).
