# 008 — The GPIO-trace family ships with no numbered decision, because the file it belongs in has no room

**State:** open
**Source:** `tasks/outpost/007`'s worker, 2026-09-06 — it drafted the decision, the size gate refused it, and it dropped the draft rather than push a file into reserve
**Scope:** outpost
**Hardware:** none
**Owner:** no

**Compacts:** embarch-outpost/decisions/tracing.md
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

- [ ] `decisions/tracing.md` has room for the GPIO decision — by compaction, or
      by the **mission split** `DOC-COMPACTION.md` §2 names as the cheaper move
      where one fits. A GPIO/pin-adjacent topic file may well be that split.
- [ ] A numbered decision records the GPIO-dispatch family: why a *handler*
      timeline rather than pin sampling, and the two traps `007` had to write
      into `wire.md` instead — `GpioCallbackDone` is an **exit marker** (misread,
      it attributes each handler's time to the wrong handler while the trace
      still looks readable), and `GpioDispatch`'s `b` is `0`, **not** a pin mask.
- [ ] `decisions.md`'s index row added, and `scripts/check-decision-refs.py`
      still resolves.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.

## Note for whoever dispatches this

Confirm `decisions/tracing.md`'s **8 KB** cap before writing a reserve line for
it. The generic 12 KB figure is wrong for this sub-project and has already
misled one dispatch.
