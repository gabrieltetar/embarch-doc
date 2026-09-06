# 015 — Decision 37 corrects itself by appending, so a reader hits the stale sentence first

**State:** done by agent/umbrella/015-decision-37-appends-instead-of-editing, 2026-09-05 22:45
**Source:** leg 012's own read of `umbrella/012`'s merge result (`embarch-doc` `811380b`), and the worker that shipped it flagged the same thing unprompted
**Scope:** umbrella
**Hardware:** none

**Reserve for `umbrella` at dispatch** (`scripts/check-doc-size.py --pressure`):
`embarch-umbrella/decisions/doctor.md` **11,918 / 12,288 B — 370 B left (97.0%)**, and
`embarch-umbrella/spec.md` **9,286 / 10,240 B — 954 B left (90.7%)**. Your own main file,
`decisions/reporting.md`, is 4,089 / 12,288 B and has no pressure whatever.

**You owe a ride-along compaction of `decisions/doctor.md`, inside this commit.**
Item 2 below edits decision 40, which lives there, and 370 B does not hold it.
`tasks/umbrella/016-compact-umbrella.md` is the parked compaction task; it is `blocked`
on `In flux: yes` and **a blocked compaction task parks the pass, not the reserve**
(`DOC-COMPACTION.md` §2). So: carry `016`'s `Must not delete:` list *for this file*
verbatim, get `decisions/doctor.md` back under its 11,059 B reserve line, and say in
your commit message that you closed `016`'s `decisions/doctor.md` item. **Leave `016`'s
`spec.md` item alone** — the next `umbrella` unit this leg carries that one, and two
workers shortening one file is how a `Must not delete:` list gets half-honoured twice.

Two things that will save you a wrong turn:

- **`scripts/check-duplication.py embarch-umbrella` is already clean** — "no overlap of
  12+ words". `016` tells you to run it first because the last pass's biggest win came
  from there; that well is dry now, so the bytes have to come from real shortening or
  from a **mission split**, which `DOC-COMPACTION.md` §2 names as the cheaper move and
  which `umbrella/012` used on this exact file a few hours ago (it cut
  `decisions/reporting.md` out of it). `doctor.md` now holds decisions 18, 19, 22, 23,
  31 and 40 — ask whether they are still one mission before you squeeze them.
- **`spec.md` already carries the roster you are moving.** Line 93 says `code` appears
  where "a check has more states than statuses (checks 1, 5, 10, 14)". So decision 37's
  body should *cite that sentence*, not re-add a list to the table — this fix costs
  `spec.md` nothing, and it must not be allowed to cost it anything, because `spec.md`
  has 954 B and another unit is compacting it. Item 3's "make sure the table has all
  seven" means **decision 37's own list of check 10's codes** in `decisions/reporting.md`,
  which has room; the roster that leaves is *which checks emit `code`*, not *which codes
  check 10 emits*. Those are different lists and the task's wording blurs them.

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

- [x] Decision 37's body no longer claims check 10 is the only user of `code`. It names no
      roster at all: which checks carry one is `spec.md`'s table's job, cited by link.
- [x] The `Users, 2026-09-05:` append is gone, its citation folded into the body.
- [x] The `Never derived from detail` rule is byte-identical; the "checks 5 and 22" clause is
      preserved as the *test* it was evidence for — more states than statuses earns a code —
      with both checks still named, since a bare rule loses why those two were the examples.
- [x] `no-cli` is recorded as a **deliberate reuse** in decision 40: both states are "there is
      no agent CLI here to consult" and take the same action, so a seventh code would split a
      set nothing branches on. Decision 37 carries the general rule that a moved referent must
      be written down, because nothing mechanical can see it.
- [x] Item 3: decision 37's list now has all seven — `no-handshake` was missing since `4e48c77`.
- [x] Ride-along compaction: `decisions/doctor.md` 11,918 → 7,774 B (63%), out of reserve, by a
      **mission split** — decisions 23 and 40 moved verbatim into `decisions/mcp.md`. `016`'s
      `decisions/doctor.md` item is closed; its `spec.md` item is untouched.
- [x] Gate green, `changelog.d/umbrella-*` fragment dropped.

## Notes

- **No code change.** Items 1-3 are all text; `judge_mcp` already emits exactly the seven codes
  decision 37 now lists, and the reuse decision confirms the arm it already has.
- **`DOC-COMPACTION.md` §7 does not exist.** The human question this task's sibling `016` cites
  moved to [DOC-COMPACTION-PASS.md](../../DOC-COMPACTION-PASS.md)'s "The gate" in the 2026-09-04
  split; that doc has five sections. `016`'s citation is corrected; the same stale reference is
  in this leg's dispatch and may be elsewhere.
