# 039 — decision 20's cut investigation log is not preserved in reversals row 105, and two named diagnostic methods now exist nowhere in the corpus

**State:** done — leg 120 (supervisor's own hands), 2026-09-16. Row 105 in
`reversals/rows-93-109.md` now names both hypotheses, both refutation methods and the handshake
test's per-candidate result. `reversals/rows-93-109.md` 12,532 → **12,838 B** (+306 B, no cap on a
reversals row file); `embarch-decision-reversals.md` unchanged at 9,309/10,240 B, so its reserve
item under `tasks/suite/004` neither moved nor grew.
`embarch-topology/decisions/link-declares.md`#20 **not touched** — still 3,717 B, 379 B of margin.
Corpus check after the edit: `grep -rnic 'debug status register\|generated devicetree'` across every
`*.md` now hits `reversals/rows-93-109.md`, so the two methods survive this task file's own deletion.
**Source:** `inbox/topology-decision-20-reversals-row-105-not-verbatim.md`, filed by the
`embarch-reviewer` on `topology/048` (doc merge `d3f2f81`), drained by leg 120.
**Scope:** suite
**Hardware:** none — doc prose only. No board, no probe, no live Core.
**Owner:** no — but **this is a `suite/` task and must not be dispatched to a worker.**
The fix lands in `reversals/rows-93-109.md`, and `check-ownership.py --scope topology`
refuses that path (verified by leg 120, both directions). The reviewer filed it as
`Scope: topology` in good faith; the gate disagrees, and the gate is right.
**Announcement:** `1789596240.452339` posted to `#embarch-fleet` by leg 120 at 2026-09-16.
The 30-minute silence-as-consent window (`../../embarch-fleet/ops.md` §4) opened at that `ts`.
**If leg 120 ends before the window closes, the next leg reads this `ts` and completes the window
rather than restarting it** — `scripts/fleet-read.py --thread 1789596240.452339`. A reply saying go
runs it now; a cancel drops this back to `open` with the reply quoted here.

## What

`topology/048` cut decision 20's investigation-log tail from
`embarch-topology/decisions/link-declares.md`, justified as *"already preserved almost verbatim as
`embarch-decision-reversals.md` row 105 — nothing lost from the corpus."* The cut hunk:

> Two hypotheses were checked and discarded before the port was suspected: that the identity gate's
> attach left the core halted (**refuted by reading the debug status register: halt clear, sleep set,
> i.e. running**) and that the overlay had not applied (**refuted in the generated devicetree**). What
> settled it was **writing a real handshake frame to each candidate by hand** — one returned nothing,
> the other returned an ack plus the bench's own log lines.

Row 105 in `reversals/rows-93-109.md` says only:

> Two well-evidenced wrong hypotheses came first, and what settled it was writing a real handshake
> frame to each candidate by hand.

That is a topic-level paraphrase. Three things from the hunk are absent from row 105 and, by a
corpus-wide grep at `d3f2f81`, absent from every indexed doc:

1. The two named hypotheses — core halted by the identity gate's attach; overlay not applied.
2. Their two refutation methods — a **debug-status-register read** (halt clear, sleep set) and a
   **generated-devicetree check**. These are reusable diagnostic techniques, not narrative texture.
3. The handshake test's per-candidate result — one candidate silent, the other ack-plus-log.

The only surviving copy was in `tasks/topology/048-...md`, which that fold deleted. It is recoverable
from `d3f2f81`, and the drop quotes it verbatim, but both of those are luck rather than design.

## Where it goes

**Expand row 105**, not decision 20. Row 105 is reversals content and is not capped at 4,096 B the
way a decision entry is; decision 20 has 379 B of margin and was just compacted to get under cap, so
re-inflating it partly undoes work that was correct.

## Watch for

- **`embarch-decision-reversals.md` is at 9,309/10,240 B — 931 B left, in reserve, and already filed
  against under `tasks/suite/004-compact-suite.md` (blocked).** `reversals/rows-93-109.md` is the
  split file; price it before writing and report before/after bytes for whichever file grows. A
  compressed restoration of the three items above is roughly 250 B. If that pushes a file past its
  reserve line and nothing has filed it, file the debt.
- **Compress, do not paste.** The timestamps and connective tissue are genuinely droppable; the two
  refutation methods and the per-candidate handshake result are not.
- **Do not close this by pointing at the task file or at `d3f2f81`.** A commit is not indexed corpus
  content a future reader consults.
- **Low-confidence side note from the drop, not part of this finding:** decision 21's reproduction
  timestamps were cut from two times to one date, and `history/topology.md:61` separately says the
  identity gate's result is "on record three times". Nobody has confirmed whether that count depended
  on the two-timestamp detail. Worth a look; not asserted as a defect.

## Done when

- [ ] Row 105 names the two hypotheses, their two refutation methods, and the handshake test's
      per-candidate result, in compressed form.
- [ ] `embarch-topology/decisions/link-declares.md`#20 is unchanged, or if touched, still at or under
      4,096 B with before/after bytes reported.
- [ ] Before/after bytes reported for whichever reversals file grew.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
