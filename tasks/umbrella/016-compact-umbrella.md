# 016 — `spec.md` is in reserve (`decisions/doctor.md`'s half is paid)

**State:** done, 2026-09-05 — both items paid as ride-alongs, `decisions/doctor.md` by `umbrella/015` and `spec.md` by `umbrella/007`.
**Source:** scripts/check-doc-size.py --pressure, after `umbrella/011`
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/spec.md
**In flux:** no longer — `tasks/umbrella/007` closed on 2026-09-05 and did the `spec.md` compaction in its own commit, which is what §2's ride-along is for. (`012`, `013` and `015` have since landed; the filer also listed `012`, which had already landed as leg 012's second unit.)
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

## Why it was blocked

`In flux: yes`, for the reason `009` gives and the same queue. It never
unparked: `umbrella/007` was the unit making the flux, so it carried the
`spec.md` clause and paid it in its own commit — which is the ride-along
[DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 exists for, and the second
time in two days it beat waiting for `009`.

## Done when

- [x] `decisions/doctor.md` out of reserve — split by mission into `decisions/mcp.md`, 11,918 → 7,774 B (`umbrella/015`).
- [x] `spec.md` out of reserve — 9,286 → 9,014 B (88.0%), ride-along in `umbrella/007`'s commit ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2). Real shortening, no split: 10 KB is a role cap on a single file, so there was nowhere to move bytes to.
- [x] Every `Must not delete:` item still findable, by search, in the compacted text — the doctor table is still **twenty rows**, and the designed-and-unbuilt set is now **two** decisions (22(a-c), 26's `--prune`), 17's amendment having been *built* by `umbrella/007` rather than deleted from the sentence.
- [x] [DOC-COMPACTION-PASS.md](../../DOC-COMPACTION-PASS.md)'s human question — *can `spec.md` alone answer what someone needs to work on this component today?* — answered in the commit message. (Filed as "`DOC-COMPACTION.md` §7"; that doc has five sections since the 2026-09-04 split moved §6–§9 out.)
- [x] Gate green, `changelog.d/umbrella-*` fragment dropped (`umbrella/007`'s).
