# 015 — Decision 24 sits in `enrollment.md`, away from the two decisions it is built on

**State:** open
**Source:** supervisor, leg 036, 2026-09-07 — landing `topology/003`, which authored decision 24
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

Decision 24 (`detected_by` gets a fourth answer for a declared serial with the VID gate off)
landed in `embarch-topology/decisions/enrollment.md`. **Its subject belongs to
`decisions/links.md`**, and so do both of the decisions its argument is built on:

- **17** — the dev-bench link's own USB serial as a declared fact — `links.md`
- **18** — the DUT signal link and its declared route, whose `Filter::for_declared_serial` is the
  exact code path decision 24 is about — `links.md`
- **20** — the declared USB *interface* — `enrollment.md` (cited too, so this genuinely straddles)

`decisions.md`'s own index describes `links.md` as *"Declared facts about wires: **a link's own
port**, and a DUT signal's route"* and `enrollment.md` as *"The one surface that needs a human, and
the facts detection cannot produce."* Decision 24 is about **what detection reports** for a link's
port — the first description, not the second.

## Why this is filed rather than fixed, and why it is not the usual defect

**The placement was forced by a hard cap, not chosen badly, and the worker disclosed the reason
rather than rationalising it.** Checked at landing: `links.md` was **10,390 / 12,288 B**, so it had
**1,898 B of hard room and 669 B before its reserve line** — and decision 24 is ~2.9 KB. It could
not have gone in `links.md` at all without compacting or splitting that file first. `enrollment.md`
had the room (7,868 B, now 10,760 B).

This log has recorded *"a supervisor pre-picking a decisions file to route around size pressure and
finding the argument afterward"* across at least three consecutive legs. **This is not quite that
instance** — the constraint was a wall rather than a preference, the byte numbers were stated up
front, and a thematic argument for `enrollment.md` was offered alongside. It is recorded anyway,
because the outcome is the same shape: a decision filed away from its family, for a reason that has
nothing to do with what the decision says. Nothing is unfindable — `decisions.md`'s index lists 24
under `enrollment.md` correctly — so this is tidiness with a real cost only for the next reader
tracing the 17 → 18 → 24 argument across two files.

## Done when

- [ ] `decisions/links.md` has room for decision 24 — by compaction or by a split, whichever
      `DOC-COMPACTION.md` §3 makes the better call for a file that is one mission already.
      **A split is the default remedy**; say which you chose and why.
- [ ] Decision 24 is moved verbatim into `links.md`, or the decision is taken **not** to move it
      with the argument written down — "it straddles 17/18 and 20, and 20's home is as defensible
      as 17's" is a legitimate answer, and better than a move made only because this task exists.
- [ ] If moved: `decisions.md`'s index rows for both files updated, and
      `scripts/check-decision-refs.py` green — decision 24 is cited from `src/hardware/port.rs`
      (three places) and `src/hardware/signal.rs`, so a move must not break those citations.
      This is exactly the failure `tasks/doc/022` is about.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
