# 182 — A swept run's restore skips the call-log segment, and republishes

**State:** claimed by agent/api/182-restore-skips-the-call-log-segment, 2026-11-23 22:05
**Source:** worker of `core/145` (2026-11-23): Core now writes `call-log-segment.jsonl` into a published revision and names it in the signed manifest
**Issue:** EMB-288
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`src/publish.rs` `restore_from_zip` PUTs every manifest subject that is not in
`CORE_PUBLISH_FILES` (four names today) to Core's
`PUT /study/{id}/restore/{name}`. Since `core/145`, a published zip can carry
`call-log-segment.jsonl` as a manifest subject. Core refuses to restore it with
`422` ("is written by a revision, not restored": `embarch-core/src/publish.rs`
`restore_handler` and `PUBLISH_FILES`), so republishing a swept run whose
earlier zip held the segment fails.

When this is done, the call-log segment is skipped on restore like
`report-data.*` and `run-log-segment.jsonl`: Core rebuilds it on publish from
its call log, which nothing sweeps. Add the name to `CORE_PUBLISH_FILES` (the
array's length changes with it) and keep `restore_from_zip` reading that one
list.

Checking the segment itself in `verify` is `api/183`'s, not this unit's.

## Why now

This bites every zip published since `core/145` landed, the first time its run
is swept and republished.

**Burndown leg: no new numbered decision.** If a decision needs amending, amend
it in place. If the work needs a new decision, stop and say so in this file and
in your report.

## Done when

- [ ] A test restores a fixture zip whose manifest names
      `call-log-segment.jsonl`, and the fake Core receives no PUT for it.
- [ ] A test names the file in `CORE_PUBLISH_FILES`.
- [ ] `interfaces/` text that lists the files Core writes on publish names the
      segment, if any such list exists.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `spec.md`/`decisions.md`/`open.md` updated where they say what restore
      skips, `changelog.d/` fragment dropped.
