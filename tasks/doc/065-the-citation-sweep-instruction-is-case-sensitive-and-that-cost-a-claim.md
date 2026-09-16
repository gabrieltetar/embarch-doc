# 065 — the canonical "grep for inbound citations" instruction is case-sensitive, and that is how the fourth claim-loss landed

**State:** open
**Source:** `inbox/doc-citation-sweeps-are-case-sensitive.md`, filed by leg 119 while folding
`ui/055`, drained by leg 120.
**Scope:** doc
**Hardware:** none — a wording change in a reserved doc, plus optionally a check in `scripts/`. No
board, no probe, no live Core.
**Owner:** required — every path that would change is reserved: `DOC-COMPACTION-PASS.md`,
`DOC-COMPACTION.md`, `tasks/README.md`'s template, `scripts/`.

## What

Every compaction task this fleet files carries some form of this instruction, usually verbatim:

> **Grep the whole doc repo for inbound `decision NN` citations first**, and remember a bare
> `decision NN` in another sub-project's file means *that* sub-project's NN.

`ui/055`'s worker followed it exactly: grepped the doc repo for `decision 25`, found three citing
files, checked all three, and cut a vertex count it had established was cited nowhere else. It was
wrong, because **prose capitalises a citation when it starts a sentence**:

```
$ grep -n  'decision 25' history/ui.md     ->  line 40 only
$ grep -ni 'decision 25' history/ui.md     ->  lines 14, 39, 40
```

Line 40 is *"Fixed: decision 25's `--brand` count ..."* — lowercase mid-sentence. Line 39 is
*"Decision 25's E vertex count was 16 ... corrected to 22 ..."* — capitalised because it starts its
own sentence. **Line 39 is the one citing the number that was cut**, one line above a line the sweep
did find. The worker got a hit in the right file and had no signal a second, differently-cased
citation sat beside it.

## Why now

Fourth claim-loss in three legs (`core/064`, `umbrella/068`, `ui/055`, plus the `core/065`
restoration that closed the first). The response each time has been to sharpen the *instruction to
the worker* — leg 118's "open that decision and confirm it covers the whole hunk sentence by
sentence, not the topic" demonstrably changed an outcome on `core/065`.

**But it cannot catch this one.** The worker's reasoning was sound at every step; its evidence was
incomplete because of a grep flag. No care at the reading stage fixes a sweep that never surfaced the
line. That makes this the cheapest fix available to the class, and the only one so far that is
mechanical rather than exhortative.

## Where it should go

Pick one or both — this is the judgement the task exists for:

- **Wording**, the cheap half: wherever the citation-sweep instruction canonically lives, say
  `grep -rni` and say why (sentence-initial capitalisation). If the canonical home is the task
  template rather than `DOC-COMPACTION-PASS.md`, note that each task file restates the instruction
  independently, so the template is the only place that reaches future ones.
- **A check**, the durable half: a `scripts/` check that a compaction diff does not delete a token
  some other file's `decision NN` citation depends on. Much larger, may not be worth it — worth
  pricing before assuming. `check-decision-refs.py` already resolves decision *links*; what dangled
  here is a citation of a *fact inside* a decision, which is different and harder.

## Watch for

- **Do not just add `-i` and consider the class closed.** Case is the cause of *this* instance. The
  general defect is "the sweep's evidence was incomplete", and other spellings exist — `#25`,
  `decisions/shell.md#25`, and a bare `25` inside a sentence about decision numbering.
- **The live dangling citation from this instance is a different task** — `tasks/ui/056`, Part A.
  Fixing the instruction does not fix `history/ui.md`, and vice versa.

## Done when

- [ ] The citation-sweep instruction, wherever it canonically lives, is case-insensitive and says why.
- [ ] A decision is recorded on whether a mechanical check is worth building, either way.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
