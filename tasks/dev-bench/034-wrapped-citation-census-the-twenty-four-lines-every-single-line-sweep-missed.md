# 034 — Wrapped-citation census: the twenty-four lines every single-line sweep missed

**State:** open
**Source:** `tasks/doc/071` (`Owner: required`, open), second `Done when` bullet — *"each
sub-project already declared 'citation swept' end to end gets a follow-up task re-censusing with the
wrap-aware method"*. `embarch-dev-bench` was swept by `dev-bench/031`, `032` and `033`, which
between them covered `app/src/` and `app/tests/` and reported the repo swept out — **all of them
single-line greps**. The same follow-up has already run for `embarch-core` (`core/069`),
`embarch-api` (`api/106`) and `embarch-umbrella` (`umbrella/074`).
**Scope:** dev-bench
**Hardware:** none — source comments only. Nothing is built, no board, no probe, no flash, no
toolchain. This is C source read as text; it is **not** one of this repo's toolchain-gated tasks.
**Owner:** no

**Doc-size reserve for `dev-bench`: three files, all filed and all blocked.**
`embarch-dev-bench/open.md` (4,782/5,120 B, 338 B left) and `spec.md` (9,460/10,240 B, 780 B left)
against `tasks/dev-bench/012`, and `decisions/link.md` (11,241/12,288 B, 1,047 B left) against
`tasks/dev-bench/014`. This unit is a source-comment census and should not need to write any of
them; if it turns out you must, spend the bytes and say so in your report.

## What

A citation whose word `decision`/`decisions` sits at the end of a comment line and whose **number**
sits on the next line is invisible to every census this suite has run: they all match a single line.
`core/068` found the class and `tasks/doc/071` named it. This repo is the one where it matters most
— `dev-bench/033` found **3 wrong numbers and 12 missing repo labels** in the single-line surface
alone, the highest defect density of any repo in the chain, and C block comments here wrap hard.

`grep -rnIE '[Dd]ecisions?[[:space:]]*$'` over `embarch-dev-bench`, excluding `.git` and `build/`,
returns about **24** lines, concentrated in:

```
app/src/serial_protocol.h        4
app/src/serial_protocol.c        3
app/src/ble_bridge_real.c        3
app/src/main.c                   2
app/src/study_ffi.h              2
app/tests/serial_protocol/src/main.c  2
app/src/eap.h, eap_interp.c, eap_interp.h, ble_bridge.h, ble_bridge_stub.c,
  study_ffi_stub.c, app/tests/scan_seen_mfg/src/main.c   1 each
workspaces/nordic/manifest/west.yml   1
```

**Re-run that grep yourself and report the count you actually got** — this one was taken at
`5a9b63b` and `main` moves. Check whether the `west.yml` hit is a real citation or a coincidence and
say which; do not fix a line that is not one.

## What to check, per citation

Read the whole wrapped citation (this line, the next, and the line *above*), then answer three
separate questions. `033` found defects in all three categories, so do not collapse them:

1. **Does the number resolve?** Does a decision with that number exist in the repo the sentence
   names — `embarch-dev-bench`'s own `decisions.md`/`decisions/*.md` when unlabelled, the named
   repo's when labelled?
2. **Is it the right repo?** A wrapped citation is exactly where a repo prefix goes missing, because
   the prefix sits on the line before the one a census matched; `core/068` mis-filed two citations as
   "bare — own repo" for that reason. **And this repo has a live same-number collision**: `033`
   found `decision 39` in `main.c` resolving to `embarch-study-designer`'s at some sites and to *this
   repo's own* decision 39 at others, in the same file, split by sentence. Same number, two right
   answers. Read the sentence, not the number.
3. **Is the sentence true?** The one a resolution check cannot answer, and the one that produced
   `033`'s most expensive defect: a comment was relabelled to a decision that resolved fine and
   **contained nothing about the claim being made**. Read the cited decision's own body and check it
   says what the comment says it says.

## How to report

Report **every cited occurrence**, not deduplicated `(repo, number)` pairs — one line citing two
numbers is two instances, and the same number cited on two lines is two instances. This convention
is the chain's (`core/069` 15 lines/25 instances, `api/106` 18/20, `umbrella/073` 13/30) and
`umbrella/074` drifted from it; say `N lines / M instances` explicitly so the running tally stays
comparable.

## Done when

- [ ] Every wrapped citation the grep returns is read in full and answered against all three
      questions above.
- [ ] Every wrong number fixed, every missing repo label added, every false sentence corrected or —
      if you cannot establish what the right referent is — **left alone and reported**, never guessed.
- [ ] `N lines / M instances / W wrong / L labels / F false` stated in the report.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). **This repo builds under a Zephyr
      toolchain that is not installed**, so there is no `west build` to run and none is expected: the
      gate for this unit is `check-docs.py` in `embarch-doc` plus
      `scripts/check-client-names.py --repo <code worktree>`. Say in your report that no firmware was
      built and why — do **not** attempt a build.
- [ ] `changelog.d/` fragment. A zero-defect result is still a result and still gets one.

## Not yours

Do not widen this to single-line citations — `031`/`032`/`033` swept those and re-reading them is
what this task exists to avoid. Do not amend a decision because a comment disagrees with it: the
comment is what this task may change. Do not touch `workspaces/` beyond reading the one `west.yml`
line, and do not move a Zephyr pin. If a decision itself looks wrong, that is an `inbox/` drop,
written to `/home/gabriel/Github/embarch/embarch-doc/inbox/` by absolute path.
