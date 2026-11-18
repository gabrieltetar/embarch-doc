# 161 — `embarch-api/spec/implementation.md` is in reserve

**State:** done
**Source:** api 160 (EMB-190) added §8 Release, leaving `spec/implementation.md` at 9,168 of 10,240 B.
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/spec/implementation.md
**Size debt due:** 2026-12-01
**In flux:** no. The release workflow is settled for step 1; the file's other sections have not moved recently.
**Must not delete:** the constants table's `[assumed]` brackets, and §8's `cosign verify-blob` command with its identity and issuer.

## What

Bring `spec/implementation.md` out of reserve by moving a settled section into a topic file verbatim, or tightening prose without dropping a fact.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [x] `scripts/check-doc-size.py --pressure` does not list `embarch-api/spec/implementation.md`.
- [x] `check-links.py` green; gate green (`../../embarch-fleet/gate.md`).
