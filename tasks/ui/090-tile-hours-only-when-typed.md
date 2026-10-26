# 090 — The tile dialog sends hours only when the user changed them, and offers a way back to computed

**State:** open
**Source:** embarch-desk task 003 (desk decision 61), DeepSeek V4 Pro review 2026-10-25 finding 1; desk side landed as `da354f8`
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`assets/desk.js` prefills `desk-hours` with the tile's current `hours` (~:893) and `dialogPatch` PATCHes it whenever the field is non-empty (~:942), before Polish, Add line and ✓. So opening a tile freezes its hours as a user override. The desk now treats `hours_override` as "a person typed this" (desk decision 61), so the UI must stop faking that.

- Send `hours` in `PATCH /tiles/{id}` only when the user edited the field away from what was prefilled.
- Offer a way back to computed hours: a "Use computed" control (or clearing the field) that PATCHes `"hours": null`. The tile JSON already carries `computed_hours`.
- The desk side (null clears, ✓ no longer writes the override, reopen proposes the current gap) is built in embarch-desk task 003; the desk service on :4891 needs the owner's rebuild before this is testable live.

## Why now

Without this the desk fix is half-effective: any dialog open still freezes hours and decision 57's self-close never applies to that tile.

## Done when

- [ ] Opening a tile, then Save/Polish/Add line/✓ without touching hours sends no `hours` key.
- [ ] Editing hours sends the number; the dialog offers a way to send `"hours": null` and the tile returns to `computed_hours`.
- [ ] A browser check against a scratch desk covers both.
- [ ] Gate green; embarch-ui spec/decisions updated.
