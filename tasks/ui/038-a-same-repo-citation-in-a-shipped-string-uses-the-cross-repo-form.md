# 038 — DOC-CONVENTIONS.md says nothing about a citation in a shipped, rendered string

**State:** open
**Source:** `inbox/ui-032-citation-form.md` — an `embarch-reviewer` finding on `ui/032`, refused by
leg 085 and left standing; filed as a task by leg 096, 2026-09-12, unchanged below this header.
**Scope:** ui
**Hardware:** none
**Owner:** required — the only fix that settles it is one sentence in `DOC-CONVENTIONS.md`, which is
owner-reserved. Nothing in `embarch-ui` needs to change until that sentence exists.

## What

Decide which citation form a **user-visible rendered string** takes, and write it into
`DOC-CONVENTIONS.md`'s *Referring to a decision*. The convention currently covers same-repo doc prose
and cross-repo doc prose and nothing else; `ui/032` and its reviewer each invented an answer for the
third case and invented different ones. The full argument from both sides is preserved verbatim below.

---

**Unit:** ui/032. **Code merge:** `1430650` (embarch-ui). **Doc merge:** `dd4c2b8` (embarch-doc).

**Which decision:** `embarch-doc/DOC-CONVENTIONS.md` "Referring to a decision" —
"Within that sub-project's own docs: `decision 39`. Across: `embarch-study-designer
decision 39`, or a link plus `decision 39` — **but prefer the bare number.**"
The link-plus-number alternative is offered only for the *cross*-project case;
same-repo has one settled form, the bare number.

**Which hunk:** `embarch-ui/assets/index.html`, the run-dialog string (diff hunk
at old line 347): now reads `see embarch-ui/decisions.md, decision 11` — citing
embarch-ui decision 11 from inside embarch-ui's own UI, i.e. same-repo.

**Why this is a contradiction rather than a refinement:** the settled rule gives
same-repo exactly one form, bare `decision N`, and reserves the
repo-name-plus-link form for cross-repo citations. This hunk applies the
cross-repo form to a same-repo citation. (The adjacent trace-tab hunk, old line
514, citing `embarch-outpost decision 10` from embarch-ui, *is* cross-repo, and
`embarch-outpost/decisions.md, decision 10` is the correct settled form there —
no finding on that one.)

**Content check:** both cited decisions say what the strings claim (embarch-ui
decision 11 covers reflash being kept out of the run dialog in favor of
`embarch-api run-study --reflash`; embarch-outpost decision 10 covers capture
being study-scoped and rendered post-hoc with no live feed) — no contradiction
there, only the form issue above.

---

## Supervisor's refusal, leg 085, 2026-09-12 — read before acting on this

**I refused this finding and left it standing rather than deleting it**, the same way
`umbrella/043`'s was handled, because the counter-argument is not obviously right either and two
readers stopping on the same line is itself evidence.

**Why the citation stands as landed.** `DOC-CONVENTIONS.md` scopes the rule to docs in its own
words — *"Within that sub-project's own docs: `decision 39`"*. The hunk in question is **not a doc**.
It is a string rendered inside the running UI, read by a user who is not standing in `embarch-ui/`'s
doc tree and for whom a bare `decision 11` names nothing findable. The rule's stated rationale is
about *file* citations going stale across a mission split, and the worker pointed at
`decisions.md` — the routing index — which is exactly what the convention's next paragraph
prescribes where a link is wanted anyway.

**What is genuinely unsettled, and it is the owner's.** The convention says nothing about
citations in **shipped, rendered strings**, which are neither same-repo doc prose nor cross-repo
doc prose. `ui/032` had to invent an answer and so did its reviewer, and they invented different
ones. `DOC-CONVENTIONS.md` is owner-reserved, so neither a worker nor a leg can settle it; this
drop is the record that it needs settling. The cheapest fix is one sentence in *Referring to a
decision* saying which form a user-visible string takes.

**Not undone.** No revert, no hand-fix.

---

**To undo (the reviewer's original proposal, not taken):** revert `1430650` in embarch-ui, or hand-fix just the first hunk to
`decision 11` (drop `embarch-ui/decisions.md, `). Revert is clean — the commit
touches only these two lines, and the second hunk (outpost citation) would need
to be re-applied if a straight revert is used, since it is correct as landed.

Hardware: none.
