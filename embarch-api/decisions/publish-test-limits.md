# embarch-api decisions: a Test report's limits

**Status:** active, 2026-11-26 (`tasks/api/216`, EMB-588; `notes/hil/03-test.md`, the decision rule and the false accept). Index: [../decisions.md](../decisions.md). Core's side is `embarch-core` decision 154 (`core/179`). Extends [144](publish-test-run.md) and [146](verify-test-run.md).

### 147 - A Test report prints each limit's decision rule, `w` and `U`, and `verify` rebuilds both fields Core adds

**What Core adds.** Each `tests[]` entry of `report-data.json` carries `decision_rule` (`{kind, w_multiple}`) and `limits` (per limit: `measurement`, `unit`, `lower`, `upper`, `expect`, `rule`, `w_multiple`, `u`, `k`, `u_declared`, `w`); `limits` is `[]` for a test with none, and both are `null` when Core did not find the test in `run.json`. `u` and `k` are the test's declared source for the measurement, not the study record's own uncertainty; `w` is `w_multiple × u` under a guard band and 0 under simple acceptance or with no source.

**The PDF** (`src/publish_test.rs`, `limits_section`) has a section "Limits and decision rule" after the tests table: one row per limit (test, measurement, bounds with unit, rule and its `w` multiple, `w`, `U`). `U` is `k × u`, the expanded uncertainty; where `u_declared` is false the cell says "U not declared", never a number. A test with `limits: []` says it has no limit; a test whose fields are `null` says Core could not find it in `run.json`. If any limit is judged under simple acceptance, one sentence follows: a result at a limit may be a false accept with a probability of up to 50 % (ILAC-G8), the figure `notes/hil/03-test.md` gives and no other. Both "not carried" sentences lost the per-limit rule.

**`verify` check 6** rebuilds both fields from `run.json`'s test (`limits_of` in `src/verify_test.rs`, the same rule as Core's) and compares them with `report-data.json`; a mismatch fails check 6 as `test <id>: report-data.json's limits is not what run.json gives for it`, beside the whole-field comparison. Check 4 needs no change: `U` and the other numbers are string literals of `report.typ`, which check 6 regenerates byte for byte, so check 4 admits them as it does the appendix's. A Study zip takes none of this path.

**Measured:** the fixture Test zip now carries a guard-band test (`w` 10, `U` 20) and a limitless one, passes every check, and prints each; one `w` altered in `report-data.json` fails check 6 naming the test and leaves check 3 passing. **Assumed:** the field shape is Core's `limits_of` on `origin/main` read 2026-11-26; no real Core zip was verified.
