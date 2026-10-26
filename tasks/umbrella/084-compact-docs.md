# 084 — `embarch-umbrella/decisions/projects.md` is back in reserve

**State:** done -- 2026-10-26 (agent/umbrella/084-compact-projects-md)
**Source:** `scripts/check-doc-size.py --pressure`, run by `umbrella/082`
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/decisions/projects.md
**In flux:** no — for a verbatim split. Decision 26 is still "deferred by choice" (`--prune` is
undesigned), so its *wording* must not be squeezed; but a verbatim move restates nothing, so the flux
cannot forbid one (`.claude/leg.md`, split-first). Decisions 13, 17 and 41 are settled.

## Dispatch note, 2026-10-26 leg — read this one first

**Unparked by the overdue ledger** (due 2026-10-17; the entries ahead of it are owner-only or have
nothing to pay). The file is 11,116 / 12,288 B, 57 B over its 11,059 B reserve line.

**The seam is decision 26 itself.** The file is titled "Integrating a firmware repo" and settles what
`init` derives (13, 17, 41); decision 26 is `study_results/` retention and build-directory pruning, a
different question that is also the file's in-flux half. Preferred move: decision 26 **verbatim** into
a new `embarch-umbrella/decisions/<name>.md` (name it for what it settles), routed from
`decisions.md`'s group table, with every inbound link to `decisions/projects.md` that means decision 26
repointed **inside `embarch-umbrella/`** (grep first; a link from another sub-project you may not edit
goes to `inbox/` by absolute path, not fixed). The next unit that designs `--prune` then edits a file
with headroom. If you find a reason the split is wrong, the fallback is shortening 13/17/41 wording only
— never decision 26's — and say why in this file. `umbrella/079` is the precedent
(`decisions/setup-reversal.md`).

**Leave `open.md` alone**; it is `umbrella/090`'s, parked.
**Unparks when:** decision 26's `--prune` is designed or built (closing the "deferred by choice"
state one way or the other), or check 16 reports real disk pressure that forces the question sooner
— either event rewrites the section this task would otherwise compact around.
**Must not delete:** decision 26's now-corrected framing that the ask was always `list-targets` (the
target menu), never a "study listing" that does not exist; the `study_results/` 803 MiB figure's
status as a *separate*, already count-bounded gap (Core's `sweep_study_results`), not evidence for
`build_dir_name`; the 2026-09-17 note that `build_dir_name` shipped (`embarch-api` decision 77) for
the *default* snippet/`extra_args` combination only; and the resulting rule that `--prune` needs
**both** `list-targets`' `build_dir_name` and per-directory `target.json` (decision 69) — never
either alone — plus decision 69's own rule that a missing `target.json` means "unattributable," never
"orphaned."

**Size debt due:** 2026-10-17

**Reserve:** `projects.md` was last relieved by `umbrella/081` (2026-09-17), which split decision 55
out to a new `serial-port.md`, dropping the file from 12,286/12,288 B (99.98%) to 10,950 B (89.1%).
`umbrella/082` (2026-09-17) then corrected decision 26's `list-targets`/`build_dir_name` claim and
recorded that `embarch-api` decision 77 closed the prerequisite for the default combination only,
pushing the file to **11,253/12,288 B (91.6%), 1,035 B left.** Both edits were load-bearing
corrections, not padding: the file was stating a claim `embarch-api`'s own decision 77 had already
made false.

Not filed against `009` (scoped to `decisions/bind.md`) or `079` (scoped to `decisions/install.md`)
— both are check-17/probe-permission episodes unrelated to decision 26.

## What

Bring `projects.md` back under 90% (11,059 B) without deleting a live question or a cited fact,
the way `081` did for decision 55: read for duplication against `spec.md` and `open.md` first
(`scripts/check-duplication.py embarch-umbrella`), then shorten wording before considering a further
split. Decision 26 is the largest single entry in the file and the newest edit; start there. Run
`scripts/check-doc-size.py --pressure` before and after and record the new percentage here.

## Why now

Not yet blocking anything — 1,035 B of headroom remains. Filed now per this repo's own reserve
convention (`DOC-COMPACTION.md`, `check-doc-size.py`'s reserve band) so the debt survives past this
leg rather than living only in a worker's report.

## In flux

**Yes**, decision 26 specifically — see `**In flux:**` above. Decisions 13, 17 and 41 are settled and
safe to shorten now if a pass is ever unblocked while 26 keeps moving.

## Done when

- [x] `projects.md` back under 90% of its 12,288 B cap, by shortening or moving, not by deleting a
      live question or a cited fact.
- [x] `scripts/check-duplication.py embarch-umbrella` checked before any content is moved elsewhere.
- [x] No question or fact disappears from `collect-open-questions.py` unless it can be named as
      answered.
- [x] Gate green, `changelog.d/umbrella-*` fragment dropped.

## Result, 2026-10-26

Decision 26 moved verbatim to `embarch-umbrella/decisions/prune-policy.md` (4,801 B); `projects.md` 11,116 -> 6,782 B (55.2%). Routed from `decisions.md`; `spec.md` decision-26 cite repointed. No decision-26 wording changed, so every Must-not-delete fact survives. `check-duplication` not rerun (nothing reworded). Other-repo links to `projects.md` meaning 26 (`embarch-api/decisions/target-json.md`, two) dropped to inbox.
