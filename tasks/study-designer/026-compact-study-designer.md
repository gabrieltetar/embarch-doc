# 026 — Compact `embarch-study-designer/open.md`

**State:** blocked — leg 065, 2026-09-10

## Dispatch note, leg 065

**Doc reserve in your scope:** the file this task compacts — `embarch-study-designer/open.md`,
4,662 / 5,120 B, **458 B left** — is the only one in reserve. Nothing else in
`embarch-study-designer/` is. Paying this debt *is* the unit, so you owe no new compaction task
unless you push some *other* file into reserve.

**`In flux: no` was asserted by leg 064's supervisor against its own worker's read, and the
argument is in this file below. Do not re-litigate it; do the work.** The compaction move for an
`open.md` is **striking questions that have since been answered** — verify each against the source
before striking it, and never delete an open question merely because it is old. `DOC-COMPACTION.md`
governs; answer its human question in your Result section in your own words: *can `spec.md` alone
answer what someone needs to work on this component today?*

**Source:** the surviving half of `tasks/study-designer/006-compact-study-designer.md`, closed
`done` by leg 064 on 2026-09-10 once its `spec.md` item was paid. Filed as a fresh task rather
than left on 006's `Compacts:` line, because `fold-commit.py` (correctly) refuses to fold a unit
whose own task file still reads `open`, and 006's remaining file is a real debt that must keep a
clock rather than be closed with it.
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/open.md
**Size debt due:** 2026-10-04

*The date is carried over unchanged from 006 — this is the same debt with a new file number, not a
new deferral, and re-dating it would be a park with extra steps.*

## In flux: no

**Leg 064's supervisor asserted this, against its own worker's read, and the reasoning belongs
here rather than only in the log.** 006's worker wanted to leave the task `blocked` on the grounds
that `open.md` is "still in flux". An open-questions file is edited every week in every
sub-project, so "in flux" applied to one is a property of the filename rather than a fact about a
subsystem settling down — and accepting it parks the debt permanently. It is also the wrong test
for the work available: the compaction move for an `open.md` is **striking questions that have
since been answered**, which restates nothing, and which no amount of flux forbids
([DOC-BUDGET.md](../../DOC-BUDGET.md)'s own wording for a 5 KB `open.md` role cap says the same).
If the owner disagrees, this is his call to make in his files, not a leg's.

## What

`embarch-study-designer/open.md` is **4,662 / 5,120 B — 458 B left**, inside the reserve floor. It
has been in reserve since `study-designer/008` tombstoned decision 45 there on 2026-09-08, and
`study-designer/019` left it untouched.

## Why now

It is the last file on 006's ledger entry, it has a clock, and it is the file every new open
question in this sub-project lands in — so it is the one place in `embarch-study-designer` where
the cap will refuse an edit that is *not* about the cap.

## Done when

- [x] `embarch-study-designer/open.md` is out of reserve (`scripts/check-doc-size.py` clean), or
      this task says in its own words why it cannot be.
- [x] Whichever it was is stated with the byte numbers before and after.
- [x] **Every question deleted was actually answered**, with the decision number or task that
      answered it named in the same edit. A live question shortened to fit is the failure this
      task exists to avoid; a question whose answer nothing records is *not* answered.
- [x] `DOC-COMPACTION-PASS.md`'s human question answered in the worker's own words.
- [x] Gate green ([protocol](../../../embarch-fleet/protocol.md) §10); `changelog.d/study-designer-*`
      fragment.

## Blocked

**Not the same claim as "in flux."** This section is not re-litigating leg 064's supervisor's
call — the file was actually re-checked, question by question, against current `spec.md` and
`decisions.md` (see Result below), not left alone on the grounds of flux. **The block is that
every question in the file is still genuinely open**, so `check-doc-size.py`'s own rule (a `done`
task is about to be deleted by the fold and cannot carry a debt forward) means this task must
stay open rather than close over an unpaid 91.1% reserve. Leaving it `done` would make
`embarch-study-designer/open.md` an unfiled file in reserve — the exact gap the size gate exists
to catch.

