# 174 — Core keeps a manual verdict, a unit's serial and the person's name

**State:** open
**Source:** EMB-372 — Core keeps no manual verdict, unit serial or person's name
**Issue:** EMB-372
**Scope:** core
**Hardware:** none
**Owner:** no

## What

A manual verdict today is a ledger row `embarch-api` writes in the firmware repo
(`embarch-api/src/ledger.rs`, api decision 98). Core keeps no unit serial and no
person's name. The HIL design: a manual verdict "is an entry in Core's run log,
made through a Core route that records the token's scope"; one entered with the
agent's token reads `relayed` and "never counts in a requirement's verdict or in
coverage"; the report names "the serial the engineer declares and its board
revision beside it, a person's act", and "the person's name is declared once in
Core's store with the person's token" (`embarch-doc/notes/hil/03-test.md`, "The
verdict", "The report"). When this is done:

- **`POST /manual-verdicts`**: `{test_id, definition_hash, unit_key, dut_image,
  verdict, reason, note}`, either token, entered in the run log with the token's
  scope; the agent's is marked `relayed`.
- **`PUT /units/{unit_key}`**: the declared serial and board revision, person
  token only, readable back.
- **`PUT /person`**: the person's name, person token only, readable back and
  marked as declared.
- **The agent's token on the last two is refused 403**, the way a discard of a
  failing run already is (decision 112).

Several issues wait on this one (publish, the person's terminal, `test_add`), so
keep the shapes plain and write them in the interface doc.

## Where to look

- `src/run_log.rs`, `src/token_store.rs`, `src/api.rs`
- `embarch-doc/notes/hil/03-test.md`, "The verdict", "It grows out of the
  ledger", "The report"
- `embarch-doc/embarch-api/decisions/ledger.md` (98), read only
- `embarch-doc/embarch-core/decisions/` (111, 112, 144)

## Where the doc goes

A new core decision in a new topic file. `run-log#111` has 120 B left and
`signing#110` is over its limit: point at them, do not grow them.
**`embarch-core/open.md` is in reserve** (893 B left; `tasks/core/171` is blocked,
In flux: yes): do not write it.

## Done when

- [ ] A manual verdict with the agent's token is entered and marked `relayed`;
      with the person's, it is not.
- [ ] A serial and a name with the agent's token are refused 403; with the
      person's, kept and readable.
- [ ] The run log's chain recomputes over the new entries.
- [ ] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).
