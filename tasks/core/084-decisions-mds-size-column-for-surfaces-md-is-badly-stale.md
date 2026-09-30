# 084 — `decisions.md`'s size column for `decisions/surfaces.md` is badly stale

**State:** claimed by agent/core/084-size-column-pass, 2026-09-29 21:05
**Filed:** drained from `inbox/core-decisions-md-surfaces-size-column-stale.md` by leg 138 at
`ui/065`'s fold, 2026-09-17.
**Source:** review of `core/080` (merge `74c410b`). That unit corrected `embarch-core/decisions.md`'s
`stream-index.md` row from 10.7 KB to 10.9 KB in the same commit it grew that file — a good update,
but scoped to the one row it was already touching. Checking the table's other rows against actual
file size at the same merge SHA found one row far outside rounding drift.
**Scope:** core
**Hardware:** none — `wc -c` against a table of numbers; re-checked by leg 138 and it holds.
**Owner:** no

**Scope corrected from `doc` to `core` by leg 138 at the drain**, for the same reason as
`tasks/core/083`: the only path it touches is `embarch-core/decisions.md`, which is a `core`
worker's to write. Whoever runs it: the second `Done when` box asks for a pass of every other row,
so do that pass rather than fixing the one row named — the reviewer that filed this already checked
five rows and found them clean at `74c410b`, but `main` has moved several units since.

**The one row this task names is already fixed, and the task is still open on purpose.** Leg 141's
`core/078` (`embarch-doc@00f9d79d`) added decision 67 to `decisions/surfaces.md` and compacted 55
and 59 in the same unit, and updated that row to **10.6 KB** against a file now at **10,896 B** —
correct. **What is left is the second `Done when` box, which is the whole value here**: a pass of
*every* row against `wc -c`, not the outlier that got noticed. Do not read the corrected row as the
task being done; the five rows the original reviewer checked were checked at `74c410b` and `main`
has moved a dozen units since. Note also that the arithmetic below is stated against `74c410b` and
is now history, not the current state.

## What

`embarch-core/decisions.md`'s index lists `decisions/surfaces.md` at **6.9 KB**. The file on disk
at `74c410b` is **11,253 bytes (~11.0 KB)** — 60%+ larger than the table says, and (per `core/077`'s
own commit message, `2c14f34`) already over 90% of its reserve. The other rows checked at the same
SHA are within normal rounding (`studies.md` 11,035 B vs "10.5 KB", `handshake.md` 8,824 B vs
"8.2 KB", `streams.md`/`logging.md`/`enrollment.md` all within ~100 B of their listed figures) —
`surfaces.md` is the outlier, not a symptom of the column being stale generally. It grew across two
same-day amendments (`core/074`, `core/077`) that both edited `decisions/surfaces.md` without
touching `decisions.md`'s table.

This is not something `core/080` caused or should have fixed — it never touched `surfaces.md` — but
it is exactly the kind of drift a hand-maintained size column accumulates one un-updated row at a
time, and a reader using the table to gauge which file is near budget would be told `surfaces.md`
has ~5 KB of headroom when it has closer to 1 KB.

## Why now

Found while checking `core/080`'s own size-column edit for correctness (decision 65's stream-index.md
row); checking the sibling rows at the same SHA is the arithmetic a size-column edit invites and
nothing else in the gate does.

## Done when

- [x] `embarch-core/decisions.md`'s `surfaces.md` row updated to its actual current size.
- [x] A quick pass of the table's other rows against `wc -c` at `main`'s tip, in case another
      same-day amendment elsewhere did the same thing.
- [x] Gate green.

## Resolution (2026-09-29)

Ran `wc -c` on every file in `embarch-core/decisions/` against `main`'s tip and compared to
`decisions.md`'s table (KB = bytes/1000, rounded to one decimal, matching the convention the
already-correct rows used). Drift had spread well past `surfaces.md`: 11 of 15 rows were stale,
not just the one named. Corrected all of them in one pass:

| File | Table said | `wc -c` | Corrected to |
|---|---|---|---|
| probes.md | 8.9 KB | 9,121 B | 9.1 KB |
| flashing.md | 3.6 KB | 4,421 B | 4.4 KB |
| flash-backend.md | 8.4 KB | 9,462 B | 9.5 KB |
| studies.md | 6.1 KB | 6,250 B | 6.3 KB |
| study-record.md | 8.8 KB | 8,890 B | 8.9 KB |
| handshake.md | 8.6 KB | 8,819 B | 8.8 KB |
| outpost-preflight.md | 4.5 KB | 4,621 B | 4.6 KB |
| streams.md | 5.6 KB | 5,760 B | 5.8 KB |
| streams-live.md | 5.8 KB | 5,889 B | 5.9 KB |
| stream-index.md | 10.4 KB | 10,986 B | 11.0 KB |
| logging.md | 8.9 KB | 9,091 B | 9.1 KB |
| surfaces.md | 11.3 KB | 11,579 B | 11.6 KB |
| enrollment.md | 8.5 KB | 8,817 B | 8.8 KB |
| roles.md | 3.5 KB | 4,128 B | 4.1 KB |

`platform.md` (5,927 B, 5.9 KB), `auth.md` (3,799 B, 3.8 KB) and `route-sweep.md` (8,468 B,
8.5 KB) were already correct and untouched.

The `surfaces.md` figure (11,579 B) matches `tasks/core/091`'s reserve-debt arithmetic exactly
(709 B left of a 12,288 B cap) — this task did not touch that file, only its row in the index; the
reserve debt itself stays parked under `core/091` per its own `In flux: yes`.

No hardware, no `status.d/` fragment (no suite-level fact changed — this table is
`embarch-core`-internal), no `features.d/` row (no capability shipped/retired/re-matured).
