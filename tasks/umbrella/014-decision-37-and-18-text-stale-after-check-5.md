# 014 — Three lines in `decisions/doctor.md` went stale the moment check 5 landed

**State:** open
**Source:** the `embarch-reviewer` pass on `umbrella/006` (`embarch-umbrella` `66e4a78`, `embarch-doc` `de8a381`, 2026-09-05) — three sub-threshold notes it judged not worth reverting for, recorded here rather than lost
**Scope:** umbrella
**Hardware:** none

## What

`umbrella/006` built check 5's Linux probe-permission branch and updated
`spec.md` correctly. Three lines in `embarch-umbrella/decisions/doctor.md` and
one test name did not follow, and each is small enough that nothing will ever
fail because of it — which is exactly why it needs a task rather than a memory.

1. **Decision 37 still says "Check 10 is the only user today"** of the `--json`
   `code` field. Check 5 is now the second user, and decision 37 itself named it
   as one of "the obvious next ones". `spec.md` was updated to "checks 5 and 10";
   the decision that introduced the field was not.
2. **Decision 18's new text says "the two warns are `no-probe-found` and
   `no-probe-unchecked`."** There is a third — `no-status`, for the check-4 skip.
   Pre-existing behaviour, newly enumerated wrongly.
3. **`check_5_passes_and_never_scans_when_core_reports_a_probe` overstates what
   it pins.** `usb_scan_for` runs before the probe count is consulted, so the
   sysfs read does happen when Core reports probes; the *verdict* is what is
   unaffected. The behaviour matches decision 18's "after zero probes are
   reported" as a description of the verdict, not of the syscall. Either rename
   the test to what it actually asserts, or move the scan behind the count and
   let the name become true.

## Why now

Not urgent, and it should not be dispatched on its own. **Fold it into whichever
`umbrella` task next edits `decisions/doctor.md`** — `tasks/umbrella/011` and
`tasks/umbrella/012` both do. A decision file whose text is stale by one check is
the shape `embarch-api` decision 51 named: the surface text is what a reader
acts on, and a reader loading decision 37 to add a `code` to a new check will
believe check 10 is alone.

Item 3 is a judgement between two fixes and the cheaper one is the rename;
whoever takes it should say which and why.

## Done when

- [ ] Decision 37 names check 5 as a user of `code`, or says the list is not
      maintained per check.
- [ ] Decision 18's warn enumeration includes `no-status`, or says it is
      listing only the probe-related warns.
- [ ] The test name and what it asserts agree, by whichever of the two fixes is
      argued for.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
