# 220 — `embarch-core-client` reads `host_type_schema_version` from `/status`

**State:** claimed by agent/api/220-core-client-reads-host-type-schema-version, 2026-11-27 01:12
**Source:** EMB-314 — the host-type schema version has three key spellings across the suite
**Issue:** EMB-314
**Scope:** api
**Hardware:** none
**Owner:** no

## What

The suite settles on `host_type_schema_version` as the one name for
`HOST_TYPE_SCHEMA_VERSION` (decided at the split of EMB-314).
`embarch-api --json versions` already uses it; Core's `/status` serves it under
`study_designer_schema_version`, and `tasks/core/191` adds the new key **beside**
the old one. When this is done, `embarch-core-client`'s `/status` type exposes
the number as `host_type_schema_version`, read from the new key and falling back
to the old one, so it reads the same value from a Core before and after
`core/191`. Its two callers (the schema checks near `post_study` and the
other `status().await?.study_designer_schema_version` site) use the new name.

**The trap:** `#[serde(alias = "study_designer_schema_version")]` on the renamed
field fails to parse a body that carries **both** keys ("duplicate field"),
which is exactly what Core serves once `core/191` lands. Read the two keys as
two `#[serde(default)]` fields and expose one accessor (or a custom
`Deserialize`), and test three bodies: old key only, new key only, both.

Before renaming a `pub` field, grep every consumer of the crate
(`embarch-ui`, `embarch-umbrella`) for struct literals or field reads of it;
none were found at the split, but check against `origin/main`. If one exists,
keep the old field and add the accessor instead, rather than break a sibling.

`embarch doctor`'s own `/status` read is `tasks/umbrella/125`, not this task.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `crates/embarch-core-client/src/client.rs` (the status type near
  `study_designer_schema_version`, its two read sites, the doc comment that
  names it at the `validate` type)
- `src/cli.rs` (`versions --json`, for the name already in use)
- `embarch-doc/embarch-api/decisions/` (the index names where the schema check
  is decided; decision 58 is the crate's "older Core still parses" rule)

## Where the doc goes

No `embarch-api` file is in reserve. Amend the decision that owns the `/status`
schema check in place, or a short new one; `interfaces/` where it names the key.

## Done when

- [ ] The client exposes `host_type_schema_version`; a test parses an
      old-key, a new-key and a both-keys `/status` body to the same value.
- [ ] Both call sites read the new name; no consumer in the suite breaks.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`, and the crate under each feature set its consumers build it
      with, per `gate.md`); decision updated; `changelog.d/` fragment.
