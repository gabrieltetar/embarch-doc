# 197 — compact `embarch-core/decisions/call-log.md`

**State:** open
**Scope:** core
**Hardware:** none
**Owner:** no
**Compacts:** embarch-core/decisions/call-log.md
**Size debt due:** 2026-12-11
**In flux:** no
**Must not delete:** decision 122's `board` rule and its null cases, the fold rule and its measured claims, decision 156's and 158's refusal rules.

## What

`decisions/call-log.md` is at 11,251 of 12,288 B after `core/196` made decision 122 say every board-acting route names its board, which puts it in reserve. The call log's shape is settled; decision 122 carries the most prose and could shed its why-a-layer and fold detail into the interface doc.

## Done when

- [ ] The file is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can `decisions.md` plus this file answer why the call log is shaped as it is?
