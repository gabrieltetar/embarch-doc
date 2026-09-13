# 019 — Decision 26's *Rejected* clause says this repo has never had CI, and it has since 2026-09-11; the same fix's own runtime note miscites decision 22

**State:** open
**Source:** leg 105 refill sweep, 2026-09-13. Both halves verified against the code and the
workflow file before filing.
**Scope:** outpost
**Hardware:** none — a decisions file and two shell strings. Nothing is built and no board is
touched.
**Owner:** no

## What — two defects in one paragraph's blast radius

**(a) The *Rejected* clause of `decisions/testing.md` decision 26 rests on three facts, and all
three are now false.** It closes with:

> Closing it for real would mean guaranteeing the siblings are actually there when it matters,
> which is what a CI workflow would buy; this repo has never had one (`../../embarch.md` §5), and
> whether to build one is a suite-scope call this repo cannot file
> (`../../../embarch-fleet/protocol.md` §8), not a problem parked against any task on disk.

- **`embarch-outpost/.github/workflows/host-tests.yml` exists** (2026-09-11).
- **The suite-scope call was made**: [suite decision 2](../../suite/decisions.md) (text in
  `suite/decisions/tooling.md`) runs `decoder_unit.py` and `vocab_check.py` on every push and PR,
  and states which legs stay uncovered and why.
- **`embarch-outpost/open.md` and `embarch.md` have already been updated** to say so. This clause
  is the last place in the repo still asserting the old state.

**The clause's conclusion survives and must not be thrown out with its premises.** The
cross-decoder leg is still deliberately *outside* that workflow — suite decision 2 says so
explicitly — so "a missing sibling fixture stays a skip" is still the right answer. What changed is
the *reason*: it is no longer "there is no CI and this repo cannot ask for one", it is "there is CI
and this leg is deliberately not in it, with a named reversal condition". Rewrite the clause to
rest on the facts that are true, keeping the rejection.

**(b) Both copies of the runtime skip note cite decision 22, and decision 26 is the one that says
it.** `embarch-outpost/tests/run-all.sh:26` (the `EXIT` trap) and `:100` (the summary block) both
print:

> See decisions/testing.md decision 22 for why that stays a skip rather than a failure.

Decision 22 is *leg ordering above the `WEST` guard*. Decision 26 is *"A skipped cross-decoder is a
skip, not a failure, and is restated in the final summary"* — and decision 26 is the decision that
added this very note, printed from that very `EXIT` trap. Decision 22's own text forward-references
26 for exactly this. Same defect class as `tasks/core/033` and `tasks/ui/038`.

## Why now

A reader who follows the citation lands on a decision about shell ordering and finds nothing about
skips; and a reader of the *Rejected* clause is told this repo has no CI while its own
`.github/workflows/` says otherwise. Neither is visible to any gate:
`check-decision-refs.py` resolves decision numbers in `*.md` under a repo root, so the shell
strings are invisible to it, and nothing at all compares a decision's prose against the repo's
file tree.

## Done when

- [ ] Decision 26's *Rejected* clause states the CI situation as it is — `host-tests.yml` exists,
      [suite decision 2](../../suite/decisions.md) is the suite-scope call that was made, the
      cross-decoder leg is deliberately outside it — while **keeping the rejection**, with the
      residual risk it prices still named.
- [ ] Both `run-all.sh` strings cite **decision 26**, not 22. `grep -n "decision 22" tests/` in
      `embarch-outpost` returns nothing that means the skip rationale.
- [ ] Check nothing else in `embarch-outpost/` — prose or shell — still says this repo has no CI.
- [ ] Host-side checks green; say plainly what could and could not be run (the Zephyr legs of
      `tests/run-all.sh` need a `west` toolchain that is not present in a worker's worktree —
      standing debt, not introduced here).
- [ ] `changelog.d/` fragment.

## Do not

**Do not add the cross-decoder to `host-tests.yml`.** Suite decision 2 deliberately leaves it out
and records the reversal condition that would bring it in; changing that is a suite-scope call and
not this task's. This task corrects what the decision *says*, not what the workflow *does*.
