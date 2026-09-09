# 021 — `embarch-ui/open.md` crossed into reserve

**State:** blocked — corrected from `open` by the supervisor at `ui/004`'s fold. `.claude/leg.md` is
explicit that a compaction task whose `In flux:` says yes must be `blocked` and must name what
unparks it, and that an `open` one means the filer got it wrong; the filer's own `In flux:` block
below argues at length that this file is in flux, so `open` was the wrong state rather than a
different judgement. **What unparks it:** `tasks/ui/007` landing (the stale-prefix bullet, which
the block below calls *explicitly* in flux and which `ui/009` already waited on once), **or** a
later reading that finds the remaining bullets settled — the block itself says the reflash-selector
and dual-clock-placement bullets are open design questions with nothing claimed against them, so
whoever unparks this checks `tasks/ui/` first and says in this line what they found.
**Source:** `ui/004`'s row-cap measurement rewrote the 250,000-row bullet with the
measured numbers, taking the file from 3,630 B to 4,191 B against a 5,120 B cap
whose reserve line is 3,920 B (`DOC-BUDGET.md`'s `RESERVE_FLOOR`); `DOC-COMPACTION.md` §2
**Scope:** ui
**Hardware:** none
**Owner:** no

**Compacts:** embarch-ui/open.md
**Size debt due:** 2026-09-23 — added 2026-09-09 by `tasks/doc/030`, which made a date
mandatory on a debt whose only item is `blocked`: `queue-status.py` never offers a blocked
task to a leg, so the date is the *only* thing that brings this one back. Set from the day
the debt opened (2026-09-09) plus two weeks, which is shorter than the loosest entries in
`--due` on purpose — a blocked debt has one drain and an open one has two.
**In flux:** **yes, and unevenly across the file's five bullets.** The row-cap
bullet `ui/004` just wrote is settled unless the cap is revisited (it says what
would reopen it: the `/study/{id}/streams` request-path budget, unmeasured).
The reflash-selector bullet and the dual-clock-placement bullet are both
open design questions with no task claimed against them right now — compacting
either without checking `tasks/ui/` first risks trimming a caveat a live
decision needs. The signal-mismatch bullet is half-closed and half-blocked on
hardware that does not exist yet, so it is stable. The stale-prefix bullet
(`ui/007`) is **explicitly** in flux — same situation `ui/009` hit before it —
so whoever compacts this file should check whether `ui/007` has landed first,
the same way `ui/009` waited on it.
**No for the reflash and signal-mismatch bullets' factual content** — their
open questions are correctly stated and are not the thing making this file
long; the bullets are long because each restates its own context rather than
pointing at `spec.md`/`decisions.md` for it.
**Must not delete:** every measured number in the row-cap bullet (257 ms / 604
ms / 1.69 s decode; 4.48 MB / 9.03 MB / 18.1 MB view JSON; 165 KB / 180 KB /
1.5 KB bins JSON) and its `[measured 2026-09-09, ...]` provenance — this is the
measurement `embarch-ui/open.md`'s cap bullet was blocked on, and losing the
numbers here loses the only place they are recorded outside `changelog.d/`
and git history. The stale-prefix bullet's **18-record** figure and its
"hardware debt, the owner's own session" framing, for the same reason `ui/009`
protected the file it compacted. The dual-clock bullet's 4.0 ms figure.

## What

`open.md` is 4,191 B against a 5,120 B cap; the reserve line is 3,920 B — 271 B
over, with 929 B still free. A runway note, not a wall: nothing is blocked on
it today.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it, and the
commit that spends the reserve is the one that files it (`DOC-COMPACTION.md`
§2). `ui/004`'s rewrite of the row-cap bullet is what spent it, filed here in
the same commit while the tradeoffs above are still fresh.

## Done when

- [ ] `open.md` is clear of its 3,920 B reserve line.
- [ ] Every `Must not delete:` item above is still readable — verified by grep
      against the post-compaction file.
- [ ] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words: what does someone starting on `embarch-ui`
      tomorrow lose if a trimmed paragraph is gone?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
