# 063 — Check K holds a record to the group its condition names

**State:** done
**Source:** EMB-113, filed while reviewing `atlas/046` (EMB-35) after it landed
**Issue:** EMB-113
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Check K reads a table with two side-by-side MIN/TYP/MAX groups, and since
`atlas/046` it holds a record to whichever group agrees with most of its
numbers: `DocText.columns` splits the header band into groups (`_hdr_groups`)
and picks one by `_agree`. That removed EMB-35's false failures, and it also
means K cannot catch a number taken from the wrong group: a record carrying the
5 V column's values for a 3.3 V row passes. Before `atlas/046` K read the wrong
group outright, so this is not a regression against a working check.

Wanted: **when the group headers carry a condition** (a supply voltage, a
temperature), K holds a record to the group its `cond` names, and a record whose
numbers sit in the other group is a K disagreement. **When they carry none**, K
falls back to the best-agreeing group, as today.

Where: `embarch-atlas/src/embarch_atlas/check.py` (`DocText.columns`,
`_hdr_groups`, `_read_group`, `_agree`, and the module docstring's K line, which
says the record is held to the group that holds its numbers);
`tests/test_check.py` (`test_k_reads_each_side_by_side_group`).

**How a condition matches a header is yours to decide** (exact text, a
normalized voltage or temperature, or both), and it is a design choice: write it
where the atlas keeps its contract, the code repo's `DESIGN.md`, with the reason.
A header that names a condition no record's `cond` can be matched to falls back
to agreement, and says so in the check's output rather than silently.

**What you may change.** Only `embarch-atlas` and `embarch-doc/embarch-atlas/`.
**Not this unit:** check L's column position (EMB-160) is a separate issue.

## Why now

K is the check that is meant to catch a number copied from the wrong column,
and a two-condition table is exactly where that mistake is easiest to make.

## Done when

- [x] On a synthetic page with two groups headed by different conditions, a
      record whose `cond` names one group and whose numbers sit in the other is
      a K disagreement.
- [x] A record matching its own group's cells still passes, and a table whose
      groups carry no condition behaves as it does today.
- [x] The module docstring's K line and `DESIGN.md` say what K now does.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet:
      `test_public_guard` ran, not skipped).
