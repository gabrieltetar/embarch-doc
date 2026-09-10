# 008 — The GPIO-trace family ships with no numbered decision, because the file it belongs in has no room

**State:** done by agent/outpost/008-gpio-family-decision, 2026-09-10
**Source:** `tasks/outpost/007`'s worker, 2026-09-06 — it drafted the decision, the size gate refused it, and it dropped the draft rather than push a file into reserve
**Scope:** outpost
**Hardware:** none
**Owner:** no

**Compacts:** embarch-outpost/decisions/tracing.md
**Size debt due:** 2026-10-02
**In flux:** no
**Must not delete:** Decision 19's rejected-alternative paragraph and its
**corrected price** — a coalesced "the instrument ran here" record costs a new
record kind and three host decoders, and **not** a layout bump. That sentence
carried the layout bump until 2026-09-06 and was wrong in three places at once;
a compaction that paraphrases it back into "and a layout bump" re-introduces the
defect this sub-project just spent a reviewer finding. Keep the more useful half
of decision 19 alongside it: **removing half the records did not move the link's
duty cycle at all** — the drain loop's shape, not its record count, sets the duty
cycle, and cutting records made frames smaller rather than rarer. That is a
measured result and is not re-derivable from the prose around it.

## What

`GPIO_DISPATCH` (kind 9), `GPIO_CALLBACK_DONE` (kind 10) and
`OUTPOST_FLAG_TRACE_GPIO` (`BIT(6)`) are **shipped and documented** — `007`
brought `interfaces/wire.md` and `interfaces/integration.md` up to them — but
there is **no numbered decision** recording why the family exists, what it
deliberately does not do, or the two traps a reader has to know. Every other
traced family in this sub-project has one.

The reasoning currently lives in `wire.md` and `integration.md`, which are
interface documents. That is the right place for the *rules* and the wrong place
for the *why*: `decisions.md` is what a later reader consults to find out
whether a behaviour was chosen or inherited, and for this family it answers
nothing.

## Why it did not land with `007`

`embarch-outpost` is the one sub-project in `check-doc-size.py`'s `TIGHTENED`
table (`scripts/check-doc-size.py:135-137`): its `decisions/<topic>.md` cap is
**8 KB, not the usual 12**. `decisions/tracing.md` is at **7,299 / 8,192 B —
89.1%**, which is *just under* the 90% reserve line, so nothing is filed against
it and `check-doc-size.py --pressure` does not list it. The worker's decision 22
draft took the file to ~8.7 KB and the gate refused it.

**That near-miss is the interesting part.** A file at 89.1% is invisible to the
pressure report and to every supervisor reserve line derived from it — including
the one on `007`'s own task file, which told the worker the `decisions/` files
"all have room". They had room against a cap that does not apply here.

## Done when

- [x] `decisions/tracing.md` has room for the GPIO decision — by compaction, or
      by the **mission split** `DOC-COMPACTION.md` §2 names as the cheaper move
      where one fits. A GPIO/pin-adjacent topic file may well be that split.
- [x] A numbered decision records the GPIO-dispatch family: why a *handler*
      timeline rather than pin sampling, and the two traps `007` had to write
      into `wire.md` instead — `GpioCallbackDone` is an **exit marker** (misread,
      it attributes each handler's time to the wrong handler while the trace
      still looks readable), and `GpioDispatch`'s `b` is `0`, **not** a pin mask.
- [x] `decisions.md`'s index row added, and `scripts/check-decision-refs.py`
      still resolves.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment dropped.

## Closing note (agent/outpost/008-gpio-family-decision, 2026-09-10)

Took the mission split, not a compaction. `decision 6` (manual markers) moved
out to a new `decisions/markers.md` — a verbatim move, no rewrite, so the
`Must not delete:` content in decision 19 (the corrected rejected-alternative
price, and the measured duty-cycle result) is untouched, still in
`decisions/tracing.md`, word for word.

That freed enough room for **decision 25** — GPIO dispatch as a handler
timeline, not pin sampling — added to `decisions/tracing.md`, with both traps
`007` had to write into `wire.md` instead: `GpioCallbackDone` as an exit
marker, and `GpioDispatch`'s `b` being `0` rather than a pin mask. It cites
`wire.md` for the exact field layout instead of repeating it, to keep the size
down.

`decisions/tracing.md` is now 6,940 / 8,192 B — clear of the reserve line
(this sub-project's reserve is a 1,200 B floor, not a flat 90%, so the room
needed was tighter than the percentage alone suggested), `check-doc-size.py`
no longer lists it. `decisions.md`'s index
row updated (tracing.md's row now reads 2, 19, 25; a new markers.md row reads
6). `check-decision-refs.py` re-run after the split: all references resolve,
including the 18 topic-file links.

