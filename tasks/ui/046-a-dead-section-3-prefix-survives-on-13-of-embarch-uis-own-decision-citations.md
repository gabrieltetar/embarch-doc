# 046 — A dead `§3` prefix survives on 13 of `embarch-ui`'s own decision citations

**State:** done — leg 110, 2026-09-13.
**Doc-size reserve (supervisor, leg 110):** **no `embarch-ui` doc is in reserve.** All 13 files
currently inside the last 10% of their cap belong to other sub-projects. If your work pushes one in,
file `tasks/ui/<NNN>-compact-ui.md` in the same commit (`scripts/check-task-numbers.py --next ui`).
**Source:** `ui/045`'s worker, sweeping `embarch-ui/src/` and its docs for `§[0-9]` per the
supervisor's note 5 (a sibling check to the `ui/045` fix, not the same defect — that one pointed a
cross-repo citation at a dead section number; this one is `embarch-ui` citing its own decisions
with a dead section-number *prefix* still attached).
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`embarch-ui/decisions.md` states the current convention plainly: "Decision numbers are permanent
and address this sub-project, not a file. Cite them as `embarch-ui decision N`." Most citations in
`src/` follow that. But 13 do not — they carry a `§3 decision N` prefix, a leftover from before
`embarch-ui` had a flat `decisions.md`/`decisions/*.md`, when `embarch-ui/design.md` still existed
and its own decisions lived under a literal numbered `§3` heading (confirmed in git history:
commit `719cb1c` still refers to "`embarch-ui/design.md`: resolve decision 3 ... and decision 5").
That heading is gone; `§3` now resolves to nothing in `decisions.md`, which has no numbered
headings at all.

Concretely, the same decision is cited both ways **in the same file**:

- `src/trace.rs`: bare `decision 10` at lines 1, 6, 150, 262, 325 — `§3 decision 10` at lines 676,
  1971, 2024, 2062, 3394, 3571, 3753 and split across 149/150 (8 instances). Bare `decision 18`
  does not otherwise appear in this file — `§3 decision 18` at lines 136, 3327, 3888, and split
  across 3560/3561 (4 instances).
- `assets/app.js:4010`: `§3 decision 18`, versus `assets/app.js:423`'s bare
  `` `embarch-topology` decision 18 `` (a different repo's decision 18, cited correctly without a
  `§` prefix — direct evidence the bare form is both the working convention and achievable here).

13 stale instances total: 12 in `src/trace.rs`, 1 in `assets/app.js`. Re-run
`grep -rno '§[0-9]' embarch-ui/src/ embarch-ui/assets/ embarch-ui/vscode-extension/` against a
fresh checkout before fixing, to catch anything landed between this drop and the fix.

**Two citations this same sweep found that are *not* defective, for contrast** — don't refile
these: `src/trace.rs:11`'s `` `embarch-outpost/spec.md` §5 `` and `assets/app.js:2542`'s
`` `embarch-study-designer/spec.md` §5 `` both resolve to real, current, on-topic numbered headings
(checked against both files directly: `embarch-outpost/spec.md`'s own `## 5. Host-side outputs`
still exists, as does `embarch-study-designer/spec.md`'s `## 5. Result storage`).

## Why now

Cheap, same class as `core/050`/`dev-bench/030`/`study-designer/039`/`ui/044`/`ui/045`: a stale
section-number citation is exactly the kind of thing that reads as authoritative and isn't. Filed
separately from `ui/045` because that task's scope was specifically the two cross-repo
`embarch-study-designer/interfaces` citations ("finishes the sweep" of *those*), not `embarch-ui`'s
own internal decision-citation style.

**Gate caveat (supervisor note 6):** `check-docs.py`'s link checker does not check section anchors,
so a green gate run here proves nothing about this defect class either way — both the fix and the
two declined-to-touch `§5` citations were verified by hand against file contents, not by any script.

## Done when

- [x] Every `§3 decision N` citation into `embarch-ui`'s own `decisions.md` in `src/`, `assets/`,
      `vscode-extension/` drops the dead `§3` prefix, matching the bare `decision N` form the
      majority of the file already uses and `decisions.md` itself prescribes.

      Re-ran `grep -rno '§[0-9]' embarch-ui/src/ embarch-ui/assets/ embarch-ui/vscode-extension/`
      against a fresh checkout before touching anything, per supervisor note 2 — **count matches:
      13 stale `§3` instances** (12 in `src/trace.rs`: lines 136, 149/150 (split across two lines),
      676, 1971, 2024, 2062, 3327, 3394, 3560/3561 (split), 3571, 3753, 3888; 1 in
      `assets/app.js:4010`), plus the two non-defective `§5` cross-repo citations at
      `src/trace.rs:11` and `assets/app.js:2542`. `vscode-extension/` had no matches. `ui/045`'s
      landing did not touch any of these 13 sites in `study_designer.rs`, so nothing shifted between
      the drop and this fix.

      Also confirmed `embarch-ui/decisions.md:7` says exactly what the drop claims: "Decision
      numbers are permanent and address this sub-project, not a file. Cite them as `embarch-ui
      decision N`." — supervisor note 4's check, done before rewriting anything.

      Fixed all 13 by dropping the `§3 ` prefix (`sed -i 's/§3 decision/decision/g'` for the 11
      single-line instances plus `assets/app.js:4010`, then a manual `Edit` for the one instance
      split across `trace.rs:149`/`150` where `§3` and `decision` were on different lines). Left the
      two `§5` citations at `trace.rs:11` and `app.js:2542` untouched — re-derived independently
      (not just taken on the drop's word) and confirmed both still resolve: `embarch-outpost/spec.md`
      has `## 5. Host-side outputs`, `embarch-study-designer/spec.md` has `## 5. Result storage`;
      both comments' content matches those sections. My own judgement agrees with the drop's: those
      two are correctly not in scope.
- [x] `changelog.d/` fragment only if judged reader-visible (precedent: `ui/044` judged the
      equivalent repoint not reader-visible for a doc comment).

      Judged not reader-visible — same call as `ui/044` and `ui/045`: a doc-comment-only fix over
      code, no behavior change. No fragment dropped.
