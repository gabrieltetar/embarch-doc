# 031 — Compact embarch-chat's spec

**State:** done
**Scope:** chat
**Hardware:** none
**Owner:** no
**Compacts:** embarch-chat/spec.md
**Size debt due:** 2026-12-17
**In flux:** no
**Must not delete:** the login bullets naming decisions 101 and 106, which state what one pick moves and what needs a reload.

## What

`embarch-chat/spec.md` is at 9119 of 10240 B, inside the reserve, after task 030 added one sentence on the login reload. Compact it per `DOC-COMPACTION.md`: edit the body, drop what decisions already say, keep every behaviour a reader needs.

## Done when

- [x] `embarch-chat/spec.md` is out of reserve and no behaviour it states is lost.
- [x] Gate green.

## Result

spec.md 9119 -> 8804 B, out of reserve. Dropped per-install commit SHAs and dates from Status (git history holds them); fixed "local, no remote" in Pointers, which contradicted the public remote. Login bullets (101, 106) untouched.

Compaction question: can spec.md alone answer what someone needs to work on this component today? Yes for behaviour and invariants, with the split files and decisions linked for detail; the Status line is the one part that is install history, not behaviour, and is now shorter.
