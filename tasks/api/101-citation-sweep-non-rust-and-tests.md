# 101 — Citation sweep: `embarch-api`'s non-Rust files and `tests/`, the half every prior sweep scoped itself out of

**State:** claimed by agent/api/101-citation-sweep-non-rust-and-tests, 2026-09-16 18:45
**Source:** leg 122's refill sweep, 2026-09-16. `api/091` swept `client.rs`/`config.rs`; `api/093`
swept `resolve.rs`/`tools.rs`/`cli.rs`; `api/095` and `097` finished `client.rs`. Every one of those
scoped its grep to `src/` and `crates/`. The files below have never been read by anything.
**Scope:** api
**Hardware:** none — comments, a config example, a workflow file and test-file comments. Nothing is
built for a board, no probe, no live Core, no deploy, no study.
**Owner:** no

**Doc-size reserve for `api`:** one file, `embarch-api/spec.md` at **9,102/10,240 B (1,138 B left)**,
filed as `tasks/api/083` and blocked. Nothing else in scope is in reserve. A citation sweep should
not need to write `spec.md`; if it does, say why. If your work leaves any `api` doc inside the last
10% of its cap and nothing has filed it, file `tasks/api/<next free NNN>-compact-api.md` in the same
commit per `tasks/README.md`. **`tasks/doc/` is not yours.**

## What

Roughly 45 citation-bearing lines across twelve files, censused at this task's filing:

```
config.example.toml                  8
tests/smoke_harness.rs               9
.github/workflows/release.yml        5
tests/core_client_http.rs            4
tests/build_capture.rs               4
tests/json_surface.rs                3
Cargo.toml (both, root and crate)    3
tests/study_events_sse.rs            2
README.md                            2
CLAUDE.md                            2
```

Sweep them by the established method: for each citation, does the cited decision exist, is its form
right for the repo it means, and does the sentence around it state something the decision actually
says.

**Re-census before you start.** These are `grep -cE '[Dd]ecision'` **line** counts, not instance
counts; every time anyone has measured both they have differed by about 10%. `topology/046` also
found three citations a grep census missed entirely because they cite by `file:line` rather than by
`decision N`.

## Why now — three repos ran this exact shape in one leg and all three yielded

Leg 122 ran "the sweep scoped itself to a directory and missed everything else" in two repos on the
same day, and `outpost/022` had already named the pattern:

- **`core/066`**: 9 instances outside `src/`, **1 wrong number, 2 false sentences** — the highest
  defect density anyone has recorded.
- **`topology/046`**: 21 instances outside `src/`, **2 wrong numbers, 1 false sentence**, after a
  `src/`-scoped sweep of 103 citations in the same repo had found zero wrong numbers.
- **`outpost/022`** put it as a method finding: *"Every sweep in this series has scoped its grep to
  the language it expected to find comments in"* — which is how a live wrong citation survived a
  sweep that had just fixed its twin.

**`config.example.toml` is the one to start with.** Eight citations, and it is a file users copy —
a wrong claim there is a wrong claim in somebody's real config, not just in a comment.

## The larger unswept block, deliberately not in this task

`src/zephyr.rs` (23), `src/main.rs` (18), `src/reflash.rs` (13), `src/study.rs` (8) and
`crates/embarch-core-client/src/api_log.rs` (8) — about 70 lines — have also never been swept.
That is a second unit, not this one, and it should be filed when this closes. It is listed here so
the remainder is written down somewhere rather than rediscovered.

## Watch for

- **Citations live in runtime string literals here, not only in comments.** `api/091`'s worst defect
  was one. A wrong decision number inside a message a user sees is a different severity from a wrong
  one in a comment.
- **`check-decision-refs.py` walks `*.md` only, and only in the doc repo.** Nothing checks a TOML
  comment, a workflow YAML or a Rust test file, and nothing will. Treat all of these as unchecked.
- **A stale `file:line` suffix is a real defect class and a new one** — `topology/046` found a
  citation whose repo, path and depth were all right and whose line number was stale, because the
  target had split two days earlier. Check line anchors, not just paths. **Do not settle whether
  `:line` should be allowed** — that is `tasks/doc/055`, owner-reserved.
- **Do not introduce a bare cross-repo citation.** A bare `decision N` is same-repo by convention.
- **`inbox/api-stale-decision-22-citations-remaining.md`'s subject is now settled and the answer is
  reusable here.** `core/066` established it by reading the decision's own text: **`embarch-core`
  decision 22 is *only* the probe/board identity gate** — a live hardware-ID readback against a stale
  label, since moved into `embarch-topology`'s `validate()`/enrollment mechanism. It has nothing to
  do with `known_boards.toml`'s format, a `toml` crate version, or any HTTP route. **Any `embarch-api`
  citation pairing decision 22 with an HTTP route or with `known_boards` is citing the wrong fact.**
  If you meet one in these files, that is a real defect.
- **Length.** Leg 122 flagged a real doubt: three sweeps in two days each replaced a short wrong
  sentence with a considerably longer right one. Fix the fact; do not write an essay in a config
  example.

## Done when

- [ ] Every citation in the listed files checked for existence, repo label, and whether the sentence
      around it is true — counted as *instances*, not grep lines.
- [ ] `config.example.toml` done first and its eight reported separately, since a defect there ships
      into users' configs.
- [ ] Wrong numbers and false sentences reported as separate counts, with the total checked.
      "Checked 45, found none" is a legitimate result.
- [ ] Any `file:line` citation checked for line drift.
- [ ] A follow-up task filed for the ~70-line `src/`/`crates/` remainder named above.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/api-*` fragment reporting the three numbers.

## Not yours

`history/api.md` is assembled from fragments.
