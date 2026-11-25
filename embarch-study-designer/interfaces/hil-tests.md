# embarch-study-designer: the HIL test, suite manifest and plan

**Status:** active, 2026-11-25 (EMB-353, `tasks/study-designer/094`; the checks, EMB-354, `095`). Code: `src/hil_test.rs` and `src/hil_check.rs`, feature `hil-test` (needs `alloc`, `verdicts`, `sha2`, `serde_json`; host-only; nothing turns it on yet); fixtures `tests/fixtures/hil-tests/`, tests `tests/hil_tests.rs`, `tests/hil_checks.rs`. Why: decision 109 in [../decisions/hil-tests.md](../decisions/hil-tests.md). Conventions (JSON, `snake_case`, `schema`, unknown keys refused): [hil-shapes.md](hil-shapes.md#conventions-all-hil-files). Source: `notes/hil/03-test.md`, "One test" and "The DUT's inputs"; `04-premade-suites.md`, "Decided".

A test is a study plus verdict rules; there is no new step format. These types check **shape only**: the definition-time checks are [below](#the-definition-time-checks); a study that does not hash to `study.hash` and a hook with no mapping are a later unit's. `check()` on each file refuses only a `schema` other than 1, a `run_count` of 0 and a suite bench `description` that is not an object.

## A test (`TestDef`)

| Key | Type | Meaning |
|---|---|---|
| `schema` | integer | 1; defaults to 1 when absent on read, always written |
| `test_id`, `title` | string | The id is stable within its suite; neither decides a verdict |
| `study` | `{file, hash}` | The study by file name and SHA-256 of its bytes (an expanded template's study is kept by its own hash) |
| `requirements` | strings | **The suite's own stable slugs**, never section numbers: lowercase letter first, then `a-z 0-9 - _ .` (`is_requirement_slug`) |
| `revision_range` | `{from, to}` | Spec revisions it applies to; `null` is open on that side |
| `bench` | `{name, config}` | The bench it needs and its config, by name, both required |
| `precondition` | `reset`, `power_cycle`, `detach`, `none` | **Required, written out**; the default policy is `reset` plus each bench board's idle line before every test |
| `requires` | strings | Test ids it depends on; default empty |
| `run_count` | integer | Default 1, at least 1; each run gets its own verdict, the test's the worst run's |
| `limits` | array | `{measurement, limit}`, `limit` tagged by `kind`: `band {lo, hi}`, `at_most {max}`, `at_least {min}`, or `expect {value}` (an observation's choice: the measurement's string value must equal `value`). `LimitSpec::numeric()` gives `verdicts::Limit` |
| `decision_rule` | `{kind: simple}` or `{kind: guard_band, w_multiple}` | Required; `DecisionRuleSpec::rule()` gives `verdicts::DecisionRule` |
| `setup_terms` | array | `{name, unit, u, k}`: a declared uncertainty term (a cable's drop), never a value; a person's act; default empty |
| `sources` | array | `{measurement, unit, range_min, range_max, resolution, u, k}`: what the test declares for each `dut` measurement it limits; only the test can say them. `as_source()` gives `verdicts::Source` |
| `tags` | strings | For a plan's selection; default empty; **not verdict-deciding** *(shape: 03 selects by tag and names no home for them)* |
| `derived_from` | string, optional | `<test id>@<suite version>`; absent on a premade test |
| `template` | `{capability}`, optional | The study lines, parse patterns and limits may hold `{capability.<field>}`; filled at expansion (a later unit) |

## A suite manifest (`SuiteManifest`)

`schema`; `id`; `version`; `validated_with` (the EmbArch release); `tests`: `{test_id, file, hash}`, the hash that of the test file; `benches`: `{name, description, boards}`.

- `description` is **the saved-bench description of embarch-ui decision 73, as a JSON object this crate does not model**: embarch-ui owns that shape and checks it, and a copy of the type here would drift. Selecting a suite copies it into the firmware repo's `embarch/topologies/`.
- `boards`: per bench board, `{part, idle, hello, read_only, preconditions}`: `part` its id in `description`; `idle` and `hello` its command lines; `read_only` the lines safe to send with no confirmation; `preconditions` the ones it can perform.
- `hash()` is the manifest hash a plan pinned to a suite Core lacks confirms once.

## A plan (`Plan`)

`schema`; `suite` `{id, version, commit}` (the EmbArch commit pinned; the version is what a release compares); `select`, `{kind: all}` or `{kind: some, tests, tags}`, a test selected by its id **or** any of its tags (`Selection::selects`); `dut` `{capabilities, hooks}`; `stop_on_fail` (boolean, required).

- A capability is `{name, value, provenance}`: `value` any JSON, `provenance` `measured`, `decoded`, `confirmed` or `declared`.
- A hook is `{hook, target}`, `target` `{kind: shell, command}` or `{kind: prompt, text}`. A hook with no entry skips its test.

## The definition hash

`definition_hash(&T)` (and `TestDef::hash()`, `SuiteManifest::hash()`): **lowercase hex SHA-256 over the canonical JSON (RFC 8785) of the value as this crate serialises it.** Keys sort by UTF-16 code unit; numbers are the ES6 spelling (`canonical_json` is public); so key order and a defaulted field's spelling in the source file never change it, and a changed limit does. A confirmation binds this hash. Integers in these files stay below 2^53.

## `derived_diff(copy, premade) -> Vec<FieldDiff>`

Every verdict-deciding field of the copy that differs from the premade test, as `{field, old, new}`, `old` the premade value and `new` the copy's, `null` where one side has none. Compared: `study`, `requirements`, `revision_range`, `bench`, `precondition`, `requires`, `run_count`, `decision_rule`, `setup_terms`, `template`, and **`limits` and `sources` per measurement** (`limits.vbus_mean`), so a widened band reports that one field, an added limit `old: null`, a dropped one `new: null`. Not compared: `schema`, `test_id`, `title`, `tags`, `derived_from`. Top-level fields first in the order above, then limits, then sources, each by measurement name.

## The definition-time checks

Why: decision 110 in [../decisions/hil-tests.md](../decisions/hil-tests.md). Source: `notes/hil/03-test.md`, "Benches" and "The verdict"; `12-prevention.md`, "Operator prompts, by kind"; `13-research-phase.md`.

`hil_check::check_test(&TestDef, StudyKind, &SuiteBench, &BTreeMap<String, Measured>) -> Result<(), Vec<Refusal>>`. `StudyKind` is `Host(&HostStudy)` or `DevBench`. `Measured` is `{by: bench | dut | person, source, metrology}`, `Metrology` being `{range_min, range_max, resolution, u}`, each `Option`. A `Refusal` is `{test, field, rule, reason}`, shown as `<test id>: <field>: <reason>`; every refusal is returned, none stops the rest. Value checks: finite, above zero.

| `Rule` | Field | Refused when |
|---|---|---|
| `WrongBench` | `bench.name` | the bench given is not the one the test names |
| `BenchHasNoDut` | `bench.name` | the description holds no part with role `dut` (legacy shape: no non-null `dut`); names the bench |
| `SourceUndeclared` | `limits[i] (<measurement>)` | a numeric limit's source declares no `U`, resolution or range; names the source. A `dut` measurement's come from the test's `sources`, an instrument's and a bench board's from `measured` |
| `LimitUnjudgeable` | same | `acceptance_width` refuses with `w = decision_rule.width(U)`: by `U`, then by resolution. A band must be wider than 2 x max(w, x), a one-sided limit more than max(w, x) inside the range |
| `UnknownMeasurement` | same | a limited measurement is not in `measured` |
| `DuplicateLimit` | same | a second limit on one measurement (the derived diff keys limits by name) |
| `PromptHasNoKind` | `study.steps[i]` | a prompt declares no kind |
| `ActionUnconfirmed` | `study.steps[i]` | an action prompt names no confirming measurement, one that is not `by: bench`, or one no limit of the test reads (an `until` marker names no measurement yet) |
| `EnergisesWithoutClearance` | `study.steps[i]` | a step that energises follows a setup or action prompt with no clearance prompt between (one refusal per prompt) |
| `PreconditionUndeclared` | `precondition` | `power_cycle` or `detach`, and no bench board lists it |
| `DevBenchStudy` | `study` | the study is a dev-bench study: not in this phase |

**`energises(&HostStep, &SuiteBench)`** is public, for the go card and a prompt's "outputs on" line: an instrument set (`query` false), every DUT line, and a bench-board line the bench does not list in that board's `read_only`; a `Repeat` if an inner step does. A signal is a bench board's only when it is named by the board's `part`, so one that cannot be placed counts as energising. Prompts and waits do not. Teardown steps are not checked.

**The worked example** is `tests/fixtures/hil-tests/`: `test.json`, `suite.json` (its bench's `unit` part holds role `dut`) and `study.json` (a setup prompt, a clearance prompt, `OUTP ON`, a parsed query, a read-only status line and an observation prompt), with `vbus_mean` and `vbus_ripple` measured by a bench instrument and `led_state` by a person. It passes every check; `tests/hil_checks.rs` has one fixture per refusal.
