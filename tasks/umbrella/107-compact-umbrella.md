# 107 — `embarch-umbrella/spec.md` is in reserve

**State:** blocked
**Source:** umbrella 106 (EMB-299) added the `schema_version` contract to `spec.md`, leaving it at 9,161 of 10,240 B (1,079 B left).
**Scope:** umbrella
**Hardware:** none
**Owner:** no

**Compacts:** embarch-umbrella/spec.md
**Size debt due:** 2026-12-08
**In flux:** yes. The umbrella still gains commands and release machinery most weeks (signed suite releases are written but not yet run on a tag), so the spec is still moving.
**Unparks when:** the next umbrella unit that writes `spec.md` runs out of its 1,079 B, or the first signed suite release has run and its paragraph can be rewritten once.
**Must not delete:** the decision numbers and issue keys cited in the command table and the release paragraph; move reference detail to a topic file verbatim and leave a link.

## What

Bring `spec.md` out of reserve by moving the longest sections into a topic file beside it, verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-umbrella/spec.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
