# embarch-study-designer decisions: the HIL test, suite and plan

**Status:** active, 2026-11-25.

What `tasks/study-designer/094` (EMB-353, the root of the HIL Test chain) decided building the types `notes/hil/03-test.md` and `04-premade-suites.md` describe. Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/hil-tests.md](../interfaces/hil-tests.md). Shapes' conventions: [hil-shapes.md](hil-shapes.md), decisions 90 and 91.

### 109 — The test, suite and plan are JSON types behind `hil-test`, hashed over RFC 8785, diffed per measurement

**`hil-test = ["verdicts", "dep:sha2", "dep:serde_json"]`**, one module (`hil_test`), host-only and additive: no existing type, wire format or schema version changes and no consumer turns it on. It reuses the verdict rules' `Limit`, `DecisionRule` and `Source` by conversion rather than by embedding, because `DecisionRule` does not refuse unknown keys and the HIL files must (decision 90); the test's own `DecisionRuleSpec` and `LimitSpec` do, with `expect` added to the limit kinds.

**Three choices are the plan's recommendations, which the owner may strike** (`notes/hil/14`): **JSON rather than TOML** (plan choice 2); **a suite's bench carrying its boards' command lines** (`idle`, `hello`, read-only lines, preconditions) **rather than a command-set file shipped with the board's firmware** (plan choice 4); **the suite's own requirement slugs rather than the atlas's `rid`** (plan choice 3). **A limit with `expect` for an observation's choice is plan choice 27**, also strikable. Striking one changes a field or a file, not the hash rule or the diff.

Where the notes were silent, each *(shape)*: `tags` sit on the test, since 03 selects by tag and names no home; `revision_range` is `{from, to}` with `null` open; `bench.config` is required; a `precondition` is required, never defaulted, so the file says it; a suite bench's saved-bench `description` is an opaque JSON object, since embarch-ui owns that shape (its decision 73); a plan's selection is `all` or `some {tests, tags}` and a test is selected by id **or** tag; `setup_terms` are `{name, unit, u, k}` uncertainty terms and never values (02: a person's act); `sources` carry `range_min`, `range_max`, `resolution`, `u` and `k`, what the acceptance-width rule reads.

**The definition hash is SHA-256 over the canonical JSON of the value as this crate serialises it**, not over the file's bytes: a test's file need not be canonical, and key order and a defaulted field's spelling must not change what a confirmation binds. The canonical form is written here (UTF-16 key order, ES6 numbers) because no JCS crate is a dependency of this one; it is checked against RFC 8785's number samples, not against a second implementation.

**`derived_diff` compares limits and sources per measurement**, so "limit widened" names the one measurement; and it leaves out `test_id`, `title`, `tags`, `schema` and `derived_from`, which decide no verdict. Measured: fixtures only; no real premade suite exists yet.
