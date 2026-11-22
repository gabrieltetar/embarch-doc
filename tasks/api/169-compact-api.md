# 169 — `embarch-api/open.md` is in reserve

**State:** done
**Source:** api 167 (EMB-225) added the `publish` item to `embarch-api/open.md`, leaving it past the reserve line (4,294 of 5,120 B).
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/open.md
**Size debt due:** 2026-11-29
**In flux:** yes. The `publish` item is rewritten by `tasks/api/168` (the oracle listing and revisions) and again when Core serves a pending revision's files.
**Must not delete:** the `publish` item's statement that Core does not serve `measurements.json` before the manifest exists (receipt: `embarch-core`'s `publish::file_handler` reads the manifest first), and the bench-verification pointer.

## What

Bring `embarch-api/open.md` out of reserve: shorten the longest items without dropping a fact or a decision pointer.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [x] `scripts/check-doc-size.py --pressure` does not list `embarch-api/open.md`.
- [x] Nothing named under **Must not delete** is lost.
- [x] `spec.md` alone answers what someone needs to work on this component today (the human question, answered in the commit message).

Done inside `tasks/api/168`: `open.md` is 3,525 B; four items moved verbatim to `open/unmeasured-details.md`.
