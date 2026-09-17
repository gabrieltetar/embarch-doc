# 069 — the citation-sweep census grep cannot see a plural citation, and every task in the chain carries it

**State:** open
**Source:** `inbox/citation-census-grep-cannot-see-a-plural-citation.md`, filed by leg 124's
supervisor, 2026-09-16, after two independent confirmations in one leg. Drained by leg 125.
**Scope:** doc
**Hardware:** none — a wording change in a reserved doc and/or a task-file template, plus optionally
a check in `scripts/`. No board, no probe, no live Core, no study. Re-checked at drain.
**Owner:** required — the instruction's home is `tasks/doc/065`'s territory (`DOC-COMPACTION-PASS.md`,
`DOC-COMPACTION.md`, `tasks/README.md`'s template, `scripts/`), every one of which is reserved.
`tasks/doc/065` already records a case-sensitivity defect in the same instruction, so this belongs
beside it rather than in a new place.

## What

Every citation-sweep task this chain has filed censuses its target files with

```
grep -cE '[Dd]ecision [0-9]'
```

copied forward verbatim from task to task for ten-plus units. **That pattern cannot match a plural
citation** — `decisions 27/29`, `decisions 53/55`, `decisions 3, 10`, `decisions 58-62` — because
"decisions" is not "decision" followed by a space and a digit.

## Two confirmations, same day, different repos, neither looking for it

- **`core/067`** — the filing census said six citations in three files. The re-census found **nine**.
  One of the three extras was `.github/workflows/release.yml:24`, `` `embarch-umbrella` decisions
  27/29 ``, invisible to the grep. The reviewer independently confirmed the row and the miss.
- **`ui/054`** — swept `assets/app.js`, censused at 72 grep lines, and reported **73 citations
  covered**: the extra is `decisions 53/55` at line 853, found the same way and named as "the bonus
  the plural form makes the census regex miss."

Two workers with no knowledge of each other hit the same blind spot in one leg. That is not a
coincidence worth ignoring.

## Why it matters more than an undercount

The tasks have always said "treat the census as a floor," and the reason they give is **multi-number
and range citations expanding per-number**. That is a real effect and it is a *different* one: it
undercounts instances within lines the grep already found. This defect makes whole lines invisible —
a citation the sweep never looks at at all, because nothing told it the line exists.

And the chain **publishes a running tally** — "406 distinct citation instances checked, 15 wrong
numbers, 4 false sentences" as of `study-designer/054` — carried forward from task to task as
cumulative evidence about whether the vein is exhausted. That tally was taken against a pattern that
cannot see a citation form in active use. It is not wrong about what it counted; it is wrong about
what it claims to have covered.

## What a fix probably looks like

`[Dd]ecisions? [0-9]` catches it, and is a one-character change. Whether the *instruction* should
name a pattern at all, or should say "census however you like, then re-census as instances," is the
question `tasks/doc/065` is already open on — a case-sensitivity miss there cost a claim, and this is
the same instruction failing in a second way.

Worth deciding at the same time: **the already-swept files were swept with the blind pattern.** Every
file this chain marked clean may contain a plural citation nobody read. That is a bounded re-check —
one grep for `[Dd]ecisions [0-9]` across the swept corpus would say how many exist before anyone
decides whether to re-open them.

## What leg 124 did not do

It did not change the pattern in any task file, including `tasks/dev-bench/031` and `tasks/ui/060`,
which it filed that leg carrying the same blind grep — `tasks/ui/060` names the defect in prose and
tells its worker to re-census with a pattern that catches the plural, but the census numbers in both
files were taken with the old one. Patching individual task files ahead of the decision would leave
the chain half-converted with no record of which half.

## Done when

The owner has decided what the canonical census instruction should say — here and in
`tasks/doc/065`, which is the same instruction failing a second way — and whichever reserved file
carries it says it. If the decision includes a corpus re-check, its result is written down rather
than left as an intention.
