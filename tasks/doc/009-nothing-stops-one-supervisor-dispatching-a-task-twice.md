# 009 — Nothing stops one supervisor from dispatching one task twice

**State:** open
**Source:** two `inbox/` drops filed independently by two workers during leg 012 on
2026-09-05 — `doc-two-workers-shared-one-worktree.md` (`api/012`) and
`doc-double-dispatch-second-instance-umbrella-012.md` (`umbrella/012`). Drained into this
one file because they are one finding with two data points; both drops' evidence is
reproduced below rather than summarised away.
**Scope:** doc
**Hardware:** none
**Owner:** required — every candidate fix lives in `.claude/agents/`, `.claude/commands/`,
`../../embarch-fleet/ops.md` or `../../embarch-fleet/protocol.md`, all of which
`check-ownership.py --supervisor` refuses to a leg. Filed here so it is visible, not fixed.

## What

**Leg 012 ran both of its first two tasks twice, concurrently, in the same worktrees.** The
supervisor concluded both of its workers were dead and re-dispatched them; both were alive
and mid-pass. The claim commit is the interlock against *two supervisors* dispatching one
task. There is no interlock against *one supervisor* dispatching it twice, and branch,
worktree and ownership row are all keyed on the task — so two workers on one task share
everything and are protected by nothing.

**How the supervisor got it wrong, stated plainly, because it is the root cause.** It was
told the workers were gone, and it confirmed with `git status --porcelain` plus
`git log origin/main..HEAD` in all four worktrees: clean, zero commits. That reading was
*true at the instant it was taken and false ninety seconds later* — the `api` worker's
transcript ends mid-sentence at "Now I'll write the compacted `spec.md`", i.e. it had done
every byte of its analysis and had not yet written the first one. **`ops.md` §3's recovery
rule reads the worktree precisely because a branch's commit count is a bad liveness probe;
this leg found that the worktree is a bad one too, for the same reason — a worker's tree is
clean for the whole reading half of its run.** Neither probe distinguishes "never started"
from "about to write". `tasks/README.md` settles claim staleness by the **process tree**,
and that is the rule that would have been right here; nothing consulted it.

### Instance 1 — `api/012`, no damage

The second worker found `embarch-api/spec.md` changing under it (10,104 → 9,557 → 9,341 →
8,878 B over four minutes) and the modified set growing to eight `embarch-api/*` docs. **Its
first two write attempts failed only because its `old_string` no longer matched** — a silent
near-miss. Had one matched a paragraph the first worker had not yet reached, the two would
have interleaved edits in one working tree and either could have committed a half-finished
snapshot of the other's work, which would read as a finished compaction pass while being a
merge of two intents nobody held. It wrote nothing, committed nothing, pushed nothing.

### Instance 2 — `umbrella/012`, reached `origin`

- 21:26 — second worker finds the first's work in the code worktree's index, builds it,
  tests it, all green. `git status -sb` on the *doc* worktree returned only the branch line
  at this moment; the same command ninety seconds later listed two modified files.
- 21:27 — it commits that work as `c54d5f0` and pushes, **exactly as its dispatch prompt's
  "commit and push incrementally" instruction told it to.**
- 21:28–21:31 — it watches `decisions/doctor.md` shrink 12,931 → 9,454 B in 45 s, a new
  `decisions/reporting.md` appear, then `spec.md`, `features.d/`, `changelog.d/` and both
  task files change. It stops writing.
- 21:33 — the first worker commits `d9844dd` and **force-pushes, removing `c54d5f0` from
  `origin`.**

**No damage, by luck of content only:** `git diff c54d5f0 d9844dd` is empty — the first
worker's own staged bytes were what the second had committed, so the rewrite swapped an
identical tree under a different message. **Had the second worker written one line of its
own first, that line would have been silently deleted from pushed history by another agent's
force-push, with no conflict and nothing to notice it.**

## Why now

`protocol.md` §1 is "prevent collisions structurally; do not resolve them", and every
structural guard held except this one. Two instances in one leg is not a coincidence to
absorb; it is the rate at which this fires once a supervisor is willing to conclude a worker
died. It will fire again the first time a leg is resumed after an interruption, which under
the relay is routine.

Candidate fixes, in the order the drops argue for them, **none of them a leg's to make**:

- **Refuse to dispatch into a dirty worktree.** One `git status --porcelain` per worktree
  before spawning; non-empty means somebody is in there. Cheapest, and it catches instance 2
  outright. Instance 1's own evidence says **sample twice, seconds apart** — a single sample
  can land in a gap between the other agent's tool calls, which is exactly what happened at
  21:26.
- **Treat an existing worktree directory as a claim.** A fresh dispatch creates its
  worktrees; finding them already there is evidence, not a state to reuse. Strictly stronger
  than the dirty test and immune to the sampling gap.
- **Require process-tree evidence before concluding a worker is dead** — `ListAgents`, the
  rule `tasks/README.md` already states for claim staleness, applied to re-dispatch. This is
  the root cause and the other two are backstops for it.
- **Qualify "commit and push incrementally" in the worker dispatch prompt.** It is good
  advice against a kill and it is what turned a survivable collision into a force-push over
  pushed history. Pair it with "if the worktree was already dirty when you arrived, do not
  push" unless a guard above makes that unreachable.
- **Tell the worker the guard exists.** Both workers spent ten minutes re-deriving this from
  inside, one seeing a failed `old_string` and the other a changing `md5sum`. A worker cannot
  tell double-dispatch from a flaky edit without being told the failure mode has a name.

## Done when

- [ ] The re-dispatch path names what evidence it requires before it may conclude a worker is
      dead and hand its task to a second worker.
- [ ] A dispatch cannot start a second worker into a worktree another worker holds.
- [ ] The "commit and push incrementally" instruction is either qualified for the
      already-dirty case or made unreachable by the guard that precedes it.
