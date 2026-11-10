# 019 — `embarch-chat` spec.md is in reserve after the Memory pass line

**State:** blocked
**Source:** `chat/008` added the memory pass to the spec's Promptu bullet and crossed the reserve line; `DOC-COMPACTION.md` §2
**Scope:** chat
**Hardware:** none
**Owner:** no

**Compacts:** embarch-chat/spec.md
**Size debt due:** 2026-11-23
**In flux:** yes — the rail and its menus (decisions 94–99, 101) were changed in the last weeks and still are.
**Unparks when:** the rail's menus have gone a leg without a change, or the owner calls it.
**Must not delete:** the Promptu bullet's pointer to decision 98's pass line and the `embarchChat.memoryPass.*` settings.

## What

`spec.md` 9,231/10,240 B.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it; this is that filing.

## Done when

- [ ] The file is clear of its reserve line.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
