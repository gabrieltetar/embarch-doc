# 108 — The Desk tab's note count matches the desk's, and its switch warning stays until it is answered

**State:** done
**Source:** Linear issue EMB-48, filed by an audit (points 4 and 5; points 1 to 3 are `tasks/desk/017`)
**Issue:** EMB-48
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Two Desk tab nits from the second review of desk notes (`embarch-desk` decision 74).

1. **The count.** The tab strips whitespace with JavaScript's `\s`; the desk trims with Rust's `trim` / `trim_end`, and the two sets differ on U+FEFF and U+0085. So a note holding either shows a count one off from the one the desk enforces. The desk stays authoritative; the tab's count should match it.
2. **The warning.** After the desk shown changes while a note is being typed, the tab warns that "nothing was added". A keystroke in the add box clears that warning, and the warning says nothing was added even when no Add was tried. It should be cleared by an Add or a desk change, not by typing, and say "nothing was added" only after an Add attempt.

## Why now

Filed by an audit; both are small and in one file.

## Where to look

- `assets/desk.js` `cleanNote`, `noteLen` — the JS-side trimming
- `assets/desk.js` `renderDeskNotes` — the "... so nothing was added ..." message
- `assets/desk.js` — the `input` listener on the add box that clears `dnotesStatus`
- `embarch-desk/src/store.rs` `clean_desk_note` — the Rust-side trimming to match; it is `desk`'s, so read it, do not edit it

## Dispatch notes

- Match Rust's `char::is_whitespace` set exactly rather than adding the two characters by hand, if a small helper can say it once; either way, a test or a check in the webview e2e that a note with U+FEFF and with U+0085 counts the same as the desk would.
- Burndown is on: no new numbered decision. None should be needed.
- No `embarch-ui` doc in `embarch-doc` is in reserve. Decision entries near their limit (bytes left): `launcher#28` 22, `tab-folders#100` 113.

## Done when

- [x] A note containing U+FEFF or U+0085 shows the same count in the Desk tab as the desk computes.
- [x] Typing in the add box does not clear the desk-switch warning, and the warning only says nothing was added after an Add attempt.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.

## Hardware-verification debt

None for hardware. The webview e2e (`tests/browser/drive_desk.py`, needs geckodriver) gained a U+FEFF/U+0085 count check and was not run here; the existing desk-switch check (Add says "nothing was added") is unchanged.
