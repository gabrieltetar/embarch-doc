# api: `dev-bench-hello --json`'s `schema_version` key collides with the envelope stamp and silently loses the real field

**State:** claimed — leg 050, 2026-09-08
**Promoted** from `inbox/api-dev-bench-hello-json-schema-version-collision.md` by leg 048,
unchanged apart from this line and the number. **The supervisor verified the mechanism
independently before filing**, rather than taking the reviewer's word: `src/json_out.rs`'s
`stamped()` does `map.insert(SCHEMA_VERSION_FIELD, SCHEMA_VERSION)` on an existing object, and
`insert` on a `serde_json::Map` overwrites. So the success object's `schema_version` is `1` on
every call, and the handshake's own number reaches no JSON consumer.
**Scope-note:** the drop said `embarch-api`; the scope field takes the sub-project name.
**Source:** embarch-reviewer, unit api/048 (embarch-api merge `4bd3b5e`, embarch-doc merge `13b5bf6`)
**Scope:** api
**Hardware:** none — found by reading; confirming the rendered value requires a real or mock Core, no board

## What

`src/cli.rs`'s new `dev_bench_hello()` (added in `4bd3b5e`, hunk around line 707-719)
builds its `--json` success object as:

```rust
serde_json::json!({
    "success": true,
    "schema_version": info.schema_version,
    "compatible": info.compatible,
    "firmware_version": info.firmware_version,
    "self_reported_hardware_id": info.self_reported_hardware_id,
    "probe_hardware_id": info.probe_hardware_id,
    "link_identity": info.link_identity,
})
```

`info.schema_version` here is `HelloAckResponse::schema_version` — the dev-bench
handshake's own schema-compat number, the same fact `render_hello_ack` prints in
its `core_fields` line and the same fact `compatible` is computed from.

That object is handed to `finish()`, which prints it via `json_out::pretty()`.
`json_out::pretty` calls `json_out::stamped()`, which **unconditionally
overwrites** any `schema_version` key already present with this crate's own
envelope constant (`json_out::SCHEMA_VERSION`, currently `1`) — see
`src/json_out.rs::stamped()`, `map.insert(SCHEMA_VERSION_FIELD.to_string(),
Value::from(SCHEMA_VERSION))`. So the printed `--json` object's `schema_version`
field is **always `1`**, never `info.schema_version`, and the real dev-bench
handshake schema number this call exists to report does not appear anywhere in
the JSON output at all — only in the human-text rendering.

This contradicts `embarch-api` decision 52 (`decisions/tool-wrapping.md`), which
hit exactly this collision for the `versions` subcommand and resolved it by
naming the field `host_type_schema_version` instead of `schema_version`,
explicitly reasoning: *"The object already carries decision 24's stamp under
that name, versioning this crate's JSON shape. The two counters are unrelated,
and one name over both is how a consumer comes to compare the wrong pair."*
Decision 24/50's own guard test in `json_out.rs`
(`overwrites_a_stale_schema_version_rather_than_trusting_the_caller`) proves the
stamper does this overwrite by design — meaning the collision was known and
guarded against at the envelope layer, but nothing stopped a new call site from
reintroducing the same colliding key name that decision 52 was written to avoid.

This is not a pre-existing gap: `grep '"schema_version"' src/cli.rs src/tools.rs`
finds exactly one hit, in this diff's own new code. It is api/048's own hunk,
not something it inherited from api/036.

Decisions 59/60 (`decisions/tool-wrapping.md`) are also relevant but not directly
contradicted: they require `link_identity`/the two hardware-id fields to never
render `None` as a pass. Those three fields *are* passed through correctly as
`null` on `None` in the `--json` object (they are not stamped over). The bug is
narrower and specific to the `schema_version` key.

`tests/json_surface.rs`'s new `EVERY_SUBCOMMAND` entry (`&["dev-bench-hello"]`)
does not catch this: that harness deliberately points Core at a closed loopback
port (its own doc comment: "every Core-backed subcommand takes its failure
path"), so `dev-bench-hello` only ever exercises `error_result`'s `{"success":
false, ...}` object in that test, never the success object containing the
colliding key. The test's own assertion (`value.get(SCHEMA_VERSION_FIELD) ==
Some(SCHEMA_VERSION)`) is satisfied by the stamp on the *error* object and would
pass unchanged whether or not the success-path bug exists.

## Why now

A script consuming `dev-bench-hello --json` today reads `schema_version: 1`
(the crate's JSON-shape version) believing it is the dev-bench handshake's
schema-compat number, and can never recover the real value from `--json` output
at all — only from the human-readable text. That is a silent, wrong read of
exactly the kind decisions 58/59/60 were written this same unit-chain to
prevent for the other three identity fields; it just landed on the fourth.

## Done when

- The literal key in `src/cli.rs`'s `dev_bench_hello()` success object is
  renamed to something that cannot collide with the envelope's
  `schema_version` stamp (e.g. `dev_bench_schema_version`, mirroring decision
  52's `host_type_schema_version` precedent), and `interfaces/tools.md`'s
  `dev_bench_hello` row / decision 61 note the field name if they come to
  describe the `--json` shape.
- `tests/json_surface.rs` (or a new client/cli-level test) actually exercises
  the **success** path for `dev-bench-hello --json` against a mock Core and
  asserts the renamed field carries `info.schema_version`'s real value, not the
  envelope's `1` — closing the gap that let this ship unexercised.

## Revert info

Merge SHAs: `embarch-api` `4bd3b5e`, `embarch-doc` `13b5bf6`. The bug is
contained in `src/cli.rs`'s new `dev_bench_hello()` function (added, not
modified, by this commit) — a revert of `4bd3b5e` is clean (removes the whole
new function/subcommand along with the bug) but throws away the otherwise-good
CLI-twin work; a forward fix (rename the one key, add the missing test) is
cheaper and does not require touching `embarch-doc`'s `13b5bf6` at all, since
decision 61's own text does not describe the `--json` field names.
