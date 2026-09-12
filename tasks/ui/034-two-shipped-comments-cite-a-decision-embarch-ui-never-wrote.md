# 034 — Two `embarch-ui` comments cite a "Core unreachable is expected" decision that does not exist

**State:** claimed — leg 096, 2026-09-12, `agent/ui/034-core-unreachable-decision`

## Dispatch note (supervisor, leg 096)

**Pick between the two answers on the evidence, and picking is the task — do not do both and do not
punt.** Read what `src/logs.rs` and `src/snapshot.rs` actually do before you decide: if a down Core
is handled deliberately as a rendered state in either place, answer 1 (write the decision) is the
one the code is already asking for. If it turns out to be incidental error handling that happens to
render, answer 2 is right and cheaper. Say in the decision or in the commit message which evidence
decided it.

**If you write a decision**, it is a new numbered `embarch-ui` decision: allocate the next free
number, put it in the right `decisions/*.md` topic file, and repoint both comments at it by bare
number (same-repo form). `ui/033`'s precedent stands: read decision **bodies**, not headings.

**No `embarch-ui` doc is in the size reserve**, so you have room. If your work puts one there, file
`tasks/ui/<NNN>-compact-ui.md` in the same commit (`scripts/check-task-numbers.py --next ui`).

**Set `State:` to `done` yourself before you finish.** Two `ui` workers in a row left it at
`claimed` and the supervisor had to correct it at fold time.
**Source:** `ui/033`, 2026-09-12, and its reviewer independently. That unit repointed every
`design.md` source-comment citation in `embarch-ui`; these two could not be repointed, because the
thing they cite was never written.
**Scope:** ui
**Hardware:** none — two comments and the decisions they should or should not cite.
**Owner:** no

## What

Two comments attribute a piece of reasoning to `embarch-ui` decision 5:

- `src/logs.rs:58` — `// here too (design.md §3 decision 5's own "confirmed" reasoning)`
- `src/snapshot.rs:73-75` — `/// renderable state (§ design.md decision 5's own "confirmed"
  reasoning: Core down is not a crash)`

The reasoning they cite is *"Core being unreachable is an expected, renderable state, not a crash."*
**`embarch-ui` decision 5 does not say that.** It lives in `decisions/wiring.md` and is about
routing every hardware-adjacent call over HTTP+Bearer to Core. Two readers — `ui/033`'s worker and
its reviewer — checked every other `embarch-ui` decisions file independently (`topology-tab.md`,
`trace-view.md`, `shape.md`, `shell.md`, and everything mentioning "unreachable") and neither found
any standing decision carrying it. `ui/033` deliberately left both comments alone rather than
repoint them at a plausible number.

## Why this is worth a task rather than a comment fix

The UI **behaves** as though the decision exists: a down Core renders as a state rather than an
error, in at least these two places. So this is not a stale citation — it is a real design position
that ships, is relied on in code, and has never been written down. That is the gap a citation to a
non-existent decision is evidence of.

## Two possible answers, and picking between them is the task

1. **Write the decision.** `embarch-ui` states that an unreachable Core is an expected, renderable
   state — what renders, what does not, and how it differs from a crash — and both comments cite it
   by its new number. Best if the behaviour is intentional and depended on, which the code suggests.
2. **Strike the claim.** Both comments stop asserting a decision backs them and just say what the
   code does. Best if the behaviour turns out to be incidental.

**Do not split the difference by citing decision 5 anyway.** That is the failure `ui/033` avoided
on purpose.

## Done when

- One of the two answers is taken, with the reasoning recorded.
- Neither comment cites a decision that does not say what it claims.
- `cargo test` and `clippy --all-targets -- -D warnings` stay clean.
