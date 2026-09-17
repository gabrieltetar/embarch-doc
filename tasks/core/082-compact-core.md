# 082 — Compact embarch-core/decisions/stream-index.md

**State:** blocked — `In flux: yes`, so nothing here is dispatchable yet.

**Renumbered from `081` to `082` by leg 138 at this unit's fold, 2026-09-17.** The `core/080`
worker allocated `081` for this file while the supervisor's own refill sweep, running in the same
twenty minutes, had already committed `tasks/core/081-open-md-still-says-the-per-lane-spans-route-is-decided-but-not-yet-built.md`.
Both are real tasks and neither is a duplicate — two actors picked "next free number" against
different views of `main`. **This is the second occurrence in two legs** (leg 137 renumbered
`core/078`→`core/079` for the identical reason) and it is now filed as a defect in its own right,
`tasks/doc/`, rather than being absorbed a third time.
**Size debt due:** 2026-09-24 (one week out — re-check the churn rate then
and either compact or extend).
**Source:** `scripts/check-doc-size.py`, run by task `core/080` (2026-09-17):
`embarch-core/decisions/stream-index.md` at 11172/12288 B (90.9%, 1116 B
left), no debt filed. Crossed reserve when `core/080` tightened decision 65's
"likely-low" claim into an accurate, longer one (dropped a false direction of
error, but the honest replacement needed more words, not fewer — see that
decision's own note on why it did not shrink instead).
**Scope:** core
**Hardware:** none
**Owner:** no

## What

**Compacts:** `embarch-core/decisions/stream-index.md`

Shorten `decisions/stream-index.md` (`DOC-COMPACTION.md`/`DOC-COMPACTION-PASS.md`)
without deleting a decision number or a distinct finding. The file holds four
decisions (62–65) documenting one route family — `/load`, `/load/spans`, and
what each says about a tap — landed across three tasks in six days
(`core/060`, `core/075`/`076`, `core/080`). Decision 65 is already the
file's longest entry and was just amended again; it is the first place to
look for prose that can tighten without losing a finding.

**In flux:** yes. The `embarch-ui` follow-up that would let `trace.rs` retire
its own duplicated row-decode/clock-health/stale-prefix/lane-building logic
in favor of consuming `/load/spans` is still outside this repo, dropped to
`inbox/` rather than filed here (decision 64's closing paragraph) — when it
lands, whatever it changes about this route family's contract likely touches
this file too. Decision 65's CSV-size argument itself may also move again if
a reference-shaped CSV or a second, differently-profiled fixture ever becomes
measurable (`core/080`'s own note: none exists today to close the lane/name-
mix gap it flagged).

**Must not delete:** decision 62's scoping rationale (sibling path vs query
flag; `OutpostTrace`-only refusal; the CSV-header pin to
`embarch_study_designer::outpost::csv_header()` and why it moves with the
computation, citing reversals row 86); decision 63's fourth-boolean-not-a-
third-`note`-meaning reasoning and its citation of `embarch-dev-bench`
decision 24; decision 64's three-reasons case for serving spans and its
explicit scope boundary (binning/study-step-row/`TraceView` shape stay
excluded); decision 65's shape section (`SpansAnswer` fields, the
`decode_with_cap` one-decode/two-reductions split) and its corrected,
direction-unestablished CSV-size finding (the 43,573 B/831 rows/52.367 B/row
measurement, the 22–67 B/51.4 B-mean row-width spread, the 4-lane/7-name vs
26-lane/112,804-span structural mismatch, and the "holds: same order of
magnitude regardless" conclusion).

## Why now

`check-doc-size.py` names this file with no filed debt; per protocol §5 item
5, that failure must be filed rather than left silent.

## Done when

- [ ] `embarch-core/decisions/stream-index.md` back under reserve (under 90%
      of 12288 B), same decision numbers still resolving, every "Must not
      delete" item above still present in substance.
- [ ] `scripts/check-doc-size.py` clean.
- [ ] Gate green.
