# 029 — A declared `PowerFrontEnd` tap and a study-authoring mistake produce the same evidence, and the honest place to say so is undecided

**State:** open
**Source:** split out of `tasks/suite/013` by leg 083, 2026-09-11. That unit closed 013's two
documentation items and deliberately did **not** take this one — see "Why it was split" below.
**Scope:** suite
**Hardware:** none to decide and implement it. Confirming the end state against a real study needs
the dev-bench board, and the bench queue is parked by the owner's `d0cf9a0`.
**Owner:** no

## What

`embarch-dev-bench` has no power front end (`app/src/main.c:685`, *"no power/waveform capture yet
(decision 21's scope)"* — that parenthesis is the comment's own shorthand for the decision the
dispatch function was written under, **not** a scoping claim; the decision that actually defers the
front end is `embarch-dev-bench` **24**), but `app/src/serial_protocol.c:166` **accepts** a `PowerFrontEnd` tap
declaration and does nothing with it. So the tap is authorable, crosses the wire, is parsed, and
yields an empty capture. Its only signal is `bytes_written: 0` — which `list_study_streams`' own
description defines as *"a tap that was declared and produced nothing"*, i.e. **as a study-authoring
outcome rather than as a missing subsystem.**

An engineer who declares a power tap therefore gets back exactly what they would get from mis-naming
a signal or pointing a tap at the wrong source. Nothing anywhere distinguishes *"you asked for
something this bench cannot do"* from *"you asked correctly and nothing happened"*.

## Why it was split rather than executed

`suite/013` fixed the four **documentation** assertions and gave power sampling its `features.d/`
row. This item needs a **code** change, and the supervisor executing 013 unattended judged that
**both candidate sites are in flux, so writing into either now is the mis-citation mechanism in a
different costume** — text placed where a queued task is about to delete or rewrite it:

- **`study_power_data`'s `#[tool(description = ...)]` in `embarch-api`** is the surface a newcomer
  actually meets, and it is the cheapest possible statement. But that tool is *"an alias for
  study_stream_data, kept for one release"* by its own description, and **`tasks/suite/015` is
  queued to retire all three fixed-channel aliases.** A carefully-worded sentence there has a known
  expiry date and no forwarding address.
- **A submit-time refusal** in `embarch-study-designer` or `embarch-core` is the more durable form —
  it makes the tap say why it cannot rather than making a tool description apologise for it. That is
  a change to **study submit behaviour**, which the supervisor announced in `#embarch-fleet`
  (`ts` `1789117538.021209`) it would *not* make unattended, and did not.

There is a third shape nobody has costed: leave submit alone and give `list_study_streams` a way to
say *"declared against a source this bench has no hardware for"* alongside `bytes_written: 0`, so
the distinction lands in the one place the guide already tells you to read first.

## Done when

- [ ] One of the three shapes is chosen and recorded as a numbered decision in the repo that owns
      the code it changes, naming why the other two were not taken.
- [ ] A study declaring a `PowerFrontEnd` tap produces evidence distinguishable from a tap that was
      declared correctly and captured nothing.
- [ ] `suite/features.md`'s power-sampling row (`features.d/dev-bench-125-power-sampling-deferred.md`)
      is updated if the new behaviour changes what "accepted, parsed, captures nothing" means.
- [ ] Gate green; `changelog.d/` fragment per repo touched.

## Constraint

**Do not simply delete the acceptance.** Refusing a `PowerFrontEnd` tap outright at submit is one of
the three shapes, not the obvious default: the roadmap calls power sampling **deferred, not
cancelled** (milestone 4), and a study file written today against a tap the firmware will support
later is not necessarily a mistake to reject. Whichever shape is chosen has to say what happens to
such a file.
