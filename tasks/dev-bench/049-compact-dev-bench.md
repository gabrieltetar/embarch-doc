# 049 — `embarch-dev-bench/spec.md` is in reserve

**State:** blocked
**Source:** dev-bench 048 (EMB-146) added the `scripts/patch-sums.py` paragraph to `embarch-dev-bench/spec.md`, leaving it at 9,275 of 10,240 B (90.6%, 965 B left).
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

**Compacts:** embarch-dev-bench/spec.md
**Size debt due:** 2026-12-01
**In flux:** yes. The pd-bench app and its patch workflow have changed in most recent units, so a rewrite now would restate paragraphs about to change.
**Unparks when:** a dev-bench unit lands that adds no spec paragraph, or the next unit that writes `embarch-dev-bench/spec.md` carries the compaction with it.
**Must not delete:** the wire and threading paragraphs, the workspace layout tree, and the pd-bench and `patch-sums.py` paragraphs as stated.

## What

Bring `embarch-dev-bench/spec.md` out of reserve: shorten the longest paragraphs without dropping a fact or a decision pointer.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-dev-bench/spec.md`.
- [ ] Nothing named under **Must not delete** is lost.
