# 146 — `embarch-core/spec.md` is in reserve

**State:** blocked
**Source:** core 143 added the running-study refusal to `embarch-core/spec.md`, leaving it at 9,049 of 10,240 B (88.4%, 1,191 B left).
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/spec.md
**Size debt due:** 2026-12-07
**In flux:** yes. Core's lease and gated-call surface is still moving (the Test phase's setup route and the call log's attested phase will add to the same bullets), so a rewrite now would restate lines about to change.
**Unparks when:** a Core unit lands that adds no spec.md line, or the Test phase's route for setup calls between benches has landed.
**Must not delete:** the lease bullets (decisions 93, 95, 122, 123) as stated.

## What

Bring `embarch-core/spec.md` out of reserve: shorten the longest bullets, or move one section into `spec/`, without dropping a fact or a decision pointer.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-core/spec.md`.
- [ ] Nothing named under **Must not delete** is lost.
