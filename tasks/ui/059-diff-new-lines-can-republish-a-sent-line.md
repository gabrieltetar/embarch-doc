# 059 — `diff_new_lines` can republish an already-sent line: decide, then record

**State:** blocked — leg 123 refused the merge on a supervisor diff read. The worker's fix
trades the duplicate for a **permanently dropped line remainder**, which inverts decision 13's own
stated preference. **Unparks the moment the fix publishes the grown line instead of swallowing it**
— see "Leg 123's refusal" below, which specifies it exactly. The branches are pushed and are worth
reusing, not redoing: `agent/ui/059-diff-new-lines-republish` in `embarch-ui` (code `21a48de`) and
`embarch-doc` (doc `dfe1d91`). **Neither was merged.**
**Source:** `inbox/ui-diff-new-lines-spurious-republish.md`, filed by the `ui/057`
worker while verifying a reviewer counter-example against real code.
**Scope:** ui
**Hardware:** none
**Owner:** no

## Leg 123's refusal — read this before the sections below

The unit chose **fix**, wrote two tests, confirmed they failed before and passed after, and got a
green gate in both repos. I still refused the merge, because the fix is wrong in a way the tests
were written to assert rather than to catch.

**The change.** In `diff_new_lines`, the overlap run's last line changed from `==` to
`new_head[k-1].starts_with(prev_tail[k-1])`, so a still-growing trailing line no longer breaks the
longest-run match.

**What that does to the grown line.** When the last line has grown, the match now succeeds at the
**full** overlap length `k`, and the function returns `new[k..]` — which is *empty*. The grown
line's new content is in `new[k-1]`, and `new[k-1]` is never returned. `publish_new_lines` then does
`*previous = latest` unconditionally, so the next poll compares against the grown text and the
remainder is never published by any later poll either. The worker's own first test asserts exactly
this: `diff_new_lines(["A","B","A"], ["A","B","A2"])` is `[]`. **"A2" never reaches the console, and
nothing ever sends it.**

**Why that is worse than what it replaced.** Before the change, the plain growth case (no repeated
line anywhere) found no overlap at all and fell through to the replay-the-whole-window branch: every
line duplicated once, **and the grown line delivered**. After the change, a viewer that is already
connected shows the line truncated at whatever it was when the poll caught it, permanently. Decision
13's own comment — quoted in `decisions/debug-tab.md` and in `logs.rs` itself — says *"a few
duplicate lines in a debug viewer is a smaller problem than missing ones."* This inverts that
ordering, and **decision 27 as drafted states the opposite of what the code does**: it says *"no
line is dropped, only 'B' is sent twice"*, which describes the **old** behaviour, not the new one.

**The fix is small and the diagnosis is the expensive half, which is already done.** When the run's
last line matched by *strict extension* rather than equality, the return should start at `k-1`, not
`k` — republish the grown line itself and everything after it. That is one duplicated line in
exactly the case decision 13 already tolerates duplicates for, and nothing is lost. Equality at the
last position must keep returning `new[k..]`, or every steady-state poll republishes its last line
forever, so the two cases have to be distinguished rather than merged.

**What the next worker owes, beyond the code:**

- A test for the **plain growth case with no repeated line** — `["X","Y"]` → `["X","Y2"]` — asserting
  the grown line is published. There is no such test today, which is why nothing caught this: both
  new tests use a window containing a deliberate repeat, so both exercise only the half the fix got
  right.
- A test that the **steady state does not republish**: `["X","Y"]` → `["X","Y"]` must stay empty.
- **Decision 27 rewritten, not patched.** Its current text asserts a property the code does not have.
  Re-measure `scripts/check-doc-size.py --decisions` first — the worker shrank decision 13 from 514 B
  to a 309 B pointer to make room, and that shrink is on the unmerged branch, not on `main`.
- The `decisions/debug-tab.md` bullet above 27 and `logs.rs`'s own doc comment both describe the
  conditional tolerance; whichever survives must say what is true of the merged code.

**Do not re-derive this from scratch.** The branches carry a correct diagnosis of the original
defect, a correct root-cause account, and two tests that are right about the repeat case. The
disagreement is one index and the claim built on top of it.

**Measured, not reasoned.** I compiled both versions of `diff_new_lines` side by side and ran six
cases. This is the table; reproduce it rather than trusting it.

| `previous` → `new` | before the change | after the change |
|---|---|---|
| `["X","Y"]` → `["X","Y2"]` (plain growth) | `["X","Y2"]` | **`[]`** |
| `["A","B","A"]` → `["A","B","A2"]` (the task's case) | `["B","A2"]` | **`[]`** |
| `["A","B","A"]` → `["A","B","A2","C"]` | `["B","A2","C"]` | **`["C"]`** |
| `["X","Y"]` → `["X","Y"]` (steady state) | `[]` | `[]` |
| `["X","Y2"]` → `["X","Y2Z"]` (line completes) | `["X","Y2Z"]` | **`[]`** |
| `["X","Y2Z"]` → `["X","Y2Z","W"]` | `["W"]` | `["W"]` |

Four of the six rows lose the grown line's content. Row 3 is the worst of them: `C` is published
while `A2` is not, so the console ends up holding a **truncated line with complete lines after it** —
a reader has no way to tell that line was cut. Rows 1 and 5 together mean a line that grows across
two polls is never delivered in full at any point in its life.

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

- [ ] A reasoned choice between fixing and accepting, stated in the commit message.
- [ ] If fixed: a test that fails against the current `diff_new_lines` and passes after.
- [ ] If accepted: the tolerance stated in `embarch-ui/decisions/debug-tab.md` (new
      decision if decision 13 has no room), plus a test pinning the current behaviour.
- [ ] `cargo test` / `clippy --all-targets -- -D warnings` green in `embarch-ui`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.

## Not yours

`history/ui.md`. It is assembled from fragments.
