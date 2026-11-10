# 046 — Check K reads side-by-side MIN/TYP/MAX groups and a lone TYP column

**State:** done
**Source:** Linear issue EMB-35, filed by a session
**Issue:** EMB-35
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Check K reads each MIN/TYP/MAX group of a table header on its own when two groups sit side by side in one header band, and reads a table whose only value column is TYP. A table K still cannot read is a K warning (`K_WARN`), never a failing `disagree`.

Today `DocText.columns` builds each header as a dict keyed by the header word (`{HDR[w[4].upper()]: x}`), so when a band holds two groups the second group's x-positions overwrite the first's and one group's values land in the wrong column. A band counts as a header only with at least two of the words (`len(h) >= 2`), so a lone TYP column is not a header at all. `compare_columns` then reports `K: {"disagree": ...}`, which `_is_fail` counts as a failure; one datasheet with two groups per table gave 63 such failures.

## Why now

False K failures make `doc check` exit 1 on a correct distillation, which trains a reader to ignore K.

## Where to look

- `src/embarch_atlas/check.py` `DocText.columns` — header detection and column assignment per row
- `src/embarch_atlas/check.py` `compare_columns` — the disagreement K reports
- `src/embarch_atlas/check.py` `record_checks`, `K_WARN` — where K runs on `limit` and `timing` records and where its warnings are named
- `tests/test_check.py`, `tests/datasheet_synth.py` — synthetic pages for check tests

## Dispatch notes

- **Synthetic pages only**; the datasheet that showed it is not in this public repo, so the third item of the issue's own list ("that datasheet gives no K failure") cannot be run here and is not asked for.
- `atlas/044` just edited `check.py` (check M's foreign cites); read `main` as it is when you start.
- No `embarch-atlas` doc in `embarch-doc` is in reserve at the split.

## Done when

- [x] A synthetic page with two side-by-side MIN/TYP/MAX groups yields no K disagreement for records that match their cells, and still yields one for a record that does not.
- [x] A page with a lone TYP column is read by K, or reported as a K warning, never as `disagree`.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `DESIGN.md` updated where it describes check K; `changelog.d/` fragment dropped.

## Result

`DocText.columns` now builds a list of groups per header band (`_hdr_groups`: a repeated key starts the next group; a lone MIN/TYP/MAX word beside a UNIT header is a group) and reads each in `_read_group`, limited to its own x-range; the record is held to the group whose cells agree with the most of its numbers. DESIGN.md has no check-K text, so the `check.py` module docstring (K line) was amended instead. Tests: `test_k_reads_each_side_by_side_group`, `test_k_reads_a_lone_typ_column`. Gate: 668 passed, 3 skipped (the three real-workspace env-var tests; `test_public_guard` ran).
