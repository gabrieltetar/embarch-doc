# 148 — `report-data.json` carries the run's call-log head, range and count

**State:** done — report-data.json observed.call_log {head, first_seq, last_seq, count} written from the signed record, absent when the record has none; paired with api/185
**Source:** decisions 116 and 119 (`decisions/publish.md`); `interfaces/signing.md` (`observed.call_log`) and `interfaces/publish.md` (`report-data.json`)
**Issue:** EMB-265
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`report-data.json` holds every claim of the audit appendix, written and signed
by Core at publish, and it has no call-log field, though the signed record
names a call-log range since `core/145`. embarch-api's check 6 compares its
keys whole, so Core cannot add the field alone: `api/185` teaches check 6 and
the appendix the same field. **This unit and `api/185` are one change in two
repos: the supervisor lands both together or neither.**

**The field, fixed here so both units write the same thing.** `report-data.json`
gains `observed.call_log`: `{head, first_seq, last_seq, count}`, copied from the
signed record's `observed.call_log` (`head`, `first_seq`, `last_seq`, which are
both null when the run made no call) with `count` the number of entries in the
range (0 when the range is null). It is **present exactly when the signed record
carries `observed.call_log`**, absent otherwise. `schema` stays 1.

When this is done, the `report-data.json` builder in `src/publish.rs` writes
the field, and `interfaces/publish.md`'s `report-data.json` paragraph lists it.

## Why now

The call-log range and segment landed in `core/145`; a published report should
say what that range was.

**Burndown leg: no new numbered decision.** Amend decision 116 or 119 in place.
If the work needs a new decision, or a `schema` bump, stop and say so in this
file and in your report: either one changes how this pair lands.

**Doc size:** `embarch-core/spec.md` is in reserve, 1,080 B left, with its debt
parked as `tasks/core/147` (blocked). Leave `spec.md` alone; this change
belongs in `interfaces/publish.md` and decision 116 or 119.

## Done when

- [x] A fixture publish's `report-data.json` carries the call log's head, range and count, taken from the signed record.
- [x] A run whose record has no `observed.call_log` gets no field.
- [x] Gate green (`../../embarch-fleet/gate.md`); the native Windows build recorded as a debt in your report.
- [x] `interfaces/publish.md` and the amended decision updated, `changelog.d/` fragment dropped.
