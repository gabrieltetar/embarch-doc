# 049 — `study_designer.rs` holds 73 citations and is the half of `embarch-ui` no sweep has reached

**State:** claimed by agent/ui/049-study-designer-rs-citations, 2026-09-13 18:27
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

- [ ] Every citation in the range you took is confirmed against the cited body or fixed, with
      **wrong numbers and false sentences counted separately**, and no number prefixed with a repo
      name without the body being re-derived.
- [ ] Any citation inside a user-visible string is left alone and named in the fold.
- [ ] A follow-up task filed for the remainder, or a fold line saying the file is fully swept.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/ui-*` fragment.
