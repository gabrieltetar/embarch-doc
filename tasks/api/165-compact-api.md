# 165 — Compact two embarch-api docs in reserve

**State:** open
**Scope:** api
**Hardware:** none
**Owner:** no
**Compacts:** embarch-api/decisions/client-crate.md, embarch-api/interfaces/config.md
**Size debt due:** 2026-11-28
**In flux:** per file
- embarch-api/decisions/client-crate.md: yes (ui/111 will add the person-token caller and may extend decision 109)
- embarch-api/interfaces/config.md: no
**Must not delete:** decision 109's rule that the person scope never falls back to the agent's token, and its reason for no CLI flag; the `EMBARCH_PERSON_TOKEN` order in config.md.

## What

Both files sit in the last 10% of their cap after api/162 (decision 109). Leave client-crate.md alone until ui/111 lands, then compact it; config.md can be compacted now.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` shows neither file in reserve.
- [ ] The compactor's commit message answers whether `spec.md` alone says what someone needs to work on this component today.
