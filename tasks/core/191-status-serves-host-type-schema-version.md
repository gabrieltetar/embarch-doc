# 191 — `/status` serves `host_type_schema_version` beside the old key

**State:** claimed by agent/core/191-status-serves-host-type-schema-version, 2026-11-27 02:13
**Source:** EMB-314 — the host-type schema version has three key spellings across the suite
**Issue:** EMB-314
**Scope:** core
**Hardware:** none
**Owner:** no

## What

One number, `embarch_study_designer::HOST_TYPE_SCHEMA_VERSION`, is served under
three names: Core's `/status` calls it `study_designer_schema_version`,
`embarch-api --json versions` calls it `host_type_schema_version`, and the
constant is `HOST_TYPE_SCHEMA_VERSION`. The suite settles on
`host_type_schema_version` (decided at the split of EMB-314). When this is done,
`GET /status` carries `host_type_schema_version` with the same value, **beside**
`study_designer_schema_version`, which stays: every reader in the field today
(`embarch-core-client`, `embarch doctor`) reads the old key, and Core's
additions are additive.

The readers move in their own tasks, each reading the new key and falling back
to the old one so it works against a Core from before this task:
`tasks/api/220` (`embarch-core-client`) and `tasks/umbrella/125`
(`embarch doctor`). Nothing here waits on them and they do not wait on this.
**Say in the decision when the old key may go**: not before both readers have
landed and a released Core has served the new key, and record the removal as a
follow-up in `open.md` rather than doing it.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/api.rs` (the `/status` response struct near `study_designer_schema_version`,
  its construction, and the test that lists `/status`'s keys)
- `embarch-doc/embarch-core/interfaces/hardware.md` (the `/status` row)
- `embarch-doc/embarch-umbrella/decisions/schema-skew.md` (what `doctor`
  compares, for context only)

## Where the doc goes

**`interfaces/hardware.md` is 11,055 of 12,288 B, 4 B under its reserve line.**
Adding a key to the `/status` row must be net-neutral there (shorten the row's
own wording), or file `tasks/core/<NNN>-compact-core.md` in the same commit
(`tasks/README.md` has the shape; number from
`scripts/check-task-numbers.py --next core`). `spec.md` and
`decisions/platform.md` are in reserve under `tasks/core/186`: do not grow
them. A short new decision in a topic file with room (the index tells you which
covers `/status`), or a new topic file. `open.md` is just under its reserve
line: net-neutral or smaller.

## Done when

- [ ] `GET /status` serves both keys with the same value; a test asserts both.
- [ ] The decision names the new key as the suite's name, says the old one
      stays until both readers have moved, and `open.md` carries the removal.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `interfaces/hardware.md` updated; `changelog.d/` fragment.
