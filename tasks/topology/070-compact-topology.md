# 070 — Compact embarch-topology's spec

**State:** done
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/spec.md
**Size debt due:** 2026-12-17
**In flux:** no
**Must not delete:** the "What a release carries" section's `cosign verify-blob` command with its exact identity and issuer.

## What

`embarch-topology/spec.md` is at 10079 of 10240 B, inside the reserve, after task 069 added the release-signing section. Compact it per `DOC-COMPACTION.md`: edit the body, drop what decisions already say, keep every behaviour a reader needs.

## Done when

- [x] `embarch-topology/spec.md` is out of reserve and no behaviour it states is lost.
- [x] Gate green.
