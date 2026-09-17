# 085 — `/load/spans`'s `Gap` is thinner than `embarch-ui`'s own, and its diagnostics are entirely absent

**State:** claimed — leg 139, 2026-09-17, branch `agent/core/085-widen-spans-gap`.
Drained from `inbox/core-widen-spans-gap-and-consider-axis-diagnostics.md` by leg
138 at `ui/065`'s fold, 2026-09-17. Body unchanged apart from this line, the number and the
supervisor note below; `Scope: core` was already correct.

**Supervisor note — this authors a decision, and that is the point.** Box 2 asks whether decisions
62/64's boundary stands permanently. Either answer is a numbered `embarch-core` decision and both
are legitimate; **do not treat "widen the `Gap`" as the default just because it is the cheap one.**
The expensive half of this task is deciding whether `embarch-core` ever serves chart-facing
diagnostics, and a mechanical `Gap` widening landed on its own would close the visible symptom while
leaving `embarch-ui` decision 27 blocked on exactly the same thing — `ui/065` established
field-for-field that widening `Gap` alone lets `embarch-ui` delete **nothing**.

**Read `tasks/ui/065`'s `## Escape hatch taken` section before you start.** It is the measurement
this task rests on, and re-deriving it would cost a unit.
**Source:** `tasks/ui/065` ("retire `trace.rs`'s own decode pipeline once `embarch-core` serves
spans"). That task's own instructions were to check the served payload against `trace.rs`
field-for-field before touching any code, and to say so here rather than widen `embarch-core`
itself — an `embarch-ui` worker cannot write this repo's task queue. Full finding recorded in
`embarch-ui` decision 27 (`decisions/trace-view.md`) and `embarch-ui/open.md`.
**Scope:** core
**Hardware:** none.

## Dispatch note — leg 139, 2026-09-17

**Doc-size reserve for `core`, read at dispatch.** Three files are in reserve and every one is
filed against a *blocked* compaction task, so none of them is being paid by anyone else:

- `embarch-core/decisions/stream-index.md` — **11,172/12,288 B, 1,116 B left** (`tasks/core/082`,
  blocked `In flux: yes`). **This is the file your decision lands in** — decisions 62–65 all live
  here.
- `embarch-core/decisions/surfaces.md` — 11,253/12,288 B, 1,035 B left (`tasks/core/079`, blocked).
- `embarch-core/decisions/auth.md` — 11,356/12,288 B, 932 B left (`tasks/core/046`, blocked).

**You compact `stream-index.md` as part of this unit** (`.claude/leg.md`; `DOC-COMPACTION.md` §2).
A new decision plus decision 64's correction will not fit in 1,116 B, and its compaction task is
parked on `In flux: yes` — which you are the cause of, so you are the only actor who can shorten
what you are rewriting without writing down a clean statement of something about to be wrong.
Carry `tasks/core/082`'s **`Must not delete:`** list verbatim (read it — it names decision 62's
scoping rationale, decision 63's fourth-boolean reasoning, decision 64's three-reasons case and its
scope boundary, and decision 65's shape section plus the corrected CSV-size measurement). Close
**only** `stream-index.md`'s item: strike that file off `tasks/core/082`'s `Compacts:` line by
**deleting** it, never by striking through in place, and say so in the body. If `082`'s
`Compacts:` line then names no file at all, mark the task `done` and `git rm` it.

**Target: `stream-index.md` under 90% of 12,288 B (≤11,059 B) *after* your own additions land.**

**The expensive half is the boundary call, not the `Gap` widening.** Box 2 is the real question and
both answers are legitimate numbered decisions. `ui/065` established field-for-field that widening
`Gap` alone lets `embarch-ui` delete **nothing** — gaps (2) and (3) below still force the row-decode
loop to stay. So do not land a mechanical `Gap` widening on its own and call the task done; that
closes the visible symptom and leaves `embarch-ui` decision 27 blocked on the identical thing.
If you decide the boundary stands permanently, say so explicitly enough that
`embarch-ui/open.md`'s bullet can be closed as *settled, permanently split*.

**Read `tasks/ui/065`'s escape-hatch section before you start** — it is the measurement this task
rests on and re-deriving it costs a unit. **Do not edit `embarch-ui` source or docs**: you own
`embarch-core` and `tasks/` only. Any `embarch-ui` follow-up is a task file in `tasks/ui/`, filed
by you, not built by you. Ownership is checked on your branches.

**Box 4 is not optional whichever way box 2 goes** — decision 64's closing sentence is a tombstone
for a gap that is still open, and `suite/decisions/placement.md` §4's "exactly one implementation"
property is presently false because of it. You may not edit `suite/decisions/placement.md`; correct
decision 64 and, if §4 needs amending too, write that as an `inbox/` drop with an absolute path
(`/home/gabriel/Github/embarch/embarch-doc/inbox/`).

## What

`GET /study/{id}/stream/{name}/load/spans` (decisions 64/65, `tasks/core/076`) serves `Lane`/`Span`
but a `Gap` shaped only `{from, to}` — `embarch-core/src/outpost_load.rs` lines ~101-105. Three
gaps against what `embarch-ui/src/trace.rs`'s own `Gap` carries and `embarch-ui/assets/app.js`
already renders from it:

1. **`Gap` is missing `records_lost`, `row_index` and `unbounded_start`.** All three are rendered
   today in `app.js`'s gap table (`assets/app.js` ~3860-3861, ~4250-4252) — a caller that switched
   to Core's shape as it stands would lose those columns, not just an internal duplication.
   `cycle_span` and `frame_index` are carried by `trace.rs`'s `Gap` too but not rendered
   client-side, so they matter less, though full parity would include them.
2. **None of the axis-health diagnostics are served anywhere** — not on `/load/spans`, not on
   `/load`'s `LoadSummary` (which only carries `has_time_base` of this whole family): `frames`,
   `resolution_ms`, `dual_clock`, `unstamped_rows`, `undated_rows`, `dut_backsteps`,
   `dut_backstep_max_us`, `dut_step_max_us`, `dut_clock_refused`, `stale_prefix_rows`,
   `stale_prefix_step_us`, `out_of_order_rows`. Every one of these is rendered today in `app.js`'s
   trace-tab clock-health notes (~3780-3848). Decisions 62 and 64 scope these out by name as
   "chart geometry" / `embarch-ui`'s own `TraceView` shape, so this is not an oversight — widening
   the route to carry them is a design call for this repo to make, not a bug to just fix.
3. **Point events are excluded by the same two decisions**, and in `trace.rs` they are built in the
   same row-iteration pass as `Lane`/`Span`/`Gap`. As long as they stay excluded, `embarch-ui` must
   keep decoding the raw CSV row-by-row regardless of what `/load/spans` serves — which means
   `dut_clock_health`, `stale_prefix_end` and the row-decode loop itself cannot be deleted from
   `trace.rs` even after (2) above, unless point events are served too.

Net effect: even fixing (1) alone would not let `embarch-ui` delete its row-decode/clock-health/
stale-prefix machinery, because (2) and (3) still require it. `ui/065` did not touch `embarch-ui`
code for this reason — a partial swap (Lane/Span/Gap only) would either regress the gap table
(missing columns) or add a second source of the same facts beside code that has to stay anyway.

## Why now

`embarch-ui` decision 27 has said "closing it needs per-span data, or a decision it stays split"
since `ui/051`. `core/076` shipped per-span data, but `ui/065` found it insufficient to close the
split, field-for-field. Filing precisely what is missing now, while the comparison is fresh,
rather than leaving the next worker to re-derive it from scratch.

## Done when

This is a decision task, not (necessarily) a build one — the right first step is deciding whether
`embarch-core` wants to widen `/load/spans`'s `Gap` (mechanical, likely cheap) and/or take on
serving the axis-health diagnostics and point events (a real scope expansion past decisions 62/64's
stated boundary, and probably its own decision either way).

- [ ] Decide: widen `Gap` to `{from, to, records_lost, row_index, unbounded_start}` (and optionally
      `cycle_span`, `frame_index` for full parity with `trace.rs`'s own `Gap`), or say why not.
- [ ] Decide: whether the axis-health diagnostics and point events are ever in scope for
      `embarch-core` to serve, or whether decisions 62/64's boundary stands permanently and
      `embarch-ui` decision 27's split is therefore not closable by this route at all — in which
      case say so, so `embarch-ui/open.md`'s bullet can be closed as "settled, permanently split"
      rather than left open waiting on something that will never land.
- [ ] If widened: `embarch-core`'s own decision record updated, and the matching `embarch-ui`
      follow-up (consuming the wider shape) filed back to `tasks/ui/`, not built here.
- [ ] **Decision 64's closing sentence is corrected, whichever way the boundary call goes.** Added
      by leg 138 on its reviewer's recommendation. Decision 64 currently reads *"Serving spans is
      what closes the gap decision 4 opened and decision 62 left standing"* — and `ui/065`
      established field-for-field that it does not: `embarch-core/src/outpost_load.rs` and
      `embarch-ui/src/trace.rs` both still build `Lane`/`Span`/`Gap` from a CSV, so
      `suite/decisions/placement.md` §4's *"exactly one implementation of that timeline exists in
      the suite"* is **presently false**. That sentence reads as a tombstone for a gap that is still
      open, and it is `embarch-core`'s to fix; nothing else will reach it. Fix it even if you
      decide the boundary is permanent — especially then, since a permanent split is precisely the
      case decision 64's sentence denies.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
