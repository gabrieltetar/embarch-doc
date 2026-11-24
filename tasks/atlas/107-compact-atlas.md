# 107 — `embarch-atlas/design.md` is in reserve

**State:** blocked
**Source:** atlas 106 (EMB-268) added the read-back of measured facts to `design.md`, leaving it at 23,474 of 25,600 B (2,126 B left).
**Scope:** atlas
**Hardware:** none
**Owner:** no

**Compacts:** embarch-atlas/design.md
**Size debt due:** 2026-12-07
**In flux:** yes. The measured plane is still moving: `via: study` / `via: test` records and where the plane lives once planes are shared are not built, and the live write-back and its read-back landed within two units of each other.
**Unparks when:** the next atlas unit that writes `design.md` runs out of its 2,126 B, or the measured plane's study and test path lands and its paragraphs can be rewritten once.
**Must not delete:** the dated decisions and their issue keys (EMB-267, EMB-268, EMB-109); move reference detail to a topic file verbatim and leave a link.

## What

Bring `design.md` out of reserve by moving the longest sections into a topic file beside it, verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-atlas/design.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
