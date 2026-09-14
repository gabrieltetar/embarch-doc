# 049 — `study_designer.rs` holds 73 citations and is the half of `embarch-ui` no sweep has reached

**State:** done by agent/ui/049-study-designer-rs-citations, 2026-09-13
**Source:** `tasks/ui/040` swept `embarch-ui`'s foreign decision citations and `tasks/ui/048`
repointed `trace.rs`'s bare decision 35. Neither reached `src/study_designer.rs`, which the leg of
2026-09-13 17:5x counted at **73** citations — more than half of `embarch-ui`'s 132 and the largest
single remaining block in the repo.
**Scope:** ui
**Hardware:** none — source comments only; no board, no study, no live Core.
**Owner:** no

## What

```
73  src/study_designer.rs
23  src/main.rs
22  src/trace.rs   (partly swept by ui/048)
 6  src/snapshot.rs
```

**`check-decision-refs.py` resolves decision numbers only inside `*.md`**, so a wrong number in a
source comment fails no gate and never has.

## Why `study_designer.rs` specifically

The file's whole job is rendering a shared crate's model, so **most of its citations are foreign by
construction** — they mean `embarch-study-designer` decisions, not `embarch-ui`'s. That is exactly
the collision `ui/040` was created to fix elsewhere in this repo, and `ui/040`'s reviewer caught two
citations that were *prefixed without being re-derived*. **Do not repeat that**: adding
`embarch-study-designer ` in front of a number is not the fix unless you have read the body it now
points at and confirmed the sentence.

`ui/032` also left a genuinely open question about citation form in a string that **ships in the
running UI** — the supervisor refused the reviewer's finding there after re-deriving it, and
`tasks/doc/055` (owner-only) is where the form gets settled. **If a citation you are fixing lives in
a user-visible string rather than a comment, leave it alone and say so in your fold** — that is the
unsettled case, and this task is not the place to settle it.

## Why this class keeps being worth running

Across four consecutive days the count of wrong *numbers* has been the less interesting half. The
real yield has been **prose a decision made false** — `umbrella/063` fixed four things and only two
were numbers. So **read the cited decision's body, then read the sentence around the citation**, in
that order. Count wrong numbers and false sentences separately, and report how many held.

## Bounding

73 citations may not fit one unit. Take `study_designer.rs` top to bottom, get as far as you
honestly can, and file `tasks/ui/<next>` for the remainder naming the line or function you stopped
after. A careful partial sweep that says where it stopped is the deliverable; a rushed complete one
is not.

If a sweep shows a *decision body* in another repo is wrong rather than the citation, that is an
`inbox/` drop written by **absolute path** to `/home/gabriel/Github/embarch/embarch-doc/inbox/` —
not an edit. You own `embarch-ui` only.

## Reserve, for planning

**No `embarch-ui` doc is in the reserve band** — you have room. If your work leaves one in the last
10% of its cap unfiled, file `tasks/ui/<next>-compact-ui.md` in the same commit — **your own
scope**, never `tasks/doc/`.

## Done when

- [x] Every citation in the range you took is confirmed against the cited body or fixed, with
      **wrong numbers and false sentences counted separately**, and no number prefixed with a repo
      name without the body being re-derived.
- [x] Any citation inside a user-visible string is left alone and named in the fold.
- [x] A follow-up task filed for the remainder, or a fold line saying the file is fully swept.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/ui-*` fragment.

## Fold

**`src/study_designer.rs` is fully swept, top to bottom, all 2973 lines.** 74 decision citations
found (73 by the simple `decisions? N` grep, plus one instance wrapped across a line break —
`` `embarch-study-designer` decision\n9's `` — that the grep missed but was read and checked anyway).

Every one was checked against the decision body it names, following "read the cited decision's body,
then read the surrounding sentence":

- **Wrong numbers: 0.**
- **False sentences: 0.** Every prose claim tied to a citation — including the two-line "the exact
  failure `embarch-study-designer` decisions 34/36/53/54 were each opened by" (verified against
  `removed.md` decision 54's own "'nothing captured, no error' family... opened by from four
  directions", which names no specific four — this file's comment is the only place that does, and
  it checks out on a read of all four bodies) — held up.
- **Wrong form (the ui/040 residue this task named): 2.** Two bare `decision 40` citations (both in
  `#[cfg(test)] mod tests`, lines ~2194 and ~2474) named `embarch-study-designer` decision 40 with no
  repo prefix — the exact class `ui/040` didn't reach because it never looked inside this file. Both
  re-derived against `embarch-study-designer/decisions/declares.md` decision 40 (confirmed: the body's
  own closing line is "a blank field is refused rather than quietly promoted, which is the distinction
  this decision rests on" — the sentence the code was paraphrasing) and given the
  `` `embarch-study-designer` `` prefix. No renumbering; the number was always right.
- **No citation lives inside a user-visible string.** All 74 sit in `///`/`//` doc comments or test
  assertion strings that never reach the browser; none is the `ui/038`/`ui/032` open-question class.
- **Adjacent finding, fixed in the same commit (own scope, not a new decision):** while re-deriving
  decision 40's body, found `embarch-ui/decisions/study-designer.md`'s own decision 11 entry linking
  `embarch-study-designer` decision 40 at `decisions/versioning.md` — decision 40 is actually defined
  in `decisions/declares.md` (confirmed via `embarch-study-designer/decisions.md`'s index). Neither
  `check-decision-refs.py`'s topic-link check nor its main resolver catches this shape (the link text
  is `[embarch-study-designer]`, not `[decision 40]`, so the topic-link regex never sees a number to
  check; the main resolver only asks "does `embarch-study-designer` define 40 *anywhere*", which it
  does). Repointed the link to `declares.md`.

No remainder: the file has no more lines to sweep, so no follow-up task is filed.
