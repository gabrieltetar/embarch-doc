# 211 — The test ledger reads Core's run log: test_show, test_pending, test_add

**State:** claimed by agent/api/211-the-test-ledger-reads-cores-run-log, 2026-11-26 19:56
**Source:** EMB-379 — the hardware test ledger has not grown into Test
**Issue:** EMB-379
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`ledger_show`, `ledger_pending` and `ledger_add` read and write `embarch/ledger/`
in the firmware repo, rows `embarch-api` writes (`src/ledger.rs`, api decision
98). The HIL Test design has them "become `test_show`, `test_pending` and
`test_add`": "Core's run log is the record" and the repo's rows its mirror; a
test is pending "when its latest run on the current DUT image is not a pass", or
its commit was rebased away; "`test_add` makes one through Core's manual-verdict
route" (`embarch-doc/notes/hil/03-test.md`, "It grows out of the ledger",
"Selecting and rerunning"). When this is done:

- **`test_show`, `test_pending` and `test_add`, as MCP tools and CLI verbs,
  replace `ledger_*`.** `ledger_*` are removed with no alias.
- **Pending is computed from Core's run log** (`GET /run-log`: the Test run's
  `test` entries and core decision 147's manual verdicts) by the rerun rule
  above, grouped by the bench each test needs. A relayed manual verdict
  (`relayed: true`) is listed and never counted as a pass.
- **`embarch/tests/results.jsonl` mirrors the run log's test entries** on each
  call; where a row differs from the log, the log wins and the row is rewritten.
- **`test_add` calls `POST /manual-verdicts`** (core 147); with the agent's token
  its result reads "relayed by the agent".
- **`embarch/ledger/` is read as legacy**, its rows listed apart as "before Test,
  not in Core's log", and never moved or rewritten.

The owner may strike the legacy handling for moving the folder on the first call
or keeping aliases (plan choice 17). Build it on the issue's default above.

## Where to look

- `src/ledger.rs`, `src/tools.rs`, `src/cli.rs`; the existing Test tools
  (`test_propose`, `test_plan`, `run_test`, `test_status`) and `embarch/tests/`
  layout, `interfaces/tools-tests.md`, `decisions/tests.md`
- `crates/embarch-core-client/src/`: whether a `GET /run-log` and a
  `POST /manual-verdicts` method exist
- `embarch-core` decisions 111 (run log), 147 (manual verdicts) and
  `interfaces/run-log.md`, `interfaces/manual-verdicts.md`, read only
- `embarch-doc/notes/hil/03-test.md`

## Where the doc goes

A new api decision for the three tools and the mirror. **Decision `ledger#98` has
15 B left before its limit**: do not grow it; mark it superseded by the new
decision in a line that keeps it under its limit, or say in the new decision what
of 98 still stands. `interfaces/tools-ledger.md` is renamed for the new tools and
the `interfaces/tools.md` row with it. **Two files in reserve, each with its
compaction blocked on In flux: yes** (`scripts/check-doc-size.py --pressure`):

- `embarch-api/spec.md`, 1,110 B left, `tasks/api/201`. Do not write it unless
  the unit needs to; if it does, compact it out of reserve in the same commit,
  keeping `api/201`'s `Must not delete:` items.
- `embarch-api/decisions/client-crate.md`, 469 B left, `tasks/api/209`. If this
  unit adds a client method and so owes a client decision there, compact that
  file out of reserve in the same commit, keeping `api/209`'s `Must not delete:`
  items. Never file a client decision in another topic file to avoid it.

Also near their limit: `lease#90`, `test-plans#134`. Write new decisions rather
than grow those.

## Done when

- [ ] Against a fake Core, a test whose latest run on the current image failed is
      pending, and one that passed is not; a relayed manual pass does not clear it.
- [ ] A mirror row differing from the log is rewritten to the log's.
- [ ] `test_add` with the agent's token reaches the manual-verdict route and reads
      relayed.
- [ ] A legacy `embarch/ledger/` row is listed apart; the folder is untouched.
- [ ] Decision 98 marked superseded, and the interface doc renamed.
- [ ] Gate green (`cargo build --workspace`, `test`, `clippy --workspace
      --all-targets -- -D warnings`).
