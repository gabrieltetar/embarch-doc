# 040 — `Action`'s doc comment describes post-hoc validation as current, three weeks after decision 48 removed it

**State:** claimed by agent/study-designer/040-action-doc-comment-post-hoc-validation, 2026-09-13 14:19
**Source:** the `embarch-reviewer` on `study-designer/038`, 2026-09-13, as an explicit out-of-scope
aside — it flagged the citation while reviewing an unrelated documentation split. Filed by the
supervisor (leg 108), who **verified it against the source and both decisions** and found it worse
than the aside described. See "What the reviewer said and what is actually there".
**Scope:** study-designer
**Hardware:** none — one doc comment, no logic change.
**Owner:** no

## What

`embarch-study-designer/src/study.rs:377-378`, the doc comment on the `Action` enum:

```rust
/// interfaces/types.md. Content validation is handled entirely post-hoc by
/// Core (decision 19) — there is no on-device validation `Action` variant.
pub enum Action {
```

Decision 19 is **`decisions/removed.md:41`**, and its heading says so: *"Two-tier validation:
real-time `Outcome` plus a Core-side post-hoc content check"*, **Retired 2026-08-25 (decision 48)**.
Decision 48 (`removed.md:13`) is unambiguous about what went: *"`Study.validations`,
`StudyResult.validations`, `PostHocValidation`, `PostHocCheck`, ... `signal.rs`'s evaluation logic
and the `core-validation` Cargo feature are all gone."*

So **Core does not handle content validation post-hoc. Core never did** — decision 48's own account
is that *"Core's result writer emitted a hardcoded empty array — not 'empty because this run had none'
but a literal string in the source, because Core never evaluated a validation in its life."*

## What the reviewer said and what is actually there

The reviewer described this as a stale **citation** — decision 19 cited for content validation, which
decision 48 retired. That is true and is the smaller half.

**The larger half is that the sentence states the retired mechanism as a live fact.** This is not a
pointer that fails to resolve; it is a positive claim about how the system works today, and it is
false. A reader asking *"how does `Action` content get validated?"* is told, in the type's own doc
comment, that Core does it post-hoc — and goes looking for a mechanism that has not existed since
2026-08-25 and never functioned before that. The citation makes it worse rather than better: decision
19 **exists**, has real text, and is about exactly this subject, so checking the reference confirms
the false claim instead of exposing it. That is the same shape as `core/050`'s defect — *"real text,
wrong subject"* — arrived at from the other direction.

**The second clause of the sentence is still true and must survive.** *"There is no on-device
validation `Action` variant"* is correct and is the useful half; decision 48 left decision 19's
real-time `Outcome` half untouched, and that is what every study has always actually used.

## Done when

1. The comment no longer says Core validates content post-hoc. **Say what is true instead**, which
   decision 48 states plainly: there is no post-hoc content validation anywhere in this suite, and
   the real-time `Outcome` a step reports is the whole of it.
2. The citation resolves to something that is not retired. Decision 48 is the one that settles this;
   decision 19's **real-time half** is what survives and is what a reader actually needs. Follow this
   repo's citation convention for which of the two to name — and if both, say which is which.
3. **Sweep `embarch-study-designer`'s source for the rest of the class before closing.** This comment
   was not found by a check and would not have been; it was found by a reviewer reading an unrelated
   diff. Grep the crate for every mention of `decision 19`, `decision 28`, `validations`,
   `PostHocValidation`, `ContentValidity`, `ValidationResult`, `core-validation` and `signal.rs` in
   prose, and report **either way** — a clean result is the only thing that tells the next leg this
   class is closed here, and it is exactly the sentence a worker omits when it finds nothing.
4. Gate green. `changelog.d/` fragment only if something reader-visible changed; a doc comment
   usually is not — say which way you judged it.

## Why a check will not catch this and what that means

`check-decision-refs.py` resolves a number to a heading. Decision 19 **has** a heading, in
`removed.md`, so the reference resolves and the gate is green. Nothing mechanical distinguishes *a
decision that exists* from *a decision whose cited half was retired*, and `tasks/doc/033`
(decision-number uniqueness, owner-reserved) would not catch it either — the number is unique and
correct. This is the third distinct member of the same family recorded this fortnight (`core/050`'s
right-number-wrong-repo, `dev-bench/030`'s resolvable-but-deleted, and now cited-but-retired), and
`core/050`'s entry already named the general fix: **one task about citations in a multi-repo suite as
a class**, not a fourth per-repo sweep. This task is filed narrowly on purpose; if it turns up more
than a handful of siblings in item 3, that is the signal for the general one.

## Dispatch note (supervisor, leg 109)

**In reserve for `study-designer`** (last 10% of cap, still writable): `spec.md` 9350/10240 B
(890 B left), `open.md` 4659/5120 B (461 B left). `interfaces/types.md` is out of reserve (73.2%)
since `038`'s split. If your work pushes a file into reserve or leaves one there that nothing has
filed, file `tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit
(`tasks/README.md` has the shape) — recording the debt, not paying it.

**`039` has landed** (code `419e196`, doc `21909b6`), so your branch point already carries the six
repointed path citations. Do not re-do or re-check them; item 3's sweep is about the *retired
mechanism* class, which is a different defect with a different cause.

**Item 3 is the half I care most about.** Report the grep result either way, in the task file, in
words — a clean sweep stated explicitly is what closes this class for `study-designer`, and it is
exactly the sentence a worker omits when it finds nothing. If you find more than a handful of
siblings, say so rather than fixing them all: that is the trigger for one general cross-repo
citation task, which is not yours to file as a `suite`-scoped item — drop it in
/home/gabriel/Github/embarch/embarch-doc/inbox/ (absolute path) and I will file it.

## Not in scope

- `tasks/study-designer/039`, which repoints stale `interfaces/types.md` path citations in this same
  source tree after the `Results` split. Different cause, already filed, and the two should not be
  merged — conflating a split-induced path staleness with a retired-mechanism claim is how a sweep's
  result stops meaning anything.
- Removing or changing any code. Decision 48's removal is complete; this is about prose that outlived
  it.
