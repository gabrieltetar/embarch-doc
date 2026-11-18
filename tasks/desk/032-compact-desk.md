# 032 — `embarch-desk/interfaces.md` is in reserve

**State:** done
**Source:** desk 031 (EMB-137) added the `get` subcommand to `embarch-desk/interfaces.md`, leaving it at 14,128 of 15,360 B (92.0%, 1,232 B left).
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/interfaces.md
**Size debt due:** 2026-12-01
**In flux:** yes. The desk's routes and MCP tools change nearly every unit (a new decision most weeks), so a rewrite now would restate rows about to change.
**Unparks when:** a desk unit lands that adds no route or tool row, or the next unit that writes `embarch-desk/interfaces.md` carries the compaction with it.
**Must not delete:** the route table rows and the caller's-desk paragraph (decision 77) as stated; the MCP tool list, which says what is agents' one access point.

## What

Bring `embarch-desk/interfaces.md` out of reserve: shorten the longest route rows without dropping a route, a field or a decision pointer.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [x] `scripts/check-doc-size.py --pressure` does not list `embarch-desk/interfaces.md`.
- [x] Nothing named under **Must not delete** is lost.
