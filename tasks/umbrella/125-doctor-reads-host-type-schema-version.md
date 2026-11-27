# 125 — `embarch doctor` reads `host_type_schema_version` from Core's `/status`

**State:** done — doctor reads host_type_schema_version with study_designer_schema_version fallback; three-body test; schema-skew amended
**Source:** EMB-314 — the host-type schema version has three key spellings across the suite
**Issue:** EMB-314
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

The suite settles on `host_type_schema_version` as the one name for
`HOST_TYPE_SCHEMA_VERSION` (decided at the split of EMB-314). `doctor` already
reads that key from `embarch-api --json versions`, but reads Core's `/status`
under `study_designer_schema_version`; `tasks/core/191` adds the new key to
`/status` **beside** the old one. When this is done, `doctor`'s authenticated
`/status` read takes `host_type_schema_version` first and falls back to
`study_designer_schema_version`, so it reads the same value from a Core before
and after `core/191`; the internal field, the check's messages and the doc
comments use the new name (a message about a Core serving neither key names
both, since an old Core only knows the old one). Test three bodies: old key
only, new key only, both.

`embarch-core-client`'s own read is `tasks/api/220`, not this task.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/doctor.rs`: `AuthedStatus` and its parse (near the
  `.get("study_designer_schema_version")` call), `check_schema_versions`, the
  doc comment that contrasts the two keys, the tests that build `/status`
  bodies with the old key
- `embarch-doc/embarch-umbrella/decisions/schema-skew.md` (names Core's served
  key twice)

## Where the doc goes

**Reserve, at dispatch:** `open.md` is 4,553 of 5,120 B, 567 B left, and its
compaction task `tasks/umbrella/127` is parked on `In flux: yes`. Do not grow
`open.md`; if you must edit it, compact it in the same unit, keeping
`umbrella/127`'s `Must not delete:` list. Amend `decisions/schema-skew.md` in
place where it names the key; `interfaces/doctor-chain.md` if a check row
names it.

## Done when

- [x] `doctor` reads the new key with the old as fallback; a test covers all
      three bodies.
- [x] Messages and docs use `host_type_schema_version`.
- [x] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
