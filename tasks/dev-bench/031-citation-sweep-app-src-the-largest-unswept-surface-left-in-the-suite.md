# 031 — Citation sweep: `app/src/`, the largest unswept citation surface left in the suite

**State:** open
**Source:** leg 124's refill sweep, 2026-09-16. The sweep chain has now closed
`embarch-topology`, `embarch-umbrella` and `embarch-outpost` completely — every one of their
citation-bearing files has had a decision-existence-and-sentence-truth pass, and the last two
passes in each found zero defects. `embarch-dev-bench` is the one repo where that pass has
**never** been run.
**Scope:** dev-bench
**Hardware:** none — C comments and doc-comments only. Nothing is built for a board, nothing is
flashed, no probe, no live Core, no study. **This classification depends on the change staying
comment-only.** `tasks/README.md`'s Hardware section says `embarch-dev-bench` is the suite's one
`toolchain` repo: its Zephyr tree lives *inside* the repo under gitignored
`workspaces/*/{zephyr,modules,.west}`, so a worker's worktree holds `app/` and a `west.yml` and no
Zephyr at all, and a build there would need a multi-GB `west update` first. **If a fix you want to
make touches anything but a comment, stop and leave the task `open` saying so** — that version of
the work is `toolchain` and belongs in the main checkout, where the
`app/tests/serial_protocol` ztest suite builds for `native_sim` and runs its 57 tests in about a
minute.
**Owner:** no

**Doc-size reserve for `dev-bench`: three files, all filed and all blocked.**
`embarch-dev-bench/open.md` at **4,782/5,120 B (338 B left)** and `spec.md` at
**9,460/10,240 B (780 B left)**, both filed as `tasks/dev-bench/012`;
`decisions/link.md` at **11,241/12,288 B (1,047 B left)**, filed as `tasks/dev-bench/014`.
A source-comment sweep should not need to write any of them. If it does, say why in your report.
If your work leaves any `dev-bench` doc inside the last 10% of its cap and nothing has filed it,
file `tasks/dev-bench/<next free NNN>-compact-dev-bench.md` in the same commit per
`tasks/README.md`. **`tasks/doc/` is not yours.**

## What has and has not been done here

Two previous units touched citations in this repo, and **neither was this pass**:

- `ble_bridge_real.c`'s 39 dead `design.md §3` citations were **repointed to
  `decisions.md`/`decision N`** — a *form* fix. Nothing checked whether the decisions they now
  name say what the surrounding comment claims.
- `dev-bench/029` fixed 22 bare section numbers pointing at a deleted document — again form,
  not truth.

So every `decision N` in this repo's firmware has had its *spelling* corrected and its *claim*
unread.

## Census (grep **line** counts, `grep -cE '[Dd]ecision [0-9]'`, taken 2026-09-16)

```
app/src/main.c                            56
app/src/serial_protocol.h                 53
app/src/ble_bridge_real.c                 49
app/src/serial_protocol.c                 40
app/tests/serial_protocol/src/main.c      38
app/src/ble_bridge.h                      20
app/src/eap.h                              7
app/src/dev_bench_log.h                    7
app/tests/dev_bench_log/src/main.c         6
app/src/dev_bench_log.c                    5
README.md                                  5
app/src/study_ffi.h                        4
```

**Re-census before you start.** These are line counts, not citation instances; every chain that
measured both found them differing by 10%–100%, the larger gaps caused by multi-number citations
(`decisions N/M`) and range citations (`decisions 58-62`) that count once as a line and several
times as instances. Treat the numbers above as a floor.

**Take `app/src/main.c` and `app/src/serial_protocol.h` first** — the two largest, and the two a
reader of this firmware opens first. If you run out of budget, sweep what you take
**thoroughly** and file the next `tasks/dev-bench/<NNN>` naming exactly which files remain, the
way the `study-designer/044`–`054` chain does. A half-read file reported as swept is worse than
an honest partial.

## The gate cannot build this repo, and that is expected, not a blocker

`embarch-dev-bench` has no `Cargo.toml`, so the cargo half of the gate selects nothing, and no
unattended worker has `west` or a Zephyr SDK — so neither a `native_sim` build nor the
`app/tests/serial_protocol` ztest suite can be built. That is the standing debt from
`dev-bench/019`, `020` and `022`, and this task **restates it rather than adding to it**.

`dev-bench/022` landed under exactly these conditions and its supervisor's reasoning applies
here verbatim: **a comment-only change is untestable in the least dangerous way there is.**
What you *can* verify mechanically, and must: the grep gate is zero, comment-block balance is
unchanged per file, no line crosses 100 columns, and `check-client-names.py` is clean on the
code repo. **Say plainly in your report that nothing was compiled.** Do not claim a partial
build as a partial payment.

## Method

For each citation, in this order:

1. **Does the cited decision exist**, in the repo the citation's form says it is in? A bare
   `decision N` means `embarch-dev-bench`'s own; a foreign one must carry the `` `<repo>` ``
   label (`DOC-CONVENTIONS.md`, "Referring to a decision").
2. **Read the cited decision's body, then read the sentence around the citation.** A number that
   resolves is not evidence the claim holds — across five-plus days of these sweeps the real
   yield has been prose a decision made false, or a citation pointing at the wrong but real
   decision, not a typo in the number.
3. **Check every number in the cited sentence**, not just the decision number.
   `study-designer/053`'s only find was a wrong enum-variant count in a sentence whose citation
   resolved perfectly.
4. **Check `file:line` suffixes for drift**, not just path correctness. `topology/046` found a
   citation whose repo, path and depth were all right and whose line number was stale after a
   split — a wrong line lands the reader on a real sentence about something else.

## Watch for

- **This repo mirrors `embarch-study-designer`'s constants and enums by hand** — 33 of them plus
  three enums, per `tasks/dev-bench/010`. A comment citing a `study-designer` decision about a
  constant is a cross-repo claim about a value this repo copies, so check the value too, not
  only the decision.
- **`check-decision-refs.py` walks `*.md` only, inside the doc repo.** It has never read a `.c`
  or a `.h`. There is no mechanical backstop here and nothing will fail if a citation is wrong.
- **Citation form is not yours to settle** — `tasks/doc/055` and `tasks/ui/038`, both
  owner-reserved. If the only problem with a line is which form it uses, say so and leave it.
- **Length.** Four sweeps in two days each replaced a short wrong sentence with a considerably
  longer right one and nobody was watching the aggregate. Fix the fact; do not write an essay in
  a firmware comment.

## Done when

- [ ] At least the two largest files fully swept, every citation checked for existence, repo
      label, and whether the sentence around it is true — counted as *instances*, not grep lines.
- [ ] Wrong numbers and false sentences reported as **separate** counts, with the total checked.
      "Checked N, found none" is a legitimate and useful result: whether this vein is exhausted
      is an open question and honest zeros are the only thing that answers it.
- [ ] Any `file:line` citation checked for line drift.
- [ ] A follow-up task filed naming exactly which files remain, or a statement that the repo is
      swept out.
- [ ] Mechanical checks green (grep gate zero, comment-block balance, 100-column limit,
      `check-client-names.py`), **and the report says in as many words that nothing was
      compiled.**
- [ ] `changelog.d/dev-bench-*` fragment reporting the counts.

## Not yours

`history/dev-bench.md` is assembled from fragments.
