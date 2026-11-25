# 094 — Types for a HIL test, a test suite and a test plan

**State:** done — types, hash and diff built behind hil-test; decision 109; gate green
**Source:** EMB-353 — no type exists for a HIL test, a test suite or a test plan
**Issue:** EMB-353
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

The crate has the verdict rules and the reducers, and `run.json`'s shape exists
only as design (`interfaces/hil-run.md`, "Design, not yet code"). There is no
type for one test, a suite or a plan. When this is done, the crate has all
three, beside `host_study.rs` and `verdicts.rs`, as JSON files under the HIL
shapes' conventions (`interfaces/hil-shapes.md`, "Conventions"):

- **A test:** `test_id`, `title`, `study` (by file name and hash),
  `requirements`, `revision_range`, `bench {name, config}`, `precondition`
  (`reset` by default, written out), `requires`, `run_count`, `limits` (a
  numeric limit, or `expect` for an observation's choice), `decision_rule`,
  `setup_terms`, and `sources`: the resolution, `U` and range the test declares
  for each `dut` measurement it limits, since only the test can say them.
  Optional `derived_from`, and `template {capability}`: a template's study
  lines, parse patterns and limits may hold `{capability.<field>}`
  placeholders, filled at expansion (a later unit), the expanded study then
  kept by its own hash.
- **A suite manifest:** `id`, `version`, the EmbArch release it was validated
  with, its tests and its benches. A suite's bench is a saved-bench description
  (embarch-ui decision 73) plus, per bench board, its `idle`, `hello` and
  read-only lines and the preconditions it can perform.
- **Requirement IDs are the suite's own stable slugs**, never section numbers.
- **A plan:** the suite id, version and commit it pins, the selection by test
  id or tag, the DUT inputs (capabilities with provenance, hook mappings), and
  `stop_on_fail`.
- **The definition hash:** SHA-256 over the canonical JSON (RFC 8785, as Core's
  files are), so key order does not change it. A confirmation binds it.
- **`derived_diff(copy, premade)`:** every verdict-deciding field that differs,
  by name, old and new.

Unknown keys are refused, as elsewhere in the HIL shapes. Three of these are
the plan's recommendations, which the owner may strike, and the decision must
say so: JSON rather than TOML (plan choice 2); a suite's bench carrying its
boards' command lines rather than a command-set file shipped with the board's
firmware (plan choice 4); the suite's own requirement slugs rather than the
atlas's `rid` (plan choice 3). Limits with `expect` are plan choice 27.

This is additive: no existing type, wire format or schema version changes, and
no consumer is touched. If you find you need to change an existing public type,
stop and say so in the task file rather than doing it.

## Why now

EMB-353 is the root of the HIL Test chain: the definition-time checks
(EMB-354), the expansion into `run.json` (EMB-355), Core's definitions and
confirmations (EMB-363), embarch-api's plans, the suites and the UI's config
guard (EMB-385) all wait on these types. Design: `embarch-doc/notes/hil/03-test.md`,
"One test" and "The DUT's inputs"; `notes/hil/04-premade-suites.md`,
"Decided"; `notes/hil/14-implementation-plan.md`.

## Where the doc goes

The shapes go in a new `interfaces/hil-tests.md`, indexed from `hil-shapes.md`.
The new decision goes in a new topic file (`decisions/hil-tests.md`), with a
dated pointer on decisions 90 and 91 only if it fits. **Decisions near their
per-decision limit (`check-doc-size.py --pressure`):** `versioning.md` 12 (67 B
left), `host-parse.md` 108 (188 B left), `authoring.md` 73 (130 B left); do not
grow them. If your work pushes a file into reserve, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit per
`tasks/README.md`.

## Done when

- [x] A fixture test, suite and plan round-trip; unknown keys are refused.
- [x] The definition hash is the same for a test with its map keys reordered,
      and differs for a changed limit.
- [x] A copy of a fixture premade test with one limit widened reports exactly
      that field, old and new.
- [x] `interfaces/hil-tests.md` gives every field, and a new decision records
      the choices above, marking the three the owner may strike.
- [x] Gate green (`../../embarch-fleet/gate.md`): `cargo build`, `cargo test`,
      `cargo clippy --all-targets -- -D warnings`, under each feature set the
      crate's consumers build it with (no features, `alloc`, `std`, and
      `--all-features` at least).
- [x] `spec`/`decisions`/`open.md` updated, `changelog.d/` fragment dropped,
      `status.d/` fragment for anything suite-level it made false.