**Unparks on any one of:** any bullet in `open.md` getting a real answer (a decision number or a
task that closes it — most plausibly decision 45 getting built, the dev-bench cross-build landing
and closing the FFI bullet, or `Study.protocols` gaining a builder row type); or the owner
deciding, in his own files, that a still-open question should be pruned anyway.

**Size debt due:** kept at 2026-10-04, unchanged — see the dispatch note above on why re-dating a
carried-over debt would be a park with extra steps.

## Result

**File stays at 4,662 / 5,120 B — unchanged.** Checked every open question in the file against
current `spec.md`/`decisions.md` and struck none, because none has actually been answered:

- The two power-profiling deferrals (bench design, `Sample` grain) are still deferred with no
  trigger fired. **Amended by `study-designer/027`:** the "decision 24" citation this line
  originally rested on was wrong — decision 24's body (`decisions/wire.md`) is about the
  `StudyStart` wire message, not a power-profiling front end, and no decision records that
  hardware pick at all. `open.md` now cites none. The verdict here is unchanged: the bullet was
  and remains open with no trigger fired, so nothing was strikeable either way.
- The bench UTC clock-resync accuracy is still unmeasured — nothing in `spec.md`/`decisions.md`
  claims real-hardware validation of it.
- `repeat`/`bitpack`/`crc32`/`fixed` still have no render consumer — `interfaces/decoders.md`'s
  `StructLayout` only covers the flat `header`/`repeat` case; the counted walker, bit-unpacker and
  CRC check this question names are still absent.
- Decision 45 (`decisions/declares.md`) is explicit, today: "Designed, never built. No `gatt`
  field exists on `Study`, no `DeclaredGatt` type exists in `src/`" — so the declared-GATT
  authoring gap is still open, not a stale question.
- `Study.protocols` still has no row type in the Study Designer builder — `spec.md`'s row-shape
  list (sample/transcript/struct) names nothing for a protocol, and the retirement that did
  happen (`decisions/authoring.md` 34, `decisions/ci.md` 65: this crate's own UI binary, not the
  builder's row types) doesn't touch this gap.
- The FFI staticlib cross-link is still unexercised — `decisions/ci.md` decision 64 says outright
  "That build root does not exist yet," in the same words the open question uses.

The two "scoped narrow on purpose" bullets are design-boundary statements, not questions, so
`DOC-COMPACTION.md`'s "strike answered questions" move does not apply to them, and per
`DOC-COMPACTION.md` §1 shortening the prose of a *kept* item is out of licence regardless (the
`embarch-ui`/decision-11 clause-loss case this file's own protocol cites).

**Size debt is real and cannot be paid by this unit without inventing an answer.** Left the
`Size debt due: 2026-10-04` clock running rather than closing it — this is not a re-litigation
of "in flux: no" (the file is not being left alone because it is in flux; it was actually
checked, question by question, against the source, and every one is still genuinely open).

**`DOC-COMPACTION-PASS.md`'s human question, in my own words:** yes, for this component.
`spec.md` states the wire shapes, the row shapes, the constants table and the explicit
"deliberately does not do" list; someone changing `embarch-study-designer` code today does not
need `open.md` to avoid a wrong move — `open.md` exists to tell them what nobody has decided yet,
not what the component currently does. Nothing in today's `open.md` is load-bearing information
missing from `spec.md`; it is a deferred-work ledger, which is exactly `open.md`'s designed role
and not a sign `spec.md` is incomplete.

Gate: `scripts/check-docs.py` (11/11 green), `check-client-names.py --repo <study-designer doc
worktree>` (green), `check-ownership.py --scope study-designer` (0 changed paths, green) all run
from the `embarch-doc` worktree; `cargo build`/`test`/`clippy --all-targets -- -D warnings` clean
in the `embarch-study-designer` code worktree (no code changes were needed — this is a doc-only
unit). `changelog.d/study-designer-026-open-checked.decided.md` added.
