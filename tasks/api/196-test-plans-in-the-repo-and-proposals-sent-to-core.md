# 196 — Test plans in the repo, and proposals sent to Core

**State:** done — test_propose and test_plan shipped; mock-Core tests green; real-Core verification debt in open/bench-verification.md
**Source:** EMB-376 — embarch-api has no test plan and no way to propose a DUT input
**Issue:** EMB-376
**Scope:** api
**Hardware:** none
**Owner:** no

## What

A Test needs a saved selection, the DUT's inputs with their provenance, and
custom tests, each proposed by the agent and confirmed by the engineer
(`notes/hil/03-test.md`, "The DUT's inputs", "Benches", "It grows out of the
ledger"). The ledger has `tests.toml` and nothing else (`src/ledger.rs`). When
this is done:

- **The layout, pinned here because `ui/120` reads it in the same wave:**
  `embarch/tests/suites/<suite>/` holds a custom suite, its `suite.json` and,
  per test, a `<test id>/` folder with the test file and its study (the crate's
  suite format, `embarch-study-designer` `interfaces/hil-tests.md`: a manifest's
  test `file` is relative to its `suite.json`); `embarch/tests/plans/<plan>.json`
  holds a plan; `embarch/tests/results.jsonl` is reserved for the results
  mirror (a later unit's, not written here). `notes/hil/02-study.md` writes a test's
  folder as `embarch/tests/<suite>/<test id>/`; the issue's `suites/` level is
  the one to follow, and the decision says it reads 02 that way.
- **`test_propose`** (MCP tool and CLI): a custom or derived test, a capability
  with its provenance (`measured`, `decoded`, `confirmed`, `declared`), or a
  hook mapping. It is checked by the crate first (`hil_test` shapes,
  `hil_check::check_test` where a study and bench travel with it), so a
  proposal the crate refuses is refused before Core is called, with the crate's
  reason. Then it is sent to Core's `POST /definitions` (`core/157`; `kind` is
  `test`, `capability` or `hook`), and the reply gives the hash and says the
  engineer confirms it on the card or in the terminal. A custom test proposed
  for a suite in the repo is written under `embarch/tests/suites/` too.
- **`test_plan`** (MCP tool and CLI): write or update a plan file; with no plan
  for a named suite, list the applicable tests grouped by bench
  (`notes/hil/01-modes.md`, "How an agent picks a mode").
- **Selecting a suite copies its benches into `embarch/topologies/`** in the
  saved-bench format (`embarch-ui` decision 73), never overwriting a saved
  bench: a name already taken with other content is left alone and reported
  with its diff. Say in the decision what "selecting" is (a plan naming a
  suite is the natural trigger).

The Core client crate (`crates/embarch-core-client`) gains the
`POST /definitions` call if it lacks one; that is in this repo. Turning on the
crate's `hil-test` feature for `embarch-api` is part of this unit. The rename of
the ledger tools to `test_show`, `test_pending`, `test_add`, and moving an
existing `embarch/ledger/`, are not (03's "Open").

## Why now

Core's definitions store, premade suites and card (`core/157`, `core/158`) and
the crate's checks and expansion (`study-designer/094` to `096`) have landed;
this is the agent's side of them. `run_test` and the confirmation card wait on
it, and `tasks/study-designer/097` unparks when it lands.

## Where to look

- `src/ledger.rs`, `src/tools.rs`, `src/cli.rs`, `crates/embarch-core-client`
- `embarch-doc/embarch-api/decisions/ledger.md` (98),
  `interfaces/tools-ledger.md`
- `embarch-doc/embarch-core/interfaces/definitions.md`
- `embarch-doc/embarch-study-designer/interfaces/hil-tests.md`
- `embarch-doc/embarch-ui/decisions/saved-benches.md` (73)
- `embarch-doc/notes/hil/01-modes.md`, `02-study.md`, `03-test.md`

## Where the doc goes

A new api decision for the layout and the two tools, in a topic file that fits
(a new one is fine), and `interfaces/` gives both tools and the layout. **Do
not grow these decisions, which are at or over their limit:** `ledger.md` 98
(15 B left), `lease.md` 90 (504 B over), `bench-exchange.md` 89 (122 B left),
`failure-reporting.md` 67 (192 B left). If 98 needs amending, a dated one-line
pointer to the new decision is the amendment. If your work pushes a file into
reserve, file `tasks/api/<NNN>-compact-api.md` in the same commit per
`tasks/README.md`.

## Done when

- [x] Against a fake Core, a proposed custom test arrives with its hash and the
      reply says it waits for confirmation.
- [x] A proposal the crate refuses is refused before Core is called, with the
      crate's reason.
- [x] Selecting a fixture suite copies its bench; a second selection with a
      changed saved bench leaves it and reports the diff.
- [x] `interfaces/` gives the tools and the layout; the new decision records
      it.
- [x] Gate green.
