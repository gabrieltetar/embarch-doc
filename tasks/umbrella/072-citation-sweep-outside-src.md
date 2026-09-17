# 072 — Citation sweep: the 17 `embarch-umbrella` citations that live outside `src/`

**State:** done
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

- [x] All citations in the five files checked for existence, repo label, and whether the sentence
      around each is true — count re-taken as *instances*, not grep lines. **27 instances** (Cargo.toml
      12, CLAUDE.md 2, README.md 5, release.yml 5, assemble-suite.yml 3) against the grep census of 17
      lines. Beyond `decision N`, four instances cited a file — `embarch-umbrella/milestone-6.md §3.7`
      / `§3.8` — by name and section rather than by decision number; that file was deleted in the
      four-file split and no longer exists anywhere in this repo.
- [x] Wrong numbers and false sentences reported as separate counts, with the total checked.
      **Checked 27, 0 wrong numbers, 8 false sentences:**
      1. Cargo.toml: "only `token_discovery` is used, nothing else calls into it" — false since
         decision 20's 2026-09-10 amendment also moved `CoreConfig` onto `embarch-core-client`.
      2. README.md: "Status: bootstrap only… every command reports itself unimplemented" — false;
         `src/` is ~12k lines of built `setup`/`doctor`/`deploy-core`.
      3. README.md: the "Milestone 6" link, and 4/6/7 below: all four cite the now-deleted
         `milestone-6.md`.
      4. README.md: the user-guide link pointed at `embarch-doc/embarch-user-guide.md`, which has
         never existed under that name; the real file is `suite/user-guide.md`.
      5. release.yml: "unlike embarch-core/embarch-api, this crate has no embarch-study-designer
         dependency" — false (Cargo.toml has depended on it since decision 33); the checkout list
         backed the false claim by only ever checking out `embarch-topology`, so a real tagged
         release's `cargo build` would fail resolving `embarch-study-designer` and
         `embarch-api/crates/embarch-core-client`. Fixed the claim and added both checkouts.
      6. release.yml: `milestone-6.md §3.7` → repointed at `decision 14`, which covers the same
         per-repo-vs-suite-release ground.
      7. assemble-suite.yml: `milestone-6.md §3.7` → `decision 14`.
      8. assemble-suite.yml: `milestone-6.md §3.8` → `decision 14`, which describes the exact
         `nullglob`/pipefail bug this comment names.
- [x] Any `file:line` citation checked for line drift, not just for path correctness. No `path:line`
      form citations found in these five files (the `§N` section citations above are to a doc that no
      longer has sections at all, which is a different defect, not line drift).
- [x] No new bare cross-repo citation introduced anywhere in the diff — all repointed citations are
      bare `decision N` (same-repo, embarch-umbrella) or `embarch-umbrella decision N` matching each
      file's own pre-existing local style.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build`/`test`/`clippy --all-targets
      -D warnings` all clean (225 tests); `check-docs.py` 11/11; `check-client-names.py` clean;
      `check-ownership.py` clean in both repos.
- [x] `changelog.d/umbrella-*` fragment reporting the three numbers.

**Declined:** the release.yml checkout fix is not verified against a real tag push — per decision
27/29's own account, that is a release and not the fleet's to do. It mirrors the already-working
`embarch-topology` checkout step verbatim, no new mechanism. `CLAUDE.md`'s "Four files, not one" line
omits the `[Reference: interfaces.md, where there is one.]` clause DOC-PROTOCOL.md §6's template
carries, even though umbrella has one (`interfaces/doctor-chain.md`) — noticed but left alone: it is a
missing pointer, not a wrong citation, and whether all eight repos' `CLAUDE.md` need that clause is a
suite-wide template question this single-repo sweep should not decide alone.

## Not yours

`history/umbrella.md` is assembled from fragments.
