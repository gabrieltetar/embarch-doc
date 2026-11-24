# 119 — The study tab uses the shared tap check

**State:** blocked — waits for the shared check
**Unparks when:** `tasks/study-designer/093` lands
**Source:** EMB-308 — `decisions/gatt-capture.md` says the tab is the only place holding both steps and taps, but `Study` holds both
**Issue:** EMB-308
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`src/study_designer.rs` refuses a stream tap no step subscribes to with its own
`any_step_subscribes`. When this is done it calls the `Study` method
`study-designer/093` adds and maps its typed error to the same wording it
shows today, and `any_step_subscribes` is gone. The test near the existing
refusal still passes unchanged.

`decisions/gatt-capture.md` no longer claims the check cannot be shared; say
that the crate computes it.

## Why now

EMB-308: one check in two places drifts, and the UI's copy was the only one.

**Burndown leg: no new numbered decision.** Amend the gatt-capture entry in
place. **Doc-size note:** that file's decision 17 has 4 B left of its
per-decision cap; if the sentence belongs to another entry in the file, check
its headroom with `scripts/check-doc-size.py --decisions` first.

## Done when

- [ ] The tab's refusal comes from the shared check, wording unchanged; the
      local helper is removed.
- [ ] `decisions/gatt-capture.md` no longer says the check cannot be shared.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped.
