# 023 — `doctor` check 1 does not locate the `embarch-api` binary, and three checks are degraded by it

**State:** claimed by agent/umbrella/023-locate-embarch-api, 2026-09-06 04:25
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

- [ ] Check 1's actual behaviour with respect to `embarch-api` is established and
      stated — defect or by-design — with the evidence you used.
- [ ] Whichever of the two shapes above follows is done, and a decision recorded
      in `embarch-umbrella/decisions/` with the losing alternative argued.
- [ ] Checks 8 and 11 either gain the located path or gain an accurate statement
      of what they cannot do and why. **Do not fabricate a live result for
      either** — no run against a real `embarch-api` or a live Core is available
      to you; what you cannot observe stays an explicit debt.
- [ ] `embarch-umbrella/open.md`'s bullets 1 and 7 reflect the outcome, and the
      `embarch-api/open.md` half is **not yours to edit** — drop a note in
      `inbox/` for it instead (`../../embarch-fleet/protocol.md` §3).
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

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
