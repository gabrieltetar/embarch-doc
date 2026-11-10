# 004 — `embarch-promptu` spec.md is in reserve after decision 41's build

**State:** blocked — `In flux: yes`.
**Unparks when:** build step 4 (the weekly sheet, decision 30) is built or dropped. The other half, the chat passing its context usage, landed 2026-11-09 (embarch-chat `a46c5ac`).
**Source:** `promptu/002` added the context-planning bullet to `spec.md` and crossed the reserve line; `DOC-COMPACTION.md` §2
**Scope:** promptu
**Hardware:** none
**Owner:** no

**Compacts:** embarch-promptu/spec.md
**Size debt due:** 2026-11-23
**In flux:** yes — build step 4 still changes what `spec.md` says it builds; the chat's half of decision 41 landed 2026-11-09.
**Must not delete:** the invariants in §3 and the "deliberately does not do" list in §5.

## What

`spec.md` 9,564/10,240 B.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it; this is that filing.

## Done when

- [ ] `spec.md` is clear of its reserve line, or a successor confirms `In flux: no` and compacts.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
