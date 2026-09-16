# 023 — `embarch-outpost` decision 17 is over the per-decision cap and untracked

**State:** done — decision 17 compacted from 4,559 B to 4,070 B (26 B margin under the 4,096 B cap).
No split, no renumbering, no pin added to `scripts/decision-size-baseline.json`.
**Reserve (leg 118):** no `embarch-outpost` file is in the last 10% of its cap. If your work pushes
one into reserve, file `tasks/outpost/<NNN>-compact-outpost.md` in the same commit.
**Source:** leg 117, 2026-09-16. `core/063` closed this gap for `embarch-core` decision 30 and named
the real finding as *"nothing is watching it."* I ran the census that implied: **five** decisions
suite-wide are over [`DOC-BUDGET.md`](../../DOC-BUDGET.md)'s **4,096 B per-decision cap** with no pin
in `scripts/decision-size-baseline.json`. `core/063` fixed one; `core/064`, `topology/047` and
`umbrella/068` file three more. **This is the fifth and the smallest breach.**
**Scope:** outpost
**Hardware:** none — doc prose only. No board, no probe, no live Core, no capture read.
**Owner:** no
**Compacts:** `embarch-outpost/decisions/clocks.md`
**In flux:** no. Decision 17 is the two-clocks split — `cycles` measures, `rx_utc_ms` places — and
it has been settled since it was written. What is still open in
[`embarch-ui/open.md`](../../embarch-ui/open.md) and
[`embarch-topology/open.md`](../../embarch-topology/open.md) is that **nothing has compared a
trace's placement against a second stream**, and that no signal tap has read a byte. Those are
**hardware debts against decision 17's claims**, not doc flux: no board is coming to change this
entry's text, and if one ever does it will *add* a measurement rather than rewrite the split.

## What

`embarch-outpost/decisions/clocks.md#17` is **4,559 B** against the 4,096 B cap: **463 B over, 111%
of the limit.** The smallest of the five breaches, and the one most likely to be a straight
compaction rather than a split.

The fork, same as `core/063`'s:

- **One decision stated at length** → compact under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full, including quoting every cut hunk
  verbatim rather than naming categories. **463 B is a realistic squeeze** — `core/063` cut 698 B out
  of a comparable entry by removing one incident blockquote.
- **One decision that has accreted several arguments** → split into two numbered decisions and
  update `embarch-outpost/decisions.md`'s index, number list **and** size column, same commit.
  **A new decision number is the most expensive thing in this suite to reverse**, so the burden of
  proof is on this branch, and at 111% of cap it is a hard case to make.

**Read it before choosing** rather than assuming the small breach means the easy answer.

## Why now

**Because the per-decision cap has no ledger and no clock.** The file-level ledger has both. A
decision that was never pinned is invisible to everything: `check-doc-size.py --decisions` prints
only its top 20 by size, which is how `embarch-core` decision 30 sat over cap until a reviewer opened
the baseline file while checking something unrelated. Whether that gap should be closed mechanically
is the owner's call under `scripts/`
([`tasks/doc/052`](../doc/052-a-verbatim-split-silently-drops-the-decision-size-pin-of-every-decision-it-moves.md)
records the adjacent defect). **This task is only about the one decision.**

## Watch for

- **Do not add a pin to `scripts/decision-size-baseline.json` to make the number go away.**
  `scripts/` is owner-reserved, and pinning an over-cap decision is the papering-over move.
- **Decision 17 cites `embarch-core` decision 30 by name** for the `rx_utc_ms` per-frame stamp — and
  `core/063` compacted that very decision earlier today (4,248 B → 3,550 B). **Check that what this
  entry says decision 30 does is still what decision 30 says**, against `main`, before you touch
  anything. The cut there was the retired-alias blockquote, not the epoch-clock paragraph, so this
  should hold — but "should hold" is exactly the kind of claim a sweep exists to verify.
- **Keep the "why not".** The entry's load-bearing sentence is that the DUT's counter **cannot** place
  a trace at all because there is no sync point between the two clocks. Losing that invites someone
  re-proposing a single-clock design. Cut measurement detail and narrative, not the impossibility
  argument.
- **Grep the whole doc repo for inbound `decision 17` citations before renumbering anything**, and
  remember a bare `decision 17` in another repo's file means *that* repo's 17 — `embarch-api` and
  `embarch-topology` both have their own real, unrelated decision 17, which is the collision
  `api/099` spent this leg fixing in a shared crate.
- **Report before/after byte counts and the margin left**, the way `core/063` did.

## Compaction taken

**Compacted, did not split.** 463 B over is the smallest of the five breaches, and decision 17 is one
decision stated at length — the DUT-clock claim, the two "cannot go backwards" reasons, the five host
rules, and four rejected alternatives — not several accreted arguments needing separate numbers.
Nothing in it is two decisions wearing one heading; a split would have bought nothing any citation
needed and would have cost a new decision number, the most expensive thing in this suite to reverse.

Grepped before touching anything: the only inbound citations of *`embarch-outpost`'s own* decision 17
(as opposed to `embarch-api`'s or `embarch-topology`'s own unrelated decision 17s, both real and both
distinct) are `embarch-outpost/interfaces/integration.md` (Core's `rx_utc_ms` is the real epoch clock;
do not join a study's column on it), `suite/decisions/naming.md` (quotes the exact retracted clause,
still quoted verbatim below), and `tasks/outpost/018` (the "other clock, not a threshold" test). All
three land on claims this pass left standing; none cited the passages that were cut.

**Decision 30's text was re-checked against `main` before editing anything**, per this task's own
warning that `core/063` compacted it the same day. Decision 30 (`embarch-core/decisions/streams.md`)
still says "Core is the trace's clock, and a join it cannot verify stamps nothing" — the cut there was
the retired-alias blockquote, not the epoch-clock paragraph, so decision 17's citation
("stamped per frame by embarch-core decision 30... Core's real epoch clock") still holds.

