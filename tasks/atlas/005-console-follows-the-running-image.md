# 005 — Pick the console the running image uses, not the one a declaration last pointed at

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — one console signal re-declared by hand twice (USB CDC ACM, then a USB-UART bridge); on 2026-10-20 it still pointed at the bridge while the flashed image had its shell on USB: 2 empty replies, then a rebuild and a second 30 s flash
**Scope:** atlas
**Hardware:** verify-only
**Owner:** no

## What

A board whose shell can be on either of two UARTs (here a debug-header UART through a USB-UART bridge, or USB CDC ACM, chosen per build by an overlay) keeps both declared as signals, and the live tools use the one the image on the board actually drives. When done: `[live] consoles` in `atlas.toml` maps a devicetree UART node (the build's `chosen` `zephyr,shell-uart`: a `usart` node or the CDC ACM node) to a signal name; when the build the board runs is known (the pinned build, or a `build=` given, confirmed by the same flash check `live_stacks` uses, `live.py:769-789`), `Console` (`live.py:449-483`) uses the matching signal and says so in the `src:` line. When it is not known, `Console` tries the declared consoles in turn and moves on only when not even the echo came back (nothing written was read, so nothing ran), never after a reply or a lost port. Today `Console` takes every direct writable signal of the role in name order (`live.py:415-421`) and falls through only on a `LiveError`, so a bridge that is present but silent is used every time and answers with nothing.

## Why now

The live-module plan (decision 5, 2026-10-06) said Core would use "whichever the target declares and is present". A USB-UART bridge is always present: it is powered by the host, not the DUT, so presence does not say which console the image uses. The field sessions kept a note telling the next session to re-declare the signal when the cabling changed; on 2026-10-20 nobody had, and the mismatch cost two empty replies, a rebuild and a second flash before a command got through.

## Done when

- [ ] Unit test: two consoles declared, the bridge's exchange returns zero bytes and the CDC one answers; `Console` uses the CDC one and names it. A second test: the bridge returns its echo and an error line; `Console` stops there.
- [ ] Unit test: with `[live] consoles` and a known build whose `zephyr,shell-uart` is the CDC node, the bridge is never opened.
- [ ] A build whose chosen shell UART maps to no declared signal answers "the image's shell is on `<node>`; no signal is declared for it" instead of trying the others.
- [ ] Bench check: flash an image with the shell on USB while both signals are declared; `shell kernel uptime` answers through the CDC signal with no re-declaration.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `DESIGN.md` "Live" and the `atlas.toml` section updated, `changelog.d/` fragment dropped.
