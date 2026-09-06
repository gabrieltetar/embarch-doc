# 012 — Check 16 reports what it found and never says where

**State:** done — `agent/umbrella/012-check-16-names-dir`, 2026-09-05
**Source:** the owner's live `embarch doctor` run, 2026-09-05
**Scope:** umbrella
**Hardware:** verify-only — see the debt below; the host-side half shipped with unit tests

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

- [x] Check 16's detail and its `--json` entry both name the resolved
      `study_results/` path. Detail reads `study_results/ at <path>: N entries, …`;
      `--json` gains a `path` field beside `code`, `null` on every other check and
      never absent (new decision 39).
- [x] The relocated-`%ProgramData%` caveat is visible from the output — **on the
      arm where it can actually mislead**, and only there. (The caveat is
      `embarch-token.md` **§5**, its last bullet, not §6; §6 does not exist. The
      stale `§6` citation in `setup.rs` is fixed too.) `data_dir_for` hardcodes
      `/mnt/c/ProgramData/embarch` for `wsl-host`, so a relocated `ProgramData`
      reads as "nothing yet at …" — identical to a machine that has simply never
      run a study. That arm now says the path is assumed rather than resolved.
      When the directory exists and holds runs it is self-evidently the right one,
      so the sentence would be noise on every healthy run.
- [x] Gate green, `changelog.d/umbrella-check-16-names-its-directory.changed.md`
      dropped.

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

## What shipped

- `Check` grows `path: Option<String>`, rendered into `--json` beside `code`,
  always present and `null` where a check resolved no single directory. **One
  path, not every path a check mentions** — check 16's per-project build roots
  are several and stay in `detail`.
- Check 16's measured arm names the directory: `study_results/ at <path>: …`.
  Its absent arm already did, which is the asymmetry the task was reporting.
- New **decision 39**, and `decisions/doctor.md` **split by mission**: 11, 37 and
  39 moved verbatim into `decisions/reporting.md` (what a consumer reads back),
  leaving 18, 19, 22, 23, 31 in `doctor.md` (what is checked). The file was
  10,566 B before this unit and would have gone over its 12 KB cap; `DOC-COMPACTION.md`
  §2 prefers a mission split to a squeeze, and a split restates nothing.
  9,454 B and 4,089 B after.
- Six new unit tests; `check_5_passes_and_never_scans_when_core_reports_a_probe`
  renamed (`tasks/umbrella/014`, below).

## Hardware-verification debt

**Not a board — a live `embarch doctor` on the owner's own machine**, where Core
is the Windows service and this binary runs under WSL2. Nothing under test ever
resolves a real data directory, by design, so the `wsl-host` path is exactly the
arm unit tests cannot reach.

What a run should print, on the primary topology, with the 50 runs already there:

```
[16] PASS Result and build-directory growth — study_results/ at /mnt/c/ProgramData/embarch/study_results: 50 entries, 809.0 MiB — swept to embarch-core's EMBARCH_STUDY_RESULTS_KEEP …
```

and `embarch doctor --json | jq '.checks[15].path'` →
`"/mnt/c/ProgramData/embarch/study_results"`. Every other check's `.path` is
`null`, and the key is present on all sixteen.

The `%ProgramData%` sentence should **not** appear on that machine, because the
directory exists. Seeing it there would mean the hardcoded path is wrong, which
is the finding the sentence exists to produce.

**This rides free on the live-`doctor` debt the owner already owes** (check 1 and
check 14's remaining `wsl-host` questions); it needs no run of its own.

## Riding along: `tasks/umbrella/014` — closed

All three items were correct on reading the source. `git rm`'d in this commit,
per the dispatch. What was done:

1. Decision 37 now carries a **Users, 2026-09-05: checks 1, 5, 10 and 14** line,
   and says why the per-check list belongs in `spec.md`'s table rather than here.
   `spec.md` already said 1, 5, 10, 14 — so the decision was stale by three
   checks, not one.
2. Decision 18 now enumerates **three** warns — `no-probe-found`,
   `no-probe-unchecked`, `no-status` — plus the pass code `probes-present`, which
   the old text omitted as well.
3. **Renamed, not restructured**, which is the cheaper of the two fixes 014
   offered and also the better one: `check_probes` takes a *finished* `UsbScan`,
   and that injection is the property that keeps `cargo test` off a real `/sys`.
   Moving the scan behind the count would have to take a closure or do the scan
   inside the check, giving up the purity to make a test name true. Now
   `check_5_verdict_ignores_the_usb_scan_when_core_reports_a_probe`, with a
   comment saying the scan does run. Decision 18 gained a paragraph saying the
   same thing about its own "after zero probes are reported" wording.
