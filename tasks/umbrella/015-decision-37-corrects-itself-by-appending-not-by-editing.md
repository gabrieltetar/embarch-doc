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

## A second item, found by leg 012 reading `umbrella/011`'s merge result

**Check 10's `no-cli` code survived `umbrella/011` with a changed meaning and nothing says
so.** It used to mean *the `claude` binary is not on `PATH`*. After decision 40 the check
never looks for that binary at all, and `src/doctor.rs`'s `judge_mcp` now emits `no-cli` for
`McpRegistration::NoCli { why }` with the detail *"no agent-CLI config to read"* — a
different condition wearing the same name. Decision 37's whole argument for the `code` field
is that a consumer can match on it because it is stable while `detail` is free to be
rephrased; a code whose *referent* changes underneath a stable name is the one way that
promise can be broken silently, and it is invisible to every check in the gate.

Nothing is wrong today — check 10 is `code`'s only consumer that anyone reads — so this is a
text fix, not a revert:

- Decision 40 should say the code was **reused deliberately** and why (both states are "there
  is no agent CLI to consult", and both take the same action), **or** the arm should take a
  new code and decision 37's list should grow one.
- Whichever way it goes, decision 37's list of check 10's codes is the place a reader checks,
  so it has to agree — which is why this rides here rather than in its own task.

## A third item, found by `umbrella/011`'s reviewer

**`judge_mcp` emits a seventh code, `no-handshake`, that decision 37's list omits.** It is
**pre-existing** — it went in with `4e48c77`, the commit that first built check 10 — and
`umbrella/011` did not touch it. So decision 37 has been describing check 10's code set
incompletely since the day the check shipped, which is the same defect as the two items
above and lands in the same edit. When the roster moves to `spec.md`'s table, make sure the
table has all seven.

## Done when

- [ ] Decision 37's body no longer claims check 10 is the only user of `code`.
- [ ] The `Users, 2026-09-05:` append is gone, its citation folded into the body.
- [ ] The `Never derived from detail` rule and the "checks 5 and 22 are next" reasoning are
      byte-identical or clearly preserved.
- [ ] `no-cli`'s changed referent is either recorded as a deliberate reuse in decision 40, or
      split into a new code that decision 37's list carries.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
