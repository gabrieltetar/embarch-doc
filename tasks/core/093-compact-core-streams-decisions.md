# 093 — `embarch-core/decisions/streams.md` is in reserve

**State:** blocked
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decisions 72 and 73
**Scope:** core
**Hardware:** none
**Owner:** no
**Compacts:** embarch-core/decisions/streams.md
**Size debt due:** 2026-09-25
**In flux:** yes
**Blocked on:** decisions 72 and 73 being validated against real hardware — a traced study run with the outpost bridge attached, which will either confirm the live path's frame indices and header handling or change them. Unparks the moment that run lands.

## What

The streams decision group is **11,094 / 12,288 B (90.3%), 1,194 B left**. Out
of reserve when this closes, or the task says why not.

Two entries landed together: **72** (an outpost trace is decoded and pushed
live, and the post-hoc render stays authoritative) and **73** (a `Text` tap gets
an arrival sidecar keyed by byte offset). Both are days old and both carry
reasoning nothing else in the corpus holds, so **neither is the one to squeeze** —
decision 72 in particular is half of a cross-repo reversal
([row 112](../../embarch-decision-reversals.md)) and its "what the render has
that live cannot" paragraph is the whole argument for keeping two paths.

The seam available is by mission: 30/38/39 are about **rendering and the file
layout**, and 70/72/73 are about **pushing live**. A split into
`decisions/streams-live.md` moves three entries verbatim.

## Why now

**In flux: yes.** The live path lands here days before its own bench validation
(the outpost bridge is not attached), so a squeeze taken now would be cutting
reasoning that has not finished being tested against hardware. A split moves it
untouched instead, which is why the split is the remedy and the squeeze is not.

## Done when

- [ ] Out of reserve, or the task says why not.
- [ ] Decisions 72 and 73 keep every clause about what the post-hoc render has
      that live cannot, and about which clock each arrival sidecar records.
      Those are what a later reader will otherwise re-derive wrongly.
- [ ] `decisions.md`'s index row split to match, with both files' numbers.
- [ ] Byte numbers before and after.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.
