# 072 — Citation sweep: the 17 `embarch-umbrella` citations that live outside `src/`

**State:** claimed by agent/umbrella/072-citation-sweep-outside-src, 2026-09-16 18:46
**Source:** leg 122's refill sweep, 2026-09-16. `tasks/umbrella/066` closed with *"All eleven files
swept"* — and its table is exactly `src/*.rs`; `065` was `doctor.rs`. Neither grep ever left `src/`.
**Scope:** umbrella
**Hardware:** none — comments in a manifest, two workflow files, a README and a `CLAUDE.md`. Nothing
is built for a board, no probe, no live Core, no deploy, no `doctor` run.
**Owner:** no

**Doc-size reserve for `umbrella`:** one file, `embarch-umbrella/decisions/bind.md` at
**11,533/12,288 B (755 B left)**, filed as `tasks/umbrella/009` and blocked. Nothing else in scope is
in reserve. A citation sweep should not need to write it; if it does, say why. If your work leaves
any `umbrella` doc inside the last 10% of its cap and nothing has filed it, file
`tasks/umbrella/<next free NNN>-compact-docs.md` in the same commit per `tasks/README.md`.
**`tasks/doc/` is not yours.**

## What

Seventeen citations, in five files, censused at this task's filing:

```
Cargo.toml                          8
CLAUDE.md                           3
README.md                           2
.github/workflows/release.yml       2
.github/workflows/assemble-suite.yml 2
```

Sweep them by the method the nine `study-designer` sweeps, `core/056`/`058`/`066`,
`topology/040`/`046` and `umbrella/065`–`066` used: for each, does the cited decision exist, is its
form right for the repo it means, and does the sentence around it state something the decision
actually says.

**Re-census before you start.** These counts are `grep -cE '[Dd]ecision'` line counts taken on
2026-09-16, and a line count is not an instance count — the two have differed by about 10% every time
anyone has measured both. `topology/046` also found **three citations the grep census missed
entirely** because they cite by `file:line` rather than by `decision N`. Look for those too.

## Why now — this exact shape yielded three times in one leg

Leg 122 ran the identical "the sweep scoped itself to a directory and missed the manifest" task in
two other repos on the same day:

- **`topology/046`**: `topology/040` had swept `src/` — 103 citations, zero wrong numbers. The three
  files outside it gave **21 instances, 2 wrong numbers, 1 false sentence**.
- **`core/066`**: **9 instances, 1 wrong number, 2 false sentences** — a two-thirds defect rate,
  the highest density anyone has recorded.

**A manifest is where the "why is this crate shaped like this" prose lives**, and that is precisely
the prose a later decision falsifies. `Cargo.toml`'s eight are the interesting ones here; the two
workflow files are the least-read text in the repo and have never been checked by anything.

## Watch for

- **`check-decision-refs.py` walks `*.md` only, and only in the doc repo.** It never reads
  `Cargo.toml` or a workflow YAML, and this code repo is outside its scope entirely — so nothing
  fails today and nothing will. Treat all seventeen as unchecked, `README.md` and `CLAUDE.md`
  included.
- **A stale `file:line` suffix is a real defect class and a new one.** `topology/046` found a
  cross-repo citation whose repo, path and relative depth were all correct and whose **line number**
  was stale, because the target file had split two days before the citation was written. A wrong line
  lands the reader on a real sentence about something else. If you find one, fix it and say so —
  `tasks/doc/055` now tracks the general question of whether `:line` should be allowed at all, and
  **do not settle that here.**
- **Do not introduce a bare cross-repo citation.** A bare `decision N` is same-repo by convention; a
  line that means another repo keeps its repo label.
- **Form is not yours to settle.** If the only problem with a line is which citation *form* it uses,
  say so in your report and leave it — `tasks/doc/055` and `tasks/ui/038` own that, both
  owner-reserved.
- **Length.** Leg 122's supervisor flagged a real doubt about this chain: three sweeps in two days all
  replaced a short wrong sentence with a considerably longer right one, and nobody is watching the
  aggregate. Fix the fact; do not write an essay in a manifest.

## Done when

- [ ] All citations in the five files checked for existence, repo label, and whether the sentence
      around each is true — count re-taken as *instances*, not grep lines.
- [ ] Wrong numbers and false sentences reported as separate counts, with the total checked. "Checked
      17, found none" is a legitimate and useful result.
- [ ] Any `file:line` citation checked for line drift, not just for path correctness.
- [ ] No new bare cross-repo citation introduced anywhere in the diff.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/umbrella-*` fragment reporting the three numbers.

## Not yours

`history/umbrella.md` is assembled from fragments.
