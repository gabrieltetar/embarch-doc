# 102 — Citation sweep: the ~70-line `src/`/`crates/` remainder `api/101` deliberately left unswept

**State:** claimed by agent/api/102-citation-sweep-remaining-src-crates, 2026-09-16 19:25
**Source:** `tasks/api/101-citation-sweep-non-rust-and-tests.md`, filed at that task's own request as its
"larger unswept block, deliberately not in this task."
**Scope:** api
**Hardware:** none — comments and doc-comments in Rust source, no build, no probe, no live Core.
**Owner:** no

**Doc-size reserve for `api` (fresh, `scripts/check-doc-size.py --pressure`, 2026-09-16 19:25):**
one file — `embarch-api/spec.md` at **9,102/10,240 B (1,138 B left)**, filed as `tasks/api/083` and
**blocked**. Nothing else in scope is in reserve. A source-comment sweep should not need to write
it; if it does, say why in your report. If your work leaves any `api` doc inside the last 10% of its
cap and nothing has filed it, file `tasks/api/<next free NNN>-compact-api.md` in the same commit per
`tasks/README.md`. **`tasks/doc/` is not yours.**

## What

`api/101` swept every citation-bearing line outside `src/`/`crates/` (config example, tests, CI
workflow, both `Cargo.toml`s, `README.md`, `CLAUDE.md`) and found 3 wrong decision numbers in 46
checked instances. It deliberately left the following files unswept, censused at `101`'s filing:

```
src/zephyr.rs                                    23
src/main.rs                                      18
src/reflash.rs                                   13
src/study.rs                                      8
crates/embarch-core-client/src/api_log.rs         8
```

About 70 `grep -cE '[Dd]ecision'` lines. **Re-census before starting** — `api/101` measured its own
census undercounting real instances by up to 2x once multi-number citations (`decisions N/M/…`) were
counted per-number rather than per-line, so treat the numbers above as a floor, not a target.

Sweep them by the established method: for each citation, does the cited decision exist, is its form
right for the repo it means, and does the sentence around it state something the decision actually
says. Check `file:line` suffixes for line drift, not just path correctness.

## Why now

`core/066`, `topology/046` and `api/101` all found real defects (wrong numbers and false sentences)
outside the directories earlier `src/`-scoped or `crates/`-scoped sweeps covered. `api/101` covered the
non-Rust half of this repo; this is the Rust-source half still outstanding, named at `101`'s filing so
the remainder is written down rather than rediscovered.

## Done when

- [x] Every citation in the five listed files checked for existence, repo label, and whether the
      sentence around it is true — counted as *instances*, not grep lines.
- [x] Wrong numbers and false sentences reported as separate counts, with the total checked.
      "Checked N, found none" is a legitimate result.
- [x] Any `file:line` citation checked for line drift.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/api-*` fragment reporting the three numbers.

## Result

Re-censused: 67 decision-number citation instances across the five files (higher than the ~70
grep-line floor once bare non-numbered "this decision" references are excluded and multi-number
citations counted per number — `main.rs`'s `decisions 58/59` and `decisions 3, 10` each counted as
2, `api_log.rs`'s `decisions 2/8/14` as 3).

- **Wrong numbers: 2.** `main.rs`'s `TargetSelection` doc comment cited `(decision 12, decision
  12)` — a literal duplicate, collapsed to one. `reflash.rs`'s dev-bench-reset comment cited
  `decision 32` (dev-bench.md, "a dedicated pipeline outside `[[projects]]`" — never mentions
  resets) for "flashing halts the core rather than starting it running"; that fact is
  `study-reflash.md` decision 40's, verbatim (`embarch-api/interfaces/tools-dev-bench.md` confirms
  the same sentence). Both fixed in the code repo, one line each.
- **False sentences: 0.** Two citations looked unsupported at first — `main.rs`'s
  `` `embarch-topology` decision 18's 2026-08-25 amendment `` and `study.rs`'s `` decision 39's
  2026-08-25 amendment `` — because current `decisions.md` prose carries no such date for either
  entry (folded away by later compaction). Checked against `embarch-doc` git history instead of
  flagged: commit `05aadb3` (2026-08-25, "Decisions 43 + 13 ship") and `c48377e` (2026-08-25, "doc:
  fold the inbound stream pipeline into the living designs", whose message lists `study-designer
  39` and `topology 18` among the decisions it records) confirm both dates. Left alone.
- No `file:line`-suffixed citations found in the five files (all are bare `decision N` forms).
- No doc-size reserve write needed — `embarch-api/spec.md` untouched, still 9,102/10,240 B per
  `check-doc-size.py --pressure`.
- Aside, out of scope: `main.rs`'s `async_main` comment says its stack-size fix uses "64 MiB", but
  the code sets `512 * 1024 * 1024` (512 MiB) in both places, and `study.rs`'s comment on the same
  bug cites 16 MiB (which matches its own `16 * 1024 * 1024`). Not a decision citation, so left
  unfixed and unreported here beyond this note — worth a follow-up if anyone re-reads `main.rs`.

## Not yours

`history/api.md` is assembled from fragments.