**Human question from `DOC-COMPACTION-PASS.md`: can `decisions/tracing.md`
alone (plus `markers.md`) answer what someone needs to know to work on
outpost tracing today?** Yes for the hook-family choice, the self-exclusion
behaviour and now the GPIO trap pair — all three are the entries a session
changing tracing would actually load. `markers.md` is one decision and reads
fine standing alone; nothing in the split changed what either file says, only
where it lives, and `decisions.md`'s index keeps both one hop away.

**`embarch-outpost`'s `tests/unit` ztest suite was not run** — no `west`, no
`ZEPHYR_BASE` in this environment, a standing debt for several days now, not a
result of this unit. This unit changed no C or Kconfig; it is
documentation-only as instructed.

`embarch-outpost` code repo: no changes needed, nothing there references
decision numbers or file layout — branch pushed as-is (no diff from main).

Gate: `check-docs.py` — all 11 checks green. `check-ownership.py --scope
outpost` green on both worktrees. `check-client-names.py` green on both.
`check-decision-refs.py` green, explicitly re-run after the split.

## Note for whoever dispatches this

Confirm `decisions/tracing.md`'s **8 KB** cap before writing a reserve line for
it. The generic 12 KB figure is wrong for this sub-project and has already
misled one dispatch.

## Dispatch note (leg 066, 2026-09-10 15:34)

**I confirmed the cap, and the file has moved since this task was written.**
`embarch-outpost/decisions/tracing.md` is now **7,408 / 8,192 B (90.4%), 784 B left** — it has
crossed the reserve line since `007`, so it *is* on the pressure report and *is* filed against
(this task is the filing). The 8 KB `TIGHTENED` cap is correct for this sub-project; the generic
12 KB does not apply. **784 bytes is not enough for the decision this task asks for**, so the
compaction or split is not optional and is the first half of your unit.

**Prefer the mission split, and here is the room to do it in.** `DOC-COMPACTION.md` §2 names a
split as the cheaper move where one fits, and this file is the case for it: the GPIO-dispatch
family is a distinct subject from the rest of `tracing.md`. Every other `decisions/` file in
this sub-project has room (largest is `transport.md` at 6,978 B), so a new topic file costs
nothing in budget terms. **A verbatim split restates nothing** — moving whole decision bodies
into a new topic file is not a rewrite and cannot lose the arguments the `Must not delete:`
section protects. That is the safest path and the one I would take.

**If you compact instead of splitting, `Must not delete:` above is binding and specific.** Two
things in it are measured results that are not re-derivable from the prose around them, and one
of them was wrong in three places until 2026-09-06:

- decision 19's rejected alternative and its **corrected price** — a new record kind and three
  host decoders, **not** a layout bump. If your compaction reintroduces "and a layout bump" in
  any paraphrase, you have re-created the defect a reviewer just found.
- decision 19's measured result: **removing half the records did not move the link's duty cycle
  at all**; the drain loop's shape sets it, and cutting records made frames smaller rather than
  rarer.

**Then the decision itself, and the two traps are the point of it.** Record why a *handler*
timeline rather than pin sampling, and write both traps into the decision body rather than
leaving them only in `wire.md`: `GpioCallbackDone` is an **exit marker** — misread, it
attributes each handler's time to the wrong handler while the trace still looks perfectly
readable — and `GpioDispatch`'s `b` field is `0`, **not** a pin mask.

**Number it per `DOC-CONVENTIONS.md`, add the `decisions.md` index row, and re-run
`scripts/check-decision-refs.py`** — a split moves bodies between files, and that is precisely
the class of change that leaves a citation pointing at the file a decision left. Three units in
the last two legs hit stale cross-file decision citations; do not add a fourth.

**Answer `DOC-COMPACTION-PASS.md`'s human question in your closing note**, in your own words:
can `decisions/tracing.md` alone (plus whatever you split out) answer what someone needs to know
to work on outpost tracing today?

**You cannot build or run this sub-project's tests from a fleet worktree** and no leg has been
able to for several days: `embarch-outpost`'s Zephyr `tests/unit` ztest suite needs `west` and
`ZEPHYR_BASE`, neither of which exists here. This unit should be **documentation-only** — if you
find yourself needing to change C or Kconfig to close it, stop and say so in the task file
rather than shipping an unbuilt source change. Say plainly in your report that the ztest suite
was not run and why; that is a standing, honest debt, not a failure of your unit.
