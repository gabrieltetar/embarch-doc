# 082 — Umbrella decision 26's `--prune` prerequisite is now closed on `embarch-api`'s side; `open.md`'s bullet needs correcting and updating

**State:** open — drained from `inbox/umbrella-build-dir-name-shipped-in-api-list-targets.md` by leg
139 at `api/109`'s fold, 2026-09-17. Body below is the `api/109` worker's, unchanged.

**Supervisor note — do not read "the prerequisite is closed" as "build `--prune` now."** Two things
this task's body cannot tell you:

1. **`api/109` also found this repo's own `open.md` bullet was factually wrong** and is what this
   task exists to correct: the bullet said `embarch-api`'s *study listing* lacked `build_dir_name`,
   and `embarch-api` has no multi-study listing at all. Decision 26's actual ask was
   **`list-targets`**, the target menu, which is what shipped. Correct the bullet's claim, not just
   its status.
2. **What shipped names only the *default* snippet/extra-args combination.** A directory built with
   a non-default combo still gets no name from `list-targets`; `embarch-api` decision 69's
   `target.json` is what attributes those. **So before this task concludes `--prune` is buildable,
   check whether `--prune` needs to attribute *every* directory or only the default one** — those
   are different answers and the difference is the whole safety argument for a delete.
   `api/109`'s own reviewer was asked this question directly; read its verdict in
   `supervisor-log.md`'s `api/109` entry before you decide.

**Reserve warning:** `embarch-umbrella/decisions/projects.md` is at **12,286/12,288 B — two bytes** —
and `tasks/umbrella/081` is its `open`, `In flux: no` compaction task, **overdue 2026-09-18**. If
this task touches `projects.md` at all, pay `081` first or as part of the same unit.

**Source:** `embarch-api` task 109 (`tasks/api/109-expose-build-dir-name-in-the-study-listing-or-record-why-prune-stays-unbuildable.md`), dispatched from this repo's own `open.md` standing bullet.
**Scope:** umbrella
**Hardware:** none. Doc-only: reading `embarch-api`'s new decision and adjusting `open.md`'s prose to match.
**Owner:** no

## What

`embarch-umbrella/open.md` currently reads: *"Decision 26's `--prune` is the last designed-and-unbuilt piece here, deferred by choice — it needs `build_dir_name` in `embarch-api`'s listing. Check 16 argues for it: `study_results/` is 803 MiB across 50 entries [measured 2026-09-06]; the sweep bounds the count, not the size."*

Two things this bullet gets wrong, found while re-deriving the claim from `embarch-api`'s own source for task 109:

1. **The listing decision 26 actually names is `list-targets` (the target menu), not a "study listing".** `embarch-api` has no listing of multiple studies at all — only a per-study `study-status`. Nothing in `StudyResult` or `study_results/<study_id>/` (keyed by `study_id`) has ever named a build directory, so there was never a study-result-to-build-directory link to add. Decision 26's own text is unambiguous on this: *"`list-targets`' JSON carries the tuple and not `build_dir_name`... so a `--prune` needs `embarch-api` to publish that name."*
2. **The 803 MiB `study_results/` figure is an unrelated gap** — that directory's retention is already count-bounded by Core's `sweep_study_results`/`EMBARCH_STUDY_RESULTS_KEEP`, and `build_dir_name` does nothing for its still-unbounded *bytes*. Citing it as the reason `build_dir_name` matters conflates two of check 16's numbers (`study_results/` bytes and per-project build-directory counts) that are about two different directories.

**The prerequisite itself is now closed.** `embarch-api` decision 77 (`embarch-api/decisions/target-json.md`) ships `build_dir_name` on every `list-targets` row for a `zephyr-west` project, computed locally (no `embarch-core` involvement) from `zephyr::Target::build_dir_name` against the project's own `default_snippets`/`default_extra_args` — the identity a bare `build` for that row writes to today. `null` when the app's available snippets don't cover `default_snippets` (the same case a real build already refuses at build time).

**What it does not close, and `--prune`'s own design still needs to fold in:** `build_dir_name` names only the *default* combination. A directory built with a non-default snippet selection or `extra_args` is exactly as current and exactly as off-limits to deletion (decision 26: "never a currently-valid target's directory regardless of age") as the default one, and this field does not name it. `target.json` (decision 69, already built 2026-09-05) is what attributes those directories instead, per-directory rather than per-listing. A sound `--prune` needs both sources, not `list-targets` alone.

## Why now

`open.md`'s bullet has stood for eleven days naming a prerequisite this repo never filed a task against; task 109 closed the prerequisite and found the bullet's own wording wrong in the process. Leaving it as-is would have the next reader chase "study listing" through a crate that has no such thing, and would read the 803 MiB figure as evidence `build_dir_name` never was.

## Done when

- [ ] `embarch-umbrella/open.md`'s decision-26 bullet is corrected (it's `list-targets`, not a study listing; the `study_results/` byte gap is separate) and updated to reflect that `build_dir_name` now exists (`embarch-api` decision 77) — or retired outright if `--prune` is picked up in the same pass.
- [ ] If `--prune` is designed/built as a result, it accounts for `build_dir_name` covering only the default combination, with `target.json` needed for the rest — decision 26 and decision 69 already state this; task 109 did not change either.
