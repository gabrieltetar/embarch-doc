# 165 — Compact two embarch-api docs in reserve

**State:** claimed by agent/api/165-compact-api, 2026-11-22 03:03
**Scope:** api
**Hardware:** none
**Owner:** no
**Compacts:** embarch-api/decisions/client-crate.md, embarch-api/interfaces/config.md
**Size debt due:** 2026-11-28
**In flux:** no. `client-crate.md` was `yes` until `ui/111` landed (2026-11-21); it built the person-token caller in `embarch-ui` without extending decision 109, so both files can be compacted now.
**Must not delete:** decision 109's rule that the person scope never falls back to the agent's token, and its reason for no CLI flag; the `EMBARCH_PERSON_TOKEN` order in config.md.

## What

Both files sit in the last 10% of their cap after api/162 (decision 109). Leave client-crate.md alone until ui/111 lands, then compact it; config.md can be compacted now.

## Dispatch notes

- **`ui/111` has landed** (2026-11-21), so both files are compacted in this unit. In reserve, 2026-11-22: `decisions/client-crate.md` 12,278 of 12,288 B (10 B left; out at 11,059 B or less), `interfaces/config.md` 11,368 of 12,288 B (920 B left; same line). Nothing else in `embarch-api/` is in reserve; `open.md` is 3,870 of 5,120 B.
- **A doc-only unit**: you get an `embarch-doc` worktree and no code worktree, since nothing here changes `embarch-api`'s source.
- **Split first** (`DOC-COMPACTION.md` §2): a verbatim move of settled text into a new topic file restates nothing, so prefer it over rewording a decision. A decision's number never changes, and a moved decision leaves its index line and links working (`check-links.py`).
- Decisions near their own size limit, not to grow: `ledger` #98 (15 B), `bench-exchange` #89 (122 B), `failure-reporting` #67 (192 B).

## Done when

- [x] `scripts/check-doc-size.py --pressure` shows neither file in reserve.
- [x] The compactor's commit message answers whether `spec.md` alone says what someone needs to work on this component today.
