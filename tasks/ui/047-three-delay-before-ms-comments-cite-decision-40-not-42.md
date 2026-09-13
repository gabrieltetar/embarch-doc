# 047 — Three `delay_before_ms` comments in `app.js` cite `embarch-study-designer` decision 40; the subject is decision 42

**State:** claimed — leg 108, unit 4, 2026-09-13, branch `agent/ui/047-delay-before-ms-decision-42`.
**Doc-size reserve for `ui`:** nothing in `embarch-ui/` is currently in reserve. This task should
need no new decision — it is comment text in a shipped asset — but if you conclude one is owed,
check `embarch-ui/decisions.md`'s index and pick the right topic file rather than the nearest one,
and file `tasks/ui/<NNN>-compact-ui.md` in the same commit if you push a file into reserve.
**Source:** a read-only hunter pass over `embarch-ui`, leg 108, 2026-09-13. Both decision bodies
were read in full by that pass; **re-derive them yourself** — a citation nobody re-checked is
exactly the defect here.
**Scope:** ui
**Hardware:** none — comments in `assets/app.js`. No behaviour, no board.
**Owner:** no

## The defect

Three comments in `assets/app.js` — at **1155**, **1192** and **1198**, all inside `sdNewRow`'s
`delay_before_ms` field and `sdCaptureTemplate` — attribute `Step.delay_before_ms` to
`embarch-study-designer` decision **40**.

- Decision 40 (`embarch-doc/embarch-study-designer/decisions/declares.md:11`) is *"A study declares
  the firmware versions it is meant to run against; reflashing is the operator's per-run choice"* —
  entirely about `requires`, `any`, provenance and reflash-as-query-parameter. **Nothing about
  timing.**
- Decision 42 (`embarch-doc/embarch-study-designer/decisions/study.md:21`) is *"`Step.delay_before_ms`
  — the 'when' half of authoring a stimulus"*, and the three comments paraphrase it closely: line
  1155 lifts its title phrase *"the 'when'"*; 1192 paraphrases its sentence about waiting inside an
  open capture window so the transcript separates unsolicited traffic from the response; 1198
  paraphrases its note that this **replaced** the UI's old second-monitor-step workaround.

So all three are wrong, and all three are wrong the same way. Line numbers are as of this task's
filing — **re-grep rather than trusting them.**

## The fix that reads well and is wrong

**Grepping `decision 40` across the repo and changing them all.** There are **nine other**
`decision 40` citations in `embarch-ui` — `assets/app.js:2403`, `assets/style.css:813`, and
`src/study_designer.rs:268, 372, 1032, 1658, 2194, 2474, 2889` — and every one is about `Declared`
vs verified provenance, `requires`, and `REQUIREMENT_ANY`, which **is** decision 40's subject. A
blanket rewrite would break nine correct citations to fix three. The defect is scoped to the
`delay_before_ms` comments in `sdNewRow` and `sdCaptureTemplate`, and nowhere else. Confirm that
yourself before you touch anything.

Note `embarch-doc/embarch-ui/` has no delay-related citation of decision 40 — this looks source-only.
Check, do not assume.

## Citation form

Line 1155 is the first mention in its own field comment and should carry the repo prefix
(`` `embarch-study-designer` decision 42 ``), matching its siblings at 1125/1129/1136/1147; 1192
keeps its existing prefix with the number corrected; 1198 is anaphoric to 1192 and may stay bare.
`ui/040` established that a foreign decision number carries its repo prefix at first mention.
**Do not amend `DOC-CONVENTIONS.md`** — reserved.

## Second item, same file, verify before taking

`assets/app.js:163-164` reads *"`embarch-core` decision 57 / (decisions/surfaces.md) declined to
persist a real last-validation instant"*. The number and the substance are right; the **filename
pointer is dead** — decision 57 lives in `embarch-doc/embarch-core/decisions/enrollment.md:27`, and
`surfaces.md` holds only 12, 13, 55 and 59 per `embarch-core/decisions.md`. Check that against the
current index and fix the pointer if it still holds. If the index disagrees with this paragraph,
report it and leave the line alone.

