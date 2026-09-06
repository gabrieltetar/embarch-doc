# 023 — `doctor` check 1 does not locate the `embarch-api` binary, and three checks are degraded by it

**State:** done, agent/umbrella/023-locate-embarch-api, 2026-09-06
**Source:** `embarch-umbrella/open.md`, bullets 1 and 7 — "**check 1 does not locate that binary** here" and "Check 8's shell-out has never run against a real `embarch-api`. **Predicted here: a warn**, `embarch-api not located`."
**Scope:** umbrella
**Hardware:** verify-only — the locator and its behaviour are testable against a synthetic tree; confirming it finds the real binary on the primary topology is a debt for the owner's own session, not for you.
**Owner:** no

## What

`embarch-umbrella/open.md` records the same missing capability from three
directions, and never as its own item:

- **Check 11** reads Core's schema version and **cannot ask `embarch-api` for its
  own**, so a mixed install stays invisible — "check 1 does not locate that
  binary here".
- **Check 8** shells out to `embarch-api` and has never run against a real one;
  the doc's own prediction for this machine is a warn, `embarch-api not located`.
- `embarch-api/open.md` independently records "Nothing reads `versions` yet:
  `doctor` check 11 compares `embarch`'s *own* host schema copy, so a mixed
  install stays invisible. Another repo's fix." **This is that other repo.**

**Establish the premise before you fix anything.** "Check 1 does not locate that
binary **here**" may be a defect, or it may be correct behaviour on a machine
where `embarch-api` is a WSL debug build rather than an installed one. Read check
1, say in your report which it is, and let that decide the shape of the work:

- If check 1 is looking in the wrong places, widen it, and say what the right set
  of places is and why — an installed suite's layout, `PATH`, and whatever the
  registered agent-CLI entry already tells `doctor` (check 10 reads that entry
  structurally now, per decision 40, so the path may already be in hand).
- If check 1 is right and this machine is simply not an installed suite, then the
  defect is that three bullets describe it as a gap. Say so once, in the place
  that makes checks 8 and 11 legible, and delete the misdescription rather than
  leaving three half-statements of a non-problem.

Either way the outcome is that a reader of `open.md` can tell whether
`embarch-api` is locatable, and checks 8 and 11 stop being blocked on an
unexamined premise.

## Why now

Three bullets in two sub-projects' `open.md` files describe one missing
capability, none of them owns it, and one of them has been carrying a *prediction*
of what a real run would print rather than a run. It is also the cheapest of the
umbrella open questions that needs no board: everything else live in that file is
waiting on a narrow-bound Core, a permission-denied probe, a Mac, or a bench.

## Done when

- [x] **Defect.** `setup` had installed `embarch-api` at decision 28's canonical
      location beside `embarch` itself and written the sourcing line into
      `~/.bashrc`; `locate_api` read `EMBARCH_API_BIN` and `PATH` and nothing
      else, so `command -v embarch-api` succeeds in an interactive shell and
      fails in `bash -c` **and** `bash -lc` (`.profile` is not a file `setup`
      writes). Check 1's verdict on an installed suite therefore turned on
      whether the shell that ran it was interactive, and with Core located and
      the API not it hard-Failed `not-found`. Argued in
      [decision 42](../../embarch-umbrella/decisions/doctor.md).
