# 026 — A compaction squeeze describes its cuts by category, and twice in one leg the categories did not cover what it cut

**State:** open
**Source:** leg 056, 2026-09-08, observed twice in three units — `topology/017` and
`study-designer/019`. Both found by the unit's own reviewer, neither by the gate.
**Scope:** doc
**Hardware:** none
**Owner:** required — the rule lives in `DOC-COMPACTION.md` / `DOC-COMPACTION-PASS.md`,
and possibly in `.claude/`'s worker template. All reserved.

## What

`DOC-COMPACTION.md` §2 prefers a **split** over a **squeeze** precisely because a split
restates nothing and so costs no argument. When no seam exists a squeeze is legitimate, and
the thing that makes it auditable afterwards is the pass's own statement of *what it cut*.
In practice that statement is written as a list of **categories** — "meta-commentary,
restated framing, one redundant cross-reference" — and nothing checks that the categories
cover the diff.

Twice in one leg they did not:

- **`topology/017`** named four categories of cold content deleted from `spec.md` (a serial
  number, an exact measurement citation, a date tag, a rationale decision 26 now owns). All
  four held. **Two further sentences and one caveat also went, named nowhere.** The reviewer
  read them and judged them asides and epistemic nuance — no invariant, constraint or failure
  signature lost.
- **`study-designer/019`** described its cuts to `decisions/registry.md` as meta-commentary,
  restated framing and one redundant cross-reference. **Two more went**: decision 35's
  "presenting that inference as fact is worse than not answering at all" — a *ranking* claim,
  not a restatement of the durable principle that survives above it — and, in decision 66,
  both the concrete rendered error string `"study has 513 steps, but the limit is 512"` and
  the sentence "They are the same kind of thing to the type system and not to the reader, and
  the reader is who an error message is for", which is a design maxim. Again no constraint
  broke; the bounds and the tests that assert them are all still stated.

Neither is a contradiction and neither was worth reverting. **The defect is that the check
worked by luck.** Both were caught because this leg's reviewers were told to enumerate the
cuts and count them against the description; a reviewer given the ordinary charter reads for
contradiction and would have passed both.

## Why now

Burndown is explicitly optimising for volume, and the squeeze is the faster of the two
compaction shapes — leg 055 said so in as many words on the day the mode was armed. Two
occurrences in one leg is the second data point, which is the threshold this log has used
before for "say it loudly rather than note it again".

The cost of closing it is small and there are at least three shapes to choose between, which
is why this is filed rather than fixed:

1. **A rule in `DOC-COMPACTION-PASS.md`**: a squeeze's commit message enumerates every
   deletion, not a category list — the categories become a summary *of* the enumeration
   rather than a substitute for it.
2. **A reviewer-charter line**: every compaction review counts the diff's deletions against
   the pass's own description and reports the residue. That is what these two reviewers did,
   but only because the supervisor asked them to, per unit, in prose.
3. **Nothing, deliberately**, on the argument that texture is allowed to go and only
   invariants matter — in which case say so in `DOC-COMPACTION.md`, because right now the
   pass doc reads as if the description is the audit trail.

## Done when

- [ ] `DOC-COMPACTION.md` or `DOC-COMPACTION-PASS.md` says which of the three above is the
      rule, in one sentence, with the reason.
- [ ] If it is (2), the reviewer template in `embarch-fleet/scripts/install.py` carries it,
      so it does not depend on a supervisor remembering to ask.
- [ ] This task names all three occurrences with their units, so a fourth one is recognisable
      as a fourth rather than as a first.

## Third occurrence, and it is the one that settles option (3): `ui/011`, 2026-09-09, leg 057

**The previous two lost texture. This one lost an invariant, and option (3) above — "texture is
allowed to go and only invariants matter" — cannot absorb it.**

`ui/011` squeezed `embarch-ui/decisions/study-designer.md` 12,064 → 10,961 B. Its commit message
described the reflash-selector hunk as cutting a parenthetical and "replaced with the shorter …
which is what shipped" — the same wording it used for cuts that genuinely were cosmetic. What the
hunk actually did was turn

> Core's study route accepts only **a mismatch override and** a *report* of what the caller already
> flashed

into

> Core's study route accepts only a *report* of what was already flashed

**which is a false statement about the API contract.** `allow_version_mismatch` is a real, live
parameter — `embarch-api/interfaces/studies.md` documents it, and `embarch-ui/open.md`'s own
carry-forward of this same decision 11 says "The mismatch override and the before-the-run mismatch
display are built and unaffected." A second cut in the same commit removed ", next to the override"
from the neighbouring paragraph, so after both cuts decision 11 did not mention the override
anywhere, and **the same decision read two different ways depending on which file you landed on.**

Everything else in that squeeze checked clean, decision 20 was genuinely untouched, and the reviewer
that found this did so **only because the supervisor asked, per unit, in prose** — the third time in
three legs that the catch has depended on a supervisor remembering. Fixed narrowly in the fold
(both clauses restored; the rest of the squeeze stands), which left the file at 11,007 B against an
11,059 B reserve line — **53 bytes of clearance**, so the next amendment re-files it. That is the
second time this exact file has landed with under 60 B of clearance; the first is described in
`tasks/ui/011`'s own history.

**What this occurrence adds to the argument.** Two data points made this a pattern; the third makes
it a pattern with a cost. It also rules out one of the three shapes: an enumeration rule (1) or a
reviewer-charter line (2) would both have caught this, and (3) would have licensed it — because the
worker's own honest reading was that the parenthetical was texture. **A squeeze cannot be trusted to
classify its own cuts**, which is the real finding, and it is why (2) is stronger than (1): (1)
still asks the actor doing the cutting to be the one who notices.
