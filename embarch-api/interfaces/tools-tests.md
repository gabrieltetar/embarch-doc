# embarch-api: test tools

**Status:** active, 2026-11-25 ([decision 134](../decisions/test-plans.md)); see [tools.md](tools.md) for the one-table premise. Each tool is also a kebab-case subcommand (`test-propose`, `test-plan`), `--project` defaulting to the session's desk's. On the CLI a JSON parameter is a file: `--definition-file`, `--study-file`, `--bench-file`, `--measured-file`, `--capabilities-file`. Code: `src/hil_repo.rs`. The crate's shapes: [hil-tests](../../embarch-study-designer/interfaces/hil-tests.md); Core's route: [definitions](../../embarch-core/interfaces/definitions.md).

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `test_propose` | `kind` (`test`, `capability`, `hook`), `definition`, `study?`, `bench?`, `measured?`, `suite?`, `project?` | The crate checks it (shape; with `study` and `bench`, `hil_check::check_test` over `measured`); a refusal is the crate's reason, one line each, `refused_before_core: true`, and Core is not called. Else `POST /definitions`; the answer has `hash`, `kept`, `checked` (`shape` or `definition`), `confirmation`, `waits_for_confirmation` and `message`. Only the engineer confirms. With `suite`, a test is then written under `embarch/tests/suites/<suite>/`, and `written` lists the paths |
| `test_plan` | `plan?`, `suite?`, `definition?`, `capabilities?`, `project?` | `plan` + `definition`: write or update the plan (`replaced` says which) and select its suite. `plan` alone: read it. `suite` alone (or with `plan`, whose capabilities it uses): `applicable_by_bench` and `not_applicable` with reasons |

**`measured`** is `{<measurement>: {by: bench\|dut\|person, source, range_min, range_max, resolution, u}}`, Core's own shape. **`study.hash`** may be left out of a test's `definition`: it is the hash of the study as the tool writes it, and is filled.

**Selecting a suite** copies each bench of its manifest to `embarch/topologies/<slug>.toml`; the answer's `selection` lists `copied`, `unchanged` and `left_alone` (each with a `diff`, `-` the saved bench's line, `+` the suite's). A saved bench is never overwritten.

**The layout**, under the project's `source_path`:

- `embarch/tests/suites/<suite>/suite.json`, and per test `<test id>/test.json` with its study file beside it; a manifest line's `file` is `<test id>/test.json`.
- `embarch/tests/plans/<plan>.json`.
- `embarch/tests/results.jsonl`: reserved for the results mirror, not written here.

Every name is `[a-z0-9][a-z0-9._-]*`. **Not verified on a bench or against a real Core** ([open.md](../open.md)).
