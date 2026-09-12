# 017 — The Study Designer's built-in action vocabulary lives in three places, two already disagree, and the crate's served copy is read by nobody

**State:** open — announced under `ops.md` §4 by leg 084, 2026-09-11, `ts 1789182068.428919`. The
30-minute window opened at that message. If this leg ends before it closes, **do not restart the
clock**: re-poll that thread and, with no objection and 30 minutes elapsed, execute.
**Source:** suite review pass 2026-09-06, dimension 2 (DRY across modules). Code-confirmed.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

One question — *which built-in actions can a Study Designer row pick* — is answered in three
places:

- `embarch-study-designer/src/merged_actions.rs:28-59` — `enum BuiltInAction` with
  `pub const ALL: [BuiltInAction; 7]`. **Seven** entries.
- `embarch-study-designer/src/study_builder.rs:39-57` — `enum BuiltInActionKind`. **Nine** — the
  same seven plus `GattMonitorSelected` and `GattMonitorSelectedStart` (decision 53).
- `embarch-ui/assets/app.js:862-880` — `var SD_BUILT_INS = [...]`, nine hand-written
  `{value, label}` pairs, and the labels are prose written only here.

The submit-side answer (9) is authoritative, the browser's answer (9) is a hand copy of it, and
the crate's **served** answer (7) has been wrong since decision 53 and nobody noticed — because
the only consumer discards it. `merge_actions` (`merged_actions.rs:122-127`) documents *"Order:
built-ins first"* and `embarch-ui/src/study_designer.rs:876` serves the whole merged list, but
`grep -c 'BuiltIn' embarch-ui/assets/app.js` returns **0**: `app.js:1049-1058` filters the served
list for `.Registered` and `.Unregistered` only, and `:1185` renders the picker from
`SD_BUILT_INS`.

So the suite has a duplicated vocabulary whose one machine-readable copy is both stale and dead.
Adding a built-in means two hand edits and a third list that will keep being wrong.

Candidate direction: the browser renders the built-ins it was served, and there is one enum behind
the served list and the submitted `RowAction` rather than two. Whichever list survives, the labels
belong on the server side with the vocabulary.

## Why now

`embarch-ui/decisions/gatt-capture.md` decision 17 did the **opposite** for `MAX_MONITOR_TARGETS`
and gave the reason: *"a browser-side copy of a limit is a number that drifts silently the day the
limit moves."* `embarch-ui/spec.md`'s Invariants state the rule outright. This is the same shape
one file over, and it has already drifted.

## Done when

- [ ] There is one definition of the built-in action vocabulary, and the picker renders what the
      server served.
- [ ] Adding a built-in action requires exactly one edit.
- [ ] No built-in action list in the suite is computed and then discarded.
- [ ] Gate green; `changelog.d/` fragments for each repo touched.

**Adjacent, not the same:** `tasks/ui/003` serves two hardcoded *numbers* (250,000 and 32). This
is a restated *vocabulary* with a live 7-versus-9 disagreement and a dead served copy — different
fix, different evidence. A worker on `ui/003` should leave this untouched.
