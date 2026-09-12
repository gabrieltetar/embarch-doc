# 067 — `decisions/core-link.md` decision 37/38 still says the two mirrors are unpinned

**State:** blocked — the one-clause fix lands in `embarch-api/decisions/core-link.md`, which is
**13,164 / 12,288 B, already over cap**, parked by `tasks/api/061` on `In flux: yes`. Whoever takes
this **pays that file's compaction as part of this unit** (`DOC-COMPACTION.md` §2, and `.claude/leg.md`'s
rule that the actor making a file's flux is the one who can shorten it): carry `tasks/api/061`'s
`Must not delete:` list, close only that file's item, and say what was cut. It unparks the moment
someone is willing to do that — it is not waiting on an event.
**Source:** `embarch-reviewer`, reviewing `api/066` (leg 084, 2026-09-11). Filed as a task rather
than left in `inbox/` because the fix is cheap and the file it lands in is not.
**Scope:** api
**Hardware:** none
**Owner:** no
**Size debt due:** 2026-09-24

**Unit reviewed:** api/066, leg 084, 2026-09-11
**Merge SHAs:** doc `2323c38`, code `f4734c9`

## Which decision

`embarch-api/decisions/core-link.md`, decision **37, 38** ("`embarch-core-client` extracted, and
given the two wrappers nothing here needed"), closing sentence: **"The alert and enrolled-board
mirrors still have that coupling unpinned."**

## Which hunk

`embarch-doc` `2323c38`, `embarch-api/open.md` line 10 (deleted): the bullet asserting Core's half
was unpinned. `embarch-api` `f4734c9`, `crates/embarch-core-client/src/client.rs` (both doc
comments, ~line 1906 and ~1940): now assert both halves are pinned, naming
`embarch-core`'s `alert_round_trips_against_the_client_s_pinned_shape` /
`enrolled_board_round_trips_against_the_client_s_pinned_shape` (`src/api.rs`, `tasks/core/024`) —
verified verbatim at `/home/gabriel/Github/embarch/embarch-core/src/api.rs:1764,1807`.

## Why this is a contradiction rather than a refinement

Decision 37/38 is a standing decision this unit did not touch, and its own text ("still have that
coupling unpinned") is the exact claim the unit's diff exists to correct. The unit removed the
claim from `open.md` and updated the two test comments, but left the decision file — the topical
home the worker itself named and declined to edit only because it is over cap — asserting the
pre-`core/024` state as still true. A reader who opens `decisions/core-link.md` for "why is it like
this" now gets the superseded fact with no pointer to the correction; nothing in this diff is wrong
about the current pinning, but decision 37/38 is now stale by the unit's own premise, not by drift
from a separate change.

## What it would take to undo

Not a revert — the diff itself is correct. Fix is forward: append a one-clause update (or a dated
correction note, per `DOC-COMPACTION.md` §5's tombstone convention) to decision 37/38 in
`decisions/core-link.md` pointing at `tasks/core/024` and the two named tests, since that file is
where the next reader will look for "is this still unpinned." Both merge SHAs (`2323c38` doc,
`f4734c9` code) are clean, self-contained commits; no revert is needed or suggested — only a
follow-up edit to the decision file, which is out of scope for this reviewer to make.

## Hardware

None — this is a documentation-consistency finding, not a claim requiring hardware to confirm.
