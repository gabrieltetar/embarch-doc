# 071 — Repeat a block of host steps and count matching console lines per pass, with no verdict

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 34 of 96 logged bench tests repeated one action 2 to 30 times and reported a count ("8 Hard Resets: 7 rx errors + 3 overruns", "30 Get_Sink_Cap", "10 rounds each"). Every count was a `grep -c` over a raw console dump
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

A host study can declare `Repeat { count | values, steps }`. It runs the inner steps `count` times, or once per entry of `values`, with `{value}` substituted into `Exchange` and `Instrument` lines. That covers both a stress loop ("send a Hard Reset 8 times, 6 s apart") and a sweep ("PPS at 5, 9, 12, 15, 18, 20, 21 V"). Each pass leaves an iteration marker in the study's record. A study can also declare `LineCount { name, tap, pattern }` views: a substring or regex over one tap's lines, counted per pass and over the whole run. **A count is shown, never compared.** The schema has no expected value, which keeps the 2026-09-25 rule that a study collects and the engineer interprets. The counts render post-run from the raw bytes on disk, the owner's 2026-09-25 choice for text taps: Core parses the text, and a finished run can be rendered again. A wrong pattern is fixed by re-rendering, never by re-running the bench.

## Why now

The field count script was one-off bash: two PowerShell readers, then six `grep -c` patterns. It could not be rerun on a finished capture with a corrected pattern. Unrolled by hand, the PD source sequence is 49 host steps. The same sequence is 3 steps around a `Repeat` over 7 values.

## Done when

- [ ] `Repeat` validates: count from 1 to a cap, or a non-empty `values` list. One nesting level only. `{value}` is refused outside a repeat.
- [ ] Iteration markers are part of the host study's result type, so a view can bucket lines by pass.
- [ ] `LineCount` validates its tap name and compiles its pattern at submit time. The schema refuses fields such as `expected`, `min` or `max`.
- [ ] A fixture study, 8 Hard Resets with counts of `Hard Reset`, `contract in force`, `rx overrun` and `rx message error` on two taps, validates.
- [ ] An inbox drop for Core's renderer, which counts per pass in the report view from the raw bytes on disk, is filed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
