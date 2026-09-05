# 007 — The daily log fold has no mechanism, and the 25 KB roll has none either

**State:** open
**Source:** leg 010, 2026-09-05 — the fold §11 owes was skipped once and then cost a
whole unit's worth of context to make by hand
**Scope:** doc
**Hardware:** none
**Owner:** required — every candidate fix is a new file under `scripts/`, which is reserved

## What

`protocol.md` §11 and `supervise.md` both say: *"On your first unit after local
midnight, fold the previous day's unit entries into one dated entry first."*
**Leg 009 owed that fold and did not make it** — it ran units at 00:18 and 00:26,
after local midnight, with nine unfolded 2026-09-04 entries sitting in the file.
`supervisor-log.md` reached **84 KB** as a result, against the 25 KB line §11
names for rolling the oldest entries into `history/archive/`.

**Leg 010 made the fold** (84 KB → 60 KB, nine entries → one, every SHA, every
debt and all nine line-anchored `**Reviewer:**` lines preserved). What this task
is about is **how much that cost and why**, because the next leg pays it again:

- The obvious mechanism is a script. Leg 010 wrote one with the `Write` tool —
  exact anchors, refusing unless it found exactly nine `## 2026-09-04 ` headers —
  and `python3 <path>` was **denied by the auto-mode permission classifier**.
- So the only route left was `Read` the whole 84 KB file and `Write` it back with
  the fold applied, re-emitting ~34 KB of retained text that was never meant to
  change. That is ~35 K tokens of a leg's context, and a transcription error
  anywhere in it would silently corrupt the relay's own handoff. It was verified
  afterwards with `git diff -U0 | grep '^@@'` — two hunks, both inside the
  replaced range, proving lines 1–242 and 1027–1329 byte-identical — but
  **"verify it afterwards with a diff" is not a mechanism, it is a save.**
- `supervise.md` is right that a leg must emit only shell a permission rule can
  match. That rule and this fold are in direct tension: the shape that keeps a
  leg from suspending on a prompt is the shape that makes this fold impractical.

**And the roll has no mechanism at all.** §11 says the oldest entries roll into
`history/archive/` past 25 KB, "matching what `scripts/build_changelog.py` already
does for a history file". `build_changelog.py` does that for `history/<scope>.md`;
**nothing does it for `supervisor-log.md`**, which is still 60 KB — 2.4× the line —
with the fold already made. No leg has ever rolled it, and none can.

## Why now

§11's own argument is that per-unit entries hit the roll cap every few days and
*"the handoff would get shorter and shorter — the opposite of what a relay
needs."* That failure has **begun**, not been predicted: the file is over the line
by more than a factor of two and every leg's step 0 reads it cold. The cost of the
fold grows with the backlog, which is exactly the shape that makes it never get
done — leg 009 skipped it, and leg 010 only managed it because it happened to have
a quiet stretch while two workers ran.

## Done when

- [ ] A leg can fold a day without re-emitting the file — most likely
      `embarch-fleet/scripts/fold-day.py <yyyy-mm-dd>`, invoked as
      `python3 scripts/...` exactly like `build_changelog.py`, `build_features.py`
      and `fold-commit.py` already are, so it is a prefix a permission rule
      matches and the classifier does not have to judge an ad-hoc script.
- [ ] It preserves what §11 requires: **every SHA**, **every hardware debt**, and
      **every line-anchored `**Reviewer:**` line** — `grep '^\*\*Reviewer:'
      supervisor-log.md` is the tally that decides whether per-unit review stays,
      and a fold that collapses nine reviewer lines into one silently destroys it.
      Leg 010's folded 2026-09-04 entry is the worked example of the shape that
      survives this.
- [ ] The roll §11 describes actually exists for this file, or §11 stops
      describing one — 60 KB against a 25 KB line means one of the two is wrong.
- [ ] `supervise.md` names the mechanism, so the next leg does not rediscover
      that the obvious one is blocked and then decide the fold is optional.

## Also worth deciding

Whether the fold should be **the listener's or the owner's rather than a leg's.**
A leg is bounded at four units precisely so it does not accumulate context, and
handing it a ~35 K-token file rewrite as its *first* act is the opposite of that.
A once-a-day job with no unit attached to it may simply not belong inside a leg.
