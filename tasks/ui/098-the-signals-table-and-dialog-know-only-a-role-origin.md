# 098 — The Topology tab's signals table and dialog know only a role as a signal's origin

**State:** open
**Source:** `tasks/suite/046`, landed 2026-10-28 by the supervisor: `embarch-topology` decision 48 lets a signal leave a role-less bench board (`SignalLink.origin_board`, its probe serial, with `origin_role` empty). The UI half was left out of that cross-repo pass.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`assets/app.js` renders a signal's origin as `sig.origin_role` (the signals table, around line 573), and the signal dialog offers only roles (`sig-origin`, defaulting to `"dut"`, around lines 6074 and 6143). A signal declared from a bench board through `embarch-api`'s `declare_signal origin_board=` now shows an empty origin cell, and re-saving it from the dialog would re-declare it from `dut`, silently moving it to another board. When this is done, the table shows a bench board origin by the board's enrolled name (the probe serial when no enrolled board matches), the dialog can pick a bench board as the origin (sending `origin_board`, never both), and re-saving a board-origin signal keeps its board.

## Why now

The Core and api halves shipped together; the dialog's re-save is the one path that can now move a declared signal to the wrong board without saying so.

## Done when

- [ ] The signals table names a board origin by its bench board's name.
- [ ] The dialog offers the enrolled bench boards beside the roles and sends `origin_board` for one; a board-origin signal re-saves unchanged.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
