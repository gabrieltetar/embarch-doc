# 058 — Restore `append-only` to decision 13's bullet 3, and report the bytes

**State:** claimed — leg 122, `agent/ui/058-restore-append-only`, 2026-09-16.
**Source:** `inbox/ui-057-decision-13-squeeze-dropped-append-only.md` — the `ui/057`
reviewer's residue check on that unit's own byte-cap squeeze.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`embarch-ui/decisions/debug-tab.md` decision 13, bullet 3 (the anchor-swallow defect)
currently reads *"The window is a contiguous run of one file"*. It read
*"a contiguous run of one **append-only** file"* until `ui/057` trimmed the entry to
fit its corrected — and longer — main sentence under the 4,096 B per-decision cap.
`append-only` is not filler: it is the property of Core's rolling logfile that makes
the suffix/prefix-overlap fix described in that same bullet valid at all, because a
file whose past content never changes is what lets a stale suffix match reliably.

Restore it. The reviewer measured the entry at **4,079 B against a 4,096 B cap — 17 B
of headroom — and `append-only ` costs 12 B**, so it fits with nothing else touched.
**Re-measure rather than trusting those numbers**: they were taken at `7694670` and
the file may have moved since.

Second, lower-priority, and explicitly a judgement call: bullet 4 of the same entry
lost `only` from *"reproduced against the live Core with only its recent-lines route
delayed"* and lost the phrase *"timestamp-contradicting interleaving"*, which tied the
bullet back to the timestamp-contradiction property the decision states two paragraphs
earlier. Restore either or both **if and only if they fit after the bullet-3 fix**. If
they do not fit, leave them and say so — texture loss is allowed where a real cut is
not, and re-blowing the cap to chase the weaker of the two drops would repeat the
mistake this task exists to undo.

**Do not trim anything else to make room.** If bullet 3's restoration does not fit,
stop and report the measurement rather than cutting a fourth thing: these two
sentences have now been wrong three times, twice because an actor cut text and
classified its own cut as "no facts lost".

## Why now

This closes a four-deep chain (`ui/055` cut → `ui/056` restored wrongly → `ui/057`
corrected but cut this → here) and it is a 12-byte edit into known headroom. The
`ui/057` log entry says explicitly that nobody should read that fix as finished.

## Reserve

No `embarch-ui` file is in doc-size reserve this leg. The binding limit here is the
**4,096 B per-decision cap on decision 13 itself**, not a file cap — check it with
`scripts/check-doc-size.py --decisions` and report the before/after byte count for the
`### 13` section, the same way `ui/057` did.

## Done when

- [x] `append-only` restored in decision 13's bullet-3 sentence.
- [x] Bullet 4's `only` / `timestamp-contradicting interleaving` restored if they fit,
      or explicitly reported as not fitting.
- [x] Before/after byte count of the `### 13` section reported, and the cap not
      exceeded.
- [x] Nothing else in the entry cut to make room.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment dropped.

## Result

`### 13` section measured **4,079 B before, 4,096 B after** — exactly at the
4,096 B cap, not over it (`check-doc-size.py` fails only on `size > limit`).

What left the text: nothing. What entered it:
- Bullet 3: `append-only ` (12 B) inserted before `file` in "The window is a
  contiguous run of one **append-only** file, so the anchor is..." — restores
  the word `ui/057` cut. Cost: 4,079 -> 4,091 B.
- Bullet 4: `only ` (5 B) inserted before `its` in "reproduced against live
  Core with **only** its recent-lines route delayed" — restores the word
  `ui/057` cut. Cost: 4,091 -> 4,096 B.
- Bullet 4's other restoration candidate, the phrase `timestamp-contradicting
  interleaving`, does **not** fit: 0 B of headroom remained after the two
  restorations above, and this phrase alone costs far more than that. Left
  as `ui/057` wrote it ("exactly why this decision avoids a merged stream").
  This is texture loss, not a cut fact — the property itself (timestamps
  contradicting on a merged stream) is still stated in bullet 2 above
  ("interleaving them by arrival order would put lines in an order their own
  timestamps contradict").

Nothing else in the entry was touched or trimmed.

## Not yours

`history/ui.md` is assembled from fragments and is **not** a file this task may edit —
`ui/056` took a real red learning that. A history line that describes a restoration now
known to have been wrong stays as it is: history records what happened, not what is
currently true.
