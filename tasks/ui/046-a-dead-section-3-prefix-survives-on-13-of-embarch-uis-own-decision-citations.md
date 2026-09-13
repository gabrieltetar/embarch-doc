# 046 — A dead `§3` prefix survives on 13 of `embarch-ui`'s own decision citations

**State:** claimed — leg 110, 2026-09-13.
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

## Done when

- [ ] Every `§3 decision N` citation into `embarch-ui`'s own `decisions.md` in `src/`, `assets/`,
      `vscode-extension/` drops the dead `§3` prefix, matching the bare `decision N` form the
      majority of the file already uses and `decisions.md` itself prescribes.
- [ ] `changelog.d/` fragment only if judged reader-visible (precedent: `ui/044` judged the
      equivalent repoint not reader-visible for a doc comment).
