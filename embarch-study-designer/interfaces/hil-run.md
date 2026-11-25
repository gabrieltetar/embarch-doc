# embarch-study-designer: `run.json`

**Status:** active, 2026-11-25. Part of the HIL file shapes ([hil-shapes.md](hil-shapes.md), the index; conventions, verdict spellings and the measurement shape are there). Design, not yet code. Choices the notes left open: [decisions/hil-shapes.md](../decisions/hil-shapes.md), 90 and 91.

## `run.json`

**The resolved run** (`notes/hil/03-test.md`, "A run" and "Selecting and rerunning"). Written by embarch-api from the selection, **re-expanded by Core through the shared crate**, which refuses one it does not reproduce from confirmed definitions and inputs; hashed, kept by Core, carried in the zip, and what `verify` recomputes against (06). **A Test's file: no unit of milestone 1 writes it** (a Study has no `run.json`, only a signed study file); the shape is fixed now because M1.3 reads it and M1.5 signs it as a subject. **The expansion is `hil_expand::expand`** (decision 111, [below](#expansion)).

Top level, all required unless marked:

| Key | Type | Meaning |
|---|---|---|
| `schema`, `run_id` | integer, string | `run_id` is **written by the caller**, a fresh random id; `expand` takes it as an argument and Core refuses one it already holds (plan choice 9: Core assigning it is the alternative, which the owner may strike) |
| `suite` | `{id, version, commit}` | The suite's name, version and commit (03: "the suite's commit"); for a custom suite `commit` is `null` where the tree is untracked and the definition hashes carry the identity |
| `plan_hash` | hash or `null` | The test plan's; `null` for an unsaved selection |
| `standard` | `{name, revision}` | The standard and revision the engineer confirmed (03, "The report") |
| `dut` | object | The unit's inputs: `hardware_id` (string or `null`, where read-out protection blocks the read), `declared_serial`, `board_revision`, `capabilities`, `hooks` |
| `resumes` | run id, optional | Absent unless this run resumes an `interrupted` one (03, item 9) |
| `options` | `{stop_on_fail: bool}` | Run options; `stop_on_fail` default `false` (03, item 5) |
| `benches` | array | In run order (the plan's `bench_order`, else the suite's): `{name, tests: [test_id…], boards}`; the run groups by bench (03, item 1). **`boards`** is `[{part, idle, hello}]`, the bench's boards' idle and hello lines from the suite's bench, so the smoke check and the default precondition need no second file |
| `tests` | array | One entry per expanded test, below |

**`dut.capabilities`**: an array of `{name, value, provenance}`, `provenance` one of `measured`, `decoded`, `confirmed`, `declared` (03's table). **`dut.hooks`**: `{name, maps_to}` (every mapped hook, and every hook a selected or `hook_unmapped` test needs, by name) where `maps_to` is `{shell: "<command>"}`, `{prompt: "<text>"}` or `null` (unmapped, which skips its tests with `hook_unmapped`). Each capability and hook carries `confirmed: {hash, scope, at_utc_ms, surface}` (`scope` `capability:<name>` or `hook:<name>`; `null` where unconfirmed) (`surface` `ui` or `cli`), the confirmation Core holds (03: "who confirmed what, when and through which surface") *(shape: the keys)*.

**One test entry:**

| Key | Type | Meaning |
|---|---|---|
| `test_id`, `title` | string | One entry per concrete pass: a template expanded once per PDO has one entry per PDO, ids suffixed `#<n>` *(shape)* |
| `definition_hash` | hash | Of the test's definition as confirmed (03: "a custom or derived test, whole, by the hash of its definition"); an unmodified premade test has it too, pinned by `suite` |
| `derived_from` | `"<test id>@<suite version>"`, optional | Present on a copy of a premade test (03); absent otherwise |
| `expanded_from` | `{capability, value}`, optional | The capability value a template was expanded for |
| `study` | object | `{kind: "host" or "dev_bench", hash, file}` (an expanded template's study is canonical JSON, named `<stem>.<n>.json`, hashed over those bytes): the study it runs, by the hash of the signed study file and its name in the zip; the study is not inlined |
| `requirements` | array of strings | The requirement IDs it claims |
| `revision_range` | `{from, to}` | Of the standard it applies to (03) |
| `bench` | `{name, config}` | The bench and its config, by name (03) |
| `precondition` | `reset`, `power_cycle`, `detach` or `none` | 03; the default `reset` is written out, never implied |
| `requires` | array of test ids | 03 |
| `run_count` | integer, at least 1 | 03, default 1 |
| `decision_rule` | `{kind, w_multiple}` | `kind` `simple_acceptance` or `guard_band`; `w_multiple` the multiple of each measurement's `U` that is the band's w (`1.0` by default for a premade test, 03); `0` under simple acceptance *(shape: the keys)* |
| `limits` | array | `{measurement, unit, lower, upper}` (and `expect`, the string an observation's measurement must equal, with both bounds `null`): the **tolerance limits**, either bound `null` for a one-sided limit, `unit` from the study's parse or the test's source or `null`; the acceptance limit is derived from them and w, never stored *(shape)* |
| `setup_terms` | array | The declared setup terms added to a `U`: `{name, unit, U, k}` (02) *(amended: the test's term carries `k`; no `scope`)* |
| `sources` | array | What the test declares for each `dut` measurement it limits: `{measurement, unit, range_min, range_max, resolution, U, k}` *(amended: it decides a verdict)* |
| `hooks` | array of strings | The hooks the test needs mapped *(amended)* |
| `step_budget_ms` | integer | The worst case of one run: every step's `timeout_ms` and `delay_before_ms` (a prompt's timeout is its deadline), a `Repeat` once per pass, teardown included *(amended)*; `duration_bound` is the sum of it times `run_count`, so the go card's bound needs no study |
| `prompt_kinds` | array | One per prompt in the study: `{step, kind}`, `kind` one of `setup`, `action`, `observation`, `clearance` (03: part of what is confirmed) |

The go card, the run record's selection (03, item 10) and the verdict rules read these keys; **a field of a test that decides a verdict and is missing from this list is a defect in this doc**, to be amended with M1.3's first fixture.

## Expansion

`hil_expand::expand(suite, plan, dut, ctx)` returns `run.json`, the **selection record** and the expanded studies (decision 111). Every test of the suite gets one status in the record, which Core signs (03, "A run", item 10):

| `status` | When |
|---|---|
| `not_applicable` | An `applies_when` condition fails, or a template's capability is absent or has no values; `reason` names it |
| `not_selected` | Applicable, and neither picked by the plan nor pulled in by a selected test's `requires` |
| `hook_unmapped` | Picked, and a hook it needs has no mapping |
| `bench_missing` | Picked, and its bench is not among the benches that exist |
| `selected` | In `run.json`; `reason` is "required by X" where a `requires` pulled it in; a template lists its `expanded` ids |

A template expands once per element of its capability's value (array order, ids `<id>#<n>` from 1, `expanded_from` set). A measurable capability's check (a test whose `checks` names it) is `required` by every test expanded from it and runs first on its bench. Two runs of the same inputs give the same bytes and the same hash (RFC 8785, `RunJson::hash`) whatever order the suite lists its tests in.

## A Study's export and check

Moved to [hil-study-export.md](hil-study-export.md): `run_status`, what a Study's run exports, its JUnit and OCP T&V exports, and what `verify` checks and cannot recompute (06's checks 0 to 9).
