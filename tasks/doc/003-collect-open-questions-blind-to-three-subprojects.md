# 003 — `collect-open-questions.py` reports nothing from three of the eight `open.md` files

**State:** open
**Source:** supervisor, leg 009, 2026-09-04 — found during the refill sweep
**Scope:** doc
**Hardware:** none
**Owner:** required

**`Owner: required` because both candidate fixes below write reserved paths** —
`scripts/collect-open-questions.py` or `DOC-CONVENTIONS.md` (`protocol.md` §3). Filed
here rather than left in `inbox/` so it is visible in the queue; `queue-status.py`
gates it out of dispatch.

## What

`scripts/collect-open-questions.py` walks every `open.md`, but only prints bullets
that sit **under a heading whose text contains "open question"**. Three of the eight
sub-project `open.md` files carry no such heading — the four-file split made the
whole file the open-questions doc, so the bullets sit at top level under the title:

| `open.md` | has an "open question" heading | bullets the collector prints |
|---|---|---|
| `embarch-api` | yes | printed |
| `embarch-core` | yes | printed |
| `embarch-dev-bench` | yes | printed |
| `embarch-outpost` | yes | printed |
| `embarch-study-designer` | yes | printed |
| **`embarch-topology`** | **no** | **none** |
| **`embarch-ui`** | **no** | **none** |
| **`embarch-umbrella`** | **no** | **none** |

The reported total, **78 across 8 docs**, is therefore 78 across *five*; the other
three docs are counted as docs and contribute nothing. The header line says
"across 8 doc(s)", which is what makes it read as complete.

## Why it matters

This is the refill sweep's primary source. `protocol.md` §4 and §6 step 1 both name
`open.md` as what a supervisor sweeps when the queue drains, and `ops.md` §7 requires
every dream proposal to come from something already written down — with this file as
the index. **A leg that swept this and found nothing for `ui`, `topology` or
`umbrella` would conclude those sub-projects have no open questions.** This leg
nearly did: it found four live `embarch-ui` questions only by opening the file by
hand after noticing three docs printed zero bullets, and one of them
(`tasks/ui/001`, the 13 MB Trace-view transfer) is the strongest task it filed all
leg.

It is the **same defect the script's own docstring records fixing on 2026-09-03** —
"Until 2026-09-03 it read design.md ONLY, which after the migration meant it saw 10
questions across 3 docs while 88 sat unread in eight open.md files. Every refill
sweep since the migration has been mostly blind." That fix moved the blindness from
five docs to three rather than removing it, because it kept the heading predicate.

## Two candidate fixes, and why the supervisor filed rather than picked

1. **In `scripts/`:** when the doc *is* `open.md`, take every top-level bullet
   regardless of heading — the filename already says what the file is. Cheapest, and
   makes the heading optional rather than load-bearing.
2. **In the three docs:** add an `## Open questions` heading to `embarch-ui/open.md`,
   `embarch-topology/open.md` and `embarch-umbrella/open.md`. Cheap too, but it is a
   *convention* decision, and `DOC-CONVENTIONS.md` — the doc that exists to hold the
   shapes scripts parse — currently says nothing about `open.md`'s shape at all, so
   nothing stops the next split from dropping the heading again.

Fix 1 plus a line in `DOC-CONVENTIONS.md` is probably the right pair, but
`scripts/` and every `DOC-*.md` are owner-reserved (`protocol.md` §3), so this is a
finding rather than a task. **A worker dispatched at it would fail on its first
edit** — the same reason leg 008 left its ownership-check finding in this directory.

## Interim, for whoever sweeps next

Until this is closed, a refill sweep must open `embarch-ui/open.md`,
`embarch-topology/open.md` and `embarch-umbrella/open.md` by hand. The collector's
output is not the whole set.
