# 012 — Check 16 reports what it found and never says where

**State:** claimed by agent/umbrella/012-check-16-does-not-name-the-directory-it-resolved, 2026-09-05 21:27
**Source:** the owner's live `embarch doctor` run, 2026-09-05
**Scope:** umbrella
**Hardware:** none

## What

Check 16 reports `study_results/: 50 entries, 809.0 MiB` and **never names the
directory**, in text or in `--json`. On `wsl-host` that path is
`setup::data_dir_for(WslHost, false)` → `/mnt/c/ProgramData/embarch`, reached
across the `/mnt` mount, and the whole reason the check existed unverified for
so long is that nobody could see whether it resolved the *right* place. Confirming
it on 2026-09-05 meant listing the directory by hand and matching the counts.

A check whose job is to resolve a real data directory should print which one it
resolved. Add the path to the detail string and to the `--json` object; the
build-directory half already names its path, so this is the two halves agreeing.

## Why now

Cheap, and it closes the verification loop that took a live run plus a manual
`du` to close once. The next person who wants to know whether it found the
Windows Core's results or something on the Linux side should read one line.

## Done when

- [ ] Check 16's detail and its `--json` entry both name the resolved
      `study_results/` path.
- [ ] The relocated-`%ProgramData%` caveat `embarch-token.md` §6 records is
      visible from the output, or the doc says why it is not worth surfacing.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.

## Riding along: `tasks/umbrella/014`, and the reserve — added by leg 012 at dispatch

**`tasks/umbrella/014-decision-37-and-18-text-stale-after-check-5.md` is yours to close in
this same commit.** Its own file says so — it is three sub-threshold text corrections that
"should not be dispatched on its own" and should fold into whichever `umbrella` task next
edits `decisions/doctor.md`, which this one does. Read that file and do all three:
decision 37's "check 10 is the only user today" (check 5 is now the second), decision 18's
"the two warns" (there are three — `no-status` for the check-4 skip), and the overstated
test name `check_5_passes_and_never_scans_when_core_reports_a_probe` (rename it to what it
asserts, or move the scan behind the count). Then set that file's `**State:** done` and
`git rm` it as part of your commit, and say in the changelog fragment that it rode along.
If one of the three turns out to be wrong on reading the source, leave that item, say so
in `tasks/umbrella/014`, and put the file back to `open` with only that item left.

**Reserve, measured by leg 012 at dispatch:** no `embarch-umbrella` file is in reserve —
`check-doc-size.py --pressure` names only two `api` files. But **`embarch-umbrella/open.md`
is at 4,606 / 5,120 B (89.96%), four hundredths of a percent under the 90% line**, and
`spec.md` is at 9,131 / 10,240 B (89.2%). One added sentence in `open.md` puts it in
reserve. `decisions/doctor.md` is 10,566 / 12,288 B (86%) and has room.

**If your edit spends that reserve — pushes `open.md` or `spec.md` past 90%, or leaves it
there — you owe the ride-along, not a new task**: `tasks/umbrella/009-compact-docs.md` is
`blocked` on `In flux: yes` and a blocked compaction task parks the pass, not the reserve
(`DOC-COMPACTION.md` §2). So compact that file inside this same commit, carry 009's
`Must not delete:` list, and close only that file's item there. The cheaper move first:
this task removes an unanswered question from `open.md`, so shortening should pay for
itself. Measure with `python3 scripts/check-doc-size.py --pressure` before you report.
