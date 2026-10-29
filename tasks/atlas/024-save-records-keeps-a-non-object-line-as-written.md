# 024 — `save_records` writes a non-object JSONL line back as it was, not as `{}`

**State:** open
**Source:** reviewer of `atlas/017` (fold of the leg started 2026-10-29 15:24), confirming the worker's own stated limitation: `common.read_jsonl` can yield a JSON line that is not an object; `run_check` now replaces it with `{}` in memory so the check no longer raises, and `records.save_records` (`src/embarch_atlas/records.py:171`) rewrites a whole file whenever any record in the run changes prov, which persists that `{}` over the original line.
**Scope:** atlas
**Hardware:** none — fixture records only.
**Owner:** no

## What

A record file line that parses as JSON but is not an object (a list, a number, a string) survives a `doc check` run byte for byte, and is reported as a `V:` finding naming its file and line rather than its id. Today it is silently replaced by `{}` on the first save that touches its file, which is a small deletion against `DESIGN.md` principle 4 ("Nothing is deleted for failing a check"). Before `atlas/017` the same input crashed the check, so this is new exposure, not an old bug.

## Why now

`atlas/017` made the checker tolerate the line; the save path is the half that still loses it, and the next translation session that writes a stray array is the one that finds out.

## Done when

- [ ] A fixture record file holding one non-object line among valid records: after `doc check` changes another record's prov in that file, the non-object line is unchanged on disk and its position kept.
- [ ] The line is reported as a `V:` issue naming file and line number.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `DESIGN.md` updated if the `doc check` row needs it; `changelog.d/` fragment dropped.
