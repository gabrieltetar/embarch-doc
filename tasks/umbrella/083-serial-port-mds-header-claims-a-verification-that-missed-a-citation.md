# 083 — `serial-port.md`'s header claims a verification that had already missed a citation

**State:** open
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

- [ ] `serial-port.md`'s header states what was actually checked and what shape of citation that
      check can and cannot see — not "no inbound link exists".
- [ ] It names `tasks/api/114` as the citation the original grep missed, and `tasks/doc/044` as the
      general defect, so the next person splitting a file in this sub-project greps for the inline
      form too.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment only if the correction is reader-facing beyond the fix itself.

## Not yours

- **Do not undo the split.** `umbrella/081` is correct: decision 55 moved verbatim, the arithmetic
  reconciles, and the rejection of moving decision 26 instead was independently re-verified.
- **Do not edit `tasks/api/114` or `tasks/doc/044`.** Both are already correct; `114` was repointed
  at this unit's fold and `doc/044` is owner-reserved.
