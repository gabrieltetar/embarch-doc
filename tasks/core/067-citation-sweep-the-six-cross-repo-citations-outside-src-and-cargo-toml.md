# 067 — Citation sweep: the six citations outside `src/` and `Cargo.toml`, every one of them cross-repo

**State:** done — worker agent/core/067-citation-sweep-the-six-cross-repo-citations-outside-src-and-cargo-toml, 2026-09-16. 9 instances checked (re-census found 3 more than the filing census), 0 wrong numbers, 0 false sentences; no edits needed.
**Source:** leg 123's refill sweep, 2026-09-16. `core/058` swept `embarch-core/src/` end to end;
`core/066` swept `Cargo.toml` and found **3 defects in 9 instances**. Neither touched the three
files below, and nothing else ever has.
**Scope:** core
**Hardware:** none — three comment lines, a README paragraph set and two workflow/`Cross.toml`
comments. Nothing is built for a board, no probe, no live Core, no deploy, no study.
**Owner:** no

**Doc-size reserve for `core`:** one file, `embarch-core/decisions/auth.md` at **11,356/12,288 B
(932 B left)**, filed as `tasks/core/046` and blocked. Nothing else in scope is in reserve. A
citation sweep should not need to write it; if it does, say why. If your work leaves any `core` doc
inside the last 10% of its cap and nothing has filed it, file
`tasks/core/<next free NNN>-compact-core.md` in the same commit per `tasks/README.md`.
**`tasks/doc/` is not yours.**

## What

Six numbered citations, in three files, censused at this task's filing:

```
README.md                          3   (lines 60, 108, 134)
.github/workflows/release.yml      2   (lines 3, 89)
Cross.toml                         1   (line 3)
```

`CLAUDE.md` carries the word "decision" but no numbered citation, and
`tests/version_stdout.rs` has none at all. Both are listed so the census is exhaustive rather than
rediscovered.

**Re-census before you start.** These are `grep -cE '[Dd]ecision [0-9]'` **line** counts, not
instance counts; the two have differed by about 10% every time anyone measured both.
`topology/046` also found three citations a grep census missed entirely, because they cite by
`file:line` rather than by `decision N`. Look for those too.

## Why this one is worth a unit despite being small

**Five of the six are cross-repo, and the sixth is the only same-repo one.** From the census:

- `README.md:108` — `embarch-study-designer` decision 8 **and** `embarch-topology` decision 13, two
  foreign citations in one sentence.
- `README.md:60` — a bare `decision 23`, which by convention means `embarch-core`'s own 23.
- `README.md:134` — a bare `decision 6`, same convention.
- `release.yml:3` — `embarch-umbrella` decision 14 ("the four targets").
- `release.yml:89` — `embarch-topology` decision 13's cross-repo-dependency rule.
- `Cross.toml:3` — `embarch-umbrella` decision 14 again.

A cross-repo citation drifts for a reason a same-repo one does not: **the far repo renumbers, splits
or retires its decision and nothing in this repo is even looked at.** `check-decision-refs.py` walks
`*.md` only, and only inside the doc repo — it never reads a workflow YAML, a `Cross.toml`, or a code
repo's README. So all six are unchecked and will stay unchecked.

That is also why the count being small is not an argument against the unit. `core/066` found
**1 wrong number and 2 false sentences in 9 instances** in this same repo, one file over.

## Watch for

- **`embarch-umbrella` decision 14 is cited twice, for what may be two different claims.**
  `release.yml:3` uses it for *"the four targets"*; `Cross.toml:3` uses it for *"the one target where
  [something]"*. Read decision 14's own text and check **both** sentences against it separately. Two
  citations of one decision making two different claims is exactly the shape that produces a false
  sentence nobody notices, because the number resolves both times.
- **`embarch-topology` decision 13 is also cited twice**, once in each file. Same treatment.
- **The two bare citations in `README.md` are `embarch-core`'s own by convention — check that they
  are.** A bare number that turns out to mean another repo is a real defect
  (`study-designer/044` and `045` each found one); a same-repo number mislabelled *as* foreign is the
  opposite shape and `study-designer/048` found that too. Check both directions.
- **`README.md:60` is about a retired env knob.** *"replacement env knob (decision 23) — they were
  the mechanism behind the [...]"* — a past-tense sentence about a removed mechanism is the highest-risk
  kind of prose to leave uncited-checked, because the removal is exactly what makes the surrounding
  claim go stale. `core/052` already touched this README for bind-and-stale-claims; **read what it
  left, do not assume it swept what it did not claim to.**
