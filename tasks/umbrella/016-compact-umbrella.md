# 016 — `spec.md` is in reserve (`decisions/doctor.md`'s half is paid)

**State:** blocked
**Source:** scripts/check-doc-size.py --pressure, after `umbrella/011`
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/spec.md
**In flux:** yes — `tasks/umbrella/007` is open and rewrites a row of `spec.md`'s doctor table. (`012`, `013` and `015` have since landed; the filer also listed `012`, which had already landed as leg 012's second unit.)
**Must not delete:** decision 22's three unbuilt checks and the sentence saying they are unbuilt; decision 23's original claim *and* the amendment saying which half of it decision 40 replaced — a retired-or-amended entry that loses what it used to say stops being a tombstone; decision 31's note that check 14 runs under the WSL user's environment rather than the service account's, which is still open; `spec.md`'s twenty-row doctor table and which rows are designed-and-unbuilt.

## What

**`decisions/doctor.md`'s half is paid, 2026-09-05, by `umbrella/015`** — the unit that
was about to write there did the compaction in its own commit ([DOC-COMPACTION.md](../../DOC-COMPACTION.md)
§2's ride-along). It came out by a **mission split**, not by squeezing: decisions 23
and 40 are one check against the agent CLI's config and became `decisions/mcp.md`, so
nothing was restated and the `Must not delete:` items below all still read verbatim —
23's original claim and its decision-40 amendment moved with it. The file is
**7,774 / 12,288 B (63%)**. What remains here is `spec.md` alone, at **9,286 / 10,240 B**.

At filing, `decisions/doctor.md` was **11,918 / 12,288 B — 370 B left**, and `spec.md` was
**9,286 / 10,240 B**. `umbrella/011` put decision 40 into the first and rewrote
check 10's row in the second; both were already close, and the new decision
would not fit under the reserve line at any length that still said why the
route was chosen.

Run `scripts/check-duplication.py embarch-umbrella` first, as `009` says — but know
that on 2026-09-05 it was **clean**, "no overlap of 12+ words". The last pass's biggest
find was `decisions/doctor.md` re-arguing build status that `spec.md`'s table owns; that
well is dry, so `spec.md`'s bytes come from real shortening, not from a duplicate.

**`009` is the sibling and is not this task.** It holds the *pass* over
`spec.md` and `open.md` and is blocked on the same queue; its reserve item for
`spec.md` was paid on 2026-09-05 and `spec.md` went back over the line here.
`open.md` is not in this item — `umbrella/011` took it 4,596 → 4,289 B.

## Why now

`spec.md` has 954 B of headroom and its doctor table is what every umbrella task
rewrites a row of — `007` is queued against exactly that. The next worker that has to
widen a row is blocked by arithmetic rather than by design. (`decisions/doctor.md`
was the acute half and is paid; that is what the ride-along is for.)

## Why blocked

`In flux: yes`, for the reason `009` gives and the same queue. **Unparks with
`009`** — one pass over the sub-project, not two.

## Done when

- [x] `decisions/doctor.md` out of reserve — split by mission into `decisions/mcp.md`, 11,918 → 7,774 B (`umbrella/015`).
- [ ] `spec.md` out of reserve.
- [ ] Every `Must not delete:` item still findable, by search, in the compacted text.
- [ ] [DOC-COMPACTION-PASS.md](../../DOC-COMPACTION-PASS.md)'s human question — *can `spec.md` alone answer what someone needs to work on this component today?* — answered in the commit message. (Filed as "`DOC-COMPACTION.md` §7"; that doc has five sections since the 2026-09-04 split moved §6–§9 out.)
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
