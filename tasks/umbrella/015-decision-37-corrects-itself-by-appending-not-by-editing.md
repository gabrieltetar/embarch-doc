# 015 — Decision 37 corrects itself by appending, so a reader hits the stale sentence first

**State:** open
**Source:** leg 012's own read of `umbrella/012`'s merge result (`embarch-doc` `811380b`), and the worker that shipped it flagged the same thing unprompted
**Scope:** umbrella
**Hardware:** none

## What

`embarch-umbrella/decisions/reporting.md` decision 37's **body** still reads "Check 10 is
the only user today", and a **`Users, 2026-09-05:` line four paragraphs below** says the
real answer is checks 1, 5, 10 and 14. That satisfies `tasks/umbrella/014`'s item 1 as
that task worded it, and `check-docs.py` is green on it — but it is an **append that
contradicts the body**, which is exactly the shape `DOC-PROTOCOL.md` §4 says not to write:
edit the body, never append. A reader reaches the false sentence first and has no reason
to keep reading to the correction.

The appended line makes the better argument itself: cite `spec.md`'s table rather than
re-listing users here, because the list went stale within a day of check 5 landing. So the
fix is not "update the count" — that just resets the same clock. It is:

- Rewrite decision 37's body so the sentence that goes stale is **gone**, not corrected
  below. The claim worth keeping is *why* `code` exists and that it is never derived from
  `detail`; the roster of users is `spec.md`'s table's job.
- Delete the `Users, 2026-09-05:` line once its content has moved into the body's citation,
  so the entry does not carry both halves of the same correction.

**Do not delete** the "checks 5 and 22 are the obvious next ones, since both exist to split
states that share a status" reasoning, or the `Never derived from detail` rule and its
justification. Those are the decision; the roster is not.

## Why now

Small, and `embarch-api` decision 51 already named this exact failure: the surface text is
what a reader acts on, so a decision whose body is stale by three checks is worse than one
that never enumerated. It is also the second time in two days that a `decisions/` entry has
been corrected by appending rather than by editing, which is the pattern worth stopping
before it becomes the house style.

`decisions/reporting.md` is 4,089 / 12,288 B, so there is no size pressure and no reason
to append rather than rewrite.

## Done when

- [ ] Decision 37's body no longer claims check 10 is the only user of `code`.
- [ ] The `Users, 2026-09-05:` append is gone, its citation folded into the body.
- [ ] The `Never derived from detail` rule and the "checks 5 and 22 are next" reasoning are
      byte-identical or clearly preserved.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
