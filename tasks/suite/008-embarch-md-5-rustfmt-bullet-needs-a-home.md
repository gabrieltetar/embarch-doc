# 008 — `embarch.md` §5's rustfmt bullet is a decision record wearing a principle's clothes

**State:** open — **announced and parked, `ts 1788689863.494449` (2026-09-06 04:57 MDT), window closes 05:27 MDT.** Leg 018 ended before the window closed. **The next leg completes this window; it does not restart it** (`../../embarch-fleet/ops.md` §4). Re-read the thread on that `ts`: a reply saying go runs it now, cancel drops it back to `open` with the reply quoted, silence past 05:27 means it may run.
**Source:** leg 017's own `suite/007` log entry, which named this and asked that the next thing landing here force the question. `api/024` is that thing.
**Scope:** suite — **never dispatched to a worker.** The supervisor executes it (`../../embarch-fleet/protocol.md` §8).
**Hardware:** none
**Owner:** no — but read the boundary section below before assuming that.

## What

`embarch.md` §5's `rustfmt` bullet is roughly **2,000 characters in a list of five
principles whose next longest is 193.** It is not a principle any more; it is a
decision record — a measurement history, a reversal condition, two rejected
command spellings, a named trap and a task pointer — living in a list of
one-sentence rules.

Three separate rounds of decision text have now landed in it:

1. `suite/006` wrote the original bullet: rustfmt is not enforced, the
   format-the-world cost, the decay measurement, the reversal condition.
2. `suite/007` added the two-spellings-are-both-wrong analysis after measuring
   that `--all --check` in `embarch-api` reports 57 files, 33 of them in other
   repos.
3. **`api/024`**, 2026-09-06, made `crates/embarch-core-client` a workspace
   member (`embarch-api` decision 56), which makes the bullet's
   "**`-p` is not an escape hatch**" sentence false for `embarch-api`.

Round 3's *factual* half was consumed as an ordinary `status.d/` correction in
leg 018's `api/024` fold — that is a correction, not design, and it did not need
this window. What is left is the structural question the corrections keep
deferring.

**Proposed: a `suite/decisions.md`**, a real decision record for suite-wide calls
the way every sub-project already has one, with the rustfmt bullet moved into it
**verbatim** and §5 keeping a one-line principle plus a pointer. A verbatim move
restates nothing, so `DOC-COMPACTION.md` §2's in-flux objection does not apply —
the same reasoning `api/023` and `umbrella/020` used for their splits.

## Why now

Leg 017's `suite/007` entry said it plainly: *"if a second suite-wide decision
lands with nowhere to go, the answer is a new home, not a sixth bullet"* — and
what happened instead is that **the same bullet absorbed a second round.** Its
closing line was that the next thing to land there should force the question
rather than be absorbed too. This is the third round. `embarch-dev-workflow.md`
is reserved, so there is genuinely nowhere else today.

## The boundary, and it is the reason this is parked rather than done

Creating a new shared suite-level doc is close to the line between design (the
supervisor's, under full delegation) and the doc corpus's own structure
(`DOC-PROTOCOL.md`, which is reserved). Two specific things to settle before or
while doing it:

- **Does `suite/decisions.md` need classifying?** `check-ownership.py --supervisor`
  asserts every tracked **top-level** `*.md` is classified reserved or
  fleet-writable. `suite/decisions.md` is not top-level, so it should not trip
  that — **verify rather than assume**, and if it does trip, the classification is
  the owner's call and this stops there.
- **`DOC-PROTOCOL.md` and `DOC-COMPACTION.md` must not need editing for this to
  make sense.** If a new doc class cannot be introduced without amending either,
  that is the signal this is the owner's and not the supervisor's. Say so and
  park it permanently rather than editing them.

## Done when

- [ ] The `ts` thread above has been re-read and the outcome recorded here.
- [ ] `suite/decisions.md` exists with the rustfmt bullet moved **verbatim**, or
      the alternative is argued and this task closes with the reason.
- [ ] `embarch.md` §5 keeps a one-line principle and a pointer; the five-principle
      list reads as five principles again.
- [ ] Every inbound reference to the moved text still resolves — check
      `tasks/doc/014` and `tasks/suite/007`'s successors, and grep the sibling
      repos, the way `api/023` checked its seam before cutting it.
- [ ] `check-ownership.py --supervisor` is clean on the leg's own diff, and the
      new file does not appear as an unclassified top-level doc.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

## Doc-size note

`embarch.md` is not in reserve. `embarch-decision-reversals.md` (9,309 / 10,240 B,
90.9%) and `suite/user-guide.md` (23,246 / 25,600 B, 90.8%) both are, filed
against `tasks/suite/004`, which is `blocked` on `In flux: yes`. This task should
make `embarch.md` **smaller**, so it owes nothing — but if the move somehow grows
a filed file, `tasks/suite/004` is where it rides.