**The hot/cold test, applied per sentence** ([DOC-COMPACTION-PASS.md](../../DOC-COMPACTION-PASS.md)):
every claim, constraint, rejected alternative and failure signature in this entry is hot — there is no
single cold incident-narrative block the way decision 30 had one blockquote to delete outright. The
squeeze is therefore distributed: many small tightenings, each keeping the claim and dropping only
narrative padding, provenance detail, or a redundant restatement. The full diff is in the branch;
every hunk that actually removed content (not just reworded it) is quoted below, verbatim, so the list
can be checked against the diff rather than trusted on its own — the gap leg 117 left was a connector
clause cut but not quoted, so this list errs toward over-inclusion rather than under.

Quoted verbatim, every cut that removed content rather than merely rephrasing it:

- `and that is the one clause in this entry that is false` (correction blockquote — dropped the
  scope-qualifier on the 2026-09-12 correction; the correction itself, its date and its task citation
  all stay)
- `milliseconds since that board booted` (correction blockquote — dropped the concrete-units gloss on
  "dev-bench uptime"; "not UTC, no epoch, no offset" stays, which is the load-bearing half)
- `One name, two clocks, in two files an analyst opens side by side.` (correction blockquote — a
  mnemonic restatement sentence, dropped whole; the two comparability facts it was restating stay in
  the next sentence, unchanged)
- `would look better and` (the "nothing interpolates" rule — dropped the temptation clause explaining
  *why* someone would interpolate; the rule itself, "even spacing... is fabricated," stays)
- `independent` (the "what separates them" test — dropped from "two independent clocks contradicting
  each other," now "the clocks disagree"; the test itself is unchanged)
- `total` (the same paragraph — dropped from "the DUT's own total forward span")
- `either way` (the same paragraph — dropped from "the harmless inversions stay reported either way")
- `took` (the same paragraph — dropped from "the whole capture took")
- `driver's` (the TX-only-DUT sentence — dropped from "the OS driver's receive buffer," now "the OS
  receive buffer")
- `one line of code, a visibly smoother chart, and` (first rejected alternative — dropped the
  temptation lead-in; the reason for rejection, "a lie: it manufactures a resolution the wire does not
  have...", stays whole)
- `in exactly the register this suite exists to refuse` (same rejected alternative — dropped the
  rhetorical framing clause; the substantive reason it was framing is unchanged)
- `at all` (third rejected alternative — dropped from "a job the DUT's counter cannot do at all")

Everything else that changed in the diff is rewording that keeps the same fact in fewer words (e.g.
"so an interrupt preempting a thread between those two operations reserves after it and is stamped
before it" → "so a preempting interrupt can land between the two and be stamped earlier than the
thread it interrupted") — no claim, constraint, rejected alternative or failure signature lost a
sentence, only some of them lost words that did not carry one.

4,559 B → 4,070 B, 489 B cut, 26 B of margin left under the 4,096 B cap. The margin is thin — this
entry has no further cold material to trade if it needs to grow again; the next byte spent here should
either come with a fresh squeeze pass or a hard look at whether it has become two decisions.

**Judgement call, recorded per this task's instruction:** decision 17's claims carry two live hardware
debts — "nothing has compared a trace's placement against a second stream" (`embarch-ui/open.md`) and
"no signal tap has read a byte" (`embarch-topology/open.md`). Neither debt lives inside `clocks.md`
itself; both live in the two `open.md` files above, untouched by this pass, and neither was quoted or
paraphrased into `clocks.md`. Checked specifically: does anything cut above turn an unverified claim
into a settled one? No — the entry never claimed the placement had been checked against a second
stream or that a signal tap had read a byte; its strongest claim, in bullet 2, was and remains "so
laying a trace beside a power capture is **an alignment rather than a guess**" — a capability claim,
not a verification claim, unchanged by this edit. The cut passages (above) were provenance, a
temptation-clause, a mnemonic restatement, and single-word intensifiers — none of them the hedge that
carries the hardware debt, because no sentence in this entry was hedging on hardware in the first
place. The debt was never local to this file, so compacting this file could not have lost it; it
survives, unread, in the two `open.md` files it already lived in.

## Done when

- [x] `embarch-outpost` decision 17 is at or under 4,096 B, or split into two decisions each under
      it, with the branch taken justified in the task body. (Compacted: 4,559 B → 4,070 B.)
- [x] `embarch-outpost/decisions.md`'s index table matches — numbers and size column. (No renumbering
      — decision 17 kept its number and file. `embarch-outpost/decisions.md` has no per-decision size
      column at all (only `core`, `dev-bench` and `api` carry one); the "Two clocks" row's decision
      list, `17, 18`, is unchanged. Verified: no edit was needed to `decisions.md`.)
- [x] The entry's claim about `embarch-core` decision 30 re-checked against that decision's current
      text on `main`. (Still says "Core is the trace's clock"; the `core/063` cut was the
      retired-alias blockquote, not the epoch-clock paragraph.)
- [x] Every inbound `decision 17` citation still resolves to the claim it was citing. (Three real
      inbound citations found, listed above; all resolve.)
- [x] If compacted: every cut hunk quoted verbatim in the task file, per `DOC-COMPACTION-PASS.md`.
      (Twelve hunks, above — every one that removed rather than reworded content.)
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). (`check-docs.py`: 11/11 green.
      `check-ownership.py --scope outpost` and `--code-repo`: both green. `check-doc-size.py
      --decisions`: decision 17 no longer appears in the over-cap list. `--pressure`: `clocks.md` now
      reports PAID, out of reserve, citing this task — closed by this same commit.)
