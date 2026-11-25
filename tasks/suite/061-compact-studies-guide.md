# 061 — `suite/studies-guide.md` is in reserve

**State:** blocked
**Source:** EMB-479 added §5, the audio-rate analog capture walkthrough, to the studies guide: 21,561 B before, in reserve after (cap 25,600 B).
**Scope:** suite
**Hardware:** none
**Owner:** no

**Compacts:** suite/studies-guide.md
**Size debt due:** 2026-12-01
**In flux:** yes. §5 describes work that has run on no board; the session prompts, the Study Designer form and `embarch-api`'s control-port flag are not built, and each landing changes §5.
**Unparks when:** the next unit that writes the guide runs out of room; the compaction rides in that unit.
**Must not delete:** §5's list of what is unmeasured on hardware and its statement that an nRF52840 DK is the only board with the backend; §3's note that 460800 is the link's ceiling.

## What

Bring the guide out of reserve by moving §4 (the outpost trace walkthrough, about 6 KB) verbatim into its own guide, leaving a pointer, as the HIL study walkthrough was moved.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `suite/studies-guide.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
