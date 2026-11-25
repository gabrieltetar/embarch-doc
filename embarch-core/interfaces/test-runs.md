# embarch-core: the test-run routes

**Status:** active, 2026-11-25 (`tasks/core/158`, [decision 134](../decisions/test-runs.md)). Index: [../interfaces.md](../interfaces.md).

Both take either token and are lease-open (a file and a rendering, never a port). Errors are plain text. Nothing here starts a run.

| Method | Path | Body | Response |
|---|---|---|---|
| `POST` | `/test-runs` | `{run, plan, suite?, studies}`: `run` is `run.json` (`embarch-study-designer`'s `RunJson`); `plan` the hash of a kept `plan`; `suite` the hash of a kept suite manifest, or absent for the premade suite the plan's id and version name; `studies` `{<study.file>: <host study>}` | `201 {run_id, run_hash, lease_holder, duration_bound_ms}`; `422` a definition Core does not keep, a manifest test it cannot resolve, a `plan_hash` that is not the plan's, or **a `run.json` it does not reproduce, naming the first differing key**; `409` the `run_id` is already prepared; `400` a `run_id` outside `[A-Za-z0-9_-]{1,128}` or a malformed hash |
| `GET` | `/test-runs/{run_id}/card` | none | `200 {run_id, run_hash, lease_holder, prepared_utc_ms, card, nonce, expires_utc_ms}`; `nonce` and `expires_utc_ms` are `null` unless the token is the person's; `404` |

`run_hash` is the hash of Core's own re-expansion, in which each capability's and hook's `confirmed` is Core's record; the comparison with the caller's `run.json` blanks `confirmed` on both sides. `lease_holder` is the name of the lease holder when the run was prepared, `null` with none.

**`card`**: `suite {id, version}`, `standard {name}`, `dut {declared_serial, board_revision, capabilities, hooks}`, `stop_on_fail`, `benches [{name, tests}]`, `duration_bound_ms`, `unconfirmed [{kind, name, hash}]` (`suite`, `capability`, `hook` or `test`; read from the run log at each request), and `tests`, each:

| Key | Meaning |
|---|---|
| `test_id`, `title`, `definition_hash`, `requirements`, `precondition`, `run_count`, `step_budget_ms` | from `run.json` |
| `origin`, `diff` | `premade`, `derived` or `custom`; for a copy `{from, fields: [{field, old, new}]}` (the crate's `derived_diff` against the premade test it names) or `{from, unavailable}` |
| `prompts` | `[{list, step, text, kind, bench_config, timeout_ms}]`, `kind` `setup`, `action`, `observation`, `clearance` or `null` |
| `energising` | `[{list, step, target, line}]`: each step `hil_check::energises` says powers something, with the line it sends; `list` is `steps` or `teardown` |
| `limits` | `[{measurement, unit, lower, upper, expect, U, k, w}]`; `U` and `k` from the test's source for the measurement (`null` where it declares none), `w` = `w_multiple` times `U` |
| `decision_rule`, `setup_terms` | `{kind, w_multiple}`; `[{name, unit, U, k}]` |
| `study` | `{file, hash, bytes_checked_against_hash}`; the last is `false`: Core does not check a study's bytes against `study.hash` yet |

**Every string a definition, a study or `run.json` wrote is `{"agent_text": "<string>"}`**; a surface escapes it. That includes every string inside a free value — a capability's `value`, a hook's `maps_to` (`{"shell": {"agent_text": cmd}}`), a diff's `old` and `new` — whose object keys stay plain. Numbers, hashes, kinds and Core's own words are plain.

A go nonce is 32 random bytes in hex, single use, ten minutes, in memory, from the store of [definitions](definitions.md); it is issued for `go:<run_id>:<run_hash>`. A prepared run is `test-runs/<run_id>.json` in the store.
