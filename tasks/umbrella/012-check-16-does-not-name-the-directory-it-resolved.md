# 012 — Check 16 reports what it found and never says where

**State:** open
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
