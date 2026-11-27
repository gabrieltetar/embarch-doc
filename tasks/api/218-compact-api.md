# 218 — compact `embarch-api/spec.md`

**State:** open
**Scope:** api
**Hardware:** none
**Owner:** no
**Compacts:** embarch-api/spec.md
**Size debt due:** 2026-12-10
**In flux:** no
**Must not delete:** the decision references on each bullet (every `decisions/...md` link and number), the `person_writer` bullet's list of what no command calls yet, and decision 144's "a resumed pair is not published as one" clause.

## What

`spec.md` is at 9,066 of 10,240 B after `api/217` made `run_test`'s bullet name `resume_test` and its decision 148, which puts it in reserve (line at 9,039 B). The overshoot is 27 B. Answered by the unit that just worked in it: the Test run tool bullets are settled (135, 142, 148, one function behind each), so a verbatim split of the longest bullets into `interfaces/` text restates nothing.

## Done when

- [ ] `spec.md` is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can `spec.md` alone answer what someone needs to work on this component today?