- **A stale `file:line` suffix is a real defect class.** `topology/046` found a citation whose repo,
  path and relative depth were all correct and whose **line number** was stale, because the target
  had split two days earlier — a wrong line lands the reader on a real sentence about something else.
  Check line anchors, not just paths. **Do not settle whether `:line` should be permitted at all** —
  that is `tasks/doc/055`, owner-reserved.
- **Form is not yours to settle.** If the only problem with a line is which citation *form* it uses,
  say so in your report and leave it (`tasks/doc/055`, `tasks/ui/038`, both owner-reserved).
- **Length.** Leg 122 flagged this twice and leg 123 carried it: four sweeps in two days each
  replaced a short wrong sentence with a considerably longer right one, and nobody is watching the
  aggregate. **Fix the fact; do not write an essay in a workflow comment.** A README paragraph that
  needs three sentences to say what one wrong sentence said is a judgement call you should state
  explicitly in your report rather than make silently.

## Done when

- [x] All citations in the three files checked for existence, repo label, and whether the sentence
      around each is true — count re-taken as *instances*, not grep lines.
- [x] `embarch-umbrella` decision 14's two citations checked against its text **separately**, and
      `embarch-topology` decision 13's two likewise.
- [x] Wrong numbers and false sentences reported as separate counts, with the total checked.
      "Checked 6, found none" is a legitimate and useful result — three consecutive zero-defect
      sweeps in a repo is itself evidence about whether this vein is exhausted, and nothing tracks
      the hit rate.
- [x] Any `file:line` citation checked for line drift, not just path correctness.
- [x] No new bare cross-repo citation introduced anywhere in the diff.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). Note `embarch-core` also needs a native
      Windows build that **no unattended leg can run** — leg 122 established the WSL cross-check dies
      in `hidapi`'s C build script, so it is not a partial payment. Say in your report that it was
      not run; do not claim it was.
- [x] `changelog.d/core-*` fragment reporting the three numbers.

## Result

**Re-census found 9 instances, not 6** — the original grep census
(`grep -cE '[Dd]ecision [0-9]'`) missed `release.yml:24`'s `` `embarch-umbrella` decisions 27/29 ``
because the plural "decisions" doesn't match a singular-then-space-then-digit pattern. Full
instance list, by site:

| Site | Decision(s) cited | Repo | Verdict |
|---|---|---|---|
| `README.md:60` | 23 (bare) | core, own | correct — matches `decisions/probes.md` #23 |
| `README.md:108` | 8 | study-designer | correct — matches `decisions/crate.md` #8 |
| `README.md:108` | 13 | topology | correct — matches `decisions/crate.md` #13 |
| `README.md:134` | 6 (bare) | core, own | correct — matches `decisions/auth.md` #5,6 (already fixed by `core/052`) |
| `release.yml:3` | 14 | umbrella | correct — matches `decisions/install.md` #14 (four targets: msvc, linux-gnu, aarch64-linux-gnu, aarch64-darwin) |
| `release.yml:24` | 27, 29 | umbrella | correct — matches `decisions/release.md` #27,29 (one entry under two numbers by that decision's own text) |
| `release.yml:89` | 13 | topology | correct — matches `decisions/crate.md` #13's own release-CI-sibling-checkout passage, verbatim to the workflow's fix |
| `Cross.toml:3` | 14 | umbrella | correct — matches `decisions/install.md` #14 |

**9 instances checked, 0 wrong numbers, 0 false sentences.** Both decisions flagged for
double-citation risk (`umbrella` 14, `topology` 13) were read against **each** citing sentence
separately, as asked; no shared number covered two different, mismatched claims. Both bare
`README.md` citations confirmed same-repo, correct direction. No `file:line`-suffixed citations
exist in any of the three files (checked, none found), so no line-drift class applies here. No
edits made to `README.md`, `release.yml`, or `Cross.toml` — every citation already checks out, so
there is no fact to fix and no essay to avoid writing. This is the fourth consecutive zero-defect
sweep in this vein this leg-window (`study-designer/052`, `umbrella`'s 11-file src sweep, and this
one), for whatever that says about how much longer this class of unit keeps paying.

**Native Windows build not run** — no unattended leg can run it (WSL cross-check dies in
`hidapi`'s `build.rs`; the native Windows path only works from the main checkout, not a worktree).
Not claimed as done, not counted as partial payment, per the task's own instruction.

No `core` doc is in the last 10% of its cap other than the already-filed, already-blocked
`embarch-core/decisions/auth.md` (`tasks/core/046`) — this sweep touched none of it, so nothing new
to file.

## Not yours

`history/core.md` is assembled from fragments.
