# 090 — The tile dialog sends hours only when the user changed them, and offers a way back to computed

**State:** claimed by agent/ui/090-tile-hours-only-when-typed, 2026-10-26 02:57
**Source:** embarch-desk task 003 (desk decision 61), DeepSeek V4 Pro review 2026-10-25 finding 1; desk side landed as `da354f8`
**Scope:** ui
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 leg

**Doc reserve in `embarch-ui/`:** `spec.md` is 9,099 / 10,240 B (1,141 B left), filed as `ui/089`
(open, not yours); `open.md` is 4,366 / 5,120 B (754 B left), filed as `ui/088` (blocked). Both are
already filed, so you owe no new compaction task for them, but do not push either over its cap: put
the new behaviour in the decision and keep the `spec.md` line short, or file a `tasks/ui/` compaction
task in the same commit if you cannot. The desk side is landed (`embarch-desk` `da354f8`, decision
61); read it there, never edit `embarch-desk`. **Never touch the owner's desk service on :4891** (no
start, stop, rebuild or request to it); for the browser check run a scratch desk on a port of your
own with its own data dir, and never `pkill` by name. Line numbers above were taken before
`ui/084` landed; re-locate before citing.

## What

`assets/desk.js` prefills `desk-hours` with the tile's current `hours` (~:893) and `dialogPatch` PATCHes it whenever the field is non-empty (~:942), before Polish, Add line and ✓. So opening a tile freezes its hours as a user override. The desk now treats `hours_override` as "a person typed this" (desk decision 61), so the UI must stop faking that.

- Send `hours` in `PATCH /tiles/{id}` only when the user edited the field away from what was prefilled.
- Offer a way back to computed hours: a "Use computed" control (or clearing the field) that PATCHes `"hours": null`. The tile JSON already carries `computed_hours`.
- The desk side (null clears, ✓ no longer writes the override, reopen proposes the current gap) is built in embarch-desk task 003; the desk service on :4891 needs the owner's rebuild before this is testable live.

## Why now

Without this the desk fix is half-effective: any dialog open still freezes hours and decision 57's self-close never applies to that tile.

## Done when

- [x] Opening a tile, then Save/Polish/Add line/✓ without touching hours sends no `hours` key.
- [x] Editing hours sends the number; the dialog offers a way to send `"hours": null` and the tile returns to `computed_hours`.
- [x] A browser check against a scratch desk covers both.
- [x] Gate green; embarch-ui spec/decisions updated.

## Done

Browser check (headless Firefox via geckodriver, scratch UI on :48901 against a python mock desk on :48911 applying desk decision 61 semantics, not the real desk): open+Save sent `{note}` only; typed 2 sent `hours:2`; untouched Save kept it; *Use computed* sent `hours:null` and the field returned to 1.5; typing after Use computed sent the number. Real desk: not run (needs the owner's rebuilt :4891 service) - verification debt, low.

Build note: embarch-ui `cargo build` is red against topology HEAD (topology/063, `Upserted` re-export ungated); gate run in a scratch copy with topology at HEAD~1 (181+2+3 tests, clippy clean). Dropped `inbox/topology-software-feature-build-breaks.md`.
