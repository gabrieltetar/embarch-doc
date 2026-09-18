# 083 — `serial-port.md`'s header claims a verification that had already missed a citation

**State:** done — 2026-09-17, `agent/umbrella/083-serial-port-header-verification`. Rewrote
`serial-port.md`'s header sentence to say what was checked (a grep for the `[decision N](path)`
link shape) and what shape it cannot see (inline code with a parenthetical), naming `tasks/api/114`
as the citation the original grep missed — cited as its `**Source:**` line, since retired in this
repo's `ca564376` fold, not as a live path — and `tasks/doc/044` as the general defect. Re-ran both
grep shapes myself over the whole `embarch-doc` tree before writing the header: the link shape
turned up one unrelated hit (`history/api.md`'s `embarch-api` decision 55, a different sub-project's
number); the inline-code-with-parenthetical shape turned up only historical task-file text (this
task's own body, and `tasks/umbrella/080`), no live stale pointer — `embarch-api/open.md` already
cites `embarch-umbrella` decision 55 by number alone, no path, per `tasks/api/114`'s own advice. No
`changelog.d/` fragment: the correction is entirely contained in the header it fixes, nothing else
reader-facing changed. Gate green: `cargo build`/`test`/`clippy --all-targets -- -D warnings` in
`embarch-umbrella` (228 tests pass, 0 clippy warnings), `check-docs.py` 11/11 in `embarch-doc`,
`check-ownership.py --scope umbrella` green on both worktrees. `decisions/serial-port.md` is
3,330/12,288 B (27%) after the edit — no compaction task needed; `projects.md`/`install.md`/
`bind.md` untouched, all still exactly where the supervisor note found them.

**Supervisor note, leg 141 — `tasks/api/114` no longer exists, and that changes one `Done when`
box.** This leg ran `api/114` as its first unit and retired the task file in that unit's fold
(`embarch-doc@ca564376`); the repointed `**Source:**` line this task is about went with it. **The
citation the original grep missed is therefore a historical fact, not a live file**, and the header
you write must say so — cite it as *"`tasks/api/114`'s `Source:` line, since retired"* with the fold
SHA, or describe the citation's **shape** without naming a file that is gone. A header that sends a
future reader to a path that 404s is the same class of defect this task exists to fix, one level up.
**Read the file at its last living version** — `git show ca564376^:tasks/api/114-close-the-serial-port-referral-in-open-md-against-umbrella-decision-55.md`
— rather than reconstructing what it said.

**Doc-size for `umbrella`, read at dispatch (leg 141), and it is tighter than it was an hour ago:**
`embarch-umbrella/decisions/serial-port.md` — the file you edit — has room, but
`embarch-umbrella/decisions/projects.md` crossed into reserve during this same leg's `umbrella/082`
and now sits at **11,163/12,288 B (90.8%)**, filed as `tasks/umbrella/084-compact-docs.md` and
`blocked`: **do not write into it.** `decisions/install.md` (98.2%) and `decisions/bind.md` (93.9%)
are also in reserve and filed against blocked tasks: **do not write into either.**
`embarch-umbrella/open.md` is 3,954/5,120 B (77.2%) and clear. Run
`python3 scripts/check-doc-size.py --pressure` before and after; if your edit pushes any file over
90%, file `tasks/umbrella/<NNN>-compact-docs.md` in the same commit, using
`python3 scripts/check-task-numbers.py --next umbrella` for the number — never read the directory.

**Source:** `embarch-reviewer` on landed unit `umbrella/081` (`embarch-doc@63f7d4ea`), leg 140,
2026-09-17, via `inbox/doc-umbrella081-stale-decision-55-source-anchor.md` — **drained and closed by
the supervisor at that unit's fold**, which fixed the citation itself. This task is the half the
supervisor deliberately did not do, because it is a sub-project's decision-file prose.
**Scope:** umbrella
**Hardware:** none — one sentence in one file, plus one grep to say what is true instead.
**Owner:** no

## What

`embarch-umbrella/decisions/serial-port.md`'s header says, of the verbatim split that created it:

> No inbound link elsewhere in the suite names `projects.md` for decision 55.

That was **false when it was written.** `tasks/api/114`'s `**Source:**` line named
`embarch-umbrella/decisions/projects.md` for decision 55 and had done since before `umbrella/081`
ran. The supervisor repointed that line at this file in `umbrella/081`'s own fold, so the sentence
is now *accidentally* true — which is worse than plainly false, because it still asserts that a
verification found nothing when in fact it missed something.

**Why the grep missed it, and why that is the interesting part.** The citation is inline code with a
parenthetical — ``` `embarch-umbrella decision 55` (`embarch-umbrella/decisions/projects.md`) ``` —
not a `[decision N](path/to/decisions/topic.md)` markdown link. `scripts/check-decision-refs.py`'s
topic-file arm inspects only the link shape, and its plain per-reference arm resolves decision 55
against the *sub-project*, which still passes. So the gate was green over a stale file pointer for
the entire window. `tasks/doc/044` is the general form of this — *"a verbatim split is the one move
`check-decision-refs.py` structurally cannot see"* — and it is still open.

## Why now

Cheap, and it is a claim about evidence rather than a claim about the system, which is the kind this
suite treats as load-bearing. A later split in this sub-project will read this header as a worked
example of how to verify a seam, and it is currently an example of a verification that did not hold.

## Done when

- [x] `serial-port.md`'s header states what was actually checked and what shape of citation that
      check can and cannot see — not "no inbound link exists".
- [x] It names `tasks/api/114` as the citation the original grep missed, and `tasks/doc/044` as the
      general defect, so the next person splitting a file in this sub-project greps for the inline
      form too.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment only if the correction is reader-facing beyond the fix itself. (Not
      filed — the correction is self-contained in the header it fixes.)

## Not yours

- **Do not undo the split.** `umbrella/081` is correct: decision 55 moved verbatim, the arithmetic
  reconciles, and the rejection of moving decision 26 instead was independently re-verified.
- **Do not edit `tasks/api/114` or `tasks/doc/044`.** Both are already correct; `114` was repointed
  at this unit's fold and `doc/044` is owner-reserved.
