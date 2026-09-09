# outpost: README.md Status section contradicts spec.md §4 on measured overhead

**State:** claimed by agent/outpost/013-readme-overhead-status, 2026-09-08 22:34
**Promoted** from `inbox/outpost-readme-status-overhead-stale.md` by leg 048, unchanged apart from
this line, the number, and the `Scope:` field taking the sub-project name. **I asked the reviewer
to file this if it agreed it deserved a drop**, which means the finding may be mine as much as
its — recorded so nobody reads it as an independent catch.
**Source:** embarch-reviewer, review of outpost/004 (merge SHAs embarch-outpost `9621112`, embarch-doc `a06da6f`)
**Scope:** outpost
**Reserve (leg 055, 2026-09-08):** `embarch-outpost/open.md` 4891/5120 B (229 B
left), `decisions/module.md` 7730/8192 (462 B), `decisions/transport.md`
7114/8192 (1078 B), `spec.md` 9187/10240 (1053 B). The first two are already in
reserve and `tasks/outpost/012-compact-outpost.md` is filed and open against
them, so you do not file another — plan your edits to fit, and say in the task
file if you could not.
**Hardware:** none — prose-only fix

## What

`README.md`'s Status section (line 189, the last line of the file) still says:

> the instrumentation overhead is deliberately uncharacterised — see `spec.md` §4.

But `spec.md` §4 ("The instrument's measured cost") says the opposite: overhead
was measured on real `dut_dev@7` hardware on 2026-08-27, with numbers —
**1.6%** on the DUT clock (misread as 78.1% on the host clock), plus ring/fill-wait
figures from the same measurement pass. outpost/004 (a comment-citation-repoint
task) correctly repointed this citation from the deleted `design.md` §7 to
`spec.md` §4, which means the citation now points at the section that
contradicts the sentence containing it — the dangling-link version of this bug
was at least silently wrong; the fixed link actively points readers at the
disproof.

## Why now

outpost/004 flagged this as a pre-existing staleness in its task file and left
it alone as out of scope for a comment-repoint task, which was the right call
for that unit. But the underlying prose fault is real, user-visible in a
Status section (the part of the README meant to be trustworthy at a glance),
and now more prominent than before this leg landed. It is not a decision
contradiction — no `decisions.md`/`decisions/*.md` entry is at stake — so
outside the reviewer's own narrow mandate, but the supervisor asked for a
filing judgment call and this is a real, cheap-to-fix inconsistency worth its
own task rather than waiting for someone to notice by accident.

## Done when

`README.md`'s Status section no longer says the overhead is "deliberately
uncharacterised"; it either states the measured numbers (1.6% DUT-clock,
misread as 78.1% on host clock, per `spec.md` §4) or points to `spec.md` §4
without asserting the opposite of what that section says.
