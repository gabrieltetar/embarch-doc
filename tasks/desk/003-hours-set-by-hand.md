# 003 — A tile's hours count as set by hand only when the user set them

**State:** claimed by agent/desk/003-hours-set-by-hand, 2026-10-26 02:40
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-desk finding 1), verified by Opus against embarch-desk@880d9707
**Scope:** desk
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 leg

Nothing in `embarch-desk/` docs is in reserve. The line numbers above were taken at `880d9707`;
`desk/001` and `desk/002` have landed since, so re-locate before citing. The `embarch-ui` half is
an inbox drop written by absolute path to `/home/gabriel/Github/embarch/embarch-doc/inbox/`, never
an edit to `embarch-ui`. Not deployed: the desk service on :4891 is the owner's to rebuild; do not
start, stop or touch it.

## What

Decision 57 makes a tile close itself once Harvest covers it, "unless its hours were set by hand", and keeps that computed, "so it opens again if the entries go". The desk stores one field, `hours_override`, for three different events:

- **✓ writes it.** `approve_tile` stores the hours it sent as the override. When the user deletes that entry from the day list, the tile reopens with its status, entry, acted time and frozen seconds cleared, but the override is kept. The reopened tile then proposes the hours of the deleted entry, not the current gap, and can never close as covered.
- **Nothing clears it.** `PATCH /tiles/{id}` drops `"hours": null`, so neither the UI nor the user can return a tile to computed hours.
- **The Desk tab writes it on every save.** The tile dialog prefills its hours field with the tile's current hours and PATCHes that value on every Save, Polish, Add line and ✓. Opening and polishing a tile therefore freezes its hours at that moment. A live session's later time no longer moves the proposal, and decision 57's self-close never applies to that tile.

When done, a tile's hours are "set by hand" only when a person typed them, and a tile can go back to computed hours. One direction: keep what ✓ sent separate from the user's override, clear only the ✓'s value on reopen, and accept `"hours": null` to clear a user's override. The UI half belongs to `embarch-ui` and goes there by an inbox drop: send hours only when the user changed the field, and offer a way back to computed.

## Why now

- `src/server.rs:1060`: `approve_tile` sets `hours_override`. `:2152-2167`: `remove_entry` reopens the tile without clearing it. `:848-875`: `TilePatch.hours` is `Option<f64>`, so null cannot clear. `:186-218`: `covered` and `hours` both depend on the override being absent.
- `embarch-ui assets/desk.js:893-894` prefills `desk-hours` with `t.hours`, and `:942` sends it whenever the field is non-empty. `dialogPatch` runs before Polish, Add line and ✓ (`:1237-1251`, `:959`).
- The spec's §2 invariant "one with nothing left to propose closes itself unless its hours were set by hand — computed, so it opens again if the entries go" and decision 41's "deleting one a tile made reopens that tile" both assume an override means a person's choice.

## Done when

- [ ] A tile whose ✓'d entry is deleted reopens proposing the current gap (captured minus what Harvest holds that day), and closes as covered once Harvest covers it again. A test drives ✓, more session time, entry deletion, and a covering entry.
- [ ] A user-set override survives a reopen, and `PATCH` with `"hours": null` clears it. A test covers both.
- [ ] An inbox drop for `embarch-ui`'s tile dialog (send hours only when changed, and a way back to computed) is filed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated (decision 57's "set by hand" stated precisely; `interfaces.md` for `PATCH` null), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
