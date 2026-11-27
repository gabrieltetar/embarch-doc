# 051 — compact `embarch-chat/spec.md` and `open.md`

**State:** done — spec.md 9318->9015 B, open.md 4298->3913 B, both out of reserve
**Scope:** chat
**Hardware:** none
**Owner:** no
**Compacts:** embarch-chat/spec.md, embarch-chat/open.md
**Size debt due:** 2026-12-09
**In flux:** no
**Must not delete:** spec.md's bullet on a container login and open.md's container-login line (decision 122), with its first-session checklist; the login and handoff bullets (101, 103, 105, 106, 109).

## What

`spec.md` is 9,318 of 10,240 B and `open.md` 4,298 of 5,120 B after `chat/050` added a container-login line to each. Compact both under `DOC-COMPACTION.md`. Answered by the unit that just worked in them: **the login surface is not still moving** beyond the container login's hardware debt, which is already in `open.md`.

## Done when

- [x] `spec.md` and `open.md` are out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
