# 034 — a size debt on an `open.md` full of still-live questions has no payable form, and five are now parked that way

**State:** open
**Source:** leg 065's supervisor, 2026-09-10, from the outcome of `study-designer/026` (doc merge
`02775af`). Filed rather than fixed because `DOC-BUDGET.md` is owner-reserved
(`protocol.md` §3), and this is a question about what that file's role caps should say.
**Scope:** doc
**Hardware:** none
**Owner:** required — `DOC-BUDGET.md` and `DOC-COMPACTION.md` are reserved paths.

## What

`study-designer/026` was a compaction unit against `embarch-study-designer/open.md`
(4,662 / 5,120 B, 91.1%, inside its reserve floor). Leg 064's supervisor had asserted
`In flux: no` on it, over its own worker's objection, with an argument that is still correct as
far as it goes: *the compaction move for an `open.md` is striking questions that have since been
answered, which restates nothing, and no amount of flux forbids it.*

**The worker did exactly that pass, question by question, against current `spec.md`,
`decisions/` and `interfaces/`, and found nothing strikeable.** Its six findings each name a
source:

- the two power-profiling deferrals — still deferred, no trigger fired;
- the bench UTC clock-resync accuracy — still unmeasured;
- the `repeat`/`bitpack`/`crc32`/`fixed` render consumer — `interfaces/decoders.md`'s
  `StructLayout` still covers only the flat case;
- decision 45, declared GATT — `decisions/declares.md` says outright *"Designed, never built"*;
- `Study.protocols` — `spec.md`'s row-shape list still names no protocol row;
- the FFI staticlib cross-link — `decisions/ci.md` decision 64 says *"That build root does not
  exist yet."*

So the file is at 91% of its cap and **every byte of it is live content**. The task moved to
`blocked` with a named unpark condition and kept its `Size debt due: 2026-10-04` clock, which is
the least-bad state available and is why I landed it.

## Why this is a gap and not just one awkward file

**The debt has no payable form, and the ledger cannot express that.** `check-doc-size.py`'s model
is: a file in reserve has a filed compaction task, and that task's clock makes the park
non-absorbing — a leg spends its first unit on the oldest overdue entry. That model assumes the
compaction *can* be done. Here it cannot be done by anyone, at any date, without either deleting
a live open question or inventing an answer to it, and both are failures the compaction protocol
explicitly names. The clock will come due on 2026-10-04 and a leg will spend its first unit
rediscovering what this unit just established.

**It is not one file.** `embarch-api/open.md` (4,763 / 5,120), `embarch-dev-bench/open.md`
(4,782 / 5,120), `embarch-umbrella/open.md` (4,870 / 5,120) and `embarch-core/open.md`
(4,813 / 5,120) are all inside the same reserve, all against the same 5 KB role cap, and every
one of their compaction tasks is `blocked`. That is **five of eight sub-projects** whose
open-questions file is nearly full. A cap that nearly every instance of a role exceeds is more
likely to be a wrong cap than five wrong files — and `DOC-BUDGET.md`'s own warning is that a cap
which misfiles is worse than a cap which refuses.

**The failure mode is already visible elsewhere.** `api/055` (leg 064) placed a numbered decision
in `decisions/shape.md` rather than `decisions/zephyr.md` because `zephyr.md` is over its cap —
the third such placement in a week, and this leg's `umbrella/044` was shaped by the same pressure,
making four. Decisions are being filed by byte count rather than by subject.

## Two candidate answers, and picking between them is the owner's

1. **Raise or drop the `open.md` role cap.** An open-questions ledger's length is a function of
   how much design is deferred, not of how badly written it is, so it is the one role where a byte
   cap may be measuring the wrong thing. A sub-project with six genuinely open questions has a
   long `open.md` and that is the file working correctly.
2. **Let the ledger record "in reserve, nothing strikeable, re-checked on <date>"** as a third
   state distinct from a filed debt and a blocked one — so a verified-unpayable file stops
   consuming a first unit every time its clock comes due, while still being visible.

Whichever it is, the mechanism lives in `DOC-BUDGET.md` and `scripts/check-doc-size.py`, both
reserved, so no leg can act on this.

## Done when

- [ ] `DOC-BUDGET.md` either changes the `open.md` role cap or states explicitly that a full
      `open.md` of live questions is an accepted state and how the size ledger should record it.
- [ ] `tasks/study-designer/026`, `api/026`, `dev-bench/012`, `umbrella/038` and `core/022` are
      reconciled against whatever that says — several of them should probably be closed rather
      than carrying a clock nobody can answer.
- [ ] The decision-placement-by-byte-count pattern (`api/055`, `api/048`, and the two before them)
      is either accepted in writing or given a rule.

## Filed from `inbox/` by leg 066, 2026-09-10

Numbered `doc/034` and moved into the queue unchanged except for this section and the heading.
It parses, its `Hardware: none` claim is correct (it is a question about two documents), and
`Owner: required` is correct and is why `queue-status.py` lists it as `owner-only` rather than
dispatchable — `DOC-BUDGET.md` and `scripts/check-doc-size.py` are both reserved paths and no
leg can act on this.

**Two numbers in it have moved since it was written**, in the direction that strengthens it, and
they are worth having on the record before the owner reads it:

- It says "five of eight sub-projects" have a nearly-full `open.md`. Measured at this leg's step
  0, the reserve list holds **`open.md` for `umbrella` (95.1%), `core` (94.0%), `dev-bench`
  (93.4%), `api` (93.0%), `study-designer` (91.1%) and `ui` (81.9%)** — six files against the
  same 5 KB role cap, and `ui`'s is filed against a blocked task too. So it is six of eight, not
  five.
- The ledger currently holds **21 dated entries and 0 overdue**, of which **17 are filed only
  against a `blocked` task**. Nothing this leg had to pay. The clock this drop is worried about
  has not come due yet, which means there is still time to answer it cheaply rather than at the
  moment a leg is forced to spend its first unit on it.

I made no judgement about which of its two candidate answers is right; both are `DOC-BUDGET.md`
changes and neither is a supervisor's to make.