## Not in scope

- `src/trace.rs:132`'s bare "decision 35", which resolves to no `embarch-ui` decision and to nothing
  plausible in a sibling repo. Real, but naming the intended referent is a judgement call, not a
  lookup. Drop it to `/home/gabriel/Github/embarch/embarch-doc/inbox/` if you want it queued.
- Bare foreign decision numbers with no repo prefix generally — adjacent to owner-reserved
  `tasks/ui/038`.
- The nine correct decision 40 citations.

## Done when

- [x] `assets/app.js` lines 1155, 1192 and 1198 cite decision 42, with 1155 carrying the repo prefix.
- [x] The nine other `decision 40` sites are confirmed untouched and confirmed still correct.
- [x] The `decisions/surfaces.md` pointer at 163-164 is either fixed or reported as still correct.
- [x] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [x] `changelog.d/` fragment.

## Closed 2026-09-13, leg 108 unit 4

Both decision bodies re-read in full from `embarch-study-designer/decisions/declares.md:11` (40)
and `embarch-study-designer/decisions/study.md:21` (42), confirming the task's characterization
exactly: 40 is firmware-version declaration/provenance/reflash, nothing about timing; 42 is
`Step.delay_before_ms`, the "when" half of authoring a stimulus, and its body's own language
("the 'when'", the open-capture-window wait, replacing the old second-monitor-step workaround) is
what the three comments paraphrase.

Fixed in `assets/app.js`: line 1155 now reads `` `embarch-study-designer` decision 42 `` (carries
the repo prefix, matching the citation form of its siblings at 1125/1129/1136/1147); 1192 keeps its
existing prefix with the number corrected to 42; 1198 stays bare (anaphoric to 1192), number
corrected to 42.

The nine other `decision 40` sites — `assets/app.js:2403`, `assets/style.css:813`,
`src/study_designer.rs:268, 372, 1032, 1658, 2194, 2474, 2889` — were each read in context. All nine
are about `Declared` vs. verified provenance, `requires`, `REQUIREMENT_ANY`, or the
`Declared`-must-not-look-verified rendering rule — decision 40's actual subject. Left untouched.

Second item: `assets/app.js:163-164`'s `embarch-core` decision 57 citation. Checked
`embarch-core/decisions.md`'s index directly: `decisions/surfaces.md` holds 12, 13, 55, 59;
`decisions/enrollment.md` holds 25, 27, 28, 50, 54 (moved to 57), 57. Decision 57's body in
`enrollment.md:27` also confirms the substance (`EnrolledBoardResponse` not growing a persisted
validation timestamp) matches the comment. The number and substance were already right; only the
filename pointer was stale. Fixed `(decisions/surfaces.md)` → `(decisions/enrollment.md)`.

Not in scope, dropped to inbox: `src/trace.rs:132`'s bare "decision 35" —
`/home/gabriel/Github/embarch/embarch-doc/inbox/ui-src-trace-rs-132-bare-decision-35-no-referent.md`.
Resolves to no `embarch-ui` decision, and no sibling repo's numbering has a plausible referent
either (checked all five: `embarch-api` hardware-selection, `embarch-study-designer` registry,
`embarch-core` handshake, `embarch-dev-bench` link, `embarch-umbrella` schema-skew — none about
naming an unnamed subject).

Gate: `cargo build`/`test`/`clippy --all-targets -D warnings` green in the code worktree;
`scripts/check-docs.py` green in the doc worktree except a pre-existing, unrelated red
(`check-task-state.py` on `tasks/core/052`, not touched by this unit);
`scripts/check-client-names.py --repo <code worktree>` clean; `scripts/check-ownership.py --scope
ui` / `--code-repo` clean on both.
