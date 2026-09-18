# 084 — `decisions.md`'s size column for `decisions/surfaces.md` is badly stale

**State:** open — drained from `inbox/core-decisions-md-surfaces-size-column-stale.md` by leg 138 at
`ui/065`'s fold, 2026-09-17. Body unchanged apart from this line, the number, and the scope
correction below.
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

- [ ] `embarch-core/decisions.md`'s `surfaces.md` row updated to its actual current size.
- [ ] A quick pass of the table's other rows against `wc -c` at `main`'s tip, in case another
      same-day amendment elsewhere did the same thing.
- [ ] Gate green.