- [x] Decision 42, in `decisions/doctor.md` — three sources added, the
      contested rank (the agent CLI's registration ahead of `PATH`) argued with
      its losing alternative, `init` deliberately excluded, and the
      rc-file residual stated rather than fixed.
- [x] Both gain the located path, and their shell-out contract was **observed
      against a real `embarch-api`** rather than predicted — that binary needs
      no Core and no bench, so running it is neither hardware nor a live Core:
      `--json`/`--config` must precede the subcommand (clap exits 2 otherwise),
      `versions` answers `host_type_schema_version` 17 from both copies on this
      bench, `list-targets` answers `{success, targets}` on stdout at exit 0 and
      `{success:false, error}` at exit 1. **Neither check has run inside a
      `doctor`**, which needs a live Core — recorded in `open.md`, and below as
      a hardware-verification debt.
- [x] Bullet 1's settled clause is deleted outright and bullet 7 is replaced by
      what is actually still unrun; `inbox/api-open-md-versions-is-read-now.md`
      carries the `embarch-api` half.
- [x] `changelog.d/umbrella-locate-api-reads-the-registration.fixed.md`; rows
      `umbrella-061` and `umbrella-030` updated in `features.d/`. Gate green.

## Doc-size reserve for `umbrella` — read before you plan, this one is unusual

**`embarch-umbrella/open.md` is 4,661 B against a 5,120 B cap — in reserve at
91.0%, 459 B of headroom**, and you are going to write it. `decisions/bind.md` is
also in reserve at 11,409 / 12,288 B (92.8%); you should not need it.

Both are filed against `tasks/umbrella/009-compact-docs.md`, which is **`blocked`
on `In flux: yes` and stays blocked** — check 17's entry is still owed a live
narrow-bound Core. Per `supervise.md`, **a blocked compaction task parks the pass,
not the reserve**, so: **compact `open.md` as part of this unit.** You are the
actor spending the reserve, so you are the only one who can shorten what you are
rewriting without writing a clean statement of something about to be wrong.

Carry `009`'s `Must not delete:` list for `open.md` verbatim — read it in that
task file, it is long and specific. Its `open.md` clauses are: **check 15 is not a
hash comparison and must not be read as one**; **check 17's two Fail branches have
never met a real narrow-bound Core, and which half of that debt each arm settles**;
and **`saved.host` is sticky and check 2 still reads it, including why it was left
unfixed** — that last is a deliberate abstention, and without the reason it reads
as an oversight somebody will "fix" on a guess.

Close only `open.md`'s item in `009`; leave the task blocked and leave
`decisions/bind.md`'s item open. **`umbrella/021` reported the ride-along spent** —
no cross-doc duplication remains, 5 KB is a role cap on a single file so nothing
can split, and what is left is protected prose. `umbrella/022` then paid 419 B by
**deleting one answered bullet outright**. That is the shape available to you:
this task answers or reframes bullets 1 and 7, so deleting what it settles is the
budget. If you genuinely cannot come out level and the `Must not delete:` list is
what stops you, **say so in your report and leave it filed** — do not delete
protected prose to hit a number.

If you push any *other* file into reserve, file
`tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit —
**`tasks/umbrella/`, never `tasks/doc/`**, which `check-ownership.py` refuses to you.

## Hardware-verification debt

**One `embarch doctor --json` on the primary topology, in the owner's own
session.** Everything host-side is done and unit-tested, but no `doctor` run has
used decision 42's locator, and this bench is its awkward case: two
`embarch-api` binaries, different contents, identical `--version`, and the one
the agent CLI is registered to run is a debug build. What to look for in the
output: check 1 Passes rather than Failing `not-found`; its detail names the
provenance and the mixed install; checks 8 and 11 answer instead of warning
`embarch-api not located`; check 11 compares 17 against 17. Also worth one
`bash -c 'embarch doctor'` — the non-interactive shell is the case that made
this a defect at all.

## Reserve accounting

`open.md` 4,661 -> **4,527 B (88.4%)**, out of reserve; its item in
`tasks/umbrella/009` is closed and nothing on that task's `Must not delete:`
list was touched. It was paid by deleting what this task settled, not by
squeezing. **`decisions/doctor.md` went the other way**, 6,188 -> **11,095 B
(90.3%)**, and is filed back onto `009` in this same commit — the trade was
deliberate, since `topology.md`, where decision 42's sibling decision 38 lives,
would have gone over cap outright. `spec.md` 9,137 -> 9,154 B (89.4%), still out.
