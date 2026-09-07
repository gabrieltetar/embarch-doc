# embarch-doc: doc conventions

**Status:** active, 2026-09-04. The shapes scripts parse and cross-references depend on: the `**Status:**` line, decision entries, how to cite one, how to retire one, and marking a constant measured or assumed. Split out of [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §7 on 2026-09-04 when that doc reached its size cap ([DOC-COMPACTION.md](DOC-COMPACTION.md) §3). **Bare `§N` references below are that doc's**; anything else names its doc.

Four scripts read these shapes — `check-doc-conventions.py`, `check-decision-refs.py`, `check-staleness.py`, `build_changelog.py` — so this is a reference, loaded when you need a shape, not the workflow. That is [DOC-PROTOCOL.md](DOC-PROTOCOL.md).

## The `**Status:**` line

First line after the title: `**Status:** <state>, <yyyy-mm-dd>` followed by any prose. Only the token and the date are machine-readable, and `scripts/check-doc-conventions.py` deliberately does not look past them.

`<state>` is one of `draft` · `active` · `done` · `planned` · `paused` · `proposal` · `retired` · `superseded-by:<path>`. The date is when the doc last *changed state*, not when it was last edited — a compaction pass does not move it. `half-accepted` is deliberately absent ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3).

This exists because `check-staleness.py` is a heuristic over two tables — guessing at status no doc stated readably. **A `done` asserted over an unmarked Definition of Done is the status claim §4 exists to prevent**: a milestone doc stays `active` until its residue has moved into the four files.

## Decision entries

Number-first headings, one level below their topical group: `### 20, 21, 25, 27 — Streaming capture, batched, with units`. A group is a section of `decisions.md` or a whole `decisions/<topic>.md`; the checker reads both. **Numbers are permanent** — unique per sub-project, never renumbered or reused, and an entry may own several where decisions were merged. Groups can be renamed, reordered, split, and moved between files freely; numbers cannot, so out-of-order numbers in a group are intended. Entry shape and length: [DOC-COMPACTION.md](DOC-COMPACTION.md) §5.

## Referring to a decision

**A decision number addresses a sub-project, not a file and not a section.** Within that sub-project's own docs: `decision 39`. Across: `embarch-study-designer decision 39`, or a link plus `decision 39` — but **prefer the bare number.** A link names a *file*, and a mission split moves an entry between a sub-project's decision files without changing its number, so `` `[decision 30](decisions/shape.md)` `` written from inside `embarch-api/` went on resolving after decision 30 moved to `decisions/tests.md`, and neither gate can see it (`tasks/doc/022`). Legacy `§3 decision 39` still parses, unmaintained — which is what let §3's decisions move to their own file untouched.

**Where a link is wanted anyway — `history/` is the standing case — link the index, not the topic file.** `<sub-project>/decisions.md` is a routing table from number to `decisions/<topic>.md`, maintained by whoever splits one, so it survives a mission split; a link straight at a topic file does not, and neither gate can see the difference. The 17 `history/` entries still linking a topic file are `tasks/doc/022`'s sweep, not an exception to this.

**A dated entry that *narrates* a move is the one case where the old filename is content rather than a pointer.** It was true on the day it was written, so neither silently amending it nor leaving a reader to follow it is right: keep the old name and say where the thing is now. `history/api.md`'s decision 30 line is the worked example.

**`history/*.md` is hand-editable, and hand edits survive.** `build_changelog.py` inserts a new entry into the existing window and leaves the rest of the file alone — verified against a real assemble on 2026-09-06, after two tasks had assumed the opposite. There is no other durable copy to fix instead: the `changelog.d/` fragment that produced a line is deleted at assembly.

`check-links.py` structurally cannot see one of these — it validates paths and skips anchors, and "decision 39" is not a link. `scripts/check-decision-refs.py` resolves all 2,362 of them, and has found two real classes of breakage:

- **A number an insertion renumbered.** Two entries looked deleted while other docs cited them (`embarch-api` 31, `embarch-umbrella` 27). Neither was: **a commit inserted a decision in the middle and renumbered the entry below it**, so every reference to the old number silently pointed elsewhere. **This is why a number is permanent here** (DOC-COMPACTION.md §5); both entries own both numbers.
- **A reversal row cited and gone.** It resolves `reversals ... row N` against the union of `reversals/rows-*.md`: 47 rows were once deleted along with a `## Changelog` heading they sat below, and **fifteen citations went on pointing at them with nothing to notice.**

## Retiring an entry

A decision that stops describing anything true is **retired, not deleted** — a one-line tombstone naming what it said and what replaced it:

```markdown
### 19 — Two-tier validation (retired 2026-08-25, see decision 48)
Post-hoc content validation alongside the real-time per-step `Outcome`. Removed
outright; the real-time half stands and is decision 48's subject.
```

A dangling reference then lands on an explanation instead of a gap, which is what keeps *Referring to a decision*'s never-reused promise cheap.

## Measured vs. assumed constants

Every load-bearing constant says which it is, inline: `460800 baud [measured 2026-08-30, DK VCOM1 over the bridge]`, `250 ms step timeout [assumed]`.

The bracket earns its place on an **inventoried** constant — one in a table or declared list, where provenance would otherwise be vague. It does **not** earn its place where prose already derives a constant precisely ("244, one full 247-byte ATT MTU minus the 3-byte ATT header"): a bracket there is noise. A sweep found only **five** sites repo-wide, not the dozens the rule's wording implied. So: mark an inventory, leave good prose alone, and mark the rest as each doc reaches a compaction pass.

## `open.md` needs no "Open questions" heading

**In an `open.md`, every top-level bullet is an open question** — the filename says what the file is, and the four-file split ([DOC-COMPACTION.md](DOC-COMPACTION.md) §2) made the whole file the open-questions doc. `scripts/collect-open-questions.py` reads it that way. Sub-headings inside it are free: group bullets by kind (`## Known wrong, not fixed`, `## Structural limits`) or leave them ungrouped.

This is written down because the shape was load-bearing while nothing said so. The collector used to require a heading whose text contained "open question"; the five files whose *title* happened to read `<name>: open questions` passed by accident, and `embarch-ui`, `embarch-topology` and `embarch-umbrella` — titled `<name>: open` — printed **zero bullets while 22 sat in them**, under a summary line that said "across 8 doc(s)" and so read as complete. Every refill sweep between the migration and 2026-09-05 swept an incomplete suite. The heading predicate now applies only to a legacy `design.md` that still carries its own section.
