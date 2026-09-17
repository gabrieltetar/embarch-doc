# 102 — Citation sweep: the ~70-line `src/`/`crates/` remainder `api/101` deliberately left unswept

**State:** open
**Source:** `tasks/api/101-citation-sweep-non-rust-and-tests.md`, filed at that task's own request as its
"larger unswept block, deliberately not in this task."
**Scope:** api
**Hardware:** none — comments and doc-comments in Rust source, no build, no probe, no live Core.
**Owner:** no

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

- [ ] Every citation in the five listed files checked for existence, repo label, and whether the
      sentence around it is true — counted as *instances*, not grep lines.
- [ ] Wrong numbers and false sentences reported as separate counts, with the total checked.
      "Checked N, found none" is a legitimate result.
- [ ] Any `file:line` citation checked for line drift.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/api-*` fragment reporting the three numbers.

## Not yours

`history/api.md` is assembled from fragments.
