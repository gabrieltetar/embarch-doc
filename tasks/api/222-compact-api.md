# 222 — compact `embarch-api/decisions/client-crate.md`

**State:** done — split 137, 139, 150 verbatim into client-crate-types.md; client-crate.md 11832 to 8427 B
**Scope:** api
**Hardware:** none
**Owner:** no
**Compacts:** embarch-api/decisions/client-crate.md
**Size debt due:** 2026-12-10
**In flux:** no
**Must not delete:** decision 36's measured 64 MiB vs 512 MiB stack figures, decision 58's rule and its `api/139` application, decision 150's `#[serde(alias)]` duplicate-field trap.

## What

`decisions/client-crate.md` is at 11,828 of 12,288 B after `api/220` added decision 150, which puts it in reserve. The crate's `/status` and `validate` shapes were still being touched when this was filed, but the extraction decisions (36 to 38) are settled prose a split would not restate.

## Done when

- [ ] The file is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can `decisions.md` plus this file answer why the client crate is shaped as it is?
