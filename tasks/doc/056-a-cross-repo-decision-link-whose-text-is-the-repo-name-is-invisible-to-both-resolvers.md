# 056 — A cross-repo decision link whose text is the repo name is invisible to both of `check-decision-refs.py`'s resolvers

**State:** open
**Source:** `ui/049`'s worker, 2026-09-13, which found a live instance while re-deriving a decision
body for its own sweep. Filed by the leg of 2026-09-13 20:0x. **Not a duplicate of
`tasks/doc/044`** — that one is about a *verbatim mission split* moving a decision out from under a
link; this is about a link shape the checker never examines at all, split or no split.
**Scope:** doc
**Hardware:** none — a script change.
**Owner:** required — `scripts/` is owner-reserved (`../../embarch-fleet/protocol.md` §3), so no
agent can make this change.

## What

`embarch-ui/decisions/study-designer.md`'s decision 11 carried:

```markdown
The human surface for [embarch-study-designer](../../embarch-study-designer/decisions/versioning.md) decision 40.
```

`embarch-study-designer` decision 40 is defined in `decisions/declares.md`, not `versioning.md`.
**The link pointed at the wrong file and nothing failed**, for two independent reasons:

- **The topic-link check never sees a number.** Its regex looks for link *text* naming a decision
  (`[decision 40]`), and here the link text is `[embarch-study-designer]` — the repo name. There is
  no number in the text, so the check has nothing to resolve against the target file.
- **The main resolver asks the wrong question.** It asks whether `embarch-study-designer` defines a
  decision 40 *anywhere*. It does. So the citation resolves, and the fact that the URL points at a
  file which does not contain it is never tested.

Fixed by hand in `ui/049` (doc merge `16e1ae0c6552f38717d8f9472a378f4ccd836b11`). **The shape is
not fixed**, and `DOC-CONVENTIONS.md` actively encourages it — naming the repo in the link text is
how a cross-repo citation is supposed to read.

## Why it matters more than one bad link

This is the third distinct hole in decision-reference checking recorded this week, and the three
compose badly: `tasks/doc/044` (a verbatim split moves a decision and a link survives pointing at
the wrong file), the standing gap that **`check-decision-refs.py` resolves numbers only inside
`*.md`** so a wrong number in a source comment fails nothing, and now this. A repo is currently
being swept file by file for citation defects by hand, one unit at a time, precisely because the
mechanical checks cannot see most of the class.

And this particular shape is the one a **mission split silently breaks in bulk**: `embarch-api`
split its decisions twice on 2026-09-13, and every inbound link of this shape into a moved decision
is now wrong and green.

## What to do

One of:

1. **When a cross-repo link's target is a decisions file and the sentence carries `decision N`
   nearby, resolve N against that target file specifically** rather than against the repo as a
   whole. That closes both halves — the link text need not carry the number, because the sentence
   does.
2. Or, cheaper: **require the index**. `DOC-CONVENTIONS.md`'s link-the-index rule already says a
   cross-repo decision citation should point at `<repo>/decisions.md`, which survives a move because
   the splitter maintains it. A check that refuses a cross-repo link pointing at a *topic* file
   would enforce the rule that already exists, and needs no resolution at all.

Option 2 is probably right and is certainly smaller; option 1 catches same-repo instances too.
Whoever does this should say which and why, because they are not equivalent.

## Done when

- [ ] A link of this shape pointing at a decisions file that does not define the cited decision
      fails the gate.
- [ ] The whole suite is swept once for existing instances — this is the first one found, by
      accident, and nothing suggests it is the only one.
- [ ] `check-decision-refs.py`'s own header records the gap it now closes and the ones it still
      leaves.
