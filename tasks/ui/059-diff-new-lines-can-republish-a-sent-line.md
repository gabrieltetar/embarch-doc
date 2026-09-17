# 059 — `diff_new_lines` can republish an already-sent line: decide, then record

**State:** claimed by agent/ui/059-diff-new-lines-republish, 2026-09-16 18:46
**Source:** `inbox/ui-diff-new-lines-spurious-republish.md`, filed by the `ui/057`
worker while verifying a reviewer counter-example against real code.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`diff_new_lines` (`embarch-ui/src/logs.rs:126`) walks overlaps from longest to
shortest and returns `new[k..]` on the first match. With `previous = ["A","B","A"]`
and `new = ["A","B","A2"]` — the trailing line grew, nothing else changed — `k=3` and
`k=2` fail, `k=1` matches on the repeated `"A"`, and the function returns
`["B","A2"]`, republishing `"B"`, which was already sent.

**This is not contrived.** Decision 13's own defect list, three bullets above, rests on
*"log lines repeat verbatim all the time (a retry, a heartbeat, a stack frame)"* to
justify a different fix in this same function's history. The same property produces
this duplicate.

**This task is a decision, not a foregone fix.** Two outcomes are legitimate and you
pick one with reasons:

1. **Fix it** — e.g. require the matched window to still contain the pre-growth content
   of the new window's trailing line, or another anchor that cannot match on a repeat.
   If you fix it, it needs a test that fails before and passes after.
2. **Accept it** — decision 13 already states a tolerance for the volume-aging case:
   *"a few duplicate lines is a smaller problem than missing ones."* If that tolerance
   covers this too, say so **in the decision text**, and add a test asserting the
   current behaviour, so the next reader meets it as recorded rather than as a surprise.

Either way the decision doc must end up stating what is true. Leaving the code and the
doc both silent about this is the one outcome that is wrong.

## Why now

`ui/057` corrected decision 13's claim from a universal to a conditional guarantee. The
condition it now states is exactly the one this defect exploits, so the doc currently
describes a behaviour that nothing tests and nothing decided to keep.

## Reserve

No `embarch-ui` file is in doc-size reserve this leg. **Decision 13 is tight**: it was
measured at 4,079 B against a per-decision cap of 4,096 B at merge `7694670`. Re-measure
with `scripts/check-doc-size.py --decisions` before you write into it. `tasks/ui/058`
may have spent some of that headroom restoring `append-only` — **read decision 13 as it
stands on `main` rather than as this task describes it**, and if what you have to say
does not fit, a **new numbered decision** is the correct shape, not a squeeze. Three of
the last four edits to this entry cut something they should not have while making room.

## Done when

- [x] A reasoned choice between fixing and accepting, stated in the commit message.
      Chosen: **fix**. Traced the concrete example by hand across three poll
      cycles: a spurious shorter match never drops genuinely new content (the
      matched prefix is always, by construction, identical to previously-sent
      previous-window content), so the defect is bounded to excess duplicates,
      not the anchor-swallowing class decision 13 already fixed once — but the
      fix itself (matching a run's last line by `starts_with` instead of `==`)
      is small, keeps the same longest-run-first search order, and closes the
      concrete case outright rather than leaving known-reachable duplicate
      output undocumented as merely "tolerated." Decision 13's own trailing
      paragraph (added by `ui/057`) described this exact failure mode as
      present-tense truth; fixing it without updating that sentence would have
      left the doc stating something false, so decision 13 was also edited
      (shrunk, since it measured exactly 4096 B / 0 room) and a new decision 27
      added with the reasoning and citing the two tests below.
- [x] If fixed: a test that fails against the current `diff_new_lines` and passes after.
      `a_growing_trailing_line_does_not_republish_a_line_already_sent` (plus
      `a_growing_trailing_line_followed_by_a_real_new_line_publishes_only_the_new_line`)
      in `embarch-ui/src/logs.rs`. Ran both against the unfixed code first —
      confirmed failure (`left: ["B", "A2"]`, `right: []`) before touching
      `diff_new_lines`, then again after the fix — both pass, and all 7
      pre-existing `logs::tests` cases still pass unchanged.
- [ ] If accepted: the tolerance stated in `embarch-ui/decisions/debug-tab.md` (new
      decision if decision 13 has no room), plus a test pinning the current behaviour.
      N/A — fixed instead, see above.
- [x] `cargo test` / `clippy --all-targets -- -D warnings` green in `embarch-ui`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment dropped.

## Not yours

`history/ui.md`. It is assembled from fragments.
