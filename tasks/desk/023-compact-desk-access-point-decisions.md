# 023 — `embarch-desk/decisions/access-point.md` is in reserve

**State:** done
**Result:** 79 and 81 split verbatim into `decisions/linear-reads.md`; `access-point.md` 11,206 → 6,477 B
**Source:** `desk/021` added decision 81 and left the file at 11,206 B of 12,288 B (91.2%); `DOC-COMPACTION.md` §2
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/decisions/access-point.md
**Size debt due:** 2026-11-26
**In flux:** no — the file's decisions (29–32, 56, 59, 79, 81) are settled; the only open edge is 81's unmeasured upload-host credentials, which a live check would confirm or correct in place.
**Must not delete:** 81's "credential goes only to Linear's upload host" paragraph, the 10 MiB cap and its status as chosen, and the assumed-not-measured list; 79's policy line on never falling back to the connector; 59's caps (2,000 and 500) as chosen, not measured.

## What

`access-point.md` has 1,082 B of headroom. Compact it: 81 and 79 are the longest entries and carry restated mechanism that `interfaces.md` also holds.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; `desk/021` is the unit that spent it.

## Done when

- [x] `access-point.md` is clear of reserve.
- [x] Every `Must not delete:` item is still readable.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
